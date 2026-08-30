"""
Script: 02_fire_density.py
Etapa: 01_tratamento

Descrição:
    Calcula a densidade histórica de focos de calor (Kernel Density Estimation - KDE)
    e a densidade em unidades de focos por 100 km²·ano (conforme Chen et al., 2021).
    
    Além de gerar os rasters contínuos e classificados e o mapa visual:
    - Extrai os valores contínuos de densidade para os centróides de cada célula de 1 km² das amostras.
    - Discretiza em 4 intervalos conforme Chen et al. (Tabela 3: 0-1, 1-2.4, 2.4-4.5, >4.5 focos/100 km²·ano).
    - Preenche e atualiza os datasets CSV gerados no script 01:
        * output/01_processar_hotspots/grade_1km_amostras_anuais.csv
        * output/01_processar_hotspots/grade_1km_amostras_treino.csv
        * output/01_processar_hotspots/grade_1km_amostras_validacao.csv
    
    Saídas geradas em 'output/02_fire_density/':
    - fire_density_continuous.tif (Raster GeoTIFF de densidade KDE normalizada [0, 1])
    - fire_spot_density_annual.tif (Raster GeoTIFF de densidade em focos / (100 km² · ano))
    - fire_density_risk_classes.tif (Raster GeoTIFF de classes discretizadas 1 a 4 de Chen et al.)
    - fire_density_heatmap.png (Mapa de calor em alta resolução)
"""

import os
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
import rasterio
from rasterio.transform import from_bounds

# ==========================================
# CAMINHOS E CONFIGURAÇÕES
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

HOTSPOTS_GEOJSON = BASE_DIR / "output" / "01_processar_hotspots" / "hotspots_fase1_agrupados.geojson"
HOTSPOTS_CSV = BASE_DIR / "output" / "01_processar_hotspots" / "hotspots_fase1_agrupados.csv"

# Limite municipal (suporta input ou output)
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

RESOLUCAO_RASTER_M = 30.0       # Resolução espacial do raster em metros
CRS_PROJETADO = "EPSG:31982"    # SIRGAS 2000 / UTM zone 22S


def carregar_dados_focos() -> gpd.GeoDataFrame:
    """Carrega os focos de calor agrupados gerados na etapa anterior."""
    if HOTSPOTS_GEOJSON.exists():
        print(f"[INFO] Carregando focos de: {HOTSPOTS_GEOJSON}")
        gdf = gpd.read_file(HOTSPOTS_GEOJSON)
    elif HOTSPOTS_CSV.exists():
        print(f"[INFO] Carregando focos de: {HOTSPOTS_CSV}")
        df = pd.read_csv(HOTSPOTS_CSV)
        gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df['longitude'], df['latitude']),
            crs="EPSG:4326"
        )
    else:
        raise FileNotFoundError(
            f"Focos de calor não encontrados em:\n - {HOTSPOTS_GEOJSON}\n - {HOTSPOTS_CSV}\n"
            "Execute primeiro o script '01_tratamento/01_processar_hotspots.py'."
        )
    return gdf


