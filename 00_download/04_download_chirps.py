"""
Script: 04_download_chirps.py
Etapa: 00_download

Descrição:
    Download automatizado dos dados de precipitação mensal CHIRPS v2.0 (Climate Hazards Center - UCSB)
    para a série temporal de 2013 a 2025.
    
    Características:
    - Salva os arquivos anuais no formato NetCDF com padrão oficial:
        `input/02_precipitacao/chirps-v2.0.{ano}.monthly.nc`
    - Estrutura de dados idêntica aos arquivos NetCDF existentes:
        * Dimensões: time (12 meses), latitude (2000), longitude (7200)
        * Variável de dados: precip (float32) em mm/mês
        * Resolução global de 0.05° (~5.5 km)
    - Verificação inteligente: se o arquivo `chirps-v2.0.{ano}.monthly.nc` já existir, pula o download.
    - Suporta download direto dos arquivos .tif.gz mensais do servidor UCSB CHC compilados em NetCDF anual.
"""

import os
import sys

# Configuração GDAL/Rasterio/Fiona para caminhos com caracteres especiais (Windows/acentuação)
os.environ['GDAL_FILENAME_IS_UTF8'] = 'NO'
os.environ['SHAPE_RESTORE_SHX'] = 'YES'

import ssl
import gzip
import io
import urllib.request
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import rasterio
from rasterio.io import MemoryFile
from tqdm import tqdm

# ==========================================
# CONFIGURAÇÕES E CAMINHOS
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_CHIRPS_DIR = BASE_DIR / "input" / "02_precipitacao"
OUTPUT_CHIRPS_DIR.mkdir(parents=True, exist_ok=True)

ANOS = list(range(2013, 2026))  # 2013 a 2025 (13 anos)
CHIRPS_TIF_GZ_URL = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/tifs/chirps-v2.0.{ano}.{mes:02d}.tif.gz"


def baixar_e_gerar_netcdf_ano(ano: int, caminho_saida_nc: Path):
    """
    Baixa os 12 meses do CHIRPS v2.0 para um ano, descompacta em memória e compila
    em um arquivo NetCDF anual padronizado com dimensões (time: 12, latitude: 2000, longitude: 7200).
    """
    print(f"\n[ANO {ano}] Baixando e compilando CHIRPS mensal (12 meses)...")
    
    ctx = ssl._create_unverified_context()
    meses_arrays = []
    latitudes = None
    longitudes = None
    
    for mes in range(1, 13):
        url = CHIRPS_TIF_GZ_URL.format(ano=ano, mes=mes)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
                gz_bytes = resp.read()
            
            decomp_bytes = gzip.decompress(gz_bytes)
            with MemoryFile(decomp_bytes) as memfile:
                with memfile.open() as src:
                    arr = src.read(1).astype(np.float32)
                    nodata_val = src.nodata
                    if nodata_val is not None:
                        arr[arr == nodata_val] = np.nan
                    
                    if latitudes is None or longitudes is None:
                        bounds = src.bounds
                        height, width = src.shape
                        # Coordenadas do centro do pixel correspondentes ao NetCDF oficial
                        latitudes = np.linspace(bounds.bottom + (bounds.top - bounds.bottom)/(2*height),
                                                bounds.top - (bounds.top - bounds.bottom)/(2*height),
                                                height, dtype=np.float32)
                        longitudes = np.linspace(bounds.left + (bounds.right - bounds.left)/(2*width),
                                                 bounds.right - (bounds.right - bounds.left)/(2*width),
                                                 width, dtype=np.float32)
                        
                        # Inverter latitudes para que fiquem de sul para norte (-49.975 a 49.975) conforme padrão
                        if latitudes[0] > latitudes[-1]:
                            latitudes = latitudes[::-1]
                            arr = np.flipud(arr)
                    else:
                        # Se latitudes estiverem invertidas, inverte o array também
                        arr = np.flipud(arr)
                        
                    meses_arrays.append(arr)
                    print(f"  -> Mês {mes:02d}/{ano} baixado com sucesso.")
        except Exception as e:
            raise RuntimeError(f"Falha ao baixar/processar mês {mes:02d}/{ano} de {url}: {e}")
            
    # Criar array 3D: (time: 12, latitude: 2000, longitude: 7200)
    precip_3d = np.stack(meses_arrays, axis=0)
    datas_meses = pd.date_range(start=f"{ano}-01-01", periods=12, freq='MS')
    
    ds = xr.Dataset(
        data_vars={
            'precip': (('time', 'latitude', 'longitude'), precip_3d)
        },
        coords={
            'time': datas_meses,
            'latitude': latitudes,
            'longitude': longitudes
        },
        attrs={
            'title': 'CHIRPS Version 2.0',
            'history': f'Created by Climate Hazards Center - UCSB / Auto-downloader for fire-risk-zoning',
            'version': 'Version 2.0',
            'comments': 'time variable denotes the first day of the given month.'
        }
    )
    
    # Salvar NetCDF com compressão LZW/zlib
    encoding = {
        'precip': {'zlib': True, 'complevel': 4, 'dtype': 'float32'}
    }
    
    caminho_saida_nc.parent.mkdir(parents=True, exist_ok=True)
    ds.to_netcdf(str(caminho_saida_nc), encoding=encoding)
    tamanho_mb = caminho_saida_nc.stat().st_size / (1024 * 1024)
    print(f"✅ Salvo: {caminho_saida_nc.name} ({tamanho_mb:.1f} MB)")


def main():
    print("=====================================================")
    print("   DOWNLOAD DE PRECIPITAÇÃO MENSAL CHIRPS (NETCDF)   ")
    print("=====================================================")
    print(f"Destino:         {OUTPUT_CHIRPS_DIR}")
    print(f"Período:         {ANOS[0]} a {ANOS[-1]} ({len(ANOS)} anos)")
    print(f"Resolução:       0.05° (~5.5 km)")

    for ano in ANOS:
        caminho_nc = OUTPUT_CHIRPS_DIR / f"chirps-v2.0.{ano}.monthly.nc"
        
        # Pula se o arquivo já existir
        if caminho_nc.exists():
            tamanho_mb = caminho_nc.stat().st_size / (1024 * 1024)
            print(f"\n[ANO {ano}] Arquivo já existe: {caminho_nc.name} ({tamanho_mb:.1f} MB) -> PULANDO")
            continue
            
        baixar_e_gerar_netcdf_ano(ano, caminho_nc)

    print("\n" + "=" * 80)
    print("✨ DOWNLOAD E PROCESSAMENTO DO CHIRPS CONCLUÍDOS!")
    print(f"Todos os arquivos NetCDF estão salvos em: {OUTPUT_CHIRPS_DIR}")
    print("=" * 80)


if __name__ == "__main__":
    main()
