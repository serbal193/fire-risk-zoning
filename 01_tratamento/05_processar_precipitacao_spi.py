"""
Script: 05_processar_spi.py
Etapa: 01_tratamento

Descrição:
    Processa a série temporal mensal de precipitação CHIRPS v2.0 (2013 a 2025)
    e calcula o índice meteorológico de seca SPI (Standardized Precipitation Index):
    
    1. Cálculo do SPI (Standardized Precipitation Index) Anual:
       - Ajusta distribuição Gamma mensal/anual conforme metodologia de McKee et al. / Rabiei et al. (2022).
       - Transforma a probabilidade acumulada em variável normal padrão $Z \sim N(0, 1)$ (SPI).
       
    2. Discretização de Classes (Rabiei et al., 2022; McKee et al.):
       - SPI (Índice Padronizado de Seca - Relação Inversa com Risco de Fogo):
           * Classe 4 (Seca Severa / Alto Risco):      SPI <= -1.50
           * Classe 3 (Seca Moderada / Risco Médio):   -1.50 < SPI <= -0.50
           * Classe 2 (Normal / Próximo à Média):      -0.50 < SPI <= 0.50
           * Classe 1 (Úmido / Baixo Risco):           SPI > 0.50

    3. Estatísticas Zonais por Célula da Grade (1 km x 1 km):
       - Extrai o valor médio contínuo (`spi_anual`)
       - Extrai a classe modal predominante (`spi_classe`)
       - Atualiza os 3 datasets CSV:
           * output/01_processar_hotspots/grade_1km_amostras_anuais.csv
           * output/01_processar_hotspots/grade_1km_amostras_treino.csv
           * output/01_processar_hotspots/grade_1km_amostras_validacao.csv

    4. Geração de Prancha A4 Retrato com Subplots (2013 a 2025):
       - `painel_a4_classes_spi_2013_2025.png` (Grid 5x3 com classes de seca/SPI, Seta Norte e Barra de Escala única)
       - Rasters GeoTIFF anuais contínuos e classificados (`SJP_spi_{ano}.tif` e `SJP_spi_{ano}_classes.tif`)
"""

import sys
import os

# Configuração GDAL/Rasterio/Fiona para caminhos com caracteres especiais (Windows/acentuação)
os.environ['GDAL_FILENAME_IS_UTF8'] = 'NO'
os.environ['SHAPE_RESTORE_SHX'] = 'YES'

import glob
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import rasterio
from rasterio.transform import from_bounds
from rasterio.warp import reproject, Resampling
import geopandas as gpd
from scipy.stats import gamma, norm
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

CHIRPS_DIR = BASE_DIR / "input" / "02_precipitacao"

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
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ANOS = list(range(2013, 2026))  # 13 anos
CRS_PROJETADO = "EPSG:31982"    # SIRGAS 2000 / UTM 22S
RESOLUCAO_M = 100.0             # Resolução de interpolação local do CHIRPS


# ==========================================
# CÁLCULO DO SPI VIA DISTRIBUIÇÃO GAMMA
# ==========================================
def calcular_spi_gamma(serie_precip: np.ndarray) -> np.ndarray:
    """
    Calcula o SPI ajustando uma distribuição Gamma sobre a série temporal de precipitação:
      1. Trata zeros e NaNs.
      2. Ajusta parâmetros (shape, loc=0, scale).
      3. Converte para CDF Gamma e depois para Z-score Normal (norm.ppf).
    """
    valid_mask = np.isfinite(serie_precip) & (serie_precip > 0)
    spi_result = np.zeros_like(serie_precip, dtype=np.float32)
    
    if np.sum(valid_mask) < 3:
        return np.full_like(serie_precip, np.nan, dtype=np.float32)
        
    valores_validos = serie_precip[valid_mask]
    
    try:
        shape, loc, scale = gamma.fit(valores_validos, floc=0)
        prob_gamma = gamma.cdf(valores_validos, shape, loc=loc, scale=scale)
        prob_gamma = np.clip(prob_gamma, 1e-6, 1.0 - 1e-6)
        spi_valid = norm.ppf(prob_gamma)
        
        q0 = np.sum(serie_precip == 0) / len(serie_precip)
        if q0 > 0:
            prob_total = q0 + (1.0 - q0) * prob_gamma
            prob_total = np.clip(prob_total, 1e-6, 1.0 - 1e-6)
            spi_valid = norm.ppf(prob_total)
            
        spi_result[valid_mask] = spi_valid
        spi_result[serie_precip == 0] = -2.5  # Seca extrema quando chuva for zero
    except Exception:
        mean_val = np.nanmean(serie_precip)
        std_val = np.nanstd(serie_precip)
        if std_val > 0:
            spi_result = (serie_precip - mean_val) / std_val
        else:
            spi_result = np.zeros_like(serie_precip)
            
    return spi_result