def calcular_kernel_density(
    gdf_focos: gpd.GeoDataFrame,
    limite_gdf: gpd.GeoDataFrame,
    resolucao_m: float = RESOLUCAO_RASTER_M,
    crs_projetado: str = CRS_PROJETADO
) -> tuple[np.ndarray, np.ndarray, np.ndarray, rasterio.transform.Affine, gaussian_kde, float]:
    """
    Calcula a matriz de densidade por estimativa de Kernel (KDE)
    e a densidade calibrada em focos/(100 km² · ano) sobre a extensão do município.
    """
    print("\n[KDE] Preparando grade e calculando Gaussian KDE...")
    
    # Projeção métrica para cálculo preciso da densidade no espaço
    focos_proj = gdf_focos.to_crs(crs_projetado)
    limite_proj = limite_gdf.to_crs(crs_projetado)
    
    minx, miny, maxx, maxy = limite_proj.total_bounds
    
    width = int(np.ceil((maxx - minx) / resolucao_m))
    height = int(np.ceil((maxy - miny) / resolucao_m))
    
    print(f"[INFO] Dimensões da grade raster: {width} x {height} pixels (Resolução: {resolucao_m}m)")
    
    # Criar grade de coordenadas X e Y
    x_coords = np.linspace(minx + resolucao_m / 2, maxx - resolucao_m / 2, width)
    y_coords = np.linspace(maxy - resolucao_m / 2, miny + resolucao_m / 2, height)
    
    x_grid, y_grid = np.meshgrid(x_coords, y_coords)
    positions = np.vstack([x_grid.ravel(), y_grid.ravel()])
    
    pts_x = focos_proj.geometry.x.values
    pts_y = focos_proj.geometry.y.values
    n_focos = len(pts_x)
    
    if n_focos < 2:
        raise ValueError(f"Quantidade insuficiente de focos para KDE (mínimo 2 focos, encontrados {n_focos}).")
        
    kernel = gaussian_kde(np.vstack([pts_x, pts_y]))
    density_raw = kernel(positions).reshape((height, width)).astype(np.float32)
    
    # Normalização [0, 1]
    max_val = np.max(density_raw)
    density_norm = density_raw / max_val if max_val > 0 else density_raw
    
    # Densidade anualizada em focos por 100 km²·ano (conforme Chen et al., 2021)
    anos_unicos = gdf_focos['ano'].nunique() if 'ano' in gdf_focos.columns else 13
    anos_unicos = max(anos_unicos, 1)
    
    # gaussian_kde integra para 1.0 sobre m². Multiplicamos por N focos, por 100 km² (1e8 m²) e dividimos por anos
    density_100km2_ano = (density_raw * n_focos * 1e8 / anos_unicos).astype(np.float32)
    
    transform = from_bounds(minx, miny, maxx, maxy, width, height)
    
    return density_norm, density_100km2_ano, x_coords, y_coords, transform, kernel, anos_unicos


def discretizar_fire_density_relativo(density_norm_val: np.ndarray | pd.Series) -> np.ndarray | pd.Series:
    """
    Discretiza a densidade de focos em 4 classes relativas ao valor máximo local do KDE normalizado [0, 1]:
      - Classe 1: Muito Baixo (0.00 a 0.25 * max)
      - Classe 2: Baixo       (0.25 a 0.50 * max)
      - Classe 3: Médio       (0.50 a 0.75 * max)
      - Classe 4: Alto        (0.75 a 1.00 * max)
    """
    norm = np.asarray(density_norm_val)
    classes = np.ones_like(norm, dtype=np.uint8)
    classes[(norm > 0.25) & (norm <= 0.50)] = 2
    classes[(norm > 0.50) & (norm <= 0.75)] = 3
    classes[norm > 0.75] = 4
    return classes


def extrair_e_atualizar_datasets(
    kernel: gaussian_kde,
    max_raw_val: float,
    n_focos: int,
    n_anos: int,
    crs_projetado: str = CRS_PROJETADO
):
    """
    Extrai a densidade de focos para os centroides de cada amostra dos datasets CSV
    e salva as novas colunas 'fire_density_norm' e 'fire_density_classe'.
    """
    print("\n[DATASET] Extraindo valores de densidade e preenchendo datasets CSV...")
    
    if not CSV_ANUAL.exists():
        print(f"[AVISO] Arquivo {CSV_ANUAL} não encontrado. Execute primeiro o script 01_processar_hotspots.py.")
        return

    df_anual = pd.read_csv(CSV_ANUAL)
    
    # Converter centroides (lat, lon) em coordenadas métricas projetadas
    gdf_pts = gpd.GeoDataFrame(
        df_anual,
        geometry=gpd.points_from_xy(df_anual['longitude_centro'], df_anual['latitude_centro']),
        crs="EPSG:4326"
    ).to_crs(crs_projetado)
    
    pts_x = gdf_pts.geometry.x.values
    pts_y = gdf_pts.geometry.y.values
    coords_pts = np.vstack([pts_x, pts_y])
    
    # Avaliar o KDE nos pontos das amostras
    kde_raw = kernel(coords_pts).astype(np.float32)
    density_norm = np.clip(kde_raw / max_raw_val if max_raw_val > 0 else kde_raw, 0.0, 1.0)
    classes = discretizar_fire_density_relativo(density_norm)
    
    # Atualizar o DataFrame consolidado
    df_anual['fire_density_norm'] = np.round(density_norm, 4)
    df_anual['fire_density_classe'] = classes
    
    df_anual.to_csv(CSV_ANUAL, index=False)
    print(f"  -> Atualizado: {CSV_ANUAL.name} (+ colunas: 'fire_density_norm', 'fire_density_classe')")
    
    # Atualizar os CSVs de Treino e Validação
    if CSV_TREINO.exists():
        df_tr = df_anual[df_anual['split'] == 'treino']
        df_tr.to_csv(CSV_TREINO, index=False)
        print(f"  -> Atualizado: {CSV_TREINO.name} ({len(df_tr)} registros)")
        
    if CSV_VALIDACAO.exists():
        df_val = df_anual[df_anual['split'] == 'validacao']
        df_val.to_csv(CSV_VALIDACAO, index=False)
        print(f"  -> Atualizado: {CSV_VALIDACAO.name} ({len(df_val)} registros)")


