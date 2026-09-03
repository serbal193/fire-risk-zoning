"""
Script: 03_processar_topografia.py
Etapa: 01_tratamento

Descrição:
    Processa o raster de elevação (DEM) e deriva os fatores topográficos de risco:
    1. Elevation (Altitude em metros) reprojetado para CRS métrico (EPSG:31982) a 30m.
    2. Slope (Declividade em graus: 0° a 90°).
    3. Aspect (Orientação da encosta em graus: 0° a 360°, onde -1 indica plano).
    
    Discretização baseada em Chen et al. (2021) - Tabela 3:
    - Elevation: (0, 145], (145, 295], (295, 575], (575, ∞)
    - Slope:     (0, 3.3°], (3.3°, 10°], (10°, 18.3°], (18.3°, 90°]
    - Aspect:    Norte (0°-45° U 315°-360°), Leste (45°-135°), Sul (135°-225°), Oeste (225°-315°)

    Além de gerar os GeoTIFFs contínuos e classificados:
    - Extrai os valores pontuais (médios ou pontuais do centroide de cada célula de 1 km²)
    - Preenche e atualiza os CSVs de amostras:
        * output/01_processar_hotspots/grade_1km_amostras_anuais.csv
        * output/01_processar_hotspots/grade_1km_amostras_treino.csv
        * output/01_processar_hotspots/grade_1km_amostras_validacao.csv

    Saídas em 'output/03_processar_topografia/':
    - elevation.tif (Raster de Elevação contínua em metros)
    - slope.tif     (Raster de Declividade contínua em graus)
    - aspect.tif    (Raster de Orientação da encosta contínua em graus)
    - elevation_classes.tif (Raster de Elevação discretizado 1 a 4)
    - slope_classes.tif     (Raster de Declividade discretizado 1 a 4)
    - aspect_classes.tif    (Raster de Aspecto discretizado 1 a 4)
"""

import sys
import os

# Configuração GDAL/Rasterio/Fiona para caminhos com caracteres especiais (Windows/acentuação)
os.environ['GDAL_FILENAME_IS_UTF8'] = 'NO'
os.environ['SHAPE_RESTORE_SHX'] = 'YES'

from pathlib import Path
import numpy as np
import pandas as pd
import rasterio
from rasterio.warp import reproject, Resampling
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.patches as mpatches

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ==========================================
# CAMINHOS E CONFIGURAÇÕES
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_DEM_TIF = BASE_DIR / "input" / "SIG" / "elevation.tif"

# Limite municipal
if (BASE_DIR / "input" / "01_vetores" / "SJP.shp").exists():
    LIMITE_SHP = BASE_DIR / "input" / "01_vetores" / "SJP.shp"
else:
    LIMITE_SHP = BASE_DIR / "output" / "01_vetores" / "SJP.shp"

# Datasets das amostras gerados no Script 01
AMOSTRAS_DIR = BASE_DIR / "output" / "01_processar_hotspots"
CSV_ANUAL = AMOSTRAS_DIR / "grade_1km_amostras_anuais.csv"
CSV_TREINO = AMOSTRAS_DIR / "grade_1km_amostras_treino.csv"
CSV_VALIDACAO = AMOSTRAS_DIR / "grade_1km_amostras_validacao.csv"

OUTPUT_DIR = BASE_DIR / "output" / Path(__file__).stem

CRS_PROJETADO = "EPSG:31982"    # SIRGAS 2000 / UTM zone 22S (métrica)
RESOLUCAO_M = 30.0              # Resolução espacial do raster final em metros


