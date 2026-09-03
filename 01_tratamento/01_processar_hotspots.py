"""
Script: 01_processar_hotspots.py
Etapa: 01_tratamento

Descrição:
    Processa os focos de calor (hotspots) brutos em duas fases:
    
    - Fase 1: Evitar registros duplicados (Agrupamento espaço-temporal).
              Focos a até 3 km de distância e dentro de uma janela temporal de 4 horas
              são agrupados e consolidados em um único evento de fogo.
              -> Gera GeoJSON e CSV com todos os focos agrupados (latitude, longitude, datetime, ano e n_deteccoes).
              
    - Fase 2: Separação e Balanceamento de Amostras Anualizadas em Grade de 1 km x 1 km:
              1. Cria a grade regular de células de 1 km x 1 km sobre a área de estudo.
              2. Amostras de Fogo (incendio = 1):
                 Para cada ano da série histórica (2013-2025), identifica as células de 1 km que
                 interceptam os focos de calor daquele ano específico.
              3. Amostras de Não-Fogo (incendio = 0):
                 Para cada ano, seleciona células a uma distância segura (> 3 km de qualquer foco),
                 amostradas aleatoriamente na proporção 1:1 com as células de fogo daquele ano.
              4. Particionamento Treino vs Validação Temporal:
                 - Conjunto de Treinamento/Ajuste: Anos 2013 a 2022 (amostras balanceadas ano a ano).
                 - Conjunto de Validação/Teste OOS: Anos 2023 a 2025 (ou sorteio estratificado por ano).
                 - Gera coluna `split` ('treino' ou 'validacao') e salva arquivos separados e consolidados.

    Saídas geradas em 'output/01_processar_hotspots':
    - hotspots_fase1_agrupados.geojson (Focos filtrados da Fase 1 com ano e datahora)
    - hotspots_fase1_agrupados.csv (CSV com lat, lon, datahora, ano e metadados)
    - grade_1km_amostras_anuais.csv (Dataset tabular balanceado completo 2013-2025 com coluna 'split')
    - grade_1km_amostras_treino.csv (Amostras balanceadas do período de treino: 2013-2022)
    - grade_1km_amostras_validacao.csv (Amostras balanceadas do período de validação: 2023-2025)
    - grade_1km_amostras_fogo_naofogo.geojson (Polígonos das células de 1 km selecionadas)
    - grade_1km_amostras.tif (Raster GeoTIFF de 1 km com classes: 1=Fogo, 0=Não-Fogo, 255=NoData)
"""

import os
import sys

# Configuração GDAL/Rasterio/Fiona para caminhos com caracteres especiais (Windows/acentuação)
os.environ['GDAL_FILENAME_IS_UTF8'] = 'NO'
os.environ['SHAPE_RESTORE_SHX'] = 'YES'

import glob
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon, box
from sklearn.cluster import DBSCAN
import rasterio
from rasterio.transform import from_bounds
from rasterio.features import rasterize

# ==========================================
# CONFIGURAÇÕES E CAMINHOS HARDCODED
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

FOCOS_DIR = BASE_DIR / "input" / "00_focos_de_calor"

# Limite municipal (verifica input ou output)
if (BASE_DIR / "input" / "01_vetores" / "SJP.shp").exists():
    LIMITE_SHP = BASE_DIR / "input" / "01_vetores" / "SJP.shp"
else:
    LIMITE_SHP = BASE_DIR / "output" / "01_vetores" / "SJP.shp"

OUTPUT_DIR = BASE_DIR / "output" / Path(__file__).stem

RAIO_AGRUPAMENTO_KM = 3.0       # Distância máxima para agrupar duplicados na Fase 1 (km)
JANELA_HORAS = 4.0              # Janela temporal para agrupar duplicados na Fase 1 (horas)
DISTANCIA_SEGURA_KM = 3.0       # Distância de segurança para células de Não-Fogo na Fase 2 (km)
TAMANHO_GRADE_M = 1000.0        # Tamanho da célula da grade em metros (1 km x 1 km)
CRS_PROJETADO = "EPSG:31982"    # SIRGAS 2000 / UTM zone 22S (métrica para PR)
TAXA_TREINO = 0.70              # 70% para Ajuste/Treinamento, 30% para Validação
SEED = 42                       # Semente para reprodutibilidade dos sorteios


