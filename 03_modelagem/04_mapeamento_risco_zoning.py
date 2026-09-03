"""
Script: 04_mapeamento_risco_zoning.py
Etapa: 03_modelagem

Descrição:
    Executa a Geração dos Mapas Espaciais Raster de Risco de Incêndio (Zoning) em Alta Resolução (100m)
    e Validação Espacial com base em WarpedVRT e inferência contínua/discreta:
    
    1. Reamostragem Espacial Raster (WarpedVRT a 100m):
       - Utiliza rasterio.vrt.WarpedVRT para reprojetar e reamostrar todos os rasters de entrada
         (Topografia, Vegetação, SPI, Infraestrutura DR/DS, LULC) para uma grade uniforme de 100 m x 100 m.
       - Aplica WarpedVRT com Resampling.bilinear para contínuos e Resampling.nearest para categóricos.
       
    2. Agrupamento Temporal dos Anos (2013-2025):
       - Agrupamento temporal das probabilidades anuais calculado pela MEDIANA dos anos,
         garantindo robustez contra outliers de secas ou anos excepcionais.
         
    3. Modelos de Inferência Aplicados Célula a Célula (Pixel a Pixel):
       - Rede Naive Bayes Network (NBN) via Tabelas CPT calibradas.
       - Regressão Logística Contínua (Logit) via coeficientes PCA calibrados.
       
    4. Zonamento em 4 Classes de Risco (Chen et al., 2021):
       - Baixo Risco (Low):       P < 25%
       - Médio Risco (Medium):   25% <= P < 50%
       - Alto Risco (High):      50% <= P < 75%
       - Muito Alto (Very High): P >= 75%
       
    5. Saídas:
       - Rasters GeoTIFF de 100m de probabilidade e classes de risco (NBN e Logit).
       - Prancha A4 da série temporal anual (2013-2025).
       - Prancha A4 comparativa (Naive Bayes vs Regressão Logística).
       - Relatório de validação espacial com os focos reais de satélite em JSON.
"""

import sys
import os

# Configuração GDAL/Rasterio/Fiona para caminhos com caracteres especiais (Windows/acentuação)
os.environ['GDAL_FILENAME_IS_UTF8'] = 'NO'
os.environ['SHAPE_RESTORE_SHX'] = 'YES'

import json
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.vrt import WarpedVRT
from rasterio.enums import Resampling
from rasterio.transform import from_bounds
from rasterio.features import rasterize
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap, BoundaryNorm
import seaborn as sns

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ==========================================
# PARÂMETROS E CONFIGURAÇÕES GLOBAIS
# ==========================================
RESOLUCAO_GRADE_M = 100.0  # Resolução espacial hardcoded para a grade de inferência WarpedVRT (100 metros)
CRS_PROJETADO = "EPSG:31982"
ANOS = list(range(2013, 2026))

BASE_DIR = Path(__file__).resolve().parent.parent

AMOSTRAS_DIR = BASE_DIR / "output" / "01_processar_hotspots"
CSV_ANUAL = AMOSTRAS_DIR / "grade_1km_amostras_anuais.csv"
CSV_TREINO = AMOSTRAS_DIR / "grade_1km_amostras_treino.csv"
CSV_VALIDACAO = AMOSTRAS_DIR / "grade_1km_amostras_validacao.csv"
FOCOS_FASE1 = AMOSTRAS_DIR / "hotspots_fase1_agrupados.geojson"

if (BASE_DIR / "input" / "01_vetores" / "SJP.shp").exists():
    LIMITE_SHP = BASE_DIR / "input" / "01_vetores" / "SJP.shp"
else:
    LIMITE_SHP = BASE_DIR / "output" / "01_vetores" / "SJP.shp"

