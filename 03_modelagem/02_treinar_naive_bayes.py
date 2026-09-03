"""
Script: 02_treinar_naive_bayes.py
Etapa: 03_modelagem

Descrição:
    Implementa o Treinamento, Inferência Probabilística, Validação e ZONAL RISK MAPPING
    utilizando a Rede Naive Bayes (NBN) conforme a metodologia de Chen et al. (2021):
    
    1. Estrutura do Modelo:
       - Fatores Condicionais P(X_i | Y):
         * Histórico: fire_density_classe
         * Topografia: elevation_classe, slope_classe, aspect_classe
         * Vegetação: ndvi_classe, ndmi_classe
         * Clima/Seca: spi_classe
         * Infraestrutura: dr_classe (estradas), ds_classe (urbano)
         * Uso do Solo: lulc_classe (MapBiomas)
       - Priori: P(Y=1) [Fogo] e P(Y=0) [Não-Fogo] no conjunto de Treino (70%).
       - Cálculo das Tabelas de Probabilidade Condicional (CPTs) com Laplace Smoothing.
       
    2. Inferência Probabilística Bayesiana:
       - P(Y=1 | X) = [ P(Y=1) * prod(P(X_i | Y=1)) ] / [ P(Y=1)*prod(P(X_i|Y=1)) + P(Y=0)*prod(P(X_i|Y=0)) ]
       
    3. Avaliação no Conjunto de Teste/Validação (30%):
       - Matriz de Confusão (TP, FP, TN, FN) no limiar padrão de 0.50.
       - Métricas: Acurácia (Pa), Recall/Sensibilidade (Pr), Precisão (Pp), F1-Score e F3-Score (beta=3, Chen et al.).
       - Curva ROC e Área sob a Curva (AUC-ROC).
       
    4. Mapeamento Espacial de Probabilidade e Risco (Zonemaneto 1 km²):
       - 4 Níveis de Risco conforme Chen et al. (2021):
         * Baixo Risco (Low):       0% <= P(Fogo) < 25%
         * Médio Risco (Medium):   25% <= P(Fogo) < 50%
         * Alto Risco (High):      50% <= P(Fogo) < 75%
         * Muito Alto (Very High): P(Fogo) >= 75%
       - Prancha A4 Retrato com Mapa Temático de Zonamento de Risco, Métricas e Matriz de Confusão.
       - Exportação dos modelos e probabilidades em CSV e GeoJSON.
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
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap, BoundaryNorm
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, fbeta_score, roc_curve, roc_auc_score

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
GEOJSON_GRADE = AMOSTRAS_DIR / "grade_1km_amostras_fogo_naofogo.geojson"

if (BASE_DIR / "input" / "01_vetores" / "SJP.shp").exists():
    LIMITE_SHP = BASE_DIR / "input" / "01_vetores" / "SJP.shp"
else:
    LIMITE_SHP = BASE_DIR / "output" / "01_vetores" / "SJP.shp"

OUTPUT_DIR = BASE_DIR / "output" / "03_modelagem" / "02_treinar_naive_bayes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Lista de fatores preditores categóricos / ambientais e antrópicos (sem vazamento de dados de fogo)
FEATURES = [
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


# ==========================================
# 1. CLASSE MODELO NAIVE BAYES NETWORK (CHEN ET AL.)
# ==========================================
class CategoricalNaiveBayesNetwork:
    """
    Implementação da Rede Bayesiana Ingênua Categórica
    com Suavização de Laplace (Laplace Smoothing) para evitar probabilidades nulas.
    """
    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha
        self.prior_fogo = 0.5
        self.prior_nao_fogo = 0.5
        self.cpt_fogo = {}
        self.cpt_nao_fogo = {}
        self.classes_por_feature = {}

    def fit(self, X: pd.DataFrame, y: pd.Series):
        """Ajusta as probabilidades a priori e as tabelas de probabilidade condicional (CPT)."""
        n_total = len(y)
        n_fogo = np.sum(y == 1)
        n_nao_fogo = np.sum(y == 0)

        # Probabilidades a Priori
        self.prior_fogo = n_fogo / n_total
        self.prior_nao_fogo = n_nao_fogo / n_total

        X_fogo = X[y == 1]
        X_nao_fogo = X[y == 0]

        for col in X.columns:
            vals_unicos = sorted(X[col].unique())
            self.classes_por_feature[col] = vals_unicos
            k = len(vals_unicos)  # número de categorias possíveis

            cpt_f = {}
            cpt_nf = {}

            # Fogo (Y = 1)
            counts_f = X_fogo[col].value_counts().to_dict()
            for v in vals_unicos:
                cnt = counts_f.get(v, 0)
                # Laplace Smoothing: (count + alpha) / (N_class + alpha * k)
                cpt_f[v] = (cnt + self.alpha) / (n_fogo + self.alpha * k)

            # Não Fogo (Y = 0)
            counts_nf = X_nao_fogo[col].value_counts().to_dict()
            for v in vals_unicos:
                cnt = counts_nf.get(v, 0)
                cpt_nf[v] = (cnt + self.alpha) / (n_nao_fogo + self.alpha * k)

            self.cpt_fogo[col] = cpt_f
            self.cpt_nao_fogo[col] = cpt_nf

        print(f"[NBN] Modelo treinado com sucesso com {len(X)} amostras.")
        print(f"  -> Prior P(Fogo=1): {self.prior_fogo:.4f} | Prior P(Não-Fogo=0): {self.prior_nao_fogo:.4f}")
        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Calcula a probabilidade a posteriori de Fogo P(Y=1 | X_1, ..., X_n)
        utilizando a regra do produto e normalização de Bayes.
        """
        probas = []
        for _, row in X.iterrows():
            log_p_fogo = np.log(self.prior_fogo)
            log_p_nao_fogo = np.log(self.prior_nao_fogo)

            for col in X.columns:
                val = row[col]
                k = len(self.classes_por_feature[col])
                
                # Probabilidade condicional P(X_i = val | Y = 1)
                p_f = self.cpt_fogo[col].get(val, self.alpha / (self.alpha * k + 1e-6))
                log_p_fogo += np.log(p_f)

                # Probabilidade condicional P(X_i = val | Y = 0)
                p_nf = self.cpt_nao_fogo[col].get(val, self.alpha / (self.alpha * k + 1e-6))
                log_p_nao_fogo += np.log(p_nf)

            # Normalização Bayesiana via log-sum-exp para estabilidade numérica
            max_log = max(log_p_fogo, log_p_nao_fogo)
            p_f_exp = np.exp(log_p_fogo - max_log)
            p_nf_exp = np.exp(log_p_nao_fogo - max_log)

            prob_fogo = p_f_exp / (p_f_exp + p_nf_exp)
            probas.append(prob_fogo)

        return np.array(probas)

    def predict(self, X: pd.DataFrame, threshold: float = 0.50) -> np.ndarray:
        """Classifica em 1 (Prone to Fire) ou 0 (Prone to Non-Fire) baseado no threshold."""
        return (self.predict_proba(X) >= threshold).astype(int)