def carregar_e_reprojetar_dem(
    caminho_dem: Path,
    limite_gdf: gpd.GeoDataFrame,
    dst_crs: str = CRS_PROJETADO,
    resolucao: float = RESOLUCAO_M
) -> tuple[np.ndarray, dict, rasterio.transform.Affine]:
    """
    Carrega o DEM, reprojeta para CRS métrico plano (UTM)
    e recorta rigorosamente pelo limite da área de estudo.
    """
    if not caminho_dem.exists():
        raise FileNotFoundError(
            f"Arquivo de elevação não encontrado em: {caminho_dem}\n"
            "Execute primeiro o script '00_download/02_download_elevation.py'."
        )

    print(f"[INFO] Carregando e reprojetando DEM para {dst_crs} ({resolucao}m)...")
    limite_proj = limite_gdf.to_crs(dst_crs)
    minx, miny, maxx, maxy = limite_proj.total_bounds

    with rasterio.open(caminho_dem) as src:
        width = int(np.ceil((maxx - minx) / resolucao))
        height = int(np.ceil((maxy - miny) / resolucao))
        dst_transform = rasterio.transform.from_bounds(minx, miny, maxx, maxy, width, height)

        dst_data = np.full((height, width), src.nodata if src.nodata is not None else -9999.0, dtype=np.float32)

        reproject(
            source=rasterio.band(src, 1),
            destination=dst_data,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear
        )

        dst_meta = {
            'driver': 'GTiff',
            'dtype': 'float32',
            'nodata': -9999.0,
            'width': width,
            'height': height,
            'count': 1,
            'crs': dst_crs,
            'transform': dst_transform,
            'compress': 'lzw'
        }

    return dst_data, dst_meta, dst_transform


def calcular_slope_e_aspect(dem: np.ndarray, res_m: float, nodata_val: float = -9999.0) -> tuple[np.ndarray, np.ndarray]:
    """
    Calcula Declividade (Slope em graus) e Aspecto (Orientação em graus: 0-360)
    usando diferenças finitas com vizinhança 3x3 (método de Horn).
    """
    print("[INFO] Calculando Slope (Declividade) e Aspect (Orientação)...")
    valid_mask = (dem != nodata_val) & (~np.isnan(dem))
    
    dem_filled = np.where(valid_mask, dem, np.nan)
    
    dy, dx = np.gradient(dem_filled, res_m, res_m)
    dz_dx = dx
    dz_dy = -dy
    
    # 1. Slope (em graus: 0 a 90)
    slope_rad = np.arctan(np.sqrt(dz_dx**2 + dz_dy**2))
    slope_deg = np.rad2deg(slope_rad)
    
    # 2. Aspect (em graus: 0 a 360 azimute, onde 0/360 = Norte, 90 = Leste, 180 = Sul, 270 = Oeste)
    aspect_rad = np.arctan2(dz_dy, -dz_dx)
    aspect_deg = np.rad2deg(aspect_rad)
    
    aspect_azimuth = 90.0 - aspect_deg
    aspect_azimuth = np.where(aspect_azimuth < 0, aspect_azimuth + 360.0, aspect_azimuth)
    
    plano_mask = (slope_deg == 0)
    aspect_azimuth[plano_mask] = -1.0
    
    slope_deg[~valid_mask] = nodata_val
    aspect_azimuth[~valid_mask] = nodata_val
    
    return slope_deg.astype(np.float32), aspect_azimuth.astype(np.float32)


# ==========================================
# DISCRETIZAÇÃO POR QUANTIS EMPÍRICOS LOCAIS (CHEN ET AL., 2021)
# ==========================================
def calcular_limiares_quartis(dados_validos: np.ndarray) -> list[float]:
    """Calcula os quantis de 25%, 50% (mediana) e 75% da distribuição local."""
    q25, q50, q75 = np.percentile(dados_validos, [25, 50, 75])
    return [float(q25), float(q50), float(q75)]


def discretizar_por_quartis(valores: np.ndarray | pd.Series, limiares: list[float]) -> np.ndarray | pd.Series:
    """Discretiza em 4 classes balanceadas usando os limiares de quartis [Q1, Q2, Q3]."""
    v = np.asarray(valores)
    classes = np.ones_like(v, dtype=np.uint8)  # Classe 1: <= Q1
    classes[v > limiares[0]] = 2               # Classe 2: (Q1, Q2]
    classes[v > limiares[1]] = 3               # Classe 3: (Q2, Q3]
    classes[v > limiares[2]] = 4               # Classe 4: > Q3
    return classes