def discretizar_spi_rabiei(spi_vals: np.ndarray | pd.Series) -> np.ndarray | pd.Series:
    """
    Discretiza SPI em 4 classes de risco de seca/incêndio (Rabiei et al., 2022; McKee et al.):
      - Classe 4 (Seca Severa / Risco Alto):     SPI <= -1.50
      - Classe 3 (Seca Moderada / Risco Médio):  -1.50 < SPI <= -0.50
      - Classe 2 (Normal / Próximo à Média):     -0.50 < SPI <= 0.50
      - Classe 1 (Úmido / Baixo Risco):          SPI > 0.50
    """
    v = np.asarray(spi_vals)
    classes = np.ones_like(v, dtype=np.uint8)  # Default: 1 (Úmido / Baixo Risco)
    classes[(v > -0.50) & (v <= 0.50)] = 2
    classes[(v > -1.50) & (v <= -0.50)] = 3
    classes[v <= -1.50] = 4                    # Seca severa = Classe 4
    return classes


# ==========================================
# PROCESSAMENTO DOS NETCDFS E EXPORTAÇÃO
# ==========================================
def processar_recorte_e_spi(limite_gdf: gpd.GeoDataFrame) -> dict[int, tuple[np.ndarray, dict]]:
    """
    Carrega os 13 NetCDFs do CHIRPS, recorta para a área de estudo,
    reprojeta para EPSG:31982 e calcula a série temporal de SPI.
    """
    print("\n[CHIRPS] Carregando e compilando série temporal 2013-2025...")
    
    limite_wgs84 = limite_gdf.to_crs("EPSG:4326")
    minx, miny, maxx, maxy = limite_wgs84.total_bounds
    pad = 0.15
    
    ds_anuais = {}
    for ano in ANOS:
        caminho_nc = CHIRPS_DIR / f"chirps-v2.0.{ano}.monthly.nc"
        if not caminho_nc.exists():
            raise FileNotFoundError(f"Arquivo NetCDF não encontrado: {caminho_nc}. Execute 00_download/04_download_chirps.py")
            
        ds = xr.open_dataset(caminho_nc)
        ds_clip = ds.sel(
            latitude=slice(miny - pad, maxy + pad),
            longitude=slice(minx - pad, maxx + pad)
        )
        ds_anuais[ano] = ds_clip

    # 1. Precipitação anual acumulada por ano
    precip_anual_por_ano = {}
    for ano in ANOS:
        ds_ano = ds_anuais[ano]['precip']
        precip_anual_por_ano[ano] = ds_ano.sum(dim='time', skipna=True)

    # 2. Calcular SPI Anual para cada pixel
    lats = ds_anuais[ANOS[0]]['latitude'].values
    lons = ds_anuais[ANOS[0]]['longitude'].values
    
    shape_3d = (len(ANOS), len(lats), len(lons))
    matriz_anual = np.zeros(shape_3d, dtype=np.float32)
    
    for i, ano in enumerate(ANOS):
        matriz_anual[i] = precip_anual_por_ano[ano].values

    matriz_spi_anual = np.zeros_like(matriz_anual)
    for r in range(len(lats)):
        for c in range(len(lons)):
            matriz_spi_anual[:, r, c] = calcular_spi_gamma(matriz_anual[:, r, c])

    # 3. Reprojetar e Recortar para CRS Projetado (EPSG:31982) a 100m
    limite_proj = limite_gdf.to_crs(CRS_PROJETADO)
    minx_p, miny_p, maxx_p, maxy_p = limite_proj.total_bounds
    
    width = int(np.ceil((maxx_p - minx_p) / RESOLUCAO_M))
    height = int(np.ceil((maxy_p - miny_p) / RESOLUCAO_M))
    dst_transform = from_bounds(minx_p, miny_p, maxx_p, maxy_p, width, height)
    
    meta_raster = {
        'driver': 'GTiff',
        'dtype': 'float32',
        'nodata': -9999.0,
        'width': width,
        'height': height,
        'count': 1,
        'crs': CRS_PROJETADO,
        'transform': dst_transform,
        'compress': 'lzw'
    }

    src_transform = from_bounds(lons.min(), lats.min(), lons.max(), lats.max(), len(lons), len(lats))
    rasters_por_ano = {}
    
    for i, ano in enumerate(ANOS):
        # Reprojetar SPI Anual
        arr_spi_src = np.flipud(matriz_spi_anual[i]) if lats[0] < lats[-1] else matriz_spi_anual[i]
        arr_spi_dst = np.full((height, width), -9999.0, dtype=np.float32)
        
        reproject(
            source=arr_spi_src,
            destination=arr_spi_dst,
            src_transform=src_transform,
            src_crs="EPSG:4326",
            dst_transform=dst_transform,
            dst_crs=CRS_PROJETADO,
            resampling=Resampling.bilinear
        )

        rasters_por_ano[ano] = (arr_spi_dst, meta_raster)

        # Salvar GeoTIFF contínuo de SPI
        out_spi = OUTPUT_DIR / f"SJP_spi_{ano}.tif"
        with rasterio.open(out_spi, 'w', **meta_raster) as dst:
            dst.write(arr_spi_dst, 1)

        # Salvar GeoTIFF de Classes de SPI
        meta_cls = meta_raster.copy()
        meta_cls.update({'dtype': 'uint8', 'nodata': 255})
        
        valid = (arr_spi_dst != -9999.0)
        cls_spi = np.full_like(arr_spi_dst, 255, dtype=np.uint8)
        cls_spi[valid] = discretizar_spi_rabiei(arr_spi_dst[valid])

        out_spi_cls = OUTPUT_DIR / f"SJP_spi_{ano}_classes.tif"
        with rasterio.open(out_spi_cls, 'w', **meta_cls) as dst:
            dst.write(cls_spi, 1)

    print(f"✅ Rasters anuais de SPI (2013-2025) gerados em: {OUTPUT_DIR}")
    return rasters_por_ano


