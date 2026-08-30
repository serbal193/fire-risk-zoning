"""
Script: 04_treinar_regressao_logistica_pca.py
Etapa: 03_modelagem

Descrição:
    Executa:
    1. Análise de Componentes Principais (PCA) sobre as variáveis contínuas padronizadas:
       - Avaliação da contribuição relativa de cada variável na 1ª Componente Principal (PC1)
         calculada como: Contrib_i (%) = (loading_i^2 / sum(loading^2)) * 100
       - Comparação com o limiar de corte teórico de contribuição uniforme: 1/p (ex: 1/15 ou 1/n_vars)
       - Seleção das variáveis preditoras cujo peso em PC1 supera a linha de corte.
       - Geração dos gráficos de diagnóstico da PCA:
         * Gráfico de barras da contribuição na PC1 com linha de corte tracejada.
         * Biplot da PCA (PC1 vs PC2) com projeção dos pontos de Fogo/Não-Fogo e vetores das variáveis.
    
    2. Treinamento e Validação da Regressão Logística:
       - Ajuste com regularização e balanceamento de classes nos dados de treino (70%).
       - Avaliação no conjunto independente de teste/validação (30%).
       - Cálculo de métricas completas: Acurácia (Pa), Recall/POD, Precisão (Pp), FAR, POFD, CSI/TS, HSS, PSS, F1, F3 e AUC-ROC.
       
    3. Saídas em output/03_modelagem/04_regressao_logistica:
       - Gráfico de Contribuição PC1 com linha de corte (`pca_contribuicao_pc1.png`)
       - Biplot da PCA (`pca_biplot_pc1_pc2.png`)
       - Prancha A4 consolidada (`painel_a4_regressao_logistica_pca.png`)
       - CSVs e JSON com coeficientes e métricas.
"""

import sys
import os
import json
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score, recall_score,
    f1_score, fbeta_score, roc_curve, roc_auc_score
)

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ==========================================
# CAMINHOS E CONFIGURAÇÕES
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

AMOSTRAS_DIR = BASE_DIR / "output" / "01_processar_hotspots"
CSV_ANUAL = AMOSTRAS_DIR / "grade_1km_amostras_anuais.csv"
CSV_TREINO = AMOSTRAS_DIR / "grade_1km_amostras_treino.csv"
CSV_VALIDACAO = AMOSTRAS_DIR / "grade_1km_amostras_validacao.csv"

OUTPUT_DIR = BASE_DIR / "output" / "03_modelagem" / "04_regressao_logistica"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Lista completa de variáveis contínuas físicas extraídas para a área de estudo
FEATURES_CONTINUAS = [
    'elevation_m',
    'slope_deg',
    'aspect_deg',
    'ndvi_valor',
    'ndmi_valor',
    'spi_anual',
    'dist_estradas_m',
    'dist_urbano_m'
]

DIC_NOMES_LEGIVEIS = {
    'elevation_m': 'Elevação (m)',
    'slope_deg': 'Declividade (°)',
    'aspect_deg': 'Orientação Aspect (°)',
    'ndvi_valor': 'NDVI (Biomassa)',
    'ndmi_valor': 'NDMI (Umidade)',
    'spi_anual': 'SPI (Seca Anual)',
    'dist_estradas_m': 'Dist. Estradas (m)',
    'dist_urbano_m': 'Dist. Urbano (m)'
}


