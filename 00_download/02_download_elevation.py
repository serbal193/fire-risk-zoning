"""
Script: 02_download_elevation.py
Etapa: 00_download

Descrição:
    Baixa automaticamente o Modelo Digital de Elevação (DEM / SRTM 30m)
    para a área de estudo (São José dos Pinhais - PR).
    
    Fonte dos dados:
    - AWS Terrain Elevation / SRTM Skadi 30m público (ou mosaico das quadrículas correspondentes).
    
    Saídas:
    - input/SIG/elevation.tif (DEM recortado para a área de estudo e salvo no diretório input/SIG)
"""

import sys
import os
import gzip
import io
import urllib.request
from pathlib import Path
import numpy as np
import rasterio
from rasterio.merge import merge
from rasterio.mask import mask
import geopandas as gpd

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ==========================================
# CAMINHOS HARDCODED
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

LIMITE_SHP = BASE_DIR / "input" / "01_vetores" / "SJP.shp"
OUTPUT_DIR = BASE_DIR / "input" / "SIG"
OUTPUT_ELEVATION_TIF = OUTPUT_DIR / "elevation.tif"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def obter_quadriculas_srtm(minx: float, miny: float, maxx: float, maxy: float, margem_graus: float = 0.05) -> list[str]:
    """
    Determina os nomes das quadrículas SRTM 1x1 grau necessárias para cobrir
    toda a BBOX da área de estudo, incluindo uma margem de segurança ao redor.
    """
    lat_min = int(np.floor(miny - margem_graus))
    lat_max = int(np.floor(maxy + margem_graus))
    lon_min = int(np.floor(minx - margem_graus))
    lon_max = int(np.floor(maxx + margem_graus))

    tiles = []
    for lat in range(lat_min, lat_max + 1):
        for lon in range(lon_min, lon_max + 1):
            ns = 'S' if lat < 0 else 'N'
            ew = 'W' if lon < 0 else 'E'
            lat_str = f"{ns}{abs(lat):02d}"
            lon_str = f"{ew}{abs(lon):03d}"
            tiles.append(f"{lat_str}{lon_str}")
    return sorted(list(set(tiles)))


def baixar_tile_srtm(tile_name: str, cache_dir: Path) -> Path:
    """Baixa e descompacta uma quadrícula SRTM (HGT.GZ) da AWS."""
    lat_prefix = tile_name[:3]
    url = f"https://s3.amazonaws.com/elevation-tiles-prod/skadi/{lat_prefix}/{tile_name}.hgt.gz"
    hgt_path = cache_dir / f"{tile_name}.hgt"

    if hgt_path.exists():
        print(f"[CACHE] Quadrícula já baixada: {hgt_path.name}")
        return hgt_path

    print(f"[DOWNLOAD] Baixando carta {tile_name} de {url} ...", flush=True)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            compressed = resp.read()
        with gzip.GzipFile(fileobj=io.BytesIO(compressed)) as gz:
            data = gz.read()
        with open(hgt_path, 'wb') as f:
            f.write(data)
        print(f"[OK] Carta {tile_name} salva ({len(data)/(1024*1024):.1f} MB).")
        return hgt_path
    except Exception as e:
        raise RuntimeError(f"Falha ao baixar carta {tile_name}: {e}")


def processar_dem():
    print("=" * 75)
    print("🏔️  DOWNLOAD E PREPARAÇÃO DO MODELO DIGITAL DE ELEVAÇÃO (DEM SRTM 30m)")
    print("=" * 75)

    if not LIMITE_SHP.exists():
        raise FileNotFoundError(f"Shapefile de limite não encontrado em: {LIMITE_SHP}")

    print(f"[INFO] Carregando limite da área: {LIMITE_SHP.name}")
    limite_gdf = gpd.read_file(LIMITE_SHP).to_crs("EPSG:4326")
    minx, miny, maxx, maxy = limite_gdf.total_bounds
    print(f"[INFO] Bounding Box de SJP (WGS84): Lon [{minx:.4f}, {maxx:.4f}] | Lat [{miny:.4f}, {maxy:.4f}]")

    # Obter todas as cartas que intersectam a BBOX + margem de segurança (~5.5 km)
    margem_graus = 0.05
    tiles = obter_quadriculas_srtm(minx, miny, maxx, maxy, margem_graus=margem_graus)
    print(f"[INFO] Cartas SRTM necessárias para cobrir toda a área: {tiles}")

    cache_dir = OUTPUT_DIR / ".cache_dem"
    cache_dir.mkdir(parents=True, exist_ok=True)

    hgt_files = []
    for t in tiles:
        hgt_p = baixar_tile_srtm(t, cache_dir)
        hgt_files.append(hgt_p)

    print("\n[INFO] Realizando mosaico das cartas baixadas...")
    src_files = [rasterio.open(p) for p in hgt_files]
    mosaic_data, mosaic_transform = merge(src_files)

    for src in src_files:
        src.close()

    # Criar raster temporário em memória para recorte pela BBOX / Geometria com margem
    meta = {
        'driver': 'GTiff',
        'dtype': mosaic_data.dtype,
        'nodata': -32768,
        'width': mosaic_data.shape[2],
        'height': mosaic_data.shape[1],
        'count': 1,
        'crs': "EPSG:4326",
        'transform': mosaic_transform,
        'compress': 'lzw'
    }

    temp_mosaic = cache_dir / "mosaic_temp.tif"
    with rasterio.open(temp_mosaic, 'w', **meta) as dst:
        dst.write(mosaic_data)

    print(f"[INFO] Recortando elevação para a extensão de São José dos Pinhais (com margem de borda)...")
    with rasterio.open(temp_mosaic) as src:
        # Reprojetar para CRS métrico plano antes de aplicar o buffer (5.000 metros)
        limite_proj_buffer = limite_gdf.to_crs("EPSG:31982").geometry.buffer(5000.0).to_crs("EPSG:4326")
        limite_geom = [limite_proj_buffer.union_all()]
        out_img, out_transform = mask(src, limite_geom, crop=True)
        out_meta = src.meta.copy()
        out_meta.update({
            "height": out_img.shape[1],
            "width": out_img.shape[2],
            "transform": out_transform,
            "compress": "lzw"
        })

    with rasterio.open(OUTPUT_ELEVATION_TIF, "w", **out_meta) as dest:
        dest.write(out_img)

    if temp_mosaic.exists():
        os.remove(temp_mosaic)

    print(f"\n[SUCESSO] DEM de elevação com cobertura total salvo em: {OUTPUT_ELEVATION_TIF}")
    print("=" * 75)


if __name__ == "__main__":
    processar_dem()