# Diretórios dos Rasters
DIR_TOPO = BASE_DIR / "output" / "03_processar_topografia"
DIR_VEG = BASE_DIR / "output" / "04_processar_indices_vegetacao"
DIR_SPI = BASE_DIR / "output" / "05_processar_precipitacao_spi"
DIR_INFRA = BASE_DIR / "output" / "06_processar_distancias_infraestrutura"
DIR_LULC = BASE_DIR / "output" / "07_processar_uso_cobertura"

OUTPUT_DIR = BASE_DIR / "output" / "03_modelagem" / "03_mapeamento_risco_zoning"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ANOS = list(range(2013, 2026))
CRS_PROJETADO = "EPSG:31982"
RESOLUCAO_ALTA_M = 100.0  # Resolução alvo de 100 metros

FEATURES_NBN = [
    'elevation_classe',
    'slope_classe',
    'aspect_classe',
    'ndvi_classe',
    'ndmi_classe',
    'spi_classe',
    'dr_classe',
    'ds_classe',
    'lulc_classe'
]

CORES_RISCO = ['#2b83ba', '#ffffbf', '#fdae61', '#d7191c']
LABELS_RISCO = [
    'Baixo Risco (Low: < 25%)',
    'Médio Risco (Medium: 25-50%)',
    'Alto Risco (High: 50-75%)',
    'Muito Alto Risco (Very High: ≥ 75%)'
]


# ==========================================
# 1. CARREGAR MODELOS
# ==========================================
def carregar_modelo_cpt():
    cpt_json = BASE_DIR / "output" / "03_modelagem" / "02_treinar_naive_bayes" / "tabelas_probabilidade_cpt_nbn.json"
    if not cpt_json.exists():
        raise FileNotFoundError(f"Arquivo CPT não encontrado em: {cpt_json}. Execute 02_treinar_naive_bayes.py.")
    with open(cpt_json, 'r', encoding='utf-8') as f:
        return json.load(f)


def carregar_modelo_logistico():
    logit_json = BASE_DIR / "output" / "03_modelagem" / "04_regressao_logistica" / "metricas_regressao_logistica_pca.json"
    if not logit_json.exists():
        return None
    with open(logit_json, 'r', encoding='utf-8') as f:
        return json.load(f)


# ==========================================
# 2. LEITURA COM WarpedVRT EM GRADE DE 100 METROS
# ==========================================
def ler_raster_vrt_100m(caminho_tif: Path, dst_crs: str, dst_transform, dst_width: int, dst_height: int, is_categorical: bool = False) -> np.ndarray:
    """Lê qualquer raster de entrada reamostrando para a grade de 100m usando WarpedVRT."""
    resampling_mode = Resampling.nearest if is_categorical else Resampling.bilinear
    
    with rasterio.open(caminho_tif) as src:
        with WarpedVRT(
            src,
            crs=dst_crs,
            transform=dst_transform,
            width=dst_width,
            height=dst_height,
            resampling=resampling_mode
        ) as vrt:
            data = vrt.read(1)
            return data