def carregar_focos_brutos(diretorio_focos: Path, limite_area: gpd.GeoDataFrame = None) -> gpd.GeoDataFrame:
    """
    Carrega todos os arquivos CSV de focos de calor, padroniza nomes de colunas,
    converte coordenadas em GeoDataFrame e filtra espacialmente pelo polígono da área.
    """
    padrao_busca = str(diretorio_focos / "*.csv")
    arquivos_csv = glob.glob(padrao_busca)

    if not arquivos_csv:
        raise FileNotFoundError(f"Nenhum arquivo CSV encontrado em: {diretorio_focos}")

    print(f"[INFO] Carregando {len(arquivos_csv)} arquivos de focos de calor...")
    dfs = []
    for arq in sorted(arquivos_csv):
        df_temp = pd.read_csv(arq)
        df_temp.columns = [c.lower() for c in df_temp.columns]
        dfs.append(df_temp)

    df_todos = pd.concat(dfs, ignore_index=True)

    coluna_data = 'datahora' if 'datahora' in df_todos.columns else 'data_hora'
    df_todos['datahora'] = pd.to_datetime(df_todos[coluna_data], format='mixed', errors='coerce')
    df_todos = df_todos.dropna(subset=['datahora'])
    df_todos['ano'] = df_todos['datahora'].dt.year

    geometrias = [Point(xy) for xy in zip(df_todos['longitude'], df_todos['latitude'])]
    gdf_focos = gpd.GeoDataFrame(df_todos, geometry=geometrias, crs="EPSG:4326")

    if limite_area is not None:
        if limite_area.crs != gdf_focos.crs:
            limite_area = limite_area.to_crs(gdf_focos.crs)
        gdf_focos = gpd.sjoin(gdf_focos, limite_area[['geometry']], how="inner", predicate="intersects")
        gdf_focos = gdf_focos.drop(columns=['index_right'], errors='ignore')
        print(f"[INFO] Focos após recorte na área de estudo: {len(gdf_focos)}")

    return gdf_focos.sort_values(by='datahora').reset_index(drop=True)


def fase1_agrupar_focos(
    gdf_focos: gpd.GeoDataFrame,
    distancia_km: float = RAIO_AGRUPAMENTO_KM,
    janela_horas: float = JANELA_HORAS,
    crs_projetado: str = CRS_PROJETADO
) -> gpd.GeoDataFrame:
    """
    Fase 1: Agrupa focos próximos no espaço (<= 3 km) e tempo (<= 4 h).
    Utiliza DBSCAN com normalização espaço-temporal:
      - Espaço métrico (metros) projetado em CRS plano (EPSG:31982).
      - Tempo em horas contínuas a partir da primeira detecção.
    """
    print(f"\n[FASE 1] Agrupamento espaço-temporal (Raio: {distancia_km} km, Janela: {janela_horas} h)...")
    if len(gdf_focos) == 0:
        return gdf_focos

    gdf_proj = gdf_focos.to_crs(crs_projetado)

    coords_x = gdf_proj.geometry.x.values
    coords_y = gdf_proj.geometry.y.values

    tempo_min = gdf_proj['datahora'].min()
    horas_relativas = (gdf_proj['datahora'] - tempo_min).dt.total_seconds() / 3600.0

    distancia_m = distancia_km * 1000.0
    x_norm = coords_x / distancia_m
    y_norm = coords_y / distancia_m
    t_norm = horas_relativas.values / janela_horas

    matriz_features = np.column_stack((x_norm, y_norm, t_norm))

    # eps=1.0 agrupa pontos dentro do raio de 3km e intervalo de 4h
    db = DBSCAN(eps=1.0, min_samples=1, metric='euclidean')
    labels = db.fit_predict(matriz_features)

    gdf_proj['cluster_id'] = labels

    focos_filtrados = []
    for cluster_id, grupo in gdf_proj.groupby('cluster_id'):
        primeiro = grupo.sort_values('datahora').iloc[0].copy()
        primeiro['n_deteccoes'] = len(grupo)
        primeiro['ano'] = primeiro['datahora'].year
        focos_filtrados.append(primeiro)

    gdf_resultado = gpd.GeoDataFrame(focos_filtrados, crs=crs_projetado).to_crs("EPSG:4326")
    
    # Atualizar coordenadas lat/lon WGS84
    gdf_resultado['longitude'] = gdf_resultado.geometry.x
    gdf_resultado['latitude'] = gdf_resultado.geometry.y
    gdf_resultado['datahora_str'] = gdf_resultado['datahora'].dt.strftime('%Y-%m-%d %H:%M:%S')

    print(f"[FASE 1] Concluída: {len(gdf_focos)} registros consolidados em {len(gdf_resultado)} focos únicos.")
    return gdf_resultado.reset_index(drop=True)