# ==========================================
# 2. TREINAMENTO E AVALIAÇÃO
# ==========================================
def treinar_e_avaliar_modelo():
    """Carrega os dados de treino/validação, treina o Naive Bayes e avalia métricas."""
    print("=" * 75)
    print("🧠 MODELAGEM PREDITIVA COM NAIVE BAYES NETWORK (CHEN ET AL., 2021)")
    print("=" * 75)

    df_treino = pd.read_csv(CSV_TREINO)
    df_val = pd.read_csv(CSV_VALIDACAO)
    df_total = pd.read_csv(CSV_ANUAL)

    print(f"[DATA] Treino (70%):     {len(df_treino)} registros (Fogo={sum(df_treino['incendio']==1)}, Não-Fogo={sum(df_treino['incendio']==0)})")
    print(f"[DATA] Validação (30%):  {len(df_val)} registros (Fogo={sum(df_val['incendio']==1)}, Não-Fogo={sum(df_val['incendio']==0)})")
    print(f"[DATA] Fatores preditores ({len(FEATURES)}): {FEATURES}\n")

    X_train = df_treino[FEATURES]
    y_train = df_treino['incendio']

    X_val = df_val[FEATURES]
    y_val = df_val['incendio']

    # Treinar modelo
    nbn = CategoricalNaiveBayesNetwork(alpha=1.0)
    nbn.fit(X_train, y_train)

    # Inferência no conjunto de teste/validação
    y_val_proba = nbn.predict_proba(X_val)
    y_val_pred = (y_val_proba >= 0.50).astype(int)

    # Métricas da Matriz de Confusão
    cm = confusion_matrix(y_val, y_val_pred)
    tn, fp, fn, tp = cm.ravel()

    # Métricas Tradicionais de ML
    acc = accuracy_score(y_val, y_val_pred)
    rec = recall_score(y_val, y_val_pred)   # POD / Hit Rate = TP / (TP + FN)
    prec = precision_score(y_val, y_val_pred)
    f1 = f1_score(y_val, y_val_pred)
    f3 = fbeta_score(y_val, y_val_pred, beta=3.0)  # F3-score (Chen et al., 2021)
    auc = roc_auc_score(y_val, y_val_proba)

    # Métricas Meteorológicas e de Avaliação de Risco de Incêndio:
    # 1. False Alarm Ratio (FAR): Proporção de alarmes falsos entre os previstos = FP / (TP + FP)
    far = fp / (tp + fp) if (tp + fp) > 0 else 0.0

    # 2. Probability of False Detection (POFD / Fall-out): FP / (FP + TN)
    pofd = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    # 3. Critical Success Index (CSI / Threat Score TS): TP / (TP + FP + FN)
    csi = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0.0

    # 4. Heidke Skill Score (HSS): Avalia acurácia relativa ao acaso
    # HSS = 2*(TP*TN - FP*FN) / [ (TP+FN)*(FN+TN) + (TP+FP)*(FP+TN) ]
    denom_hss = ((tp + fn) * (fn + tn)) + ((tp + fp) * (fp + tn))
    hss = 2.0 * (tp * tn - fp * fn) / denom_hss if denom_hss > 0 else 0.0

    # 5. Peirce Skill Score / True Skill Statistic (PSS / TSS / Hanssen-Kuipers):
    # PSS = (TP / (TP + FN)) - (FP / (FP + TN)) = POD - POFD
    pod = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    pss = pod - pofd

    print("\n" + "=" * 65)
    print("📊 RESULTADOS DA VALIDAÇÃO (CONJUNTO DE TESTE 30%)")
    print("=" * 65)
    print(f"Acurácia Global (Pa):              {acc * 100:.2f}%")
    print(f"Probabilidade de Detecção (POD/Pr): {rec * 100:.2f}%")
    print(f"Precisão do Alerta (Pp):           {prec * 100:.2f}%")
    print(f"Taxa de Falso Alarme (FAR):        {far * 100:.2f}%")
    print(f"Probab. de Falsa Detecção (POFD):  {pofd * 100:.2f}%")
    print(f"Critical Success Index (CSI/TS):   {csi * 100:.2f}%")
    print(f"Heidke Skill Score (HSS):          {hss:.4f} (Excelente > 0.60)")
    print(f"Peirce Skill Score (PSS / TSS):    {pss:.4f} (Excelente > 0.60)")
    print(f"F1-Score:                          {f1 * 100:.2f}%")
    print(f"F3-Score (β=3):                    {f3 * 100:.2f}% (Chen et al., 2021)")
    print(f"Área sob a Curva (AUC-ROC):        {auc:.4f}")
    print(f"Matriz de Confusão [ [TN={tn}, FP={fp}], [FN={fn}, TP={tp}] ]")
    print("=" * 65)

    # 3. Inferência em Todo o Conjunto de Amostras
    df_total['probabilidade_fogo'] = nbn.predict_proba(df_total[FEATURES])
    
    # Classificação em 4 Níveis de Risco de Chen et al. (2021)
    p = df_total['probabilidade_fogo']
    df_total['nivel_risco_nbn'] = 1
    df_total.loc[(p >= 0.25) & (p < 0.50), 'nivel_risco_nbn'] = 2
    df_total.loc[(p >= 0.50) & (p < 0.75), 'nivel_risco_nbn'] = 3
    df_total.loc[p >= 0.75, 'nivel_risco_nbn'] = 4

    out_csv_preds = OUTPUT_DIR / "grade_1km_predicoes_naive_bayes.csv"
    df_total.to_csv(out_csv_preds, index=False)
    print(f"\n[SAÍDA] Predições e probabilidades salvas em: {out_csv_preds.name}")

    # Salvar CPTs e Métricas em JSON
    cpts_dict = {
        'prior_fogo': nbn.prior_fogo,
        'prior_nao_fogo': nbn.prior_nao_fogo,
        'cpt_fogo': {k: {str(val): round(prob, 4) for val, prob in v.items()} for k, v in nbn.cpt_fogo.items()},
        'cpt_nao_fogo': {k: {str(val): round(prob, 4) for val, prob in v.items()} for k, v in nbn.cpt_nao_fogo.items()},
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
    out_json = OUTPUT_DIR / "tabelas_probabilidade_cpt_nbn.json"
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(cpts_dict, f, indent=4, ensure_ascii=False)
    print(f"✅ Tabelas CPT e métricas salvas em: {out_json.name}")

    # 4. Gerar Prancha A4 de Avaliação e Mapeamento
    metricas_dict = {
        'Pa': acc, 'POD': rec, 'Pp': prec, 'FAR': far,
        'POFD': pofd, 'CSI': csi, 'HSS': hss, 'PSS': pss,
        'F1': f1, 'F3': f3, 'AUC': auc
    }
    gerar_painel_a4_modelagem(df_val, y_val, y_val_proba, y_val_pred, cm, metricas_dict, nbn)


# ==========================================
# 3. GRÁFICOS DE AVALIAÇÃO (LAYOUT LIVRE)
# ==========================================
def gerar_painel_a4_modelagem(
    df_val: pd.DataFrame,
    y_val: pd.Series,
    y_val_proba: np.ndarray,
    y_val_pred: np.ndarray,
    cm: np.ndarray,
    m: dict[str, float],
    nbn: CategoricalNaiveBayesNetwork
):
    """Gera um painel gráfico com 4 subplots detalhando o desempenho do Naive Bayes em layout livre."""
    print("\n[PLOT] Gerando gráficos de avaliação do Naive Bayes...")

    fig, axes = plt.subplots(2, 2, figsize=(13, 10), dpi=300)
    
    # -------------------------------------------------------------
    # (A) Matriz de Confusão
    # -------------------------------------------------------------
    ax_cm = axes[0, 0]
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['Não-Fogo (Pred)', 'Fogo (Pred)'],
                yticklabels=['Não-Fogo (Real)', 'Fogo (Real)'],
                annot_kws={'size': 13, 'weight': 'bold'}, ax=ax_cm)
    ax_cm.set_title('(A) Matriz de Confusão (Validação 30%)', fontsize=11, fontweight='bold', pad=8)
    ax_cm.tick_params(labelsize=10)

    # -------------------------------------------------------------
    # (B) Curva ROC (AUC-ROC)
    # -------------------------------------------------------------
    ax_roc = axes[0, 1]
    fpr, tpr, _ = roc_curve(y_val, y_val_proba)
    ax_roc.plot(fpr, tpr, color='#2b83ba', linewidth=2.5, label=f'NBN (AUC = {m["AUC"]:.3f})')
    ax_roc.plot([0, 1], [0, 1], color='gray', linestyle='--', linewidth=1.2)
    ax_roc.set_title('(B) Curva ROC de Discriminação de Risco', fontsize=11, fontweight='bold', pad=8)
    ax_roc.set_xlabel('Taxa de Falsos Positivos (POFD)', fontsize=9.5)
    ax_roc.set_ylabel('Taxa de Verdadeiros Positivos (POD)', fontsize=9.5)
    ax_roc.legend(loc='lower right', fontsize=10, frameon=True)
    ax_roc.grid(True, linestyle=':', alpha=0.6)
    ax_roc.tick_params(labelsize=9.5)

    # -------------------------------------------------------------
    # (C) Gráfico de Barras: Métricas de Desempenho e Skill Scores
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
    # (D) Distribuição de Probabilidades Preditas por Classe Real
    # -------------------------------------------------------------
    ax_prob = axes[1, 1]
    df_plot_val = pd.DataFrame({
        'Probabilidade': y_val_proba,
        'Classe_Real': ['Fogo' if y == 1 else 'Não-Fogo' for y in y_val]
    })
    sns.boxplot(x='Classe_Real', y='Probabilidade', data=df_plot_val, hue='Classe_Real', palette=['#5353EC', '#F97306'], legend=False, ax=ax_prob, width=0.45)
    ax_prob.axhline(0.50, color='red', linestyle='--', linewidth=1.2, label='Limiar (0.50)')
    ax_prob.set_title('(D) Probabilidade Predita por Classe Real', fontsize=11, fontweight='bold', pad=8)
    ax_prob.set_xlabel('Evento Real Observado', fontsize=9.5)
    ax_prob.set_ylabel('Probabilidade Predita P(Fogo)', fontsize=9.5)
    ax_prob.legend(loc='upper left', fontsize=9.5, frameon=True)
    ax_prob.tick_params(labelsize=9.5)
    ax_prob.grid(axis='y', linestyle=':', alpha=0.6)

    fig.suptitle('Avaliação de Desempenho e Skill Scores da Rede Naive Bayes (NBN)\nSão José dos Pinhais - PR (Chen et al., 2021)',
                 fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0.02, 1, 0.95])

    out_png = OUTPUT_DIR / "painel_avaliacao_naive_bayes.png"
    plt.savefig(out_png, dpi=300)
    plt.close()
    print(f"✅ Painel de Avaliação Naive Bayes salvo: {out_png.name}")


# ==========================================
# MAIN
# ==========================================
def main():
    treinar_e_avaliar_modelo()


if __name__ == "__main__":
    main()
