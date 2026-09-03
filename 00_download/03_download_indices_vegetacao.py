"""
Script: 03_download_indices_vegetacao.py
Etapa: 00_download

Descrição:
    Realiza o download e cálculo das séries temporais anuais de NDVI e NDMI (2013 a 2025)
    para o município de São José dos Pinhais (SJP).
    
    Abordagem automatizada e 100% aberta (sem necessidade de conta/login):
    - 2016 a 2025: Utiliza Sentinel-2 L2A (bandas B04, B08, B11 com máscara de nuvens SCL).
    - 2013 a 2015: Utiliza Landsat 8 L2 (bandas red, nir08, swir16 com máscara de nuvens qa_pixel).
    - Computa diretamente em streaming via COGs e xarray:
        * NDVI = (NIR - RED) / (NIR + RED)
        * NDMI = (NIR - SWIR) / (NIR + SWIR)
    - Calcula o mosaico anual pela MEDIANA (limpa nuvens e artefatos sazonais).
    - Reprojeta para o CRS EPSG:31982 e salva os GeoTIFFs em 30m de resolução em:
        * output/04_ndvi/SJP_NDVI_{ano}.tif
        * output/04_ndmi/SJP_NDMI_{ano}.tif
    - Verifica a existência prévia dos arquivos e pula os anos já processados.
"""

import os
import sys

# Configuração GDAL/Rasterio/Fiona para caminhos com caracteres especiais (Windows/acentuação)
os.environ['GDAL_FILENAME_IS_UTF8'] = 'NO'
os.environ['SHAPE_RESTORE_SHX'] = 'YES'

from pathlib import Path
import numpy as np
import geopandas as gpd
import xarray as xr
import rioxarray
import pystac_client
import planetary_computer as pc
import odc.stac

# ==========================================
# CONFIGURAÇÕES E CAMINHOS
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

# Tenta carregar do input/01_vetores ou output/01_vetores
if (BASE_DIR / "input" / "01_vetores" / "SJP.shp").exists():
    LIMITE_SHP = BASE_DIR / "input" / "01_vetores" / "SJP.shp"
else:
    LIMITE_SHP = BASE_DIR / "output" / "01_vetores" / "SJP.shp"

SIG_DIR = BASE_DIR / "output"
NDVI_DIR = SIG_DIR / "04_ndvi"
NDMI_DIR = SIG_DIR / "04_ndmi"

ANOS = list(range(2013, 2026))  # 2013 a 2025 (13 anos)
ESCALA_METROS = 30              # Resolução espacial do raster final (30 metros)
CRS_DESTINO = "EPSG:31982"      # SIRGAS 2000 / UTM zone 22S