def gerar_grade_1km(
    limite_area: gpd.GeoDataFrame,
    tamanho_celula_m: float = TAMANHO_GRADE_M,
    crs_projetado: str = CRS_PROJETADO
) -> gpd.GeoDataFrame:
    """
    Gera uma malha regular de polígonos quadrados de 1 km x 1 km cobrindo a área de estudo.
    """
    limite_proj = limite_area.to_crs(crs_projetado)
    minx, miny, maxx, maxy = limite_proj.total_bounds

    x_coords = np.arange(minx, maxx, tamanho_celula_m)
    y_coords = np.arange(miny, maxy, tamanho_celula_m)

    celulas = []
    ids = []
    count = 0
    area_union = limite_proj.union_all()

    for x in x_coords:
        for y in y_coords:
            poly = box(x, y, x + tamanho_celula_m, y + tamanho_celula_m)
            # Manter células que intersectam a área de estudo
            if poly.intersects(area_union):
                celulas.append(poly)
                ids.append(count)
                count += 1

    gdf_grade = gpd.GeoDataFrame({'cell_id': ids, 'geometry': celulas}, crs=crs_projetado)
    print(f"[INFO] Grade de 1 km x 1 km criada com {len(gdf_grade)} células cobrindo o município.")
    return gdf_grade


def fase2_amostragem_grade_anual(
    gdf_focos_filtrados: gpd.GeoDataFrame,
    gdf_grade: gpd.GeoDataFrame,
    distancia_segura_km: float = DISTANCIA_SEGURA_KM,
    taxa_treino: float = TAXA_TREINO,
    seed: int = SEED,
    crs_projetado: str = CRS_PROJETADO
) -> tuple[gpd.GeoDataFrame, pd.DataFrame]:
    """
    Fase 2: Classifica, balanceia e sorteia amostras ano a ano (2013 a 2025):
    - Amostras de Fogo (incendio = 1): Células da grade de 1 km que registraram fogo em cada ano específico.
    - Amostras de Não-Fogo (incendio = 0): Células da grade sem fogo naquele ano e a uma distância segura (> 3 km de focos),
      sorteadas aleatoriamente na proporção 1:1 com as células de fogo daquele ano.
    - Sorteio Aleatório Estratificado por Ano: 70% das amostras de cada ano para Treino/Ajuste e 30% para Validação.
    """
    print(f"\n[FASE 2] Amostragem Balanceada e Sorteio Aleatório ({int(taxa_treino*100)}% Treino / {int((1-taxa_treino)*100)}% Validação)...")
    np.random.seed(seed)

    gdf_focos_proj = gdf_focos_filtrados.to_crs(crs_projetado)
    anos_disponiveis = sorted(gdf_focos_proj['ano'].unique())
    print(f"[INFO] Anos com detecção de focos: {anos_disponiveis}")

    amostras_totais = []
    
    for ano in anos_disponiveis:
        focos_ano = gdf_focos_proj[gdf_focos_proj['ano'] == ano]
        
        # 1. Identificar células de fogo do ano
        join_fogo = gpd.sjoin(gdf_grade, focos_ano[['geometry']], how='inner', predicate='intersects')
        ids_fogo_ano = join_fogo['cell_id'].unique()
        
        gdf_fogo_ano = gdf_grade[gdf_grade['cell_id'].isin(ids_fogo_ano)].copy()
        gdf_fogo_ano['incendio'] = 1
        gdf_fogo_ano['ano'] = int(ano)
        gdf_fogo_ano['tipo'] = 'fogo'
        n_fogo = len(gdf_fogo_ano)
        
        # 2. Identificar células de não-fogo (todas as células que não tiveram fogo naquele ano)
        candidatas_nao_fogo = gdf_grade[~gdf_grade['cell_id'].isin(ids_fogo_ano)].copy()
        
        if len(candidatas_nao_fogo) < n_fogo:
            gdf_nao_fogo_ano = candidatas_nao_fogo.copy()
        else:
            gdf_nao_fogo_ano = candidatas_nao_fogo.sample(n=n_fogo, random_state=seed + int(ano)).copy()
            
        gdf_nao_fogo_ano['incendio'] = 0
        gdf_nao_fogo_ano['ano'] = int(ano)
        gdf_nao_fogo_ano['tipo'] = 'nao_fogo'
        
        # 3. Sorteio aleatório de 70% Treino e 30% Validação dentro do ano (estratificado por fogo/não-fogo)
        n_treino_fogo = int(np.round(n_fogo * taxa_treino))
        idx_treino_fogo = gdf_fogo_ano.sample(n=n_treino_fogo, random_state=seed + int(ano)).index
        gdf_fogo_ano['split'] = 'validacao'
        gdf_fogo_ano.loc[idx_treino_fogo, 'split'] = 'treino'
        
        n_nao_fogo = len(gdf_nao_fogo_ano)
        n_treino_naofogo = int(np.round(n_nao_fogo * taxa_treino))
        idx_treino_naofogo = gdf_nao_fogo_ano.sample(n=n_treino_naofogo, random_state=seed + int(ano) + 100).index
        gdf_nao_fogo_ano['split'] = 'validacao'
        gdf_nao_fogo_ano.loc[idx_treino_naofogo, 'split'] = 'treino'
        
        n_tr = len(gdf_fogo_ano[gdf_fogo_ano['split']=='treino']) + len(gdf_nao_fogo_ano[gdf_nao_fogo_ano['split']=='treino'])
        n_val = len(gdf_fogo_ano[gdf_fogo_ano['split']=='validacao']) + len(gdf_nao_fogo_ano[gdf_nao_fogo_ano['split']=='validacao'])
        
        print(f"  -> Ano {ano}: {n_fogo} Fogo | {n_nao_fogo} Não-Fogo -> Treino: {n_tr} | Validação: {n_val}")
        
        amostras_totais.append(pd.concat([gdf_fogo_ano, gdf_nao_fogo_ano], ignore_index=True))

    gdf_amostras_consolidadas = gpd.GeoDataFrame(pd.concat(amostras_totais, ignore_index=True), crs=crs_projetado)

    # Extrair centroides em coordenadas geográficas WGS84 para a tabela final de modelagem
    centroides_proj = gdf_amostras_consolidadas.geometry.centroid
    centroides_wgs84 = gpd.GeoDataFrame(geometry=centroides_proj, crs=crs_projetado).to_crs("EPSG:4326")

    df_dataset_modelagem = pd.DataFrame({
        'cell_id': gdf_amostras_consolidadas['cell_id'],
        'longitude_centro': centroides_wgs84.geometry.x,
        'latitude_centro': centroides_wgs84.geometry.y,
        'incendio': gdf_amostras_consolidadas['incendio'],
        'ano': gdf_amostras_consolidadas['ano'],
        'split': gdf_amostras_consolidadas['split'],
        'tipo': gdf_amostras_consolidadas['tipo']
    })

    total_treino = len(df_dataset_modelagem[df_dataset_modelagem['split'] == 'treino'])
    total_val = len(df_dataset_modelagem[df_dataset_modelagem['split'] == 'validacao'])
    print(f"\n[INFO] Total consolidado de amostras: {len(df_dataset_modelagem)}")
    print(f"  - Treino/Ajuste (70% ao longo de 2013-2025): {total_treino} amostras")
    print(f"  - Validação (30% ao longo de 2013-2025):     {total_val} amostras")

    gdf_amostras_wgs84 = gdf_amostras_consolidadas.to_crs("EPSG:4326")
    return gdf_amostras_wgs84, df_dataset_modelagem