# ==========================================
# 3. INFERÊNCIA VETORIALIZADA (PIXEL A PIXEL)
# ==========================================
def calcular_probabilidade_nbn_grid(dict_features_cls: dict, cpt_data: dict, mask_valida: np.ndarray) -> np.ndarray:
    """Calcula a probabilidade Naive Bayes de forma vetorizada sobre a matriz 2D."""
    prior_f = cpt_data['prior_fogo']
    prior_nf = cpt_data['prior_nao_fogo']

    log_p_f = np.full(mask_valida.shape, np.log(prior_f), dtype=np.float32)
    log_p_nf = np.full(mask_valida.shape, np.log(prior_nf), dtype=np.float32)

    cpt_f = cpt_data['cpt_fogo']
    cpt_nf = cpt_data['cpt_nao_fogo']

    for feat in FEATURES_NBN:
        grid_vals = dict_features_cls[feat]
        
        # Mapear probabilidades da CPT
        cpt_f_feat = cpt_f.get(feat, {})
        cpt_nf_feat = cpt_nf.get(feat, {})

        prob_f_arr = np.zeros_like(grid_vals, dtype=np.float32)
        prob_nf_arr = np.zeros_like(grid_vals, dtype=np.float32)

        for val_k in np.unique(grid_vals[mask_valida]):
            str_k = str(int(val_k))
            p_f = cpt_f_feat.get(str_k, 0.01)
            p_nf = cpt_nf_feat.get(str_k, 0.01)

            mask_k = (grid_vals == val_k) & mask_valida
            prob_f_arr[mask_k] = max(p_f, 1e-6)
            prob_nf_arr[mask_k] = max(p_nf, 1e-6)

        log_p_f[mask_valida] += np.log(prob_f_arr[mask_valida])
        log_p_nf[mask_valida] += np.log(prob_nf_arr[mask_valida])

    max_log = np.maximum(log_p_f, log_p_nf)
    p_f_exp = np.exp(log_p_f - max_log)
    p_nf_exp = np.exp(log_p_nf - max_log)

    prob_fogo = np.zeros(mask_valida.shape, dtype=np.float32)
    prob_fogo[mask_valida] = p_f_exp[mask_valida] / (p_f_exp[mask_valida] + p_nf_exp[mask_valida])
    return prob_fogo


def calcular_probabilidade_logit_grid(dict_features_cont: dict, logit_data: dict, df_ref: pd.DataFrame, mask_valida: np.ndarray) -> np.ndarray:
    """Calcula a probabilidade Logística de forma vetorizada sobre a matriz 2D."""
    intercept = logit_data['intercepto']
    coefs = {c['feature']: c['coef_beta'] for c in logit_data['coeficientes']}
    vars_logit = logit_data['variaveis_selecionadas_pca']

    means = df_ref[vars_logit].mean()
    stds = df_ref[vars_logit].std()

    z = np.full(mask_valida.shape, intercept, dtype=np.float32)

    for var in vars_logit:
        val_grid = dict_features_cont[var]
        mu = means[var]
        sigma = stds[var] + 1e-6
        
        val_norm = (val_grid - mu) / sigma
        beta = coefs.get(var, 0.0)
        z[mask_valida] += beta * val_norm[mask_valida]

    prob_logit = np.zeros(mask_valida.shape, dtype=np.float32)
    prob_logit[mask_valida] = 1.0 / (1.0 + np.exp(-z[mask_valida]))
    return prob_logit


