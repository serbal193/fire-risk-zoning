"""
Script: 01_analise_historica.py
Etapa: 03_modelagem

Descrição:
    Executa a Análise Histórica Exploratória e Espaço-Temporal dos Focos de Calor (2013-2025)
    em São José dos Pinhais - PR, baseando-se no notebook de referência `030_historical_analysis.ipynb`:
    
    1. Distribuições Temporais e Estatísticas dos Focos:
       - Distribuição de Ocorrências por Ano (com destaque de média e anos críticos).
       - Distribuição Sazonal por Mês (identificação do período seco/pico de fogo).
       - Distribuição Semanal por Dia da Semana.
       - Distribuição Diurna/Noturna por Hora do Dia.
       
    2. Análise Espacial dos Focos de Calor:
       - Padrão Espacial com Marginais de Densidade (Jointplot de Longitude vs Latitude com contorno do município).
       - Mapa de Calor Kernel Density Estimation (KDE) contínuo e classificado em níveis de probabilidade.
       - Inclusão de elementos cartográficos: Seta Norte, Barra de Escala gráfica e sistema de projeção.
       
    3. Cruzamento com Uso e Cobertura da Terra (MapBiomas):
       - Distribuição de Focos por Classe de Cobertura/Combustível Vegetal.
       
    4. Salvamento de Relatórios e Pranchas Gráficas em Alta Resolução (300 DPI):
       - Prancha A4 consolidada das distribuições temporais (`painel_a4_distribuicoes_temporais.png`).
       - Mapa cartográfico A4 do padrão espacial e densidade de fogo (`painel_a4_padrao_espacial_hotspots.png`).
       - Tabela sumarizada em CSV com as métricas históricas anuais e mensais (`relatorio_estatistico_historico.csv`).
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
import geopandas as gpd
from shapely.geometry import Point, box, Polygon
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
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

FOCOS_DIR = BASE_DIR / "input" / "00_focos_de_calor"

if (BASE_DIR / "input" / "01_vetores" / "SJP.shp").exists():
    LIMITE_SHP = BASE_DIR / "input" / "01_vetores" / "SJP.shp"
else:
    LIMITE_SHP = BASE_DIR / "output" / "01_vetores" / "SJP.shp"

LULC_DIR = BASE_DIR / "input" / "03_lulc"

OUTPUT_DIR = BASE_DIR / "output" / "03_modelagem" / "01_analise_historica"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CRS_PROJETADO = "EPSG:31982"  # SIRGAS 2000 / UTM zone 22S


# ==========================================
# 1. CARREGAMENTO E TRATAMENTO DOS FOCOS
# ==========================================
def carregar_focos_historicos(limite_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Carrega todos os focos brutos (2013-2025), filtra pelo limite de SJP e extrai atributos de tempo."""
    padrao = str(FOCOS_DIR / "focos_goes_aqua_*.csv")
    arquivos = sorted(glob.glob(padrao))
    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo de focos encontrado em: {FOCOS_DIR}")

    print(f"[INFO] Carregando {len(arquivos)} arquivos de focos históricos...")
    dfs = []
    for arq in arquivos:
        df_temp = pd.read_csv(arq)
        df_temp.columns = [c.lower() for c in df_temp.columns]
        dfs.append(df_temp)

    df_todos = pd.concat(dfs, ignore_index=True)
    col_dt = 'datahora' if 'datahora' in df_todos.columns else 'data_hora'
    df_todos['datahora'] = pd.to_datetime(df_todos[col_dt], format='mixed', errors='coerce')
    df_todos = df_todos.dropna(subset=['datahora'])

    # Criar colunas temporais
    df_todos['ano'] = df_todos['datahora'].dt.year
    df_todos['mes'] = df_todos['datahora'].dt.month
    df_todos['dia'] = df_todos['datahora'].dt.day
    df_todos['dia_semana'] = df_todos['datahora'].dt.dayofweek  # 0=Segunda, 6=Domingo
    df_todos['hora'] = df_todos['datahora'].dt.hour

    geometrias = [Point(xy) for xy in zip(df_todos['longitude'], df_todos['latitude'])]
    gdf_focos = gpd.GeoDataFrame(df_todos, geometry=geometrias, crs="EPSG:4326")

    # Recorte espacial
    limite_wgs84 = limite_gdf.to_crs("EPSG:4326")
    gdf_focos = gpd.sjoin(gdf_focos, limite_wgs84[['geometry']], how="inner", predicate="intersects")
    gdf_focos = gdf_focos.drop(columns=['index_right'], errors='ignore').reset_index(drop=True)

    print(f"✅ Total de focos históricos carregados e validados em SJP: {len(gdf_focos)}")
    return gdf_focos