def discretizar_aspect_chen(aspect_vals: np.ndarray | pd.Series) -> np.ndarray | pd.Series:
    """
    Aspect (°):
      - 1: North (0°, 45°] U (315°, 360°]
      - 2: East  (45°, 135°]
      - 3: South (135°, 225°]
      - 4: West  (225°, 315°]
    """
    aspect = np.asarray(aspect_vals)
    classes = np.ones_like(aspect, dtype=np.uint8)  # Default North / Flat (1)
    
    classes[(aspect > 45.0) & (aspect <= 135.0)] = 2   # East
    classes[(aspect > 135.0) & (aspect <= 225.0)] = 3  # South
    classes[(aspect > 225.0) & (aspect <= 315.0)] = 4  # West
    return classes


def extrair_e_atualizar_datasets(
    elevation_tif: Path,
    slope_tif: Path,
    aspect_tif: Path,
    elev_cls_tif: Path,
    slope_cls_tif: Path,
    aspect_cls_tif: Path
):
    """
    Extrai Elevation, Slope e Aspect para cada célula de 1 km x 1 km usando estatísticas zonais:
      - Valor contínuo representativo da célula: média (mean)
      - Classe discreta predominante na célula: moda (majority / mode)
    """
    print("\n[DATASET] Extraindo estatísticas zonais (média e moda) por célula de 1 km²...")
    
    if not CSV_ANUAL.exists():
        print(f"[AVISO] Arquivo {CSV_ANUAL} não encontrado. Execute primeiro o script 01_processar_hotspots.py.")
        return

    from rasterstats import zonal_stats

    df_anual = pd.read_csv(CSV_ANUAL)
    GEOJSON_GRADE = AMOSTRAS_DIR / "grade_1km_amostras_fogo_naofogo.geojson"
    
    if GEOJSON_GRADE.exists():
        gdf_polys = gpd.read_file(GEOJSON_GRADE)
    else:
        from shapely.geometry import box
        gdf_pts = gpd.GeoDataFrame(
            df_anual,
            geometry=gpd.points_from_xy(df_anual['longitude_centro'], df_anual['latitude_centro']),
            crs="EPSG:4326"
        ).to_crs(CRS_PROJETADO)
        polys = [box(pt.x - 500, pt.y - 500, pt.x + 500, pt.y + 500) for pt in gdf_pts.geometry]
        gdf_polys = gpd.GeoDataFrame(df_anual, geometry=polys, crs=CRS_PROJETADO)

    with rasterio.open(elevation_tif) as src_meta:
        raster_crs = src_meta.crs
    if gdf_polys.crs != raster_crs:
        gdf_polys = gdf_polys.to_crs(raster_crs)
    
    # 1. Estatísticas zonais contínuas (mean)
    stats_elev = zonal_stats(gdf_polys, str(elevation_tif), stats="mean", nodata=-9999.0)
    stats_slope = zonal_stats(gdf_polys, str(slope_tif), stats="mean", nodata=-9999.0)
    stats_aspect = zonal_stats(gdf_polys, str(aspect_tif), stats="mean", nodata=-9999.0)

    # 2. Estatísticas zonais categóricas (majority / moda da classe na célula)
    stats_elev_cls = zonal_stats(gdf_polys, str(elev_cls_tif), stats="majority", nodata=255)
    stats_slope_cls = zonal_stats(gdf_polys, str(slope_cls_tif), stats="majority", nodata=255)
    stats_aspect_cls = zonal_stats(gdf_polys, str(aspect_cls_tif), stats="majority", nodata=255)

    elev_vals = [s['mean'] if s['mean'] is not None else np.nan for s in stats_elev]
    slope_vals = [s['mean'] if s['mean'] is not None else np.nan for s in stats_slope]
    aspect_vals = [s['mean'] if s['mean'] is not None else np.nan for s in stats_aspect]

    elev_classes = [int(s['majority']) if s['majority'] is not None else 1 for s in stats_elev_cls]
    slope_classes = [int(s['majority']) if s['majority'] is not None else 1 for s in stats_slope_cls]
    aspect_classes = [int(s['majority']) if s['majority'] is not None else 1 for s in stats_aspect_cls]

    # 3. Atualizar DataFrame consolidado
    df_anual['elevation_m'] = np.round(elev_vals, 2)
    df_anual['elevation_classe'] = elev_classes
    
    df_anual['slope_deg'] = np.round(slope_vals, 2)
    df_anual['slope_classe'] = slope_classes
    
    df_anual['aspect_deg'] = np.round(aspect_vals, 2)
    df_anual['aspect_classe'] = aspect_classes
    
    df_anual.to_csv(CSV_ANUAL, index=False)
    print(f"  -> Atualizado: {CSV_ANUAL.name} (Zonal Mean/Majority da célula de 1 km²)")
    
    # Atualizar os CSVs de Treino e Validação
    if CSV_TREINO.exists():
        df_tr = df_anual[df_anual['split'] == 'treino']
        df_tr.to_csv(CSV_TREINO, index=False)
        print(f"  -> Atualizado: {CSV_TREINO.name} ({len(df_tr)} registros)")
        
    if CSV_VALIDACAO.exists():
        df_val = df_anual[df_anual['split'] == 'validacao']
        df_val.to_csv(CSV_VALIDACAO, index=False)
        print(f"  -> Atualizado: {CSV_VALIDACAO.name} ({len(df_val)} registros)")


