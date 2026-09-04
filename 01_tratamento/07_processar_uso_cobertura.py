"""
Script: 07_processar_uso_cobertura.py
Etapa: 01_tratamento

Descrição:
    Processa a série temporal de Uso e Cobertura da Terra (LULC) do MapBiomas Coleção 10.1 (2013 a 2025)
    para São José dos Pinhais - PR:
    
    1. Mantém os códigos originais/nativos de classe do MapBiomas (ex: 3=Formação Florestal, 9=Silvicultura, 15=Pastagem, 21=Mosaico de Usos, 24=Área Urbanizada, 33=Corpo d'Água, etc.).
    
    2. Estatísticas Zonais por Célula da Grade (1 km x 1 km):
       - Extrai a classe predominante do MapBiomas (moda / majority) em cada célula de 1 km² para cada ano.
       - Atualiza os 3 datasets CSV:
           * `output/01_processar_hotspots/grade_1km_amostras_anuais.csv` -> coluna `lulc_classe`
           * `output/01_processar_hotspots/grade_1km_amostras_treino.csv`
           * `output/01_processar_hotspots/grade_1km_amostras_validacao.csv`
           
    3. Geração de Prancha A4 Retrato com Subplots (2013 a 2025):
       - `painel_a4_mapbiomas_lulc_2013_2025.png` (Grid 5x3 com a legenda oficial de cores do MapBiomas, Seta Norte e Barra de Escala única).
"""

import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd
import rasterio
from rasterio.transform import from_bounds
from rasterio.warp import reproject, Resampling
from rasterio.features import rasterize
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

# ==========================================
# LEGENDA OFICIAL DE CORES MAPBIOMAS
# ==========================================
MAPBIOMAS_PALETTE = {
    3:  {'nome': 'Formação Florestal',       'cor': '#006400'},
    4:  {'nome': 'Formação Savânica',        'cor': '#389404'},
    9:  {'nome': 'Silvicultura',            'cor': '#7a5900'},
    11: {'nome': 'Área Úmida',               'cor': '#45c2a5'},
    12: {'nome': 'Formação Campestre',       'cor': '#b8af4f'},
    15: {'nome': 'Pastagem',                 'cor': '#ffd966'},
    19: {'nome': 'Lavoura Temporária',       'cor': '#c27ba0'},
    21: {'nome': 'Mosaico de Usos',          'cor': '#fff1d2'},
    24: {'nome': 'Área Urbanizada',          'cor': '#d4271e'},
    25: {'nome': 'Outras Áreas Não Veg.',    'cor': '#db4d4f'},
    30: {'nome': 'Mineração',                'cor': '#9c0053'},
    31: {'nome': 'Aquicultura',              'cor': '#091077'},
    33: {'nome': 'Corpo d\'Água',            'cor': '#2532e8'},
    39: {'nome': 'Soja',                     'cor': '#c59ff4'},
    41: {'nome': 'Outras Lavouras Temp.',    'cor': '#e787f8'}
}


# ==========================================
# 1. PROCESSAMENTO E RECORTE DOS RASTERS LULC
# ==========================================
def processar_recorte_mapbiomas(limite_gdf: gpd.GeoDataFrame) -> dict[int, Path]:
    """
    Recorta e reprojeta os rasters do MapBiomas para a extensão e projeção de SJP (EPSG:31982 a 30m).
    """
    print("\n[LULC] Reprojetando e recortando coleções MapBiomas (2013 a 2025)...")
    
    limite_proj = limite_gdf.to_crs(CRS_PROJETADO)
    minx, miny, maxx, maxy = limite_proj.total_bounds
    
    width = int(np.ceil((maxx - minx) / RESOLUCAO_M))
    height = int(np.ceil((maxy - miny) / RESOLUCAO_M))
    transform = from_bounds(minx, miny, maxx, maxy, width, height)
    
    meta_dst = {
        'driver': 'GTiff',
        'dtype': 'uint8',
        'nodata': 0,
        'width': width,
        'height': height,
        'count': 1,
        'crs': CRS_PROJETADO,
        'transform': transform,
        'compress': 'lzw'
    }

    mask_limite = rasterize([(geom, 1) for geom in limite_proj.geometry], out_shape=(height, width), transform=transform, fill=0, dtype=np.uint8)

    arquivos_ano = {}

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

        # Mascarar fora do limite municipal com 0 (NoData)
        dst_data[mask_limite == 0] = 0

        out_tif = OUTPUT_DIR / f"SJP_MapBiomas_{ano}.tif"
        with rasterio.open(out_tif, 'w', **meta_dst) as dst:
            dst.write(dst_data, 1)

        arquivos_ano[ano] = out_tif

    print(f"✅ Rasters anuais do MapBiomas exportados em: {OUTPUT_DIR}")
    return arquivos_ano


