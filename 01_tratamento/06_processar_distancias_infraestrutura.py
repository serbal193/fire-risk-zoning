"""
Script: 06_processar_distancias_infraestrutura.py
Etapa: 01_tratamento

Descrição:
    Processa e calcula as distâncias euclidianas (em metros) de infraestrutura antrópica,
    conforme metodologia de Chen et al. (2021):
    
    1. Distância a Estradas / Vias (DR - Distance to Roads):
       - Fonte: `input/01_vetores/vias_urbanas_periurbanas.shp` (reprojetado para EPSG:31982).
       - Rasterização e cálculo da distância euclidiana (`scipy.ndimage.distance_transform_edt`) a 30m.
       
    2. Distância a Áreas Urbanizadas / Assentamentos (DS - Distance to Settlements):
       - Fonte: `input/03_lulc/mapbiomas-brazil-collection-101-saojosedospinhais-{ano}.tif`
       - Extrai as classes de área urbanizada e infraestrutura urbana do MapBiomas (Classe 24: Área Urbanizada, Classe 30: Mineração / Não Vegetada).
       - Rasterização e cálculo da distância euclidiana ano a ano (2013-2025).

    3. Discretização de Classes (Chen et al., 2021 - Tabela 3):
       - DR (Distância a Estradas / Vias em metros - Relação Inversa de Risco):
           * Classe 4 (Muito Próximo / Alto Risco):      <= 832.6 m
           * Classe 3 (Próximo / Moderado-Alto):         832.6 < DR <= 2043.7 m
           * Classe 2 (Distante / Moderado-Baixo):       2043.7 < DR <= 3860.3 m
           * Classe 1 (Muito Distante / Baixo Risco):    > 3860.3 m
           
       - DS (Distância a Áreas Urbanas em metros - Relação Inversa de Risco):
           * Classe 4 (Muito Próximo / Alto Risco):      <= 356.5 m
           * Classe 3 (Próximo / Moderado-Alto):         356.5 < DS <= 635.7 m
           * Classe 2 (Distante / Moderado-Baixo):       635.7 < DS <= 1041.8 m
           * Classe 1 (Muito Distante / Baixo Risco):    > 1041.8 m

    4. Estatísticas Zonais por Célula da Grade (1 km x 1 km):
       - Extrai valor médio contínuo (`dist_estradas_m`, `dist_urbano_m`)
       - Extrai moda da classe predominante (`dr_classe`, `ds_classe`)
       - Atualiza os 3 datasets CSV:
           * output/01_processar_hotspots/grade_1km_amostras_anuais.csv
           * output/01_processar_hotspots/grade_1km_amostras_treino.csv
           * output/01_processar_hotspots/grade_1km_amostras_validacao.csv

    5. Geração de Pranchas A4 Retrato com Subplots:
       - `painel_a4_classes_dr_estradas.png` (Mapa de Classes de DR com Seta Norte e Escala)
       - `painel_a4_classes_ds_urbano_2013_2025.png` (Grid 5x3 com a dinâmica anual das classes de DS)
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
from rasterio.transform import from_bounds
from rasterio.warp import reproject, Resampling
from rasterio.features import rasterize
import geopandas as gpd
from scipy.ndimage import distance_transform_edt
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

VIAS_SHP = BASE_DIR / "input" / "01_vetores" / "vias_urbanas_periurbanas.shp"
LULC_DIR = BASE_DIR / "input" / "03_lulc"

if (BASE_DIR / "input" / "01_vetores" / "SJP.shp").exists():
    LIMITE_SHP = BASE_DIR / "input" / "01_vetores" / "SJP.shp"
else:
    LIMITE_SHP = BASE_DIR / "output" / "01_vetores" / "SJP.shp"

AMOSTRAS_DIR = BASE_DIR / "output" / "01_processar_hotspots"
CSV_ANUAL = AMOSTRAS_DIR / "grade_1km_amostras_anuais.csv"
CSV_TREINO = AMOSTRAS_DIR / "grade_1km_amostras_treino.csv"
CSV_VALIDACAO = AMOSTRAS_DIR / "grade_1km_amostras_validacao.csv"

OUTPUT_DIR = BASE_DIR / "output" / Path(__file__).stem
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ANOS = list(range(2013, 2026))
CRS_PROJETADO = "EPSG:31982"    # SIRGAS 2000 / UTM 22S
RESOLUCAO_M = 30.0              # Resolução espacial 30m

# Classes MapBiomas de Área Urbanizada / Infraestrutura
CLASSES_URBANAS = [24, 30]


# ==========================================
# DISCRETIZAÇÃO POR QUANTIS EMPÍRICOS LOCAIS
# ==========================================
def calcular_limiares_distancia(dist_validos: np.ndarray) -> list[float]:
    """Calcula os quantis empíricos locais (25%, 50%, 75%) de distância."""
    q25, q50, q75 = np.percentile(dist_validos, [25, 50, 75])
    return [float(q25), float(q50), float(q75)]


def discretizar_distancia_decrescente(dist_vals: np.ndarray | pd.Series, limiares: list[float]) -> np.ndarray | pd.Series:
    """
    Discretiza distância em 4 classes onde MENOR distância = MAIOR risco antrópico:
      - Classe 4 (Muito Próximo / Alto Risco):      <= Q1
      - Classe 3 (Próximo / Moderado-Alto):         Q1 < Dist <= Q2
      - Classe 2 (Distante / Moderado-Baixo):       Q2 < Dist <= Q3
      - Classe 1 (Muito Distante / Baixo Risco):    > Q3
    """
    v = np.asarray(dist_vals)
    classes = np.ones_like(v, dtype=np.uint8)  # Default: 1 (> Q3)
    classes[(v > limiares[1]) & (v <= limiares[2])] = 2
    classes[(v > limiares[0]) & (v <= limiares[1])] = 3
    classes[v <= limiares[0]] = 4              # Mais próximo = Classe 4
    return classes


# ==========================================
# 1. PROCESSAMENTO DE DISTÂNCIA A ESTRADAS (DR)
# ==========================================
def processar_distancia_estradas(limite_gdf: gpd.GeoDataFrame) -> tuple[Path, Path, list[float]]:
    """
    Carrega o vetor de vias urbanas/periurbanas, rasteriza para resolução de 30m
    e calcula a transformada de distância euclidiana exata com buffer de 30m.
    """
    print("\n[DR] Processando distância a estradas e vias...")
    
    if not VIAS_SHP.exists():
        raise FileNotFoundError(f"Arquivo de vias não encontrado em: {VIAS_SHP}")
        
    vias_gdf = gpd.read_file(VIAS_SHP).to_crs(CRS_PROJETADO)
    limite_proj = limite_gdf.to_crs(CRS_PROJETADO)
    
    minx, miny, maxx, maxy = limite_proj.total_bounds
    pad = 2000.0
    minx -= pad; miny -= pad; maxx += pad; maxy += pad
    
    width = int(np.ceil((maxx - minx) / RESOLUCAO_M))
    height = int(np.ceil((maxy - miny) / RESOLUCAO_M))
    transform = from_bounds(minx, miny, maxx, maxy, width, height)
    
    meta = {
        'driver': 'GTiff',
        'dtype': 'float32',
        'nodata': -9999.0,
        'width': width,
        'height': height,
        'count': 1,
        'crs': CRS_PROJETADO,
        'transform': transform,
        'compress': 'lzw'
    }

    # 1. Aplicar buffer de 30 metros nas geometrias das vias
    print("  -> Aplicando buffer de 30 metros nas geometrias das vias...")
    vias_buffered = vias_gdf.geometry.buffer(30.0)

    # 2. Queimar no grid binário
    shapes = [(geom, 1) for geom in vias_buffered if geom.is_valid and not geom.is_empty]
    raster_vias = rasterize(shapes, out_shape=(height, width), transform=transform, fill=0, dtype=np.uint8)
    
    # 3. Distância Euclidiana em metros
    dist_matrix = distance_transform_edt(raster_vias == 0, sampling=(RESOLUCAO_M, RESOLUCAO_M)).astype(np.float32)

    # 4. Mascarar fora do limite municipal
    mask_limite = rasterize([(geom, 1) for geom in limite_proj.geometry], out_shape=(height, width), transform=transform, fill=0, dtype=np.uint8)
    dist_matrix[mask_limite == 0] = -9999.0

    # 5. Salvar GeoTIFF Contínuo
    out_dr = OUTPUT_DIR / "SJP_DR_estradas_distancia.tif"
    with rasterio.open(out_dr, 'w', **meta) as dst:
        dst.write(dist_matrix, 1)

    # 6. Calcular Quartis Locais de DR
    valid = (dist_matrix != -9999.0)
    lim_dr = calcular_limiares_distancia(dist_matrix[valid])
    print(f"[INFO] Quantis locais de Distância a Estradas (DR em metros): Q1={lim_dr[0]:.1f}m, Q2={lim_dr[1]:.1f}m, Q3={lim_dr[2]:.1f}m")

    # 7. Salvar GeoTIFF de Classes
    meta_cls = meta.copy()
    meta_cls.update({'dtype': 'uint8', 'nodata': 255})
    
    cls_dr = np.full_like(dist_matrix, 255, dtype=np.uint8)
    cls_dr[valid] = discretizar_distancia_decrescente(dist_matrix[valid], lim_dr)

    out_dr_cls = OUTPUT_DIR / "SJP_DR_estradas_classes.tif"
    with rasterio.open(out_dr_cls, 'w', **meta_cls) as dst:
        dst.write(cls_dr, 1)

    print(f"✅ Raster de Distância Contínua a Estradas (DR) salvo: {out_dr.name}")
    print(f"✅ Raster de Classes DR calibradas salvo: {out_dr_cls.name}")
    return out_dr, out_dr_cls, lim_dr


# ==========================================
# 2. PROCESSAMENTO DE DISTÂNCIA A URBANO (DS)
# ==========================================
def processar_distancia_urbano_anual(limite_gdf: gpd.GeoDataFrame) -> tuple[dict[int, tuple[Path, Path]], list[float]]:
    """
    Processa ano a ano a mancha urbana a partir das coleções do MapBiomas (2013 a 2025),
    calcula as matrizes de distância euclidiana, extrai os quantis empíricos da série temporal
    e exporta os rasters contínuos e classificados.
    """
    print("\n[DS] Processando distância a áreas urbanizadas (MapBiomas 2013-2025)...")
    
    limite_proj = limite_gdf.to_crs(CRS_PROJETADO)
    minx, miny, maxx, maxy = limite_proj.total_bounds
    pad = 2000.0
    minx -= pad; miny -= pad; maxx += pad; maxy += pad
    
    width = int(np.ceil((maxx - minx) / RESOLUCAO_M))
    height = int(np.ceil((maxy - miny) / RESOLUCAO_M))
    transform = from_bounds(minx, miny, maxx, maxy, width, height)
    
    meta_dst = {
        'driver': 'GTiff',
        'dtype': 'float32',
        'nodata': -9999.0,
        'width': width,
        'height': height,
        'count': 1,
        'crs': CRS_PROJETADO,
        'transform': transform,
        'compress': 'lzw'
    }

    mask_limite = rasterize([(geom, 1) for geom in limite_proj.geometry], out_shape=(height, width), transform=transform, fill=0, dtype=np.uint8)

    matrizes_dist = {}
    amostras_todos_anos = []

    for ano in ANOS:
        caminho_mapb = LULC_DIR / f"mapbiomas-brazil-collection-101-saojosedospinhais-{ano}.tif"
        if not caminho_mapb.exists():
            print(f"[AVISO] Raster MapBiomas {ano} não encontrado em {caminho_mapb}")
            continue
            
        with rasterio.open(caminho_mapb) as src:
            src_data = src.read(1)
            dst_data = np.zeros((height, width), dtype=np.uint8)
            reproject(
                source=src_data,
                destination=dst_data,
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=CRS_PROJETADO,
                resampling=Resampling.nearest
            )

        mask_urbano = np.isin(dst_data, CLASSES_URBANAS).astype(np.uint8)

        if np.sum(mask_urbano) > 0:
            dist_matrix = distance_transform_edt(mask_urbano == 0, sampling=(RESOLUCAO_M, RESOLUCAO_M)).astype(np.float32)
        else:
            dist_matrix = np.full((height, width), 99999.0, dtype=np.float32)

        dist_matrix[mask_limite == 0] = -9999.0
        matrizes_dist[ano] = dist_matrix
        
        valid = (dist_matrix != -9999.0)
        pts = np.random.choice(dist_matrix[valid], size=min(10000, np.sum(valid)), replace=False)
        amostras_todos_anos.extend(pts)

    # 1. Calcular Quartis Globais de DS (2013-2025)
    lim_ds = calcular_limiares_distancia(np.array(amostras_todos_anos))
    print(f"[INFO] Quantis locais de Distância a Urbano (DS em metros): Q1={lim_ds[0]:.1f}m, Q2={lim_ds[1]:.1f}m, Q3={lim_ds[2]:.1f}m")

    # 2. Exportar GeoTIFFs
    meta_cls = meta_dst.copy()
    meta_cls.update({'dtype': 'uint8', 'nodata': 255})
    arquivos_ds_ano = {}

    for ano, dist_matrix in matrizes_dist.items():
        out_ds = OUTPUT_DIR / f"SJP_DS_urbano_{ano}_distancia.tif"
        with rasterio.open(out_ds, 'w', **meta_dst) as dst:
            dst.write(dist_matrix, 1)

        valid = (dist_matrix != -9999.0)
        cls_ds = np.full_like(dist_matrix, 255, dtype=np.uint8)
        cls_ds[valid] = discretizar_distancia_decrescente(dist_matrix[valid], lim_ds)

        out_ds_cls = OUTPUT_DIR / f"SJP_DS_urbano_{ano}_classes.tif"
        with rasterio.open(out_ds_cls, 'w', **meta_cls) as dst:
            dst.write(cls_ds, 1)

        arquivos_ds_ano[ano] = (out_ds, out_ds_cls)

    print(f"✅ Rasters de Distância a Assentamentos/Urbano (DS 2013-2025) gerados com sucesso!")
    return arquivos_ds_ano, lim_ds


# ==========================================
# 3. GERAÇÃO DE PAINÉIS GRÁFICOS A4 RETRATO
# ==========================================
def gerar_painel_a4_dr(out_dr: Path, out_dr_cls: Path, limite_gdf: gpd.GeoDataFrame, lim_dr: list[float]):
    """Gera mapa temático A4 com o gradiente contínuo de distância e as classes de Distância a Estradas (DR)."""
    print("\n[PLOT] Gerando mapa temático de Distância e Classes de Estradas (DR)...")
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.27, 11.69), dpi=300)
    
    limite_proj = limite_gdf.to_crs(CRS_PROJETADO)
    
    with rasterio.open(out_dr) as src:
        data_dist = src.read(1)
        bounds = src.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        dist_masked_km = np.ma.masked_equal(data_dist, -9999.0) / 1000.0
        
        im1 = ax1.imshow(dist_masked_km, extent=extent, origin='upper', cmap='viridis_r', interpolation='bilinear')
        limite_proj.boundary.plot(ax=ax1, color='black', linewidth=0.8)
        
        cbar1 = plt.colorbar(im1, ax=ax1, orientation='vertical', pad=0.02, shrink=0.85)
        cbar1.set_label('Distância a Vias / Estradas (km)', fontsize=8, fontweight='bold')
        cbar1.ax.tick_params(labelsize=7)

    ax1.set_title('(A) Distância Euclidiana Contínua a Vias / Estradas (DR)', fontsize=10, fontweight='bold', pad=4)
    ax1.set_xticks([])
    ax1.set_yticks([])

    cores = ['#2b83ba', '#abdda4', '#fdae61', '#d7191c']
    labels = [
        f'Classe 1: Muito Distante (> {lim_dr[2]:.0f} m)',
        f'Classe 2: Distante ({lim_dr[1]:.0f} - {lim_dr[2]:.0f} m)',
        f'Classe 3: Próximo ({lim_dr[0]:.0f} - {lim_dr[1]:.0f} m)',
        f'Classe 4: Muito Próximo / Alto Risco (≤ {lim_dr[0]:.0f} m)'
    ]
    cmap_cls = ListedColormap(cores)
    norm_cls = BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5], cmap_cls.N)

    with rasterio.open(out_dr_cls) as src:
        data_cls = src.read(1)
        cls_masked = np.ma.masked_equal(data_cls, 255)
        
        ax2.imshow(cls_masked, extent=extent, origin='upper', cmap=cmap_cls, norm=norm_cls, interpolation='nearest')
        limite_proj.boundary.plot(ax=ax2, color='black', linewidth=0.8)

    minx, miny, maxx, maxy = extent
    x_arrow, y_arrow = minx + (maxx - minx) * 0.08, maxy - (maxy - miny) * 0.08
    ax2.annotate('N', xy=(x_arrow, y_arrow), xytext=(x_arrow, y_arrow - (maxy - miny) * 0.05),
                 arrowprops=dict(facecolor='black', edgecolor='black', width=2, headwidth=8),
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

    scale_len_m = 10000.0
    scale_x0 = minx + (maxx - minx) * 0.05
    scale_y0 = miny + (maxy - miny) * 0.05
    ax2.plot([scale_x0, scale_x0 + scale_len_m], [scale_y0, scale_y0], color='black', linewidth=3)
    ax2.text(scale_x0 + scale_len_m / 2, scale_y0 + (maxy - miny) * 0.015, '10 km',
             ha='center', va='bottom', fontsize=8, fontweight='bold',
             bbox=dict(boxstyle='square,pad=0.2', facecolor='white', alpha=0.85, edgecolor='none'))

    patches = [mpatches.Patch(color=cores[i], label=labels[i]) for i in range(4)]
    ax2.legend(handles=patches, loc='lower right', fontsize=7.5, frameon=True, framealpha=0.9)

    ax2.set_title('(B) Classes de Risco por Distância a Estradas (Quantis Empíricos - Chen et al., 2021)', fontsize=10, fontweight='bold', pad=4)
    ax2.set_xticks([])
    ax2.set_yticks([])

    fig.suptitle('Fator Antrópico de Risco: Distância a Estradas / Vias (DR)\nSão José dos Pinhais - PR (Buffer 30m / Quartis Locais)',
                 fontsize=11, fontweight='bold', y=0.98)
    plt.subplots_adjust(left=0.06, right=0.94, top=0.92, bottom=0.04, hspace=0.15)

    out_png = OUTPUT_DIR / "painel_a4_classes_dr_estradas.png"
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Prancha A4 de DR salva: {out_png.name}")


def gerar_painel_a4_ds(limite_gdf: gpd.GeoDataFrame, lim_ds: list[float]):
    """Gera prancha gráfica A4 com subplots (2013-2025) para Distância a Áreas Urbanizadas (DS)."""
    print("\n[PLOT] Gerando prancha A4 retrato com subplots para Distância a Urbano (DS)...")
    
    fig, axes = plt.subplots(5, 3, figsize=(8.27, 11.69), dpi=300)
    axes_flat = axes.flatten()
    
    cores = ['#2b83ba', '#abdda4', '#fdae61', '#d7191c']
    labels = [
        f'Classe 1: Muito Distante (> {lim_ds[2]:.0f} m)',
        f'Classe 2: Distante ({lim_ds[1]:.0f} - {lim_ds[2]:.0f} m)',
        f'Classe 3: Próximo ({lim_ds[0]:.0f} - {lim_ds[1]:.0f} m)',
        f'Classe 4: Muito Próximo / Alto Risco (≤ {lim_ds[0]:.0f} m)'
    ]
    cmap = ListedColormap(cores)
    norm = BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5], cmap.N)

    for idx, ano in enumerate(ANOS):
        ax = axes_flat[idx]
        caminho_cls = OUTPUT_DIR / f"SJP_DS_urbano_{ano}_classes.tif"
        
        if caminho_cls.exists():
            with rasterio.open(caminho_cls) as src:
                data = src.read(1)
                bounds = src.bounds
                extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
                data_masked = np.ma.masked_equal(data, 255)
                
                ax.imshow(data_masked, extent=extent, origin='upper', cmap=cmap, norm=norm, interpolation='nearest')
                limite_proj = limite_gdf.to_crs(src.crs)
                limite_proj.boundary.plot(ax=ax, color='black', linewidth=0.5)
        else:
            ax.text(0.5, 0.5, f"Sem dados\n{ano}", ha='center', va='center', transform=ax.transAxes, fontsize=8)

        ax.set_title(f"{ano}", fontsize=8, fontweight='bold', pad=2)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')

    # Desabilitar eixo 14 e utilizar o espaço do eixo 13 (abaixo de 2025) para quadro de informações
    axes_flat[14].axis('off')
    
    ax_info = axes_flat[13]
    ax_info.axis('off')
    ax_info.set_xlim(0, 1)
    ax_info.set_ylim(0, 1)
    
    # Seta Norte
    ax_info.annotate('N', xy=(0.5, 0.75), xytext=(0.5, 0.45),
                     arrowprops=dict(facecolor='black', edgecolor='black', width=2, headwidth=7),
                     ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Barra de Escala (10 km)
    ax_info.plot([0.3, 0.7], [0.25, 0.25], color='black', linewidth=2.5)
    ax_info.text(0.5, 0.28, '10 km', ha='center', va='bottom', fontsize=7, fontweight='bold')
    ax_info.text(0.5, 0.12, 'Projeção: SIRGAS 2000 / UTM 22S\nFonte: MapBiomas Coleção 10.1',
                 ha='center', va='bottom', fontsize=5.5, color='#444444', multialignment='center')

    # Legenda
    patches = [mpatches.Patch(color=cores[i], label=labels[i]) for i in range(4)]
    fig.legend(
        handles=patches,
        loc='lower center',
        ncol=2,
        fontsize=7,
        frameon=True,
        bbox_to_anchor=(0.5, 0.02)
    )

    fig.suptitle('Série Histórica de Classes de Risco por Distância a Urbano (DS 2013-2025)\nSão José dos Pinhais - PR (Chen et al., 2021)', fontsize=10, fontweight='bold', y=0.98)
    plt.subplots_adjust(left=0.04, right=0.96, top=0.93, bottom=0.08, wspace=0.10, hspace=0.20)

    out_png = OUTPUT_DIR / "painel_a4_classes_ds_urbano_2013_2025.png"
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Prancha A4 de DS salva: {out_png.name}")


# ==========================================
# 4. EXTRAÇÃO ZONAL E ATUALIZAÇÃO DOS DATASETS
# ==========================================
def extrair_e_atualizar_datasets(out_dr: Path, out_dr_cls: Path, arquivos_ds_ano: dict, limite_gdf: gpd.GeoDataFrame):
    """
    Extrai DR (estático) e DS (dinâmico anual) para cada célula de 1 km x 1 km:
      - Valor contínuo representativo da célula: média (mean)
      - Classe discreta predominante na célula: moda (majority / mode)
    """
    print("\n[DATASET] Extraindo estatísticas zonais de DR e DS por célula de 1 km²...")
    
    if not CSV_ANUAL.exists():
        raise FileNotFoundError(f"Arquivo de dataset não encontrado: {CSV_ANUAL}")

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
    # 1. Extração de DR (Distância a Estradas - no centróide de cada célula)
    print("  -> Extraindo DR (Estradas) no centróide...")
    gdf_pts = gpd.GeoDataFrame(
        df_anual,
        geometry=gpd.points_from_xy(df_anual['longitude_centro'], df_anual['latitude_centro']),
        crs="EPSG:4326"
    ).to_crs(CRS_PROJETADO)

    coords_pts = [(pt.x, pt.y) for pt in gdf_pts.geometry]

    with rasterio.open(out_dr) as src_dr:
        valores_dr = [v[0] for v in src_dr.sample(coords_pts)]
    with rasterio.open(out_dr_cls) as src_dr_cls:
        classes_dr = [v[0] for v in src_dr_cls.sample(coords_pts)]

    df_anual['dist_estradas_m'] = [np.round(v, 2) if v != -9999.0 else np.nan for v in valores_dr]
    df_anual['dr_classe'] = [int(c) if c != 255 else 1 for c in classes_dr]

    # 2. Extração de DS (Distância a Urbano - no centróide da célula ano a ano)
    print("  -> Extraindo DS (Áreas Urbanizadas por ano) no centróide...")
    df_anual['dist_urbano_m'] = np.nan
    df_anual['ds_classe'] = np.nan

    anos_presentes = sorted(df_anual['ano'].unique())
    for ano in anos_presentes:
        ano = int(ano)
        if ano not in arquivos_ds_ano:
            continue
            
        mask_ano = (df_anual['ano'] == ano)
        indices_ano = df_anual[mask_ano].index
        gdf_ano_pts = gdf_pts.iloc[indices_ano]
        coords_ano = [(pt.x, pt.y) for pt in gdf_ano_pts.geometry]
        
        caminho_ds, caminho_ds_cls = arquivos_ds_ano[ano]
        with rasterio.open(caminho_ds) as src_ds:
            valores_ds = [v[0] for v in src_ds.sample(coords_ano)]
        with rasterio.open(caminho_ds_cls) as src_ds_cls:
            classes_ds = [v[0] for v in src_ds_cls.sample(coords_ano)]
        
        df_anual.loc[mask_ano, 'dist_urbano_m'] = [np.round(v, 2) if v != -9999.0 else np.nan for v in valores_ds]
        df_anual.loc[mask_ano, 'ds_classe'] = [int(c) if c != 255 else 1 for c in classes_ds]

    # Converter colunas de classes para int
    df_anual['dr_classe'] = df_anual['dr_classe'].astype('Int64')
    df_anual['ds_classe'] = df_anual['ds_classe'].astype('Int64')

    # Salvar CSVs atualizados
    df_anual.to_csv(CSV_ANUAL, index=False)
    print(f"\n[SAÍDA] Dataset consolidado atualizado: {CSV_ANUAL.name} (DR e DS Zonal Stats)")

    if CSV_TREINO.exists():
        df_tr = df_anual[df_anual['split'] == 'treino']
        df_tr.to_csv(CSV_TREINO, index=False)
        print(f"[SAÍDA] Dataset de Treino atualizado:     {CSV_TREINO.name} ({len(df_tr)} registros)")

    if CSV_VALIDACAO.exists():
        df_val = df_anual[df_anual['split'] == 'validacao']
        df_val.to_csv(CSV_VALIDACAO, index=False)
        print(f"[SAÍDA] Dataset de Validação atualizado:  {CSV_VALIDACAO.name} ({len(df_val)} registros)")


# ==========================================
# MAIN
# ==========================================
def main():
    print("=" * 75)
    print("🚗 PROCESSAMENTO DE INFRAESTRUTURA: DR (ESTRADAS) E DS (URBANO)")
    print("=" * 75)
    print(f"Vias de Entrada:       {VIAS_SHP}")
    print(f"LULC MapBiomas:        {LULC_DIR}")
    print(f"Diretório de Saída:    {OUTPUT_DIR}")

    if not LIMITE_SHP.exists():
        raise FileNotFoundError(f"Arquivo de limite não encontrado em: {LIMITE_SHP}")
    limite_gdf = gpd.read_file(LIMITE_SHP)

    # 1. Processar Distância a Estradas (DR)
    out_dr, out_dr_cls, lim_dr = processar_distancia_estradas(limite_gdf)

    # 2. Processar Distância a Assentamentos/Urbano (DS)
    arquivos_ds_ano, lim_ds = processar_distancia_urbano_anual(limite_gdf)

    # 3. Extração Zonal e Atualização dos Datasets
    extrair_e_atualizar_datasets(out_dr, out_dr_cls, arquivos_ds_ano, limite_gdf)

    # 4. Gerar Pranchas A4 Retrato
    gerar_painel_a4_dr(out_dr, out_dr_cls, limite_gdf, lim_dr)
    gerar_painel_a4_ds(limite_gdf, lim_ds)

    print("\n" + "=" * 75)
    print("✨ PROCESSAMENTO DE DR E DS CONCLUÍDO COM SUCESSO!")
    print("=" * 75)


if __name__ == "__main__":
    main()