# ==========================================
# GERAÇÃO DE PAINEL A4 RETRATO COM SUBPLOTS
# ==========================================
def gerar_painel_a4_spi(limite_gdf: gpd.GeoDataFrame):
    """
    Gera uma prancha gráfica em formato A4 retrato (8.27 x 11.69 pol / 210 x 297 mm)
    com subplots em grid (5 linhas x 3 colunas) para os 13 anos de SPI (2013-2025).
    """
    print(f"\n[PLOT] Gerando prancha A4 retrato com subplots para SPI (2013 a 2025)...")
    
    fig, axes = plt.subplots(5, 3, figsize=(8.27, 11.69), dpi=300)
    axes_flat = axes.flatten()
    
    cores = ['#2b83ba', '#abdda4', '#fdae61', '#d7191c']  # Azul (úmido) a Vermelho (seca severa)
    labels_legenda = [
        'Classe 1: Úmido / Baixo Risco (SPI > 0.50)',
        'Classe 2: Normal (-0.50 < SPI ≤ 0.50)',
        'Classe 3: Seca Moderada (-1.50 < SPI ≤ -0.50)',
        'Classe 4: Seca Severa / Alto Risco (SPI ≤ -1.50)'
    ]
    titulo_painel = 'Série Histórica de Classes de Seca Meteorológica (SPI 2013 - 2025)\nSão José dos Pinhais - PR (CHIRPS / Rabiei et al., 2022)'

    cmap = ListedColormap(cores)
    norm = BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5], cmap.N)
    
    for idx, ano in enumerate(ANOS):
        ax = axes_flat[idx]
        caminho_cls = OUTPUT_DIR / f"SJP_spi_{ano}_classes.tif"
        
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
    ax_info.text(0.5, 0.12, 'Projeção: SIRGAS 2000 / UTM 22S\nFonte: CHIRPS v2.0 (0.05°)',
                 ha='center', va='bottom', fontsize=5.5, color='#444444', multialignment='center')

    # Legenda customizada na parte inferior da prancha
    patches = [mpatches.Patch(color=cores[i], label=labels_legenda[i]) for i in range(4)]
    fig.legend(
        handles=patches,
        loc='lower center',
        ncol=2,
        fontsize=7,
        frameon=True,
        bbox_to_anchor=(0.5, 0.02)
    )

    fig.suptitle(titulo_painel, fontsize=10, fontweight='bold', y=0.98)
    plt.subplots_adjust(left=0.04, right=0.96, top=0.93, bottom=0.08, wspace=0.10, hspace=0.20)

    out_painel = OUTPUT_DIR / "painel_a4_classes_spi_2013_2025.png"
    plt.savefig(out_painel, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Prancha A4 de SPI salva com sucesso: {out_painel.name}")


# ==========================================
# EXTRAÇÃO ZONAL E ATUALIZAÇÃO DOS DATASETS
# ==========================================
def extrair_e_atualizar_datasets(limite_gdf: gpd.GeoDataFrame):
    """
    Extrai o índice de seca SPI ano a ano para cada amostra dos datasets CSV usando estatísticas zonais:
      - Valor contínuo representativo da célula de 1 km²: média (mean)
      - Classe discreta predominante na célula de 1 km²: moda (majority / mode)
    """
    print("\n[DATASET] Extraindo estatísticas zonais de SPI por célula de 1 km²...")
    
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
        polys = [box(pt.x - 500, pt.y - 500, pt.x + 500, pt.y + 500) for pt in gdf_pts.geometry]
        gdf_polys = gpd.GeoDataFrame(df_anual, geometry=polys, crs=CRS_PROJETADO).to_crs("EPSG:4326")
    
    # Inicializar colunas com NaN
    df_anual['spi_anual'] = np.nan
    df_anual['spi_classe'] = np.nan

    anos_presentes = sorted(df_anual['ano'].unique())
    print(f"[INFO] Anos presentes no dataset: {anos_presentes}")

    for ano in anos_presentes:
        ano = int(ano)
        mask_ano = (df_anual['ano'] == ano)
        indices_ano = df_anual[mask_ano].index
        
        caminho_spi = OUTPUT_DIR / f"SJP_spi_{ano}.tif"
        caminho_spi_cls = OUTPUT_DIR / f"SJP_spi_{ano}_classes.tif"
        
        if not caminho_spi.exists():
            print(f"[AVISO] Rasters para o ano {ano} não encontrados.")
            continue
            
        gdf_ano = gdf_polys.iloc[indices_ano]
        with rasterio.open(caminho_spi) as src_r:
            if gdf_ano.crs != src_r.crs:
                gdf_ano = gdf_ano.to_crs(src_r.crs)
        
        # Estatísticas zonais contínuas (mean) e categóricas (majority / moda da classe)
        stats_spi_mean = zonal_stats(gdf_ano, str(caminho_spi), stats="mean", nodata=-9999.0)
        stats_spi_cls = zonal_stats(gdf_ano, str(caminho_spi_cls), stats="majority", nodata=255)
        
        spi_vals = [np.round(s['mean'], 3) if s['mean'] is not None else np.nan for s in stats_spi_mean]
        spi_classes = [int(s['majority']) if s['majority'] is not None else 1 for s in stats_spi_cls]
        
        # Inserir no DataFrame
        df_anual.loc[mask_ano, 'spi_anual'] = spi_vals
        df_anual.loc[mask_ano, 'spi_classe'] = spi_classes
        
        print(f"  -> Ano {ano}: {len(indices_ano)} amostras extraídas (Média zonal e Moda de SPI).")

    # Converter coluna de classe para int
    df_anual['spi_classe'] = df_anual['spi_classe'].astype('Int64')

    # Salvar CSVs atualizados
    df_anual.to_csv(CSV_ANUAL, index=False)
    print(f"\n[SAÍDA] Dataset consolidado atualizado: {CSV_ANUAL.name} (Zonal Stats SPI 1km)")

    if CSV_TREINO.exists():
        df_tr = df_anual[df_anual['split'] == 'treino']
        df_tr.to_csv(CSV_TREINO, index=False)
        print(f"[SAÍDA] Dataset de Treino atualizado:     {CSV_TREINO.name} ({len(df_tr)} registros)")

    if CSV_VALIDACAO.exists():
        df_val = df_anual[df_anual['split'] == 'validacao']
        df_val.to_csv(CSV_VALIDACAO, index=False)
        print(f"[SAÍDA] Dataset de Validação atualizado:  {CSV_VALIDACAO.name} ({len(df_val)} registros)")

    # Gerar Prancha Gráfica A4 Retrato para SPI
    gerar_painel_a4_spi(limite_gdf)


def main():
    print("=" * 75)
    print("🌧️ PROCESSAMENTO E EXTRAÇÃO DO ÍNDICE DE SECA SPI (CHIRPS 2013-2025)")
    print("=" * 75)
    print(f"Diretório CHIRPS: {CHIRPS_DIR}")
    print(f"Diretório Saída:  {OUTPUT_DIR}")

    if not LIMITE_SHP.exists():
        raise FileNotFoundError(f"Arquivo de limite não encontrado em: {LIMITE_SHP}")
    limite_gdf = gpd.read_file(LIMITE_SHP)

    # 1. Processar recorte espacial e cálculo de SPI
    processar_recorte_e_spi(limite_gdf)

    # 2. Extração zonal e atualização dos CSVs
    extrair_e_atualizar_datasets(limite_gdf)

    print("\n" + "=" * 75)
    print("✨ PROCESSAMENTO DE SPI CONCLUÍDO COM SUCESSO!")
    print("=" * 75)


if __name__ == "__main__":
    main()