# ==========================================
# 2. GERAÇÃO DE PAINEL A4 RETRATO COM SUBPLOTS
# ==========================================
def gerar_painel_a4_mapbiomas(arquivos_ano: dict[int, Path], limite_gdf: gpd.GeoDataFrame):
    """
    Gera uma prancha gráfica em formato A4 retrato (8.27 x 11.69 pol / 210 x 297 mm)
    com subplots em grid (5 linhas x 3 colunas) para os 13 anos (2013-2025).
    """
    print("\n[PLOT] Gerando prancha A4 retrato com subplots para Uso do Solo MapBiomas...")
    
    # Identificar todas as classes presentes nos rasters processados
    classes_presentes = set()
    for ano, caminho_tif in arquivos_ano.items():
        with rasterio.open(caminho_tif) as src:
            arr = src.read(1)
            classes_presentes.update(np.unique(arr[arr > 0]))

    classes_presentes = sorted(list(classes_presentes))
    print(f"[INFO] Classes nativas MapBiomas encontradas na área de estudo: {classes_presentes}")

    # Montar colormap e norm
    cores = []
    labels = []
    for cod in classes_presentes:
        if cod in MAPBIOMAS_PALETTE:
            cores.append(MAPBIOMAS_PALETTE[cod]['cor'])
            labels.append(f"{cod} - {MAPBIOMAS_PALETTE[cod]['nome']}")
        else:
            cores.append('#808080')
            labels.append(f"Classe {cod}")

    # Mapear valor da classe para índice 0..(N-1)
    class_to_idx = {cod: idx for idx, cod in enumerate(classes_presentes)}
    cmap = ListedColormap(cores)
    norm = BoundaryNorm(np.arange(-0.5, len(classes_presentes) + 0.5, 1), cmap.N)

    fig, axes = plt.subplots(5, 3, figsize=(8.27, 11.69), dpi=300)
    axes_flat = axes.flatten()
    
    for idx, ano in enumerate(ANOS):
        ax = axes_flat[idx]
        if ano in arquivos_ano:
            caminho_tif = arquivos_ano[ano]
            with rasterio.open(caminho_tif) as src:
                data = src.read(1)
                bounds = src.bounds
                extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
                
                # Mapear para índices de cor
                mapped_data = np.full_like(data, -1, dtype=np.int16)
                for cod, c_idx in class_to_idx.items():
                    mapped_data[data == cod] = c_idx
                
                data_masked = np.ma.masked_equal(mapped_data, -1)
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

    # Legenda customizada na parte inferior da prancha
    patches = [mpatches.Patch(color=cores[i], label=labels[i]) for i in range(len(classes_presentes))]
    fig.legend(
        handles=patches,
        loc='lower center',
        ncol=3,
        fontsize=6.5,
        frameon=True,
        bbox_to_anchor=(0.5, 0.015)
    )

    fig.suptitle('Série Histórica de Uso e Cobertura da Terra (MapBiomas 2013 - 2025)\nSão José dos Pinhais - PR',
                 fontsize=10, fontweight='bold', y=0.98)
    plt.subplots_adjust(left=0.04, right=0.96, top=0.93, bottom=0.09, wspace=0.10, hspace=0.20)

    out_png = OUTPUT_DIR / "painel_a4_mapbiomas_lulc_2013_2025.png"
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Prancha A4 MapBiomas salva: {out_png.name}")


# ==========================================
# 3. EXTRAÇÃO ZONAL E ATUALIZAÇÃO DOS DATASETS
# ==========================================
def extrair_e_atualizar_datasets(arquivos_ano: dict[int, Path], limite_gdf: gpd.GeoDataFrame):
    """
    Extrai a classe predominante do MapBiomas (moda / majority) em cada célula de 1 km x 1 km ano a ano.
    """
    print("\n[DATASET] Extraindo classe modal de LULC por célula de 1 km²...")
    
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

    df_anual['lulc_classe'] = np.nan

    anos_presentes = sorted(df_anual['ano'].unique())
    for ano in anos_presentes:
        ano = int(ano)
        if ano not in arquivos_ano:
            continue
            
        mask_ano = (df_anual['ano'] == ano)
        indices_ano = df_anual[mask_ano].index
        gdf_ano = gdf_polys.iloc[indices_ano]
        
        caminho_tif = arquivos_ano[ano]
        with rasterio.open(caminho_tif) as src_r:
            if gdf_ano.crs != src_r.crs:
                gdf_ano = gdf_ano.to_crs(src_r.crs)
        
        # Moda da classe nativa do MapBiomas na célula de 1 km² (desconsiderando NoData=0)
        stats_lulc = zonal_stats(gdf_ano, str(caminho_tif), stats="majority", nodata=0)
        classes_extraidas = [int(s['majority']) if s['majority'] is not None else 0 for s in stats_lulc]
        
        df_anual.loc[mask_ano, 'lulc_classe'] = classes_extraidas
        print(f"  -> Ano {ano}: {len(indices_ano)} amostras extraídas (Moda LULC MapBiomas).")

    df_anual['lulc_classe'] = df_anual['lulc_classe'].astype('Int64')

    # Salvar CSVs atualizados
    df_anual.to_csv(CSV_ANUAL, index=False)
    print(f"\n[SAÍDA] Dataset consolidado atualizado: {CSV_ANUAL.name} (+ coluna lulc_classe)")

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
    print("🌳 PROCESSAMENTO E EXTRAÇÃO DE USO DO SOLO (MAPBIOMAS 2013-2025)")
    print("=" * 75)
    print(f"Diretório MapBiomas: {LULC_DIR}")
    print(f"Diretório Saída:     {OUTPUT_DIR}")

    if not LIMITE_SHP.exists():
        raise FileNotFoundError(f"Arquivo de limite não encontrado em: {LIMITE_SHP}")
    limite_gdf = gpd.read_file(LIMITE_SHP)

    # 1. Recortar e reprojetar rasters anuais do MapBiomas
    arquivos_ano = processar_recorte_mapbiomas(limite_gdf)

    # 2. Extrair a moda por célula de 1 km² e atualizar datasets CSV
    extrair_e_atualizar_datasets(arquivos_ano, limite_gdf)

    # 3. Gerar Prancha A4 Retrato com Subplots Anuais
    gerar_painel_a4_mapbiomas(arquivos_ano, limite_gdf)

    print("\n" + "=" * 75)
    print("✨ PROCESSAMENTO DE USO DO SOLO CONCLUÍDO COM SUCESSO!")
    print("=" * 75)


if __name__ == "__main__":
    main()