# ==========================================
# 1. ANÁLISE DE COMPONENTES PRINCIPAIS (PCA)
# ==========================================
def executar_pca_e_selecao(df_treino: pd.DataFrame):
    """
    Executa a PCA sobre as variáveis contínuas padronizadas, calcula a contribuição
    percentual de cada variável na PC1, compara com a linha de corte (1/15 ou 1/p)
    e plota o gráfico de barras e o Biplot.
    """
    print("\n" + "=" * 70)
    print("🔬 1. ANÁLISE DE COMPONENTES PRINCIPAIS (PCA) & SELEÇÃO DE VARIÁVEIS")
    print("=" * 70)

    X_raw = df_treino[FEATURES_CONTINUAS].copy()
    y_raw = df_treino['incendio'].values

    # Imputação de possíveis valores nulos com a mediana e Padronização (Z-score)
    from sklearn.impute import SimpleImputer
    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X_raw)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    var_exp = pca.explained_variance_ratio_ * 100
    print(f"[PCA] Variância Explicada:")
    print(f"  -> PC1: {var_exp[0]:.2f}%")
    print(f"  -> PC2: {var_exp[1]:.2f}% (Acumulada: {sum(var_exp):.2f}%)")

    # Autovetores (Loadings) da PC1
    loadings_pc1 = pca.components_[0]
    loadings_pc2 = pca.components_[1]

    # Contribuição de cada variável na PC1: (loading_i^2 / sum(loading^2)) * 100
    # Como os componentes são ortonormais (sum(loading^2) = 1), contrib_i = loading_i^2 * 100
    contrib_pc1 = (loadings_pc1 ** 2) / np.sum(loadings_pc1 ** 2) * 100

    # Linha de corte: critério uniforme 1/15 (6.67%) conforme solicitado ou 1/p
    # Vamos considerar 1/15 (6.67%) e destacar também 1/8 (12.5%) se aplicável
    corte_1_15 = (1.0 / 15.0) * 100.0  # 6.667%

    df_contrib = pd.DataFrame({
        'feature': FEATURES_CONTINUAS,
        'nome_legivel': [DIC_NOMES_LEGIVEIS[f] for f in FEATURES_CONTINUAS],
        'loading_pc1': loadings_pc1,
        'loading_pc2': loadings_pc2,
        'contrib_pc1_pct': contrib_pc1,
        'selecionada': contrib_pc1 >= corte_1_15
    }).sort_values(by='contrib_pc1_pct', ascending=False).reset_index(drop=True)

    print("\n[CONTRIBUIÇÃO NA PRIMEIRA COMPONENTE PRINCIPAL (PC1)]")
    print(f"Linha de corte (1/15 da variância): {corte_1_15:.2f}%")
    for _, row in df_contrib.iterrows():
        status = "✅ SELECIONADA" if row['selecionada'] else "❌ REJEITADA"
        print(f"  -> {row['nome_legivel']:<25}: {row['contrib_pc1_pct']:>6.2f}% (Loading={row['loading_pc1']:>+.3f}) | {status}")

    vars_selecionadas = df_contrib[df_contrib['selecionada']]['feature'].tolist()
    print(f"\n[INFO] Total de variáveis selecionadas para a modelagem: {len(vars_selecionadas)} de {len(FEATURES_CONTINUAS)}")

    # -------------------------------------------------------------
    # (A) Gráfico de Barras de Contribuição na PC1 com Linha de Corte
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    cores = ['#d7191c' if s else '#2b83ba' for s in df_contrib['selecionada']]
    
    bars = ax.bar(df_contrib['nome_legivel'], df_contrib['contrib_pc1_pct'], color=cores, edgecolor='black', width=0.55)
    
    # Linha de corte de 1/15
    ax.axhline(corte_1_15, color='red', linestyle='--', linewidth=2.0, label=f'Linha de Corte 1/15 ({corte_1_15:.2f}%)')
    
    for bar, val in zip(bars, df_contrib['contrib_pc1_pct']):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.6, f"{val:.1f}%", ha='center', va='bottom', fontsize=8.5, fontweight='bold')

    ax.set_title('Contribuição das Variáveis Contínuas na 1ª Componente Principal (PC1)', fontsize=11, fontweight='bold', pad=10)
    ax.set_ylabel('Contribuição na PC1 (%)', fontsize=9, fontweight='bold')
    ax.tick_params(axis='x', rotation=30, labelsize=8.5)
    ax.tick_params(axis='y', labelsize=8.5)
    ax.set_ylim(0, max(df_contrib['contrib_pc1_pct']) + 5)
    ax.legend(loc='upper right', fontsize=9, frameon=True)
    ax.grid(axis='y', linestyle=':', alpha=0.6)

    plt.tight_layout()
    out_bar = OUTPUT_DIR / "pca_contribuicao_pc1.png"
    plt.savefig(out_bar, dpi=300)
    plt.close()
    print(f"✅ Gráfico de Contribuição PC1 salvo: {out_bar.name}")

    # -------------------------------------------------------------
    # (B) Biplot da PCA (PC1 vs PC2)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.5, 6.5), dpi=300)
    
    # Scatter dos pontos (Amostras de Fogo e Não-Fogo)
    idx_fogo = (y_raw == 1)
    idx_nao_fogo = (y_raw == 0)
    
    ax.scatter(X_pca[idx_nao_fogo, 0], X_pca[idx_nao_fogo, 1], color='#4575b4', s=35, alpha=0.65, label='Não-Fogo (0)', edgecolor='none')
    ax.scatter(X_pca[idx_fogo, 0], X_pca[idx_fogo, 1], color='#d7301f', s=40, alpha=0.85, label='Fogo (1)', edgecolor='black', linewidth=0.5)

    # Vetores das variáveis no Biplot
    scale_factor = np.max(np.abs(X_pca)) * 0.85
    for i, feat in enumerate(FEATURES_CONTINUAS):
        vx = loadings_pc1[i] * scale_factor
        vy = loadings_pc2[i] * scale_factor
        cor_vetor = '#b2182b' if df_contrib.loc[df_contrib['feature']==feat, 'selecionada'].values[0] else '#525252'
        
        ax.arrow(0, 0, vx, vy, color=cor_vetor, alpha=0.85, width=0.03, head_width=0.18, length_includes_head=True)
        ax.text(vx * 1.12, vy * 1.12, DIC_NOMES_LEGIVEIS[feat], color=cor_vetor, fontsize=8, fontweight='bold', ha='center', va='center')

    ax.axhline(0, color='gray', linestyle=':', linewidth=0.8)
    ax.axvline(0, color='gray', linestyle=':', linewidth=0.8)
    ax.set_title(f'Biplot PCA: PC1 ({var_exp[0]:.1f}%) vs PC2 ({var_exp[1]:.1f}%)\nDistribuição Espacial das Amostras e Vetores de Variáveis',
                 fontsize=11, fontweight='bold', pad=10)
    ax.set_xlabel(f'Componente Principal 1 - PC1 ({var_exp[0]:.1f}% variância)', fontsize=9, fontweight='bold')
    ax.set_ylabel(f'Componente Principal 2 - PC2 ({var_exp[1]:.1f}% variância)', fontsize=9, fontweight='bold')
    ax.legend(loc='upper right', fontsize=8.5, frameon=True)
    ax.grid(True, linestyle=':', alpha=0.5)

    plt.tight_layout()
    out_biplot = OUTPUT_DIR / "pca_biplot_pc1_pc2.png"
    plt.savefig(out_biplot, dpi=300)
    plt.close()
    print(f"✅ Biplot da PCA salvo: {out_biplot.name}")

    return vars_selecionadas, df_contrib, scaler