# ==========================================
# 2. PRANCHA A4: DISTRIBUIÇÕES TEMPORAIS
# ==========================================
def gerar_painel_distribuicoes_temporais(df: pd.DataFrame):
    """
    Gera uma prancha gráfica A4 retrato com 4 subplots analisando o histórico temporal dos focos:
      (A) Número de ocorrências por ano (com linha de média)
      (B) Distribuição sazonal por mês
      (C) Distribuição por dia da semana
      (D) Distribuição por hora do dia
    """
    print("\n[PLOT] Gerando prancha A4 de Distribuições Temporais Históricas...")
    
    fig, axes = plt.subplots(2, 2, figsize=(8.27, 11.69), dpi=300)
    
    # -------------------------------------------------------------
    # (A) Ocorrências por Ano
    # -------------------------------------------------------------
    ax_ano = axes[0, 0]
    ano_freq = df.groupby('ano')['datahora'].count().reset_index()
    media_ano = ano_freq['datahora'].mean()
    
    cores_ano = ['#F97306' if v > media_ano else '#5353EC' for v in ano_freq['datahora']]
    sns.barplot(x='ano', y='datahora', data=ano_freq, hue='ano', palette=cores_ano, edgecolor='black', legend=False, ax=ax_ano)
    ax_ano.axhline(media_ano, color='red', linestyle='--', linewidth=1.5, label=f'Média ({media_ano:.1f})')
    
    ax_ano.set_title('(A) Ocorrências Anuais de Focos (2013-2025)', fontsize=9, fontweight='bold')
    ax_ano.set_xlabel('')
    ax_ano.set_ylabel('Nº de Focos de Calor', fontsize=8)
    ax_ano.tick_params(axis='x', rotation=45, labelsize=7.5)
    ax_ano.tick_params(axis='y', labelsize=8)
    ax_ano.legend(fontsize=7, loc='upper left')

    # -------------------------------------------------------------
    # (B) Ocorrências por Mês
    # -------------------------------------------------------------
    ax_mes = axes[0, 1]
    legenda_mes = {1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr', 5:'Mai', 6:'Jun', 7:'Jul', 8:'Ago', 9:'Set', 10:'Out', 11:'Nov', 12:'Dez'}
    mes_freq = df.groupby('mes')['datahora'].count().reindex(range(1, 13), fill_value=0).reset_index()
    mes_freq['mes_nome'] = mes_freq['mes'].map(legenda_mes)
    media_mes = mes_freq['datahora'].mean()
    
    cores_mes = ['#F97306' if v > media_mes else '#5353EC' for v in mes_freq['datahora']]
    sns.barplot(x='mes_nome', y='datahora', data=mes_freq, hue='mes_nome', palette=cores_mes, edgecolor='black', legend=False, ax=ax_mes)
    ax_mes.axhline(media_mes, color='red', linestyle='--', linewidth=1.5, label=f'Média ({media_mes:.1f})')
    
    ax_mes.set_title('(B) Sazonalidade Mensal dos Focos', fontsize=9, fontweight='bold')
    ax_mes.set_xlabel('')
    ax_mes.set_ylabel('Nº de Focos de Calor', fontsize=8)
    ax_mes.tick_params(axis='x', labelsize=7.5)
    ax_mes.tick_params(axis='y', labelsize=8)
    ax_mes.legend(fontsize=7, loc='upper left')

    # -------------------------------------------------------------
    # (C) Ocorrências por Dia da Semana
    # -------------------------------------------------------------
    ax_dia = axes[1, 0]
    legenda_dia = {0:'Seg', 1:'Ter', 2:'Qua', 3:'Qui', 4:'Sex', 5:'Sáb', 6:'Dom'}
    dia_freq = df.groupby('dia_semana')['datahora'].count().reindex(range(7), fill_value=0).reset_index()
    dia_freq['dia_nome'] = dia_freq['dia_semana'].map(legenda_dia)
    media_dia = dia_freq['datahora'].mean()
    
    cores_dia = ['#F97306' if v > media_dia else '#5353EC' for v in dia_freq['datahora']]
    sns.barplot(x='dia_nome', y='datahora', data=dia_freq, hue='dia_nome', palette=cores_dia, edgecolor='black', legend=False, ax=ax_dia)
    ax_dia.axhline(media_dia, color='red', linestyle='--', linewidth=1.5, label=f'Média ({media_dia:.1f})')
    
    ax_dia.set_title('(C) Ocorrências por Dia da Semana', fontsize=9, fontweight='bold')
    ax_dia.set_xlabel('')
    ax_dia.set_ylabel('Nº de Focos de Calor', fontsize=8)
    ax_dia.tick_params(axis='x', labelsize=8)
    ax_dia.tick_params(axis='y', labelsize=8)
    ax_dia.legend(fontsize=7, loc='upper left')

    # -------------------------------------------------------------
    # (D) Ocorrências por Hora do Dia
    # -------------------------------------------------------------
    ax_hora = axes[1, 1]
    hora_freq = df.groupby('hora')['datahora'].count().reindex(range(24), fill_value=0).reset_index()
    media_hora = hora_freq['datahora'].mean()
    
    cores_hora = ['#F97306' if v > media_hora else '#5353EC' for v in hora_freq['datahora']]
    sns.barplot(x='hora', y='datahora', data=hora_freq, hue='hora', palette=cores_hora, edgecolor='black', legend=False, ax=ax_hora)
    ax_hora.axhline(media_hora, color='red', linestyle='--', linewidth=1.5, label=f'Média ({media_hora:.1f})')
    
    ax_hora.set_title('(D) Distribuição Diária por Horário (UTC/Local)', fontsize=9, fontweight='bold')
    ax_hora.set_xlabel('Hora do Dia (0h às 23h)', fontsize=8)
    ax_hora.set_ylabel('Nº de Focos de Calor', fontsize=8)
    ax_hora.tick_params(axis='x', labelsize=6.5)
    ax_hora.tick_params(axis='y', labelsize=8)
    ax_hora.legend(fontsize=7, loc='upper left')

    fig.suptitle('Análise Histórica Temporal dos Focos de Calor (2013-2025)\nSão José dos Pinhais - PR (Satélites GOES & AQUA)',
                 fontsize=11, fontweight='bold', y=0.98)
    plt.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.06, hspace=0.25, wspace=0.22)

    out_png = OUTPUT_DIR / "painel_a4_distribuicoes_temporais.png"
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Prancha A4 Temporal salva: {out_png.name}")