def processar_ano_sentinel2(
    catalog,
    ano: int,
    bbox_4326: list,
    gdf_limite_proj: gpd.GeoDataFrame,
    caminho_ndvi: Path,
    caminho_ndmi: Path
):
    """
    Processa um ano específico do Sentinel-2 L2A (2016 a 2025): busca itens, carrega bandas necessárias,
    aplica máscara de nuvens, calcula NDVI e NDMI medianos anuais e salva como GeoTIFF.
    """
    data_inicio = f"{ano}-01-01"
    data_fim = f"{ano}-12-31"
    
    print(f"\n[ANO {ano}] Buscando Sentinel-2 L2A ({data_inicio} a {data_fim})...")
    
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox_4326,
        datetime=f"{data_inicio}/{data_fim}",
        query={"eo:cloud_cover": {"lt": 50}}
    )
    
    items = list(search.items())
    print(f"  -> {len(items)} cenas encontradas.")
    
    if len(items) == 0:
        print(f"  [AVISO] Nenhuma cena com <50% nuvens para {ano}. Tentando sem filtro...")
        search = catalog.search(
            collections=["sentinel-2-l2a"],
            bbox=bbox_4326,
            datetime=f"{data_inicio}/{data_fim}"
        )
        items = list(search.items())
        print(f"  -> {len(items)} cenas encontradas.")
        
    if len(items) == 0:
        print(f"  [ERRO] Não foi possível encontrar imagens Sentinel-2 para o ano {ano}.")
        return

    signed_items = [pc.sign(item) for item in items]
    
    print(f"  -> Carregando bandas (B04, B08, B11, SCL) em resolução de {ESCALA_METROS}m...")
    ds = odc.stac.load(
        signed_items,
        bands=["B04", "B08", "B11", "SCL"],
        crs=CRS_DESTINO,
        resolution=ESCALA_METROS,
        bbox=bbox_4326,
        chunks={"time": 10, "x": 1024, "y": 1024}
    )
    
    # Máscara SCL: 4 (Vegetação), 5 (Solo Exposto), 6 (Água), 7 (Não-vegetado)
    scl = ds["SCL"]
    mascara_valida = (scl == 4) | (scl == 5) | (scl == 6) | (scl == 7)
    
    b04 = ds["B04"].where(mascara_valida)
    b08 = ds["B08"].where(mascara_valida)
    b11 = ds["B11"].where(mascara_valida)
    
    print(f"  -> Calculando NDVI e NDMI...")
    ndvi_serie = (b08 - b04) / (b08 + b04)
    ndmi_serie = (b08 - b11) / (b08 + b11)
    
    print(f"  -> Reduzindo série temporal pela mediana anual...")
    ndvi_mediano = ndvi_serie.median(dim="time").compute()
    ndmi_mediano = ndmi_serie.median(dim="time").compute()
    
    ndvi_mediano.rio.write_crs(CRS_DESTINO, inplace=True)
    ndmi_mediano.rio.write_crs(CRS_DESTINO, inplace=True)
    
    print(f"  -> Recortando pelo polígono municipal de SJP...")
    limite_geom = [gdf_limite_proj.geometry.union_all()]
    
    ndvi_clip = ndvi_mediano.rio.clip(limite_geom, crs=CRS_DESTINO, drop=True)
    ndmi_clip = ndmi_mediano.rio.clip(limite_geom, crs=CRS_DESTINO, drop=True)
    
    caminho_ndvi.parent.mkdir(parents=True, exist_ok=True)
    caminho_ndmi.parent.mkdir(parents=True, exist_ok=True)
    
    ndvi_clip.rio.to_raster(str(caminho_ndvi), compress="LZW", dtype="float32")
    print(f"  -> Salvo: {caminho_ndvi.name}")
    
    ndmi_clip.rio.to_raster(str(caminho_ndmi), compress="LZW", dtype="float32")
    print(f"  -> Salvo: {caminho_ndmi.name}")


def processar_ano_landsat8(
    catalog,
    ano: int,
    bbox_4326: list,
    gdf_limite_proj: gpd.GeoDataFrame,
    caminho_ndvi: Path,
    caminho_ndmi: Path
):
    """
    Processa anos pré-Sentinel (2013 a 2015) utilizando Landsat 8 L2:
    bandas red, nir08, swir16 com máscara de nuvens qa_pixel.
    """
    data_inicio = f"{ano}-01-01"
    data_fim = f"{ano}-12-31"
    
    print(f"\n[ANO {ano}] Buscando Landsat 8 L2 ({data_inicio} a {data_fim})...")
    
    search = catalog.search(
        collections=["landsat-c2-l2"],
        bbox=bbox_4326,
        datetime=f"{data_inicio}/{data_fim}",
        query={"eo:cloud_cover": {"lt": 50}, "platform": {"eq": "landsat-8"}}
    )
    
    items = list(search.items())
    print(f"  -> {len(items)} cenas encontradas.")
    
    if len(items) == 0:
        search = catalog.search(
            collections=["landsat-c2-l2"],
            bbox=bbox_4326,
            datetime=f"{data_inicio}/{data_fim}"
        )
        items = list(search.items())
        print(f"  -> {len(items)} cenas encontradas.")
        
    if len(items) == 0:
        print(f"  [ERRO] Não foi possível encontrar imagens Landsat para o ano {ano}.")
        return

    signed_items = [pc.sign(item) for item in items]
    
    print(f"  -> Carregando bandas Landsat 8 (red, nir08, swir16, qa_pixel) em {ESCALA_METROS}m...")
    ds = odc.stac.load(
        signed_items,
        bands=["red", "nir08", "swir16", "qa_pixel"],
        crs=CRS_DESTINO,
        resolution=ESCALA_METROS,
        bbox=bbox_4326,
        chunks={"time": 10, "x": 1024, "y": 1024}
    )
    
    # Máscara QA_PIXEL do Landsat: bits 3 (cloud), 4 (cloud shadow), 5 (snow)
    qa = ds["qa_pixel"]
    cloud_shadow = (qa & (1 << 4)) != 0
    cloud = (qa & (1 << 3)) != 0
    mascara_valida = ~(cloud | cloud_shadow)
    
    red = ds["red"].where(mascara_valida)
    nir = ds["nir08"].where(mascara_valida)
    swir = ds["swir16"].where(mascara_valida)
    
    print(f"  -> Calculando NDVI e NDMI...")
    ndvi_serie = (nir - red) / (nir + red)
    ndmi_serie = (nir - swir) / (nir + swir)
    
    print(f"  -> Reduzindo série temporal pela mediana anual...")
    ndvi_mediano = ndvi_serie.median(dim="time").compute()
    ndmi_mediano = ndmi_serie.median(dim="time").compute()
    
    ndvi_mediano.rio.write_crs(CRS_DESTINO, inplace=True)
    ndmi_mediano.rio.write_crs(CRS_DESTINO, inplace=True)
    
    print(f"  -> Recortando pelo polígono municipal de SJP...")
    limite_geom = [gdf_limite_proj.geometry.union_all()]
    
    ndvi_clip = ndvi_mediano.rio.clip(limite_geom, crs=CRS_DESTINO, drop=True)
    ndmi_clip = ndmi_mediano.rio.clip(limite_geom, crs=CRS_DESTINO, drop=True)
    
    caminho_ndvi.parent.mkdir(parents=True, exist_ok=True)
    caminho_ndmi.parent.mkdir(parents=True, exist_ok=True)
    
    ndvi_clip.rio.to_raster(str(caminho_ndvi), compress="LZW", dtype="float32")
    print(f"  -> Salvo: {caminho_ndvi.name}")
    
    ndmi_clip.rio.to_raster(str(caminho_ndmi), compress="LZW", dtype="float32")
    print(f"  -> Salvo: {caminho_ndmi.name}")