# ==========================================
# 2. TREINAMENTO DA REGRESSÃO LOGÍSTICA
# ==========================================
def treinar_modelo_logistico(vars_selecionadas: list[str]):
    """Treina o modelo logístico padrão com as variáveis contínuas selecionadas pela PCA."""
    print("\n" + "=" * 70)
    print("📈 2. AJUSTE E VALIDAÇÃO DA REGRESSÃO LOGÍSTICA PADRÃO")
    print("=" * 70)

    df_treino = pd.read_csv(CSV_TREINO)
    df_val = pd.read_csv(CSV_VALIDACAO)
    df_total = pd.read_csv(CSV_ANUAL)

    X_train = df_treino[vars_selecionadas].copy()
    y_train = df_treino['incendio'].values

    X_val = df_val[vars_selecionadas].copy()
    y_val = df_val['incendio'].values

    # Imputação e Padronização específicas para as variáveis selecionadas
    from sklearn.impute import SimpleImputer
    imputer = SimpleImputer(strategy='median')
    X_train_imp = imputer.fit_transform(X_train)
    X_val_imp = imputer.transform(X_val)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_imp)
    X_val_scaled = scaler.transform(X_val_imp)

    # Modelo de Regressão Logística Padrão
    modelo_logit = LogisticRegression(
        penalty='l2',
        C=1.0,
        solver='lbfgs',
        class_weight='balanced',
        random_state=42,
        max_iter=1000
    )
    modelo_logit.fit(X_train_scaled, y_train)

    # Predição e Probabilidades
    y_val_proba = modelo_logit.predict_proba(X_val_scaled)[:, 1]
    y_val_pred = (y_val_proba >= 0.50).astype(int)

    # Métricas da Matriz de Confusão
    cm = confusion_matrix(y_val, y_val_pred)
    tn, fp, fn, tp = cm.ravel()

    acc = accuracy_score(y_val, y_val_pred)
    rec = recall_score(y_val, y_val_pred)
    prec = precision_score(y_val, y_val_pred)
    f1 = f1_score(y_val, y_val_pred)
    f3 = fbeta_score(y_val, y_val_pred, beta=3.0)
    auc = roc_auc_score(y_val, y_val_proba)

    far = fp / (tp + fp) if (tp + fp) > 0 else 0.0
    pofd = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    csi = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0.0

    denom_hss = ((tp + fn) * (fn + tn)) + ((tp + fp) * (fp + tn))
    hss = 2.0 * (tp * tn - fp * fn) / denom_hss if denom_hss > 0 else 0.0

    pod = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    pss = pod - pofd

    print("=" * 65)
    print("📊 RESULTADOS DA VALIDAÇÃO (REGRESSÃO LOGÍSTICA CONTÍNUA)")
    print("=" * 65)
    print(f"Acurácia Global (Pa):              {acc * 100:.2f}%")
    print(f"Probabilidade de Detecção (POD/Pr): {rec * 100:.2f}%")
    print(f"Precisão do Alerta (Pp):           {prec * 100:.2f}%")
    print(f"Taxa de Falso Alarme (FAR):        {far * 100:.2f}%")
    print(f"Probab. de Falsa Detecção (POFD):  {pofd * 100:.2f}%")
    print(f"Critical Success Index (CSI/TS):   {csi * 100:.2f}%")
    print(f"Heidke Skill Score (HSS):          {hss:.4f}")
    print(f"Peirce Skill Score (PSS / TSS):    {pss:.4f}")
    print(f"F1-Score:                          {f1 * 100:.2f}%")
    print(f"F3-Score (β=3):                    {f3 * 100:.2f}%")
    print(f"Área sob a Curva (AUC-ROC):        {auc:.4f}")
    print(f"Matriz de Confusão [ [TN={tn}, FP={fp}], [FN={fn}, TP={tp}] ]")
    print("=" * 65)

    # Coeficientes do Modelo Logístico
    coefs = modelo_logit.coef_[0]
    intercept = modelo_logit.intercept_[0]

    df_coefs = pd.DataFrame({
        'feature': vars_selecionadas,
        'nome_legivel': [DIC_NOMES_LEGIVEIS[f] for f in vars_selecionadas],
        'coef_beta': np.round(coefs, 4),
        'odds_ratio': np.round(np.exp(coefs), 4),
        'direcao': ['Aumenta Risco (+)' if c > 0 else 'Reduz Risco (-)' for c in coefs]
    }).sort_values(by='coef_beta', key=abs, ascending=False).reset_index(drop=True)

    print("\n[COEFICIENTES ESTIMADOS DA REGRESSÃO LOGÍSTICA]")
    print(df_coefs.to_string(index=False))
    print(f"Intercepto (Beta 0): {intercept:.4f}")

    # Inferência em todas as amostras
    X_total_imp = imputer.transform(df_total[vars_selecionadas])
    X_total_scaled = scaler.transform(X_total_imp)
    df_total['probabilidade_fogo_logit'] = modelo_logit.predict_proba(X_total_scaled)[:, 1]
    
    p = df_total['probabilidade_fogo_logit']
    df_total['nivel_risco_logit'] = 1
    df_total.loc[(p >= 0.25) & (p < 0.50), 'nivel_risco_logit'] = 2
    df_total.loc[(p >= 0.50) & (p < 0.75), 'nivel_risco_logit'] = 3
    df_total.loc[p >= 0.75, 'nivel_risco_logit'] = 4

    out_csv = OUTPUT_DIR / "grade_1km_predicoes_regressao_logistica.csv"
    df_total.to_csv(out_csv, index=False)
    print(f"\n[SAÍDA] Predições salvas em: {out_csv.name}")

    # Salvar métricas e coeficientes em JSON
    metricas_dict = {
        'Pa': acc, 'POD': rec, 'Pp': prec, 'FAR': far,
        'POFD': pofd, 'CSI': csi, 'HSS': hss, 'PSS': pss,
        'F1': f1, 'F3': f3, 'AUC': auc
    }

    relatorio_json = {
        'variaveis_selecionadas_pca': vars_selecionadas,
        'intercepto': round(float(intercept), 4),
        'coeficientes': df_coefs.to_dict(orient='records'),
        'matriz_confusao': {'TN': int(tn), 'FP': int(fp), 'FN': int(fn), 'TP': int(tp)},
        'metricas_validacao': {
            'acuracia_pa': round(acc, 4),
            'recall_pod': round(rec, 4),
            'precisao_pp': round(prec, 4),
            'false_alarm_ratio_far': round(far, 4),
            'prob_false_detection_pofd': round(pofd, 4),
            'critical_success_index_csi': round(csi, 4),
            'heidke_skill_score_hss': round(hss, 4),
            'peirce_skill_score_pss': round(pss, 4),
            'f1_score': round(f1, 4),
            'f3_score': round(f3, 4),
            'auc_roc': round(auc, 4)
        }
    }
    out_json = OUTPUT_DIR / "metricas_regressao_logistica_pca.json"
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(relatorio_json, f, indent=4, ensure_ascii=False)
    print(f"✅ Relatório JSON salvo em: {out_json.name}")

    # -------------------------------------------------------------
    # (C) Prancha A4 Consolidada (PCA + Avaliação do Logit)
    # -------------------------------------------------------------
    gerar_prancha_a4_consolidada(y_val, y_val_proba, cm, metricas_dict, df_coefs)