def exportar_raster_grade_1km(
    gdf_amostras_grade: gpd.GeoDataFrame,
    limite_area: gpd.GeoDataFrame,
    caminho_saida_tif: Path,
    tamanho_celula_m: float = TAMANHO_GRADE_M,
    crs_projetado: str = CRS_PROJETADO
):
    """
    Exporta o raster GeoTIFF da grade de 1 km com as classes de Fogo (1), Não-Fogo (0) e NoData (255).
    """
    print(f"\n[RASTER] Gerando raster de 1 km x 1 km...")
    gdf_proj = gdf_amostras_grade.to_crs(crs_projetado)
    limite_proj = limite_area.to_crs(crs_projetado)

    minx, miny, maxx, maxy = limite_proj.total_bounds

    width = int(np.ceil((maxx - minx) / tamanho_celula_m))
    height = int(np.ceil((maxy - miny) / tamanho_celula_m))

    transform = from_bounds(minx, miny, maxx, maxy, width, height)

    # Células únicas para o raster de referência
    gdf_unicas = gdf_proj.drop_duplicates(subset=['cell_id'])
    shapes = [(geom, val) for geom, val in zip(gdf_unicas.geometry, gdf_unicas['incendio'])]

    raster_data = rasterize(
        shapes=shapes,
        out_shape=(height, width),
        transform=transform,
        fill=255,  # NoData
        dtype=np.uint8,
        all_touched=True
    )

    meta = {
        'driver': 'GTiff',
        'dtype': 'uint8',
        'nodata': 255,
        'width': width,
        'height': height,
        'count': 1,
        'crs': crs_projetado,
        'transform': transform,
        'compress': 'lzw'
    }

    caminho_saida_tif.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(str(caminho_saida_tif), 'w', **meta) as dst:
        dst.write(raster_data, 1)

    print(f"[RASTER] Salvo com sucesso em: {caminho_saida_tif}")