def main():
    print("=" * 75)
    print("⛰️  PROCESSAMENTO TOPOGRÁFICO E EXTRAÇÃO (CHEN ET AL., 2021)")
    print("=" * 75)
    print(f"DEM de Entrada:   {INPUT_DEM_TIF}")
    print(f"Limite de Estudo: {LIMITE_SHP}")
    print(f"Diretório Saída:  {OUTPUT_DIR}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not LIMITE_SHP.exists():
        raise FileNotFoundError(f"Arquivo de limite não encontrado em: {LIMITE_SHP}")
    limite_gdf = gpd.read_file(LIMITE_SHP)

    # 1. Reprojetar e Recortar Elevação
    elevation_data, meta, transform = carregar_e_reprojetar_dem(
        INPUT_DEM_TIF,
        limite_gdf,
        dst_crs=CRS_PROJETADO,
        resolucao=RESOLUCAO_M
    )

    # 2. Calcular Slope e Aspect
    slope_data, aspect_data = calcular_slope_e_aspect(
        elevation_data,
        res_m=RESOLUCAO_M,
        nodata_val=meta['nodata']
    )

def gerar_painel_a4_topografia(
    elev_cls_tif: Path,
    slope_cls_tif: Path,
    aspect_cls_tif: Path,
    limite_gdf: gpd.GeoDataFrame,
    lim_elev: list[float],
    lim_slope: list[float]
):
    """
    Gera uma prancha gráfica em formato A4 retrato (8.27 x 11.69 pol / 210 x 297 mm)
    com subplots para as 3 variáveis topográficas discretizadas por quartis locais
    conforme metodologia empírica de Chen et al. (2021).
    """
    print("\n[PLOT] Gerando prancha A4 retrato com subplots topográficos (Quartis Locais)...")
    
    fig, axes = plt.subplots(2, 2, figsize=(8.27, 11.69), dpi=300)
    axes_flat = axes.flatten()
    
    configs = [
        {
            'ax': axes_flat[0],
            'tif': elev_cls_tif,
            'titulo': '(A) Elevação (Elevation)',
            'cores': ['#ffffcc', '#c2e699', '#78c679', '#238443'],
            'labels': [
                f'Classe 1: ≤ {lim_elev[0]:.0f} m',
                f'Classe 2: {lim_elev[0]:.0f} - {lim_elev[1]:.0f} m',
                f'Classe 3: {lim_elev[1]:.0f} - {lim_elev[2]:.0f} m',
                f'Classe 4: > {lim_elev[2]:.0f} m'
            ]
        },
        {
            'ax': axes_flat[1],
            'tif': slope_cls_tif,
            'titulo': '(B) Declividade (Slope)',
            'cores': ['#fef0d9', '#fdcc8a', '#fc8d59', '#d7301f'],
            'labels': [
                f'Classe 1: Suave (≤ {lim_slope[0]:.1f}°)',
                f'Classe 2: Moderada ({lim_slope[0]:.1f}° - {lim_slope[1]:.1f}°)',
                f'Classe 3: Forte ({lim_slope[1]:.1f}° - {lim_slope[2]:.1f}°)',
                f'Classe 4: Escarpada (> {lim_slope[2]:.1f}°)'
            ]
        },
        {
            'ax': axes_flat[2],
            'tif': aspect_cls_tif,
            'titulo': '(C) Orientação da Encosta (Aspect)',
            'cores': ['#4575b4', '#91bfdb', '#fee090', '#fc8d59'],
            'labels': [
                'Classe 1: Norte (315°-45°) / Plano',
                'Classe 2: Leste (45°-135°)',
                'Classe 3: Sul (135°-225°)',
                'Classe 4: Oeste (225°-315°)'
            ]
        }
    ]
    
    for cfg in configs:
        ax = cfg['ax']
        tif_path = cfg['tif']
        cores = cfg['cores']
        labels = cfg['labels']
        
        cmap = ListedColormap(cores)
        norm = BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5], cmap.N)
        
        if tif_path.exists():
            with rasterio.open(tif_path) as src:
                data = src.read(1)
                bounds = src.bounds
                extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
                data_masked = np.ma.masked_equal(data, 255)
                
                ax.imshow(data_masked, extent=extent, origin='upper', cmap=cmap, norm=norm, interpolation='nearest')
                limite_proj = limite_gdf.to_crs(src.crs)
                limite_proj.boundary.plot(ax=ax, color='black', linewidth=0.6)
                
        ax.set_title(cfg['titulo'], fontsize=9, fontweight='bold', pad=4)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')
        
        patches = [mpatches.Patch(color=cores[i], label=labels[i]) for i in range(4)]
        ax.legend(handles=patches, loc='lower left', fontsize=6.5, frameon=True, framealpha=0.85)

    ax_info = axes_flat[3]
    ax_info.axis('off')
    ax_info.set_xlim(0, 1)
    ax_info.set_ylim(0, 1)
    
    ax_info.annotate('N', xy=(0.5, 0.70), xytext=(0.5, 0.40),
                     arrowprops=dict(facecolor='black', edgecolor='black', width=2.5, headwidth=9),
                     ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax_info.plot([0.3, 0.7], [0.25, 0.25], color='black', linewidth=3)
    ax_info.text(0.5, 0.28, '10 km', ha='center', va='bottom', fontsize=8, fontweight='bold')
    ax_info.text(0.5, 0.12, 'Projeção: SIRGAS 2000 / UTM zone 22S\nFonte do DEM: SRTM 30m / Quartis Locais SJP',
                 ha='center', va='bottom', fontsize=6.5, color='#333333', multialignment='center')

    fig.suptitle('Fatores Topográficos de Risco de Incêndio (Quantis Empíricos - Chen et al., 2021)\nSão José dos Pinhais - PR',
                 fontsize=11, fontweight='bold', y=0.97)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.05, wspace=0.12, hspace=0.15)

    out_painel = OUTPUT_DIR / "painel_a4_classes_topografia.png"
    plt.savefig(out_painel, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Prancha A4 Topográfica salva: {out_painel.name}")


def main():
    print("=" * 75)
    print("⛰️  PROCESSAMENTO TOPOGRÁFICO E EXTRAÇÃO (QUANTIS LOCAIS)")
    print("=" * 75)
    print(f"DEM de Entrada:   {INPUT_DEM_TIF}")
    print(f"Limite de Estudo: {LIMITE_SHP}")
    print(f"Diretório Saída:  {OUTPUT_DIR}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not LIMITE_SHP.exists():
        raise FileNotFoundError(f"Arquivo de limite não encontrado em: {LIMITE_SHP}")
    limite_gdf = gpd.read_file(LIMITE_SHP)

    # 1. Reprojetar e Recortar Elevação
    elevation_data, meta, transform = carregar_e_reprojetar_dem(
        INPUT_DEM_TIF,
        limite_gdf,
        dst_crs=CRS_PROJETADO,
        resolucao=RESOLUCAO_M
    )

    # 2. Calcular Slope e Aspect
    slope_data, aspect_data = calcular_slope_e_aspect(
        elevation_data,
        res_m=RESOLUCAO_M,
        nodata_val=meta['nodata']
    )

    # 3. Exportar os Rasters Contínuos
    elevation_out = OUTPUT_DIR / "elevation.tif"
    with rasterio.open(elevation_out, 'w', **meta) as dst:
        dst.write(elevation_data, 1)
    print(f"[SAÍDA] Elevação contínua salva: {elevation_out}")

    slope_out = OUTPUT_DIR / "slope.tif"
    with rasterio.open(slope_out, 'w', **meta) as dst:
        dst.write(slope_data, 1)
    print(f"[SAÍDA] Slope contínuo salvo:     {slope_out}")

    aspect_out = OUTPUT_DIR / "aspect.tif"
    with rasterio.open(aspect_out, 'w', **meta) as dst:
        dst.write(aspect_data, 1)
    print(f"[SAÍDA] Aspect contínuo salvo:    {aspect_out}")

    # 4. Calcular Quartis Empíricos Locais
    valid_mask = (elevation_data != meta['nodata'])
    lim_elev = calcular_limiares_quartis(elevation_data[valid_mask])
    lim_slope = calcular_limiares_quartis(slope_data[valid_mask])
    print(f"[INFO] Quartis locais de Elevação (m):  Q1={lim_elev[0]:.1f}, Q2={lim_elev[1]:.1f}, Q3={lim_elev[2]:.1f}")
    print(f"[INFO] Quartis locais de Declividade (°): Q1={lim_slope[0]:.1f}, Q2={lim_slope[1]:.1f}, Q3={lim_slope[2]:.1f}")

    # 5. Gerar e Exportar Rasters de Classes
    meta_class = meta.copy()
    meta_class.update({'dtype': 'uint8', 'nodata': 255})
    
    elev_cls_raster = np.full_like(elevation_data, 255, dtype=np.uint8)
    elev_cls_raster[valid_mask] = discretizar_por_quartis(elevation_data[valid_mask], lim_elev)
    
    slope_cls_raster = np.full_like(slope_data, 255, dtype=np.uint8)
    slope_cls_raster[valid_mask] = discretizar_por_quartis(slope_data[valid_mask], lim_slope)
    
    aspect_cls_raster = np.full_like(aspect_data, 255, dtype=np.uint8)
    aspect_cls_raster[valid_mask] = discretizar_aspect_chen(aspect_data[valid_mask])
    
    elev_cls_out = OUTPUT_DIR / "elevation_classes.tif"
    with rasterio.open(elev_cls_out, 'w', **meta_class) as dst:
        dst.write(elev_cls_raster, 1)
        
    slope_cls_out = OUTPUT_DIR / "slope_classes.tif"
    with rasterio.open(slope_cls_out, 'w', **meta_class) as dst:
        dst.write(slope_cls_raster, 1)
        
    aspect_cls_out = OUTPUT_DIR / "aspect_classes.tif"
    with rasterio.open(aspect_cls_out, 'w', **meta_class) as dst:
        dst.write(aspect_cls_raster, 1)

    print(f"[SAÍDA] Rasters de classes topográficas calibradas salvos (1 a 4).")

    # 6. Extrair para os polígonos das células de 1 km² (Média contínua e Moda da classe)
    extrair_e_atualizar_datasets(elevation_out, slope_out, aspect_out, elev_cls_out, slope_cls_out, aspect_cls_out)

    # 7. Gerar Prancha Gráfica A4 Retrato
    gerar_painel_a4_topografia(elev_cls_out, slope_cls_out, aspect_cls_out, limite_gdf, lim_elev, lim_slope)

    print("\n[SUCESSO] Todos os rasters, prancha A4 e extrações topográficas foram concluídos!")
    print(f"Arquivos salvos em: {OUTPUT_DIR}\n")


if __name__ == "__main__":
    main()