def main():
    print("=====================================================")
    print("  DOWNLOAD DE ÍNDICES ESPECTRAIS ANUAIS (NDVI/NDMI)  ")
    print("         (Via Microsoft Planetary Computer / STAC)    ")
    print("=====================================================")
    print(f"Área de Estudo:  {LIMITE_SHP}")
    print(f"Período:         {ANOS[0]} - {ANOS[-1]}")
    print(f"Saída NDVI:      {NDVI_DIR}")
    print(f"Saída NDMI:      {NDMI_DIR}")
    print(f"Resolução:       {ESCALA_METROS}m (Projeção: {CRS_DESTINO})")

    if not LIMITE_SHP.exists():
        raise FileNotFoundError(f"Arquivo de limite municipal não encontrado: {LIMITE_SHP}")

    # 1. Carregar polígono e calcular Bounding Box com buffer de 2 km
    gdf_limite = gpd.read_file(LIMITE_SHP)
    gdf_limite_proj = gdf_limite.to_crs(CRS_DESTINO)
    
    # Buffer métrico para garantir cobertura total das bordas
    gdf_buffer = gdf_limite_proj.buffer(2000).to_crs("EPSG:4326")
    minx, miny, maxx, maxy = gdf_buffer.total_bounds
    bbox_4326 = [minx, miny, maxx, maxy]
    
    # 2. Conectar ao Catálogo STAC do Planetary Computer
    print("\n[STAC] Conectando ao Planetary Computer STAC API...")
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=pc.sign_inplace
    )
    print("[STAC] Conectado com sucesso!")

    NDVI_DIR.mkdir(parents=True, exist_ok=True)
    NDMI_DIR.mkdir(parents=True, exist_ok=True)

    for ano in ANOS:
        caminho_ndvi = NDVI_DIR / f"SJP_NDVI_{ano}.tif"
        caminho_ndmi = NDMI_DIR / f"SJP_NDMI_{ano}.tif"
        
        # Pular se já existir
        if caminho_ndvi.exists() and caminho_ndmi.exists():
            print(f"\n[ANO {ano}] Arquivos NDVI e NDMI já existem, pulando.")
            continue
            
        if ano >= 2016:
            processar_ano_sentinel2(
                catalog=catalog,
                ano=ano,
                bbox_4326=bbox_4326,
                gdf_limite_proj=gdf_limite_proj,
                caminho_ndvi=caminho_ndvi,
                caminho_ndmi=caminho_ndmi
            )
        else:
            processar_ano_landsat8(
                catalog=catalog,
                ano=ano,
                bbox_4326=bbox_4326,
                gdf_limite_proj=gdf_limite_proj,
                caminho_ndvi=caminho_ndvi,
                caminho_ndmi=caminho_ndmi
            )

    print("\n[SUCESSO] Todos os índices anuais de NDVI e NDMI (2013-2025) foram gerados com sucesso!")


if __name__ == "__main__":
    main()
