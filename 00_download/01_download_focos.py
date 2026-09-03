"""
Script: 01_download_focos.py
Etapa: 00_download

Descrição:
    Download e extração automática dos focos de calor brutos do INPE (BDQueimadas)
    para satélites GOES e AQUA (AQUA_M-T) no município de São José dos Pinhais (PR)
    ou Bounding Box / Estado do Paraná (2015–2025).

    Substitui e padroniza os dados na pasta 'input/00_focos_de_calor/'.

Satélites suportados:
    - GOES (GOES-16, GOES-13, GOES-12)
    - AQUA (AQUA_M-T / AQUA_M-N / MODIS)
"""

import sys
import io
import ssl
import zipfile
import urllib.request
import os
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Configuração GDAL/Rasterio/Fiona para caminhos com caracteres especiais (Windows/acentuação)
os.environ['GDAL_FILENAME_IS_UTF8'] = 'NO'
os.environ['SHAPE_RESTORE_SHX'] = 'YES'

# Ajusta stdout para UTF-8 no Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ==========================================
# CAMINHOS HARDCODED
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_FOCOS_DIR = BASE_DIR / "input" / "00_focos_de_calor"
LIMITE_SHP = BASE_DIR / "input" / "01_vetores" / "SJP.shp"

OUTPUT_FOCOS_DIR.mkdir(parents=True, exist_ok=True)

INPE_ZIP_URL_PATTERN = "https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/anual/Brasil_todos_sats/focos_br_todos-sats_{year}.zip"
TARGET_YEARS = list(range(2013, 2026))  # 2013 a 2025 (13 anos)

# Satélites alvo: GOES e AQUA
SATELITES_ALVO = ['GOES', 'AQUA']