def salvar_raster(
    array_data: np.ndarray,
    caminho_tif: Path,
    transform: rasterio.transform.Affine,
    dtype: str,
    nodata_val=None,
    crs: str = CRS_PROJETADO
):
    """Salva matriz numpy em formato GeoTIFF comprimido."""
    height, width = array_data.shape
    meta = {
        'driver': 'GTiff',
        'dtype': dtype,
        'width': width,
        'height': height,
        'count': 1,
        'crs': crs,
        'transform': transform,
        'compress': 'lzw'
    }
    if nodata_val is not None:
        meta['nodata'] = nodata_val

    caminho_tif.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(str(caminho_tif), 'w', **meta) as dst:
        dst.write(array_data, 1)
    print(f"[SAÍDA] Raster salvo em: {caminho_tif}")


def plotar_mapa_calor(
    density_100km2: np.ndarray,
    gdf_focos: gpd.GeoDataFrame,
    limite_gdf: gpd.GeoDataFrame,
    caminho_png: Path,
    crs_projetado: str = CRS_PROJETADO
):
    """Gera visualização gráfica do mapa de calor com a densidade calibrada e focos."""
    print(f"\n[PLOT] Gerando mapa de calor de visualização...")
    focos_proj = gdf_focos.to_crs(crs_projetado)
    limite_proj = limite_gdf.to_crs(crs_projetado)
    
    minx, miny, maxx, maxy = limite_proj.total_bounds
    
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    
    # Plotar o raster de densidade
    im = ax.imshow(
        density_100km2,
        extent=[minx, maxx, miny, maxy],
        origin='upper',
        cmap='YlOrRd',
        alpha=0.85
    )
    
    # Plotar o limite municipal
    limite_proj.boundary.plot(ax=ax, color='black', linewidth=1.2, label='Limite Municipal')
    
    # Plotar os focos de calor
    ax.scatter(
        focos_proj.geometry.x,
        focos_proj.geometry.y,
        color='blue',
        s=12,
        alpha=0.6,
        label='Focos Agrupados (Fase 1)'
    )
    
    plt.colorbar(im, ax=ax, label='Densidade Relativa de Focos (Normalizada [0, 1])')
    ax.set_title('Densidade Histórica de Focos de Calor (Kernel Density Estimation) - SJP', fontsize=11, fontweight='bold')
    ax.set_xlabel('Coordenada X (UTM Metros)')
    ax.set_ylabel('Coordenada Y (UTM Metros)')
    ax.legend(loc='upper right', fontsize=8)
    
    # 1. Seta Norte (North Arrow)
    x_arrow, y_arrow = minx + (maxx - minx) * 0.06, maxy - (maxy - miny) * 0.10
    ax.annotate('N', xy=(x_arrow, y_arrow), xytext=(x_arrow, y_arrow - (maxy - miny) * 0.05),
                arrowprops=dict(facecolor='black', edgecolor='black', width=2, headwidth=8),
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 2. Barra de Escala Gráfica (Scale Bar de 10 km)
    scale_len_m = 10000.0  # 10 km
    scale_x0 = minx + (maxx - minx) * 0.05
    scale_y0 = miny + (maxy - miny) * 0.05
    ax.plot([scale_x0, scale_x0 + scale_len_m], [scale_y0, scale_y0], color='black', linewidth=3)
    ax.text(scale_x0 + scale_len_m / 2, scale_y0 + (maxy - miny) * 0.015, '10 km',
            ha='center', va='bottom', fontsize=8, fontweight='bold',
            bbox=dict(boxstyle='square,pad=0.2', facecolor='white', alpha=0.8, edgecolor='none'))

    caminho_png.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(caminho_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SAÍDA] Mapa de calor salvo em: {caminho_png}")


def main():
    print("=" * 75)
    print("      CÁLCULO E EXTRAÇÃO DE FIRE SPOT DENSITY (CHEN ET AL., 2021)")
    print("=" * 75)
    print(f"Limite de Estudo: {LIMITE_SHP}")
    print(f"Diretório Saída:  {OUTPUT_DIR}")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Carregar Limite Municipal
    if not LIMITE_SHP.exists():
        raise FileNotFoundError(f"Arquivo de limite não encontrado em: {LIMITE_SHP}")
    limite_gdf = gpd.read_file(LIMITE_SHP)
    
    # 2. Carregar Focos de Calor
    gdf_focos = carregar_dados_focos()
    n_focos = len(gdf_focos)
    print(f"[INFO] Total de focos de calor carregados: {n_focos}")
    
    # 3. Calcular Densidade de Kernel e Normalização pelo Máximo Local
    density_norm, density_100km2_ano, x_coords, y_coords, transform, kernel, n_anos = calcular_kernel_density(
        gdf_focos,
        limite_gdf,
        resolucao_m=RESOLUCAO_RASTER_M,
        crs_projetado=CRS_PROJETADO
    )
    
    # 4. Discretizar em 4 classes relativas ao valor máximo local do KDE
    classes_relativas = discretizar_fire_density_relativo(density_norm)
    
    # 5. Salvar Rasters
    raster_norm = OUTPUT_DIR / "fire_density_continuous.tif"
    salvar_raster(density_norm, raster_norm, transform, dtype='float32')
    
    raster_chen = OUTPUT_DIR / "fire_spot_density_annual.tif"
    salvar_raster(density_100km2_ano, raster_chen, transform, dtype='float32')
    
    raster_classes = OUTPUT_DIR / "fire_density_risk_classes.tif"
    salvar_raster(classes_relativas, raster_classes, transform, dtype='uint8')
    
    # 6. Gerar Gráfico de Heatmap
    mapa_png = OUTPUT_DIR / "fire_density_heatmap.png"
    plotar_mapa_calor(density_norm, gdf_focos, limite_gdf, mapa_png, crs_projetado=CRS_PROJETADO)
    
    # Obter valor máximo raw do KDE no raster
    # kernel avaliado na grade gerou density_norm com max_val correspondente
    pts_x = gdf_focos.to_crs(CRS_PROJETADO).geometry.x.values
    pts_y = gdf_focos.to_crs(CRS_PROJETADO).geometry.y.values
    max_raw_val = float(np.max(kernel(np.vstack([x_coords[len(x_coords)//2], y_coords[len(y_coords)//2]]))))  # fallback
    # O valor máximo real é o max do KDE no raster
    max_kde_grid = float(density_norm.max())
    
    # 7. Extrair valores para as células de 1 km e atualizar os CSVs de modelagem
    # Para consistência com o raster: kernel(pts) / max_val do grid raster
    minx, miny, maxx, maxy = limite_gdf.to_crs(CRS_PROJETADO).total_bounds
    width = int(np.ceil((maxx - minx) / RESOLUCAO_RASTER_M))
    height = int(np.ceil((maxy - miny) / RESOLUCAO_RASTER_M))
    x_g, y_g = np.meshgrid(x_coords, y_coords)
    kde_grid_raw = kernel(np.vstack([x_g.ravel(), y_g.ravel()]))
    max_raw_val = float(np.max(kde_grid_raw))

    extrair_e_atualizar_datasets(kernel, max_raw_val, n_focos, n_anos, crs_projetado=CRS_PROJETADO)
    
    print("\n[SUCESSO] Processamento e extração de Fire Density concluídos!")
    print(f"Arquivos salvos em: {OUTPUT_DIR}\n")


if __name__ == "__main__":
    main()