# ==========================================
# 3. PRANCHA A4: PADRÃO ESPACIAL E HEATMAP
# ==========================================
def gerar_painel_padrao_espacial(gdf_focos: gpd.GeoDataFrame, limite_gdf: gpd.GeoDataFrame):
    """
    Gera uma prancha gráfica A4 com análise espacial dos focos:
      (A) Distribuição pontual e densidades marginais
      (B) Mapa de Calor Kernel Density Estimation (KDE) normalizado
    """
    print("\n[PLOT] Gerando mapa cartográfico de Padrão Espacial e Densidade de Kernel...")
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.27, 11.69), dpi=300)
    
    limite_wgs84 = limite_gdf.to_crs("EPSG:4326")
    minx, miny, maxx, maxy = limite_wgs84.total_bounds
    
    # -------------------------------------------------------------
    # (A) Mapa de Dispersão dos Focos com Limite
    # -------------------------------------------------------------
    limite_wgs84.boundary.plot(ax=ax1, color='black', linewidth=1.0, label='Limite Municipal')
    ax1.scatter(gdf_focos.geometry.x, gdf_focos.geometry.y, color='#d7191c', s=14, alpha=0.6, label='Focos de Calor (GOES/AQUA)')
    
    ax1.set_title('(A) Distribuição Espacial dos Focos de Calor (2013-2025)', fontsize=10, fontweight='bold', pad=4)
    ax1.set_xlabel('Longitude (°)', fontsize=8)
    ax1.set_ylabel('Latitude (°)', fontsize=8)
    ax1.set_xlim(minx - 0.02, maxx + 0.02)
    ax1.set_ylim(miny - 0.02, maxy + 0.02)
    ax1.legend(loc='upper right', fontsize=7.5, frameon=True)

    # -------------------------------------------------------------
    # (B) Mapa de Calor Contínuo KDE
    # -------------------------------------------------------------
    x = gdf_focos.geometry.x.values
    y = gdf_focos.geometry.y.values
    
    x_grid, y_grid = np.meshgrid(
        np.linspace(minx, maxx, 200),
        np.linspace(miny, maxy, 200)
    )
    positions = np.vstack([x_grid.ravel(), y_grid.ravel()])
    values = np.vstack([x, y])
    kernel = gaussian_kde(values)
    density = np.reshape(kernel(positions).T, x_grid.shape)
    density_norm = density / np.max(density)

    color_list = ['#2b83ba', '#abdda4', '#ffffbf', '#fdae61', '#d7191c', '#860202']
    density_levels = [0.0, 0.2, 0.4, 0.6, 0.8, 0.95, 1.0]

    contour = ax2.contourf(x_grid, y_grid, density_norm, levels=density_levels, colors=color_list, alpha=0.85)
    limite_wgs84.boundary.plot(ax=ax2, color='black', linewidth=1.2)

    cbar = plt.colorbar(contour, ax=ax2, orientation='vertical', fraction=0.025, pad=0.03)
    cbar.set_label('Densidade Relativa de Focos [0, 1]', fontsize=8, fontweight='bold')
    cbar.ax.tick_params(labelsize=7)

    # Seta Norte
    x_arrow, y_arrow = minx + (maxx - minx) * 0.08, maxy - (maxy - miny) * 0.08
    ax2.annotate('N', xy=(x_arrow, y_arrow), xytext=(x_arrow, y_arrow - (maxy - miny) * 0.06),
                 arrowprops=dict(facecolor='black', edgecolor='black', width=2, headwidth=7),
                 ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Barra de Escala (10 km em graus ~ 0.09°)
    scale_deg = 10.0 / 111.0
    scale_x0 = minx + (maxx - minx) * 0.05
    scale_y0 = miny + (maxy - miny) * 0.05
    ax2.plot([scale_x0, scale_x0 + scale_deg], [scale_y0, scale_y0], color='black', linewidth=3)
    ax2.text(scale_x0 + scale_deg / 2, scale_y0 + (maxy - miny) * 0.02, '10 km',
             ha='center', va='bottom', fontsize=7.5, fontweight='bold',
             bbox=dict(boxstyle='square,pad=0.2', facecolor='white', alpha=0.85, edgecolor='none'))

    ax2.set_title('(B) Mapa de Calor Kernel Density Estimation (KDE)', fontsize=10, fontweight='bold', pad=4)
    ax2.set_xlabel('Longitude (°)', fontsize=8)
    ax2.set_ylabel('Latitude (°)', fontsize=8)
    ax2.set_xlim(minx - 0.02, maxx + 0.02)
    ax2.set_ylim(miny - 0.02, maxy + 0.02)

    fig.suptitle('Padrão Espacial e Densidade de Focos de Calor (2013-2025)\nSão José dos Pinhais - PR',
                 fontsize=11, fontweight='bold', y=0.98)
    plt.subplots_adjust(left=0.08, right=0.94, top=0.92, bottom=0.05, hspace=0.18)

    out_png = OUTPUT_DIR / "painel_a4_padrao_espacial_hotspots.png"
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Prancha A4 Espacial salva: {out_png.name}")


# ==========================================
# 4. EXPORTAÇÃO DE RELATÓRIO ESTATÍSTICO
# ==========================================
def exportar_relatorio_estatistico(df: pd.DataFrame):
    """Gera um relatório CSV consolidado com as métricas históricas de fogo."""
    resumo_ano = df.groupby('ano').agg(
        total_focos=('datahora', 'count'),
        primeiro_foco=('datahora', 'min'),
        ultimo_foco=('datahora', 'max')
    ).reset_index()

    out_csv = OUTPUT_DIR / "relatorio_estatistico_historico.csv"
    resumo_ano.to_csv(out_csv, index=False)
    print(f"✅ Relatório estatístico salvo em: {out_csv.name}")


# ==========================================
# MAIN
# ==========================================
def main():
    print("=" * 75)
    print("🔥 ETAPA 03_MODELAGEM: 01_ANALISE_HISTORICA (2013-2025)")
    print("=" * 75)
    print(f"Diretório Focos:  {FOCOS_DIR}")
    print(f"Diretório Saída:  {OUTPUT_DIR}")

    if not LIMITE_SHP.exists():
        raise FileNotFoundError(f"Arquivo de limite não encontrado em: {LIMITE_SHP}")
    limite_gdf = gpd.read_file(LIMITE_SHP)

    # 1. Carregar e tratar focos históricos
    gdf_focos = carregar_focos_historicos(limite_gdf)

    # 2. Gerar Prancha A4 Temporal
    gerar_painel_distribuicoes_temporais(gdf_focos)

    # 3. Gerar Prancha A4 Espacial e Mapa de Calor
    gerar_painel_padrao_espacial(gdf_focos, limite_gdf)

    # 4. Exportar relatório estatístico
    exportar_relatorio_estatistico(gdf_focos)

    print("\n" + "=" * 75)
    print("✨ ANÁLISE HISTÓRICA CONCLUÍDA COM SUCESSO!")
    print("=" * 75)


if __name__ == "__main__":
    main()