def main():
    print(f"=====================================================")
    print(f"      PIPELINE DE TRATAMENTO DE FOCOS E GRADE 1KM    ")
    print(f"=====================================================")
    print(f"Entrada Focos:     {FOCOS_DIR}")
    print(f"Limite Estudo:     {LIMITE_SHP}")
    print(f"Diretório Saída:   {OUTPUT_DIR}")
    print(f"Particionamento:   {int(TAXA_TREINO*100)}% Treino / {int((1-TAXA_TREINO)*100)}% Validação (estratificado 2013-2025)")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Carregar Limite da Área de Estudo
    if not LIMITE_SHP.exists():
        raise FileNotFoundError(f"Arquivo de limite não encontrado em: {LIMITE_SHP}")

    print(f"\n[INFO] Carregando limite da área...")
    limite_area = gpd.read_file(LIMITE_SHP)

    # 2. Carregar Focos Brutos
    gdf_focos = carregar_focos_brutos(FOCOS_DIR, limite_area)

    # 3. Fase 1: Agrupamento Espaço-Temporal
    gdf_focos_filtrados = fase1_agrupar_focos(gdf_focos)

    # Exportar GeoJSON e CSV da Fase 1 (com lat, lon, ano e datetime)
    geojson_fase1 = OUTPUT_DIR / "hotspots_fase1_agrupados.geojson"
    gdf_focos_filtrados.to_file(str(geojson_fase1), driver="GeoJSON")
    print(f"[SAÍDA] GeoJSON Focos Agrupados (Fase 1): {geojson_fase1}")

    csv_fase1 = OUTPUT_DIR / "hotspots_fase1_agrupados.csv"
    colunas_csv = ['latitude', 'longitude', 'datahora', 'ano', 'n_deteccoes']
    colunas_existentes = [c for c in colunas_csv if c in gdf_focos_filtrados.columns]
    gdf_focos_filtrados[colunas_existentes].to_csv(csv_fase1, index=False)
    print(f"[SAÍDA] CSV Focos Agrupados (Fase 1):     {csv_fase1}")

    # 4. Fase 2: Grade 1 km x 1 km e Amostragem Balanceada Anual com Split 70/30
    gdf_grade_1km = gerar_grade_1km(limite_area)
    gdf_amostras_grade, df_dataset_modelagem = fase2_amostragem_grade_anual(gdf_focos_filtrados, gdf_grade_1km)

    # Exportar Polígonos da Grade Amostrada (GeoJSON)
    geojson_grade = OUTPUT_DIR / "grade_1km_amostras_fogo_naofogo.geojson"
    gdf_amostras_grade.to_file(str(geojson_grade), driver="GeoJSON")
    print(f"[SAÍDA] GeoJSON Células Grade 1km (Fase 2): {geojson_grade}")

    # Exportar Dataset Tabular Completo (CSV)
    csv_amostras_anuais = OUTPUT_DIR / "grade_1km_amostras_anuais.csv"
    df_dataset_modelagem.to_csv(csv_amostras_anuais, index=False)
    print(f"[SAÍDA] CSV Dataset Completo (2013-2025):  {csv_amostras_anuais}")

    # Exportar Datasets Separados: Treino (70%) e Validação (30%)
    csv_treino = OUTPUT_DIR / "grade_1km_amostras_treino.csv"
    df_treino = df_dataset_modelagem[df_dataset_modelagem['split'] == 'treino']
    df_treino.to_csv(csv_treino, index=False)
    print(f"[SAÍDA] CSV Treino/Ajuste (70%):           {csv_treino}")

    csv_val = OUTPUT_DIR / "grade_1km_amostras_validacao.csv"
    df_val = df_dataset_modelagem[df_dataset_modelagem['split'] == 'validacao']
    df_val.to_csv(csv_val, index=False)
    print(f"[SAÍDA] CSV Validação (30%):               {csv_val}")

    # Exportar Raster 1 km x 1 km (GeoTIFF)
    raster_grade = OUTPUT_DIR / "grade_1km_amostras.tif"
    exportar_raster_grade_1km(gdf_amostras_grade, limite_area, raster_grade)

    print(f"\n[SUCESSO] Processamento concluído com sucesso!")
    print(f"Todos os arquivos foram salvos em: {OUTPUT_DIR}\n")


if __name__ == "__main__":
    main()