# ==========================================
# 4. PROCESSAMENTO PRINCIPAL DO ZONEAMENTO
# ==========================================
def processar_mapeamento_zoning():
    print("=" * 75)
    print(f"🗺️ MAPEAMENTO DE RISCO E ZONEAMENTO EM ALTA RESOLUÇÃO (100m)")
    print(f"  -> Reamostragem com WarpedVRT")
    print(f"  -> Agrupamento Temporal pela MEDIANA dos anos (2013-2025)")
    print("=" * 75)

    limite_gdf = gpd.read_file(LIMITE_SHP).to_crs(CRS_PROJETADO)
    minx, miny, maxx, maxy = limite_gdf.total_bounds
    
    # Grade em Alta Resolução (100 metros)
    width = int(np.ceil((maxx - minx) / RESOLUCAO_GRADE_M))
    height = int(np.ceil((maxy - miny) / RESOLUCAO_GRADE_M))
    dst_transform = from_bounds(minx, miny, maxx, maxy, width, height)

    meta_100m = {
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

    # Máscara do limite municipal
    mask_municipio = rasterize(
        [(geom, 1) for geom in limite_gdf.geometry],
        out_shape=(height, width),
        transform=dst_transform,
        fill=0,
        dtype=np.uint8
    ) == 1

    cpt_data = carregar_modelo_cpt()
    logit_data = carregar_modelo_logistico()
    df_ref = pd.read_csv(CSV_TREINO) if CSV_TREINO.exists() else pd.read_csv(CSV_ANUAL)

    # 1. Carregar Rasters Estáticos a 100m
    print("\n[VRT] Reamostrando camadas estáticas a 100m...")
    elev_cls = ler_raster_vrt_100m(DIR_TOPO / "elevation_classes.tif", CRS_PROJETADO, dst_transform, width, height, is_categorical=True)
    slope_cls = ler_raster_vrt_100m(DIR_TOPO / "slope_classes.tif", CRS_PROJETADO, dst_transform, width, height, is_categorical=True)
    aspect_cls = ler_raster_vrt_100m(DIR_TOPO / "aspect_classes.tif", CRS_PROJETADO, dst_transform, width, height, is_categorical=True)
    dr_cls = ler_raster_vrt_100m(DIR_INFRA / "SJP_DR_estradas_classes.tif", CRS_PROJETADO, dst_transform, width, height, is_categorical=True)

    elev_cont = ler_raster_vrt_100m(DIR_TOPO / "elevation.tif", CRS_PROJETADO, dst_transform, width, height, is_categorical=False)
    slope_cont = ler_raster_vrt_100m(DIR_TOPO / "slope.tif", CRS_PROJETADO, dst_transform, width, height, is_categorical=False)
    aspect_cont = ler_raster_vrt_100m(DIR_TOPO / "aspect.tif", CRS_PROJETADO, dst_transform, width, height, is_categorical=False)
    dr_cont = ler_raster_vrt_100m(DIR_INFRA / "SJP_DR_estradas_distancia.tif", CRS_PROJETADO, dst_transform, width, height, is_categorical=False)

    pilha_probas_nbn = []
    pilha_probas_logit = []
    mapas_anuais_nbn = {}

    for ano in ANOS:
        ndvi_cls_tif = DIR_VEG / f"SJP_NDVI_{ano}_classes.tif"
        ndmi_cls_tif = DIR_VEG / f"SJP_NDMI_{ano}_classes.tif"
        spi_cls_tif = DIR_SPI / f"SJP_spi_{ano}_classes.tif"
        ds_cls_tif = DIR_INFRA / f"SJP_DS_urbano_{ano}_classes.tif"
        lulc_tif = DIR_LULC / f"SJP_mapbiomas_{ano}.tif"

        ndvi_cont_tif = BASE_DIR / "output" / "04_ndvi" / f"SJP_NDVI_{ano}.tif"
        ndmi_cont_tif = BASE_DIR / "output" / "04_ndmi" / f"SJP_NDMI_{ano}.tif"
        spi_cont_tif = DIR_SPI / f"SJP_spi_{ano}.tif"
        ds_cont_tif = DIR_INFRA / f"SJP_DS_urbano_{ano}_distancia.tif"

        if not (ndvi_cls_tif.exists() and ndmi_cls_tif.exists() and spi_cls_tif.exists() and ds_cls_tif.exists() and lulc_tif.exists()):
            continue

        ndvi_cls = ler_raster_vrt_100m(ndvi_cls_tif, CRS_PROJETADO, dst_transform, width, height, is_categorical=True)
        ndmi_cls = ler_raster_vrt_100m(ndmi_cls_tif, CRS_PROJETADO, dst_transform, width, height, is_categorical=True)
        spi_cls = ler_raster_vrt_100m(spi_cls_tif, CRS_PROJETADO, dst_transform, width, height, is_categorical=True)
        ds_cls = ler_raster_vrt_100m(ds_cls_tif, CRS_PROJETADO, dst_transform, width, height, is_categorical=True)
        lulc = ler_raster_vrt_100m(lulc_tif, CRS_PROJETADO, dst_transform, width, height, is_categorical=True)

        dict_nbn = {
            'elevation_classe': elev_cls,
            'slope_classe': slope_cls,
            'aspect_classe': aspect_cls,
            'ndvi_classe': ndvi_cls,
            'ndmi_classe': ndmi_cls,
            'spi_classe': spi_cls,
            'dr_classe': dr_cls,
            'ds_classe': ds_cls,
            'lulc_classe': lulc
        }

        prob_nbn_ano = calcular_probabilidade_nbn_grid(dict_nbn, cpt_data, mask_municipio)
        pilha_probas_nbn.append(prob_nbn_ano)
        mapas_anuais_nbn[ano] = prob_nbn_ano

        if logit_data is not None and ndvi_cont_tif.exists() and ndmi_cont_tif.exists() and spi_cont_tif.exists() and ds_cont_tif.exists():
            ndvi_cont = ler_raster_vrt_100m(ndvi_cont_tif, CRS_PROJETADO, dst_transform, width, height, is_categorical=False)
            ndmi_cont = ler_raster_vrt_100m(ndmi_cont_tif, CRS_PROJETADO, dst_transform, width, height, is_categorical=False)
            spi_cont = ler_raster_vrt_100m(spi_cont_tif, CRS_PROJETADO, dst_transform, width, height, is_categorical=False)
            ds_cont = ler_raster_vrt_100m(ds_cont_tif, CRS_PROJETADO, dst_transform, width, height, is_categorical=False)

            dict_logit = {
                'elevation_m': elev_cont,
                'slope_deg': slope_cont,
                'aspect_deg': aspect_cont,
                'dist_estradas_m': dr_cont,
                'dist_urbano_m': ds_cont,
                'ndvi_valor': ndvi_cont,
                'ndmi_valor': ndmi_cont,
                'spi_anual': spi_cont
            }
            prob_logit_ano = calcular_probabilidade_logit_grid(dict_logit, logit_data, df_ref, mask_municipio)
            pilha_probas_logit.append(prob_logit_ano)

        print(f"  -> Ano {ano}: VRT 100m inferido com sucesso.")

    # 2. Agrupamento Temporal pela MEDIANA
    print("\n[AGRUPAMENTO] Calculando a MEDIANA temporal (2013-2025)...")
    prob_nbn_mediana = np.median(np.array(pilha_probas_nbn), axis=0)
    
    # 4 Níveis de Risco NBN
    risco_nbn_classes = np.zeros((height, width), dtype=np.uint8)
    risco_nbn_classes[mask_municipio & (prob_nbn_mediana < 0.25)] = 1
    risco_nbn_classes[mask_municipio & (prob_nbn_mediana >= 0.25) & (prob_nbn_mediana < 0.50)] = 2
    risco_nbn_classes[mask_municipio & (prob_nbn_mediana >= 0.50) & (prob_nbn_mediana < 0.75)] = 3
    risco_nbn_classes[mask_municipio & (prob_nbn_mediana >= 0.75)] = 4

    # Exportar GeoTIFF NBN Mediana 100m
    out_tif_prob = OUTPUT_DIR / "SJP_risco_fogo_nbn_100m_prob_mediana.tif"
    with rasterio.open(out_tif_prob, 'w', **meta_100m) as dst:
        data_out = np.where(mask_municipio, prob_nbn_mediana, -9999.0).astype(np.float32)
        dst.write(data_out, 1)

    meta_cls = meta_100m.copy()
    meta_cls['dtype'] = 'uint8'
    meta_cls['nodata'] = 0
    out_tif_cls = OUTPUT_DIR / "SJP_risco_fogo_nbn_100m_classes_mediana.tif"
    with rasterio.open(out_tif_cls, 'w', **meta_cls) as dst:
        dst.write(risco_nbn_classes, 1)

    print(f"✅ Raster de Probabilidade NBN 100m salvo: {out_tif_prob.name}")
    print(f"✅ Raster de Classes NBN 100m salvo:       {out_tif_cls.name}")

    if len(pilha_probas_logit) > 0:
        prob_logit_mediana = np.median(np.array(pilha_probas_logit), axis=0)
        risco_logit_classes = np.zeros((height, width), dtype=np.uint8)
        risco_logit_classes[mask_municipio & (prob_logit_mediana < 0.25)] = 1
        risco_logit_classes[mask_municipio & (prob_logit_mediana >= 0.25) & (prob_logit_mediana < 0.50)] = 2
        risco_logit_classes[mask_municipio & (prob_logit_mediana >= 0.50) & (prob_logit_mediana < 0.75)] = 3
        risco_logit_classes[mask_municipio & (prob_logit_mediana >= 0.75)] = 4

        out_tif_logit_cls = OUTPUT_DIR / "SJP_risco_fogo_logit_100m_classes_mediana.tif"
        with rasterio.open(out_tif_logit_cls, 'w', **meta_cls) as dst:
            dst.write(risco_logit_classes, 1)
        print(f"✅ Raster de Classes Logit 100m salvo:     {out_tif_logit_cls.name}")

    # 3. Validação com Focos Reais
    val_stats = validar_raster_com_focos(out_tif_cls, out_tif_logit_cls if len(pilha_probas_logit)>0 else None)

    # 4. Pranchas Cartográficas A4
    gerar_pranchas_cartograficas(mapas_anuais_nbn, prob_nbn_mediana, risco_nbn_classes, risco_logit_classes if len(pilha_probas_logit)>0 else None, limite_gdf, dst_transform, width, height, val_stats)


# ==========================================
# 5. VALIDAÇÃO ESPACIAL
# ==========================================
def validar_raster_com_focos(caminho_nbn_cls: Path, caminho_logit_cls: Path = None) -> dict:
    print("\n[VALIDAÇÃO] Extraindo taxa de acerto espacial nos rasters de 100m...")
    if not FOCOS_FASE1.exists():
        return {}

    gdf_focos = gpd.read_file(FOCOS_FASE1).to_crs(CRS_PROJETADO)
    total_focos = len(gdf_focos)
    coords = [(pt.x, pt.y) for pt in gdf_focos.geometry]

    with rasterio.open(caminho_nbn_cls) as src:
        classes_nbn = [v[0] for v in src.sample(coords)]

    n_alto_nbn = sum(c in [3, 4] for c in classes_nbn)
    pct_nbn = (n_alto_nbn / total_focos) * 100.0

    pct_logit = 0.0
    if caminho_logit_cls and caminho_logit_cls.exists():
        with rasterio.open(caminho_logit_cls) as src:
            classes_logit = [v[0] for v in src.sample(coords)]
        n_alto_logit = sum(c in [3, 4] for c in classes_logit)
        pct_logit = (n_alto_logit / total_focos) * 100.0

    print("=" * 65)
    print("🎯 VALIDAÇÃO ESPACIAL 100m (FOCOS REAIS SOBRE A MEDIANA)")
    print("=" * 65)
    print(f"Total de focos reais validados:                   {total_focos}")
    print(f"👉 Taxa em Alto+Muito Alto (Naive Bayes 100m):     {pct_nbn:.1f}%")
    if caminho_logit_cls:
        print(f"👉 Taxa em Alto+Muito Alto (Regressão Logística):  {pct_logit:.1f}%")
    print("=" * 65)

    stats = {
        'total_focos': total_focos,
        'nbn_alto_muito_alto_pct': round(pct_nbn, 2),
        'logit_alto_muito_alto_pct': round(pct_logit, 2)
    }
    with open(OUTPUT_DIR / "validacao_espacial_100m.json", 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)
    return stats


# ==========================================
# 6. GRÁFICOS E MAPAS (LAYOUT LIVRE)
# ==========================================
def gerar_pranchas_cartograficas(mapas_anuais, prob_nbn_mediana, risco_nbn_classes, risco_logit_classes, limite_gdf, transform, width, height, val_stats):
    print("\n[PLOT] Gerando mapas em layout livre e alta resolução...")

    minx, miny, maxx, maxy = limite_gdf.total_bounds
    extent = [minx, maxx, miny, maxy]
    cmap_risco = ListedColormap(CORES_RISCO)
    norm_risco = BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5], cmap_risco.N)
    patches = [mpatches.Patch(color=CORES_RISCO[i], label=LABELS_RISCO[i]) for i in range(4)]

    # 1. Painel Panorâmico Série Anual NBN (4 linhas x 4 colunas)
    fig, axes = plt.subplots(4, 4, figsize=(16, 14), dpi=300)
    axes_flat = axes.flatten()

    for idx, ano in enumerate(ANOS):
        ax = axes_flat[idx]
        if ano in mapas_anuais:
            p_ano = mapas_anuais[ano]
            r_ano = np.zeros_like(p_ano, dtype=np.uint8)
            r_ano[(p_ano > 0) & (p_ano < 0.25)] = 1
            r_ano[(p_ano >= 0.25) & (p_ano < 0.50)] = 2
            r_ano[(p_ano >= 0.50) & (p_ano < 0.75)] = 3
            r_ano[p_ano >= 0.75] = 4
            
            r_masked = np.ma.masked_equal(r_ano, 0)
            ax.imshow(r_masked, extent=extent, origin='upper', cmap=cmap_risco, norm=norm_risco)
            limite_gdf.boundary.plot(ax=ax, color='black', linewidth=0.6)

        ax.set_title(f"Ano {ano}", fontsize=11, fontweight='bold', pad=4)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect('equal')

    # Subplot 13: Mediana Temporal NBN + Focos de Calor
    ax_sintese = axes_flat[13]
    r_med_masked = np.ma.masked_equal(risco_nbn_classes, 0)
    ax_sintese.imshow(r_med_masked, extent=extent, origin='upper', cmap=cmap_risco, norm=norm_risco)
    limite_gdf.boundary.plot(ax=ax_sintese, color='black', linewidth=0.8)

    if FOCOS_FASE1.exists():
        gdf_focos = gpd.read_file(FOCOS_FASE1).to_crs(CRS_PROJETADO)
        gdf_focos.plot(ax=ax_sintese, color='black', markersize=6, alpha=0.8)

    ax_sintese.set_title("Mediana (2013-2025) + Focos", fontsize=11, fontweight='bold', pad=4)
    ax_sintese.set_xticks([]); ax_sintese.set_yticks([]); ax_sintese.set_aspect('equal')

    # Subplot 14: Mapa Contínuo de Probabilidade
    ax_prob = axes_flat[14]
    p_med_masked = np.ma.masked_equal(np.where(risco_nbn_classes > 0, prob_nbn_mediana, 0), 0)
    im_p = ax_prob.imshow(p_med_masked, extent=extent, origin='upper', cmap='YlOrRd')
    limite_gdf.boundary.plot(ax=ax_prob, color='black', linewidth=0.8)
    ax_prob.set_title("Probabilidade P(Fogo) Contínua", fontsize=11, fontweight='bold', pad=4)
    ax_prob.set_xticks([]); ax_prob.set_yticks([]); ax_prob.set_aspect('equal')
    cbar = plt.colorbar(im_p, ax=ax_prob, fraction=0.046, pad=0.04)
    cbar.set_label('Probabilidade', fontsize=9)

    # Subplot 15: Info & Legenda
    ax_info = axes_flat[15]
    ax_info.axis('off'); ax_info.set_xlim(0, 1); ax_info.set_ylim(0, 1)
    ax_info.annotate('N', xy=(0.5, 0.85), xytext=(0.5, 0.60),
                     arrowprops=dict(facecolor='black', edgecolor='black', width=3, headwidth=8),
                     ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax_info.plot([0.25, 0.75], [0.48, 0.48], color='black', linewidth=3)
    ax_info.text(0.5, 0.52, '10 km', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    pct_acerto = val_stats.get('nbn_alto_muito_alto_pct', 0.0)
    info_text = f"Resolução: 100m (WarpedVRT)\nAgrupamento: Mediana Anual (2013-2025)\nTaxa de Focos em Alto Risco: {pct_acerto:.1f}%\nMetodologia: Naive Bayes Network"
    ax_info.text(0.5, 0.15, info_text, ha='center', va='bottom', fontsize=8.5, color='#222222', multialignment='center')

    fig.legend(handles=patches, loc='lower center', ncol=4, fontsize=9.5, frameon=True, bbox_to_anchor=(0.5, 0.01))
    fig.suptitle('Zonamento do Risco de Incêndio Florestal por Rede Naive Bayes (100m - 2013-2025)\nSão José dos Pinhais - PR',
                 fontsize=14, fontweight='bold', y=0.98)
    plt.subplots_adjust(left=0.03, right=0.97, top=0.93, bottom=0.05, wspace=0.12, hspace=0.18)

    out_png_nbn = OUTPUT_DIR / "painel_zonamento_risco_nbn_100m_mediana.png"
    plt.savefig(out_png_nbn, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Painel de Zonamento NBN 100m salvo: {out_png_nbn.name}")

    # 2. Painel Comparativo Lado a Lado (Layout Widescreen Livre)
    if risco_logit_classes is not None:
        fig_comp, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), dpi=300)
        
        ax1.imshow(r_med_masked, extent=extent, origin='upper', cmap=cmap_risco, norm=norm_risco)
        limite_gdf.boundary.plot(ax=ax1, color='black', linewidth=0.8)
        if FOCOS_FASE1.exists():
            gdf_focos.plot(ax=ax1, color='black', markersize=6, alpha=0.8)
        ax1.set_title(f"(A) Rede Naive Bayes (100m)\nTaxa de Focos em Alto Risco: {val_stats.get('nbn_alto_muito_alto_pct',0):.1f}%", fontsize=12, fontweight='bold', pad=8)
        ax1.set_xticks([]); ax1.set_yticks([]); ax1.set_aspect('equal')

        r_logit_masked = np.ma.masked_equal(risco_logit_classes, 0)
        ax2.imshow(r_logit_masked, extent=extent, origin='upper', cmap=cmap_risco, norm=norm_risco)
        limite_gdf.boundary.plot(ax=ax2, color='black', linewidth=0.8)
        if FOCOS_FASE1.exists():
            gdf_focos.plot(ax=ax2, color='black', markersize=6, alpha=0.8)
        ax2.set_title(f"(B) Regressão Logística Contínua (100m)\nTaxa de Focos em Alto Risco: {val_stats.get('logit_alto_muito_alto_pct',0):.1f}%", fontsize=12, fontweight='bold', pad=8)
        ax2.set_xticks([]); ax2.set_yticks([]); ax2.set_aspect('equal')

        fig_comp.legend(handles=patches, loc='lower center', ncol=4, fontsize=9.5, frameon=True, bbox_to_anchor=(0.5, 0.03))
        fig_comp.suptitle('Comparação de Modelos de Zonamento de Risco em Alta Resolução (100m - Mediana Temporal)\nSão José dos Pinhais - PR', fontsize=13, fontweight='bold', y=0.98)
        plt.subplots_adjust(left=0.04, right=0.96, top=0.88, bottom=0.12, wspace=0.15)

        out_png_comp = OUTPUT_DIR / "painel_comparativo_nbn_vs_logit_100m.png"
        plt.savefig(out_png_comp, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Painel Comparativo (NBN vs Logit 100m) salvo: {out_png_comp.name}")


# ==========================================
# MAIN
# ==========================================
def main():
    processar_mapeamento_zoning()


if __name__ == "__main__":
    main()