# ==========================================
# 3. GRÁFICOS DE AVALIAÇÃO (LAYOUT LIVRE)
# ==========================================
def gerar_prancha_a4_consolidada(
    y_val: np.ndarray,
    y_val_proba: np.ndarray,
    cm: np.ndarray,
    m: dict[str, float],
    df_coefs: pd.DataFrame
):
    """Gera um painel gráfico com 4 subplots detalhando o modelo logístico contínuo em layout livre."""
    print("\n[PLOT] Gerando painel de avaliação da Regressão Logística...")

    fig, axes = plt.subplots(2, 2, figsize=(13, 10), dpi=300)

    # -------------------------------------------------------------
    # (A) Matriz de Confusão
    # -------------------------------------------------------------
    ax_cm = axes[0, 0]
    sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges', cbar=False,
                xticklabels=['Não-Fogo (Pred)', 'Fogo (Pred)'],
                yticklabels=['Não-Fogo (Real)', 'Fogo (Real)'],
                annot_kws={'size': 13, 'weight': 'bold'}, ax=ax_cm)
    ax_cm.set_title('(A) Matriz de Confusão (Validação 30%)', fontsize=11, fontweight='bold', pad=8)
    ax_cm.tick_params(labelsize=10)

    # -------------------------------------------------------------
    # (B) Curva ROC
    # -------------------------------------------------------------
    ax_roc = axes[0, 1]
    fpr, tpr, _ = roc_curve(y_val, y_val_proba)
    ax_roc.plot(fpr, tpr, color='#e6550d', linewidth=2.5, label=f'Logit Contínuo (AUC = {m["AUC"]:.3f})')
    ax_roc.plot([0, 1], [0, 1], color='gray', linestyle='--', linewidth=1.2)
    ax_roc.set_title('(B) Curva ROC de Discriminação de Risco', fontsize=11, fontweight='bold', pad=8)
    ax_roc.set_xlabel('Taxa de Falsos Positivos (POFD)', fontsize=9.5)
    ax_roc.set_ylabel('Taxa de Verdadeiros Positivos (POD)', fontsize=9.5)
    ax_roc.legend(loc='lower right', fontsize=10, frameon=True)
    ax_roc.grid(True, linestyle=':', alpha=0.6)
    ax_roc.tick_params(labelsize=9.5)

    # -------------------------------------------------------------
    # (C) Gráfico de Barras das Métricas e Skill Scores
    # -------------------------------------------------------------
    ax_met = axes[1, 0]
    nomes_met = ['Acurácia\n(Pa)', 'Detecção\n(POD)', 'Falso Alarme\n(FAR)', 'Threat\n(CSI)', 'Heidke\n(HSS)', 'Peirce\n(PSS)', 'F3-Score\n(β=3)']
    valores_met = [m['Pa'] * 100, m['POD'] * 100, m['FAR'] * 100, m['CSI'] * 100, m['HSS'] * 100, m['PSS'] * 100, m['F3'] * 100]
    cores_met = ['#4575b4', '#74add1', '#d7301f', '#fee090', '#66c2a5', '#3288bd', '#f46d43']

    bars = ax_met.bar(nomes_met, valores_met, color=cores_met, edgecolor='black', width=0.58)
    for bar, val in zip(bars, valores_met):
        ax_met.text(bar.get_x() + bar.get_width() / 2, val + 1.5, f"{val:.1f}%", ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax_met.set_ylim(0, 115)
    ax_met.set_title('(C) Métricas de Avaliação e Skill Scores', fontsize=11, fontweight='bold', pad=8)
    ax_met.set_ylabel('Score (%)', fontsize=9.5)
    ax_met.tick_params(axis='x', labelsize=8)
    ax_met.tick_params(axis='y', labelsize=9.5)
    ax_met.grid(axis='y', linestyle=':', alpha=0.6)

    # -------------------------------------------------------------
    # (D) Coeficientes Padronizados (Beta) do Modelo Logístico
    # -------------------------------------------------------------
    ax_coef = axes[1, 1]
    df_sorted = df_coefs.sort_values(by='coef_beta', ascending=True)
    cores_coef = ['#d7301f' if c > 0 else '#2b83ba' for c in df_sorted['coef_beta']]

    ax_coef.barh(df_sorted['nome_legivel'], df_sorted['coef_beta'], color=cores_coef, edgecolor='black', height=0.55)
    ax_coef.axvline(0, color='black', linewidth=0.8, linestyle='--')
    ax_coef.set_title('(D) Coeficientes Padronizados (Beta)', fontsize=11, fontweight='bold', pad=8)
    ax_coef.set_xlabel('Magnitude do Coeficiente (Padronizado)', fontsize=9.5)
    ax_coef.tick_params(axis='y', labelsize=9.5)
    ax_coef.tick_params(axis='x', labelsize=9.5)
    ax_coef.grid(axis='x', linestyle=':', alpha=0.6)

    fig.suptitle('Modelagem de Risco de Incêndio com Regressão Logística Contínua (PCA Selected)\nSão José dos Pinhais - PR (Variáveis Físicas Padronizadas)',
                 fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0.02, 1, 0.95])

    out_png = OUTPUT_DIR / "painel_regressao_logistica_pca.png"
    plt.savefig(out_png, dpi=300)
    plt.close()
    print(f"✅ Painel de Regressão Logística salvo: {out_png.name}")


# ==========================================
# MAIN
# ==========================================
def main():
    print("=" * 75)
    print("🚀 ETAPA 03_MODELAGEM: 04_REGRESSAO_LOGISTICA_PCA")
    print("=" * 75)
    print(f"Diretório de Saída: {OUTPUT_DIR}")

    df_treino = pd.read_csv(CSV_TREINO)

    # 1. Executar PCA, calcular contribuições, linha de corte e gerar Biplot
    vars_selecionadas, df_contrib, scaler = executar_pca_e_selecao(df_treino)

    # 2. Treinar Regressão Logística com variáveis contínuas selecionadas
    treinar_modelo_logistico(vars_selecionadas)

    print("\n" + "=" * 75)
    print("✨ PROCESSAMENTO DA REGRESSÃO LOGÍSTICA & PCA CONCLUÍDO COM SUCESSO!")
    print("=" * 75)


if __name__ == "__main__":
    main()