def download_e_filtrar_focos_inpe():
    """
    Baixa os arquivos anuais compactados de todos os satélites do INPE,
    filtra para o Paraná / São José dos Pinhais e para os satélites GOES e AQUA,
    salvando os CSVs padronizados diretamente em input/00_focos_de_calor.
    Pula anos que já possuem arquivo baixado.
    """
    print("=" * 80)
    print(f"🔥 DOWNLOAD DE FOCOS DE CALOR INPE (GOES & AQUA) - {TARGET_YEARS[0]} a {TARGET_YEARS[-1]}")
    print("=" * 80)
    print(f"Destino dos dados: {OUTPUT_FOCOS_DIR}")
    print(f"Satélites alvo:    {', '.join(SATELITES_ALVO)}")

    # Carregar limite se disponível para recorte rigoroso ou BBOX
    limite_gdf = None
    if LIMITE_SHP.exists():
        print(f"Carregando shapefile de limite: {LIMITE_SHP.name}")
        limite_gdf = gpd.read_file(LIMITE_SHP).to_crs("EPSG:4326")
        minx, miny, maxx, maxy = limite_gdf.total_bounds
        # Margem de segurança ao redor do município
        bbox_filtro = (minx - 0.05, miny - 0.05, maxx + 0.05, maxy + 0.05)
    else:
        # Bounding Box aproximada do Paraná se não houver shapefile
        bbox_filtro = (-55.0, -27.5, -47.5, -21.5)

    ctx = ssl._create_unverified_context()
    total_geral = 0

    for year in TARGET_YEARS:
        out_csv = OUTPUT_FOCOS_DIR / f"focos_goes_aqua_{year}.csv"
        
        if out_csv.exists():
            df_existente = pd.read_csv(out_csv)
            print(f"\n[ANO {year}] Arquivo já existe ({len(df_existente)} focos): {out_csv.name} (PULANDO)")
            total_geral += len(df_existente)
            continue
            
        url = INPE_ZIP_URL_PATTERN.format(year=year)

        print(f"\n[ANO {year}] Baixando {url} ...", flush=True)

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx, timeout=180) as resp:
                zip_bytes = resp.read()

            tamanho_mb = len(zip_bytes) / (1024 * 1024)
            print(f" -> Download concluído ({tamanho_mb:.1f} MB). Extraindo e filtrando...", flush=True)

            with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
                csv_files = [f for f in z.namelist() if f.endswith('.csv')]
                if not csv_files:
                    print(f"❌ Nenhum CSV encontrado no ZIP de {year}!")
                    continue

                with z.open(csv_files[0]) as f_in:
                    df_raw = pd.read_csv(f_in, dtype=str, low_memory=False)

            # Normalizar nomes de colunas
            df_raw.columns = [c.lower().strip() for c in df_raw.columns]

            # 1. Filtro espacial: Bounding Box e/ou Município/Estado
            lats = pd.to_numeric(df_raw['latitude'].astype(str).str.replace(',', '.'), errors='coerce')
            lons = pd.to_numeric(df_raw['longitude'].astype(str).str.replace(',', '.'), errors='coerce')

            mask_spatial = (
                (lons >= bbox_filtro[0]) & (lons <= bbox_filtro[2]) &
                (lats >= bbox_filtro[1]) & (lats <= bbox_filtro[3])
            )

            # Também verificar nome do município / estado se disponível
            if 'municipio' in df_raw.columns:
                mask_muni = df_raw['municipio'].astype(str).str.upper().str.contains('S.*O JOS.* DOS PINHAIS|PINHAIS', regex=True, na=False)
                mask_spatial = mask_spatial | mask_muni

            df_filtrado = df_raw[mask_spatial].copy()
            df_filtrado['latitude'] = lats[mask_spatial]
            df_filtrado['longitude'] = lons[mask_spatial]

            # 2. Filtro de Satélites: GOES e AQUA
            if 'satelite' in df_filtrado.columns:
                mask_sat = df_filtrado['satelite'].astype(str).str.upper().str.contains('GOES|AQUA', regex=True, na=False)
                df_filtrado = df_filtrado[mask_sat].copy()

            # 3. Recorte exato pelo polígono (se shapefile disponível)
            if limite_gdf is not None and not df_filtrado.empty:
                geoms = [Point(xy) for xy in zip(df_filtrado['longitude'], df_filtrado['latitude'])]
                gdf_temp = gpd.GeoDataFrame(df_filtrado, geometry=geoms, crs="EPSG:4326")
                gdf_temp = gpd.sjoin(gdf_temp, limite_gdf[['geometry']], how="inner", predicate="intersects")
                df_filtrado = pd.DataFrame(gdf_temp.drop(columns=['geometry', 'index_right'], errors='ignore'))

            # Padronizar coluna de data
            date_col = 'datahora' if 'datahora' in df_filtrado.columns else ('data_pas' if 'data_pas' in df_filtrado.columns else 'data_hora_gmt')
            if date_col in df_filtrado.columns:
                df_filtrado['datahora'] = pd.to_datetime(df_filtrado[date_col].astype(str), format='mixed', errors='coerce')
                df_filtrado = df_filtrado.dropna(subset=['datahora'])

            # Salvar CSV anual padronizado
            cols_export = ['datahora', 'satelite', 'pais', 'estado', 'municipio', 'bioma',
                           'diasemchuva', 'precipitacao', 'riscofogo', 'frp', 'latitude', 'longitude']
            cols_finais = [c for c in cols_export if c in df_filtrado.columns]

            df_filtrado = df_filtrado[cols_finais].sort_values(by='datahora').reset_index(drop=True)
            df_filtrado.to_csv(out_csv, index=False, encoding='utf-8')

            total_ano = len(df_filtrado)
            total_geral += total_ano
            sats_encontrados = df_filtrado['satelite'].value_counts().to_dict() if 'satelite' in df_filtrado.columns else {}

            print(f"✅ Ano {year}: {total_ano} focos salvos ({sats_encontrados}) -> {out_csv.name}")

        except Exception as e:
            print(f"❌ Erro no download/processamento do ano {year}: {e}")

    print("\n" + "=" * 80)
    print(f"✨ DOWNLOAD CONCLUÍDO! Total de focos (GOES + AQUA): {total_geral} registros.")
    print(f"Arquivos salvos em: {OUTPUT_FOCOS_DIR}")
    print("=" * 80)


if __name__ == "__main__":
    download_e_filtrar_focos_inpe()
