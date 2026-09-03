"""
Script: 04_processar_indices_vegetacao.py
Etapa: 01_tratamento

Descrição:
    Processa e padroniza as séries temporais anuais de NDVI e NDMI (2013 a 2025):
    
    1. Discretização de Classes baseada na Literatura (Chen et al., 2021; Bilal, 2025; Rabiei et al., 2022):
       - NDVI (Biomassa / Cobertura Vegetal - Chen et al., Tabela 3):
           * Classe 1: (0.00, 0.80]  -> Cobertura esparsa / baixa biomassa
           * Classe 2: (0.80, 0.86]  -> Biomassa moderada
           * Classe 3: (0.86, 0.90]  -> Alta biomassa
           * Classe 4: (0.90, 1.00]  -> Máxima densidade de dossel
           
       - NDMI (Estresse Hídrico / Umidade do Dossel - Bilal, 2025; Rabiei et al., 2022):
         *Importante (Bilal, 2025)*: NDMI tem relação INVERSA com o perigo de fogo:
           * Classe 4 (Alto Risco / Seca Severa):   NDMI <= 0.00  (Dossel desidratado / inflamável)
           * Classe 3 (Risco Moderado-Alto):        0.00 < NDMI <= 0.15
           * Classe 2 (Risco Moderado-Baixo):       0.15 < NDMI <= 0.30
           * Classe 1 (Baixo Risco / Muito Úmido):  NDMI > 0.30   (Dossel túrgido / seguro)

    2. Extração Temporal Dinâmica Ano a Ano:
       - Para cada amostra da grade de 1 km (com seu respectivo `ano` de 2013 a 2025),
         extrai o valor e a classe de NDVI e NDMI correspondentes.
       - Preenche e atualiza os datasets CSV (anuais, treino e validação).

    3. Geração de Pranchas A4 Retrato com Subplots de Classes (2013 a 2025):
       - `painel_a4_classes_ndvi_2013_2025.png` (Grid 5x3 no formato A4 retrato)
       - `painel_a4_classes_ndmi_2013_2025.png` (Grid 5x3 no formato A4 retrato)
       - Rasters GeoTIFF classificados anuais.
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

NDVI_DIR = BASE_DIR / "output" / "04_ndvi"
NDMI_DIR = BASE_DIR / "output" / "04_ndmi"

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


# ==========================================
# FUNÇÕES DE DISCRETIZAÇÃO POR QUANTIS EMPÍRICOS LOCAIS
# ==========================================
def calcular_limiares_serie_temporal(diretorio: Path, prefixo: str) -> list[float]:
    """Calcula os quantis empíricos globais (25%, 50%, 75%) da série temporal de SJP (2013-2025)."""
    amostras_todos_anos = []
    for ano in ANOS:
        f = diretorio / f"{prefixo}_{ano}.tif"
        if f.exists():
            with rasterio.open(f) as src:
                d = src.read(1)
                nodata = src.nodata if src.nodata is not None else -9999.0
                valid = (d != nodata) & (~np.isnan(d))
                if np.sum(valid) > 0:
                    # Amostrar 10.000 pixels aleatórios por ano para compilar a distribuição
                    pts = np.random.choice(d[valid], size=min(10000, np.sum(valid)), replace=False)
                    amostras_todos_anos.extend(pts)
    
    if len(amostras_todos_anos) == 0:
        return [0.0, 0.0, 0.0]
        
    q25, q50, q75 = np.percentile(amostras_todos_anos, [25, 50, 75])
    return [float(q25), float(q50), float(q75)]


def discretizar_por_quartis_crescente(valores: np.ndarray | pd.Series, limiares: list[float]) -> np.ndarray | pd.Series:
    """Para variáveis onde MAIOR valor = MAIOR classe (ex: NDVI / Carga de Biomassa)."""
    v = np.asarray(valores)
    classes = np.ones_like(v, dtype=np.uint8)  # Classe 1: <= Q1
    classes[v > limiares[0]] = 2               # Classe 2: (Q1, Q2]
    classes[v > limiares[1]] = 3               # Classe 3: (Q2, Q3]
    classes[v > limiares[2]] = 4               # Classe 4: > Q3
    return classes


def discretizar_por_quartis_decrescente(valores: np.ndarray | pd.Series, limiares: list[float]) -> np.ndarray | pd.Series:
    """Para variáveis onde MENOR valor = MAIOR risco (ex: NDMI / Seca foliar)."""
    v = np.asarray(valores)
    classes = np.ones_like(v, dtype=np.uint8)  # Classe 1: > Q3 (Mais úmido)
    classes[(v > limiares[1]) & (v <= limiares[2])] = 2
    classes[(v > limiares[0]) & (v <= limiares[1])] = 3
    classes[v <= limiares[0]] = 4              # Classe 4: <= Q1 (Seca severa / Maior risco)
    return classes


def gerar_rasters_classificados(ano: int, lim_ndvi: list[float], lim_ndmi: list[float]):
    """Gera versões GeoTIFF classificadas para NDVI e NDMI daquele ano usando os quantis locais."""
    caminho_ndvi = NDVI_DIR / f"SJP_NDVI_{ano}.tif"
    caminho_ndmi = NDMI_DIR / f"SJP_NDMI_{ano}.tif"
    
    if caminho_ndvi.exists():
        with rasterio.open(caminho_ndvi) as src:
            data = src.read(1)
            meta = src.meta.copy()
            nodata = src.nodata if src.nodata is not None else -9999.0
            
            valid = (data != nodata) & (~np.isnan(data))
            classes = np.full_like(data, 255, dtype=np.uint8)
            classes[valid] = discretizar_por_quartis_crescente(data[valid], lim_ndvi)
            
            meta.update({'dtype': 'uint8', 'nodata': 255, 'compress': 'lzw'})
            out_f = OUTPUT_DIR / f"SJP_NDVI_{ano}_classes.tif"
            with rasterio.open(out_f, 'w', **meta) as dst:
                dst.write(classes, 1)

    if caminho_ndmi.exists():
        with rasterio.open(caminho_ndmi) as src:
            data = src.read(1)
            meta = src.meta.copy()
            nodata = src.nodata if src.nodata is not None else -9999.0
            
            valid = (data != nodata) & (~np.isnan(data))
            classes = np.full_like(data, 255, dtype=np.uint8)
            classes[valid] = discretizar_por_quartis_decrescente(data[valid], lim_ndmi)
            
            meta.update({'dtype': 'uint8', 'nodata': 255, 'compress': 'lzw'})
            out_f = OUTPUT_DIR / f"SJP_NDMI_{ano}_classes.tif"
            with rasterio.open(out_f, 'w', **meta) as dst:
                dst.write(classes, 1)


# ==========================================
# GERAÇÃO DE PAINEL A4 RETRATO COM SUBPLOTS
# ==========================================
def gerar_painel_a4_classes(tipo_indice: str, limite_gdf: gpd.GeoDataFrame, limiares: list[float]):
    """
    Gera uma prancha gráfica em formato A4 retrato (8.27 x 11.69 pol / 210 x 297 mm)
    com subplots em grid (5 linhas x 3 colunas) para os 13 anos (2013-2025) usando quantis locais.
    """
    print(f"\n[PLOT] Gerando prancha A4 retrato com subplots para {tipo_indice.upper()} (Quartis Locais 2013-2025)...")
    
    fig, axes = plt.subplots(5, 3, figsize=(8.27, 11.69), dpi=300)
    axes_flat = axes.flatten()
    
    if tipo_indice.lower() == 'ndvi':
        cores = ['#ffffcc', '#a1dab4', '#41b6c4', '#225ea8'] # Amarelo claro a Azul/Verde escuro
        labels_legenda = [
            f'Classe 1: Baixa biomassa (≤ {limiares[0]:.2f})',
            f'Classe 2: Média ({limiares[0]:.2f} - {limiares[1]:.2f})',
            f'Classe 3: Alta ({limiares[1]:.2f} - {limiares[2]:.2f})',
            f'Classe 4: Muito Alta (> {limiares[2]:.2f})'
        ]
        titulo_painel = 'Série Histórica Anual de Classes de NDVI (2013 - 2025)\nSão José dos Pinhais - PR (Quantis Empíricos - Chen et al., 2021)'
    else:
        cores = ['#2b83ba', '#abdda4', '#fdae61', '#d7191c'] # Azul (úmido) a Vermelho (seco/perigo)
        labels_legenda = [
            f'Classe 1: Muito Úmido / Baixo Risco (> {limiares[2]:.2f})',
            f'Classe 2: Moderado-Baixo ({limiares[1]:.2f} - {limiares[2]:.2f})',
            f'Classe 3: Moderado-Alto ({limiares[0]:.2f} - {limiares[1]:.2f})',
            f'Classe 4: Seca Severa / Alto Risco (≤ {limiares[0]:.2f})'
        ]
        titulo_painel = 'Série Histórica Anual de Classes de Risco NDMI (2013 - 2025)\nSão José dos Pinhais - PR (Quantis Empíricos - Bilal, 2025; Rabiei et al., 2022)'
        
    cmap = ListedColormap(cores)
    norm = BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5], cmap.N)
    
    for idx, ano in enumerate(ANOS):
        ax = axes_flat[idx]
        caminho_cls = OUTPUT_DIR / f"SJP_{tipo_indice.upper()}_{ano}_classes.tif"
        
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

    axes_flat[14].axis('off')
    
    ax_info = axes_flat[13]
    ax_info.axis('off')
    ax_info.set_xlim(0, 1)
    ax_info.set_ylim(0, 1)
    
    ax_info.annotate('N', xy=(0.5, 0.75), xytext=(0.5, 0.45),
                     arrowprops=dict(facecolor='black', edgecolor='black', width=2, headwidth=7),
                     ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax_info.plot([0.3, 0.7], [0.25, 0.25], color='black', linewidth=2.5)
    ax_info.text(0.5, 0.28, '10 km', ha='center', va='bottom', fontsize=7, fontweight='bold')
    ax_info.text(0.5, 0.12, 'Projeção SIRGAS 2000 / UTM 22S\nFonte: Landsat 30m / Quantis SJP', ha='center', va='bottom', fontsize=5.5, color='#444444', multialignment='center')

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

    out_painel = OUTPUT_DIR / f"painel_a4_classes_{tipo_indice.lower()}_2013_2025.png"
    plt.savefig(out_painel, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Prancha A4 salva com sucesso: {out_painel.name}")


def extrair_e_atualizar_datasets(limite_gdf: gpd.GeoDataFrame):
    """
    Extrai NDVI e NDMI ano a ano para cada amostra dos datasets CSV usando estatísticas zonais:
      - Valor contínuo representativo da célula de 1 km²: média (mean)
      - Classe discreta predominante na célula de 1 km²: moda (majority / mode)
    """
    print("\n[DATASET] Calculando quantis empíricos locais para NDVI e NDMI...")
    lim_ndvi = calcular_limiares_serie_temporal(NDVI_DIR, "SJP_NDVI")
    lim_ndmi = calcular_limiares_serie_temporal(NDMI_DIR, "SJP_NDMI")
    print(f"[INFO] Quantis locais NDVI (2013-2025): Q1={lim_ndvi[0]:.3f}, Q2={lim_ndvi[1]:.3f}, Q3={lim_ndvi[2]:.3f}")
    print(f"[INFO] Quantis locais NDMI (2013-2025): Q1={lim_ndmi[0]:.3f}, Q2={lim_ndmi[1]:.3f}, Q3={lim_ndmi[2]:.3f}")

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
    
    df_anual['ndvi_valor'] = np.nan
    df_anual['ndvi_classe'] = np.nan
    df_anual['ndmi_valor'] = np.nan
    df_anual['ndmi_classe'] = np.nan

    anos_presentes = sorted(df_anual['ano'].unique())
    print(f"[INFO] Anos presentes no dataset: {anos_presentes}")

    for ano in anos_presentes:
        ano = int(ano)
        mask_ano = (df_anual['ano'] == ano)
        indices_ano = df_anual[mask_ano].index
        
        caminho_ndvi = NDVI_DIR / f"SJP_NDVI_{ano}.tif"
        caminho_ndmi = NDMI_DIR / f"SJP_NDMI_{ano}.tif"
        
        if not caminho_ndvi.exists() or not caminho_ndmi.exists():
            print(f"[AVISO] Rasters para o ano {ano} não encontrados.")
            continue
            
        gerar_rasters_classificados(ano, lim_ndvi, lim_ndmi)
        
        out_ndvi_cls = OUTPUT_DIR / f"SJP_NDVI_{ano}_classes.tif"
        out_ndmi_cls = OUTPUT_DIR / f"SJP_NDMI_{ano}_classes.tif"
        
        gdf_ano = gdf_polys.iloc[indices_ano]
        with rasterio.open(caminho_ndvi) as src_r:
            if gdf_ano.crs != src_r.crs:
                gdf_ano = gdf_ano.to_crs(src_r.crs)
        
        stats_ndvi_mean = zonal_stats(gdf_ano, str(caminho_ndvi), stats="mean", nodata=-9999.0)
        stats_ndmi_mean = zonal_stats(gdf_ano, str(caminho_ndmi), stats="mean", nodata=-9999.0)
        
        stats_ndvi_cls = zonal_stats(gdf_ano, str(out_ndvi_cls), stats="majority", nodata=255)
        stats_ndmi_cls = zonal_stats(gdf_ano, str(out_ndmi_cls), stats="majority", nodata=255)
        
        ndvi_vals = [np.round(s['mean'], 4) if s['mean'] is not None else np.nan for s in stats_ndvi_mean]
        ndmi_vals = [np.round(s['mean'], 4) if s['mean'] is not None else np.nan for s in stats_ndmi_mean]
        
        ndvi_classes = [int(s['majority']) if s['majority'] is not None else 1 for s in stats_ndvi_cls]
        ndmi_classes = [int(s['majority']) if s['majority'] is not None else 1 for s in stats_ndmi_cls]
        
        df_anual.loc[mask_ano, 'ndvi_valor'] = ndvi_vals
        df_anual.loc[mask_ano, 'ndvi_classe'] = ndvi_classes
        df_anual.loc[mask_ano, 'ndmi_valor'] = ndmi_vals
        df_anual.loc[mask_ano, 'ndmi_classe'] = ndmi_classes
        
        print(f"  -> Ano {ano}: {len(indices_ano)} amostras extraídas (Quartis calibrados).")

    df_anual['ndvi_classe'] = df_anual['ndvi_classe'].astype('Int64')
    df_anual['ndmi_classe'] = df_anual['ndmi_classe'].astype('Int64')

    df_anual.to_csv(CSV_ANUAL, index=False)
    print(f"\n[SAÍDA] Dataset consolidado atualizado: {CSV_ANUAL.name} (Zonal Stats 1km)")

    if CSV_TREINO.exists():
        df_tr = df_anual[df_anual['split'] == 'treino']
        df_tr.to_csv(CSV_TREINO, index=False)
        print(f"[SAÍDA] Dataset de Treino atualizado:     {CSV_TREINO.name} ({len(df_tr)} registros)")

    if CSV_VALIDACAO.exists():
        df_val = df_anual[df_anual['split'] == 'validacao']
        df_val.to_csv(CSV_VALIDACAO, index=False)
        print(f"[SAÍDA] Dataset de Validação atualizado:  {CSV_VALIDACAO.name} ({len(df_val)} registros)")

    gerar_painel_a4_classes('ndvi', limite_gdf, lim_ndvi)
    gerar_painel_a4_classes('ndmi', limite_gdf, lim_ndmi)


def main():
    print("=" * 75)
    print("🌿 PROCESSAMENTO E EXTRAÇÃO DE ÍNDICES ESPECTRAIS (NDVI / NDMI)")
    print("=" * 75)
    print(f"Diretório NDVI:  {NDVI_DIR}")
    print(f"Diretório NDMI:  {NDMI_DIR}")
    print(f"Diretório Saída: {OUTPUT_DIR}")

    if not LIMITE_SHP.exists():
        raise FileNotFoundError(f"Arquivo de limite não encontrado em: {LIMITE_SHP}")
    limite_gdf = gpd.read_file(LIMITE_SHP)

    extrair_e_atualizar_datasets(limite_gdf)

    print("\n" + "=" * 75)
    print("✨ PROCESSAMENTO DE NDVI E NDMI CONCLUÍDO COM SUCESSO!")
    print("=" * 75)


if __name__ == "__main__":
    main()
