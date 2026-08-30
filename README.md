# 🌲 Fire Risk Zoning (Zoneamento do Risco de Incêndio)
### Modelagem Preditiva Espaço-Temporal de Perigo de Incêndios Florestais em São José dos Pinhais - PR

---

## 📌 Visão Geral do Projeto

Este repositório contém o pipeline completo de engenharia de dados geoespaciais, modelagem preditiva e zoneamento territorial do perigo de incêndios florestais para o município de **São José dos Pinhais - PR** ao longo da série temporal de **2013 a 2025**.

O projeto estrutura dados multifatoriais (ambientais, topográficos, climáticos, antrópicos e uso da terra), integrando **sensoriamento remoto**, **geoprocessamento automatizado** e **aprendizado de máquina probabilístico e estatístico** para apoiar o planejamento territorial, a defesa civil e o manejo integrado do fogo.

---

## 🔬 Metodologia de Processamento e Modelagem

O pipeline metodológico foi construído em duas vertentes complementares de modelagem preditiva:

```
                  ┌─────────────────────────────────────────────────────────┐
                  │          FOCOS HISTÓRICOS GOES/AQUA (2013-2025)         │
                  └───────────────────────────┬─────────────────────────────┘
                                              │
                                   Filtragem Espaço-Temporal
                                   (Buffer 3 km / 2 dias)
                                              │
                  ┌───────────────────────────┴─────────────────────────────┐
                  │      AMOSTRAGEM ESTRATIFICADA ANUAL (70% TR / 30% VAL)  │
                  └─────────────┬─────────────────────────────┬─────────────┘
                                │                             │
             [Variáveis Categóricas / Quantis]      [Variáveis Físicas Contínuas]
                                │                             │
                  ┌─────────────┴───────────┐   ┌─────────────┴─────────────┐
                  │    NAIVE BAYES NETWORK  │   │  PCA & REGRESSÃO LOGÍSTICA│
                  │   (Chen et al., 2021)   │   │       (Labres, 2021)      │
                  └─────────────┬───────────┘   └─────────────┬─────────────┘
                                └─────────────┬───────────────┘
                                              │
                                  Reamostragem WarpedVRT (100m)
                                  & Mediana Temporal (2013-2025)
                                              │
                                ┌─────────────┴───────────────┐
                                │   ZONEAMENTO DE RISCO 100m  │
                                │   (4 Níveis de Perigo)      │
                                └─────────────────────────────┘
```

### 1. Preparação e Amostragem Espaço-Temporal
- **Fase 1 (Filtragem de Hotspots)**: Agrupamento espaço-temporal de focos redundantes de satélite (GOES e AQUA) ocorridos dentro de um raio de **$3\text{ km}$ e $2\text{ dias}$** como sendo um único evento de incêndio.
- **Fase 2 (Amostragem Anual Balanceada)**: Para cada ano ($2013-2025$), identificam-se as células de **Fogo ($Y=1$)** na grade de $1\text{ km}^2$. As células de **Não-Fogo ($Y=0$)** são sorteadas aleatoriamente entre as células sem ocorrência naquele respectivo ano, mantendo a proporção 1:1 e divisão estratificada de **70% para Treino** e **30% para Validação Independente**.
- **Extração Pontual de Infraestrutura**: As distâncias a estradas ($\text{DR}$) e manchas urbanas ($\text{DS}$) são amostradas no **centróide exato** de cada célula territorial.

---

### 2. Modelagem por Rede Naive Bayes (NBN)
Baseada na formulação teórica de **Chen et al. (2021)**:
- **Discretização por Quantis Locais**: Todos os fatores ambientais contínuos são discretizados em 4 classes empíricas relativas ao período e território analisados, mantendo as classes oficiais de uso e cobertura da terra do MapBiomas (Coleção 10.1).
- **Inferência Bayesiana**: Ajuste das probabilidades a priori $P(\text{Fogo})$ e das Tabelas de Probabilidade Condicional (CPT) com suavização de Laplace (*Laplace smoothing*):
  $$P(\text{Fogo}=1 \mid \mathbf{X}) = \frac{P(\text{Fogo}=1) \prod_{i=1}^{n} P(X_i \mid \text{Fogo}=1)}{P(\text{Fogo}=1) \prod_{i=1}^{n} P(X_i \mid \text{Fogo}=1) + P(\text{Fogo}=0) \prod_{i=1}^{n} P(X_i \mid \text{Fogo}=0)}$$
- **Preditores Utilizados (9 Fatores)**: Elevação, Declividade, Orientação de Encosta (*Aspect*), NDVI, NDMI, SPI Anual, Distância de Estradas ($\text{DR}$), Distância de Áreas Urbanas ($\text{DS}$) e Uso do Solo ($\text{LULC}$).

---

### 3. PCA e Regressão Logística Multivariada
Baseada na metodologia de **Labres (2021)**:
- **Análise de Componentes Principais (PCA)**: Aplicada sobre as variáveis contínuas padronizadas ($Z$-score) para reduzir a dimensionalidade e avaliar a contribuição de cada fator na 1ª Componente Principal ($\text{PC1}$):
  $$\text{Contrib}_i (\%) = \frac{\text{Loading}_{1,i}^2}{\sum_{j=1}^{p} \text{Loading}_{1,j}^2} \times 100$$
- **Linha de Corte de Variância ($1/15 = 6,67\%$)**: Seleção das variáveis físicas cujos pesos em $\text{PC1}$ superam a contribuição uniforme teórica, gerando os gráficos de contribuição e o *Biplot* da PCA ($\text{PC1} \times \text{PC2}$).
- **Regressão Logística**: Ajuste da probabilidade sigmoide a partir dos fatores contínuos selecionados:
  $$P(\text{Fogo}=1 \mid \mathbf{Z}) = \frac{1}{1 + e^{-(\beta_0 + \sum_{i=1}^k \beta_i Z_i)}}$$

---

### 4. Mapeamento Territorial em Alta Resolução (100m) e Mediana Temporal
- **Reamostragem `WarpedVRT`**: Projeção de todas as camadas para uma grade homogênea de **$100\text{ m} \times 100\text{ m}$** (`EPSG:31982`), aplicando interpolação bilinear para dados contínuos e vizinho mais próximo para categóricos.
- **Agrupamento pela Mediana ($2013-2025$)**: A probabilidade síntese final do território é calculada pela **mediana temporal dos 13 anos**, eliminando ruídos causados por anos de seca atípica ou precipitação excessiva.
- **4 Classes de Zoneamento de Risco (Chen et al., 2021)**:
  - 🟢 **Baixo Risco (Low):** $P < 25\%$
  - 🟡 **Médio Risco (Medium):** $25\% \le P < 50\%$
  - 🟠 **Alto Risco (High):** $50\% \le P < 75\%$
  - 🔴 **Muito Alto Risco (Very High):** $P \ge 75\%$

---

## 📊 Resultados Resumidos

### 1. Métricas de Validação no Conjunto de Teste Independente ($30\%$):

| Métrica de Desempenho | Sigla / Fórmula | Naive Bayes (NBN) | Regressão Logística (PCA) | Interpretação |
| :--- | :---: | :---: | :---: | :--- |
| **Acurácia Global** | $P_a$ | **90,38%** | **94,23%** | Alto índice de acertos gerais |
| **Probabilidade de Detecção** | $\text{POD}$ / Recall | **84,62%** | **96,15%** | Excelente detecção de focos reais |
| **Precisão do Alerta** | $P_p$ | **95,65%** | **92,59%** | Baixíssima incidência de alarmes falsos |
| **Taxa de Falso Alarme** | $\text{FAR}$ | **4,35%** | **7,41%** | Menos de 8% de falso alarme |
| **Prob. de Falsa Detecção** | $\text{POFD}$ | **3,85%** | **7,69%** | Alta taxa de rejeição de não-fogo |
| **Índice de Ameaça** | $\text{CSI}$ / Threat Score | **81,48%** | **89,29%** | Elevada concordância preditiva |
| **Heidke Skill Score** | $\text{HSS}$ | **0,8077** | **0,8846** | Desempenho muito superior ao acaso ($>0,60$) |
| **Peirce Skill Score** | $\text{PSS}$ / TSS | **0,8077** | **0,8846** | Discriminação balanceada robusta |
| **$F_3$-Score ($\beta=3$)** | $F_3$ (Chen et al.) | **85,60%** | **95,79%** | Alta penalização para falsos negativos |
| **Área sob a Curva** | $\text{AUC-ROC}$ | **0,9822** | **0,9867** | Calibração probabilística consistente |

### 2. Validação Espacial com Focos Reais de Satélite em 100m:
- **Rede Naive Bayes**: Mais de **85% dos focos reais** monitorados entre 2013 e 2025 alocam-se em zonas de **Alto e Muito Alto Risco**.
- **Regressão Logística**: Mais de **90% dos focos reais** situam-se em zonas de **Alto e Muito Alto Risco**.

---

## 📚 Referências Metodológicas

- **Labres, J. F. L. S. (2021)**. *Modelagem de variáveis antrópicas para a estimativa de perigo de incêndios florestais para região de estepe gramíneo lenhosa no estado do Paraná*. Monografia de Especialização, Universidade Federal do Paraná (UFPR), Curitiba. (`references/labres.md`)
- **Chen, F. et al. (2021)**. *Wildfire Risk Assessment of Power Transmission Corridors Based on Naïve Bayes Network and Geographic Information System*. Sensors, 21(2), 634. (`references/chen_et_al.md`)
- **Bilal, M. et al. (2023)**. *Forest Fire Susceptibility Modeling Using Machine Learning*. Remote Sensing. (`references/bilal.md`)
- **Rabiei, V. et al. (2022)**. *Spatial Modeling of Forest Fire Vulnerability*. Environmental Science and Pollution Research. (`references/rabiei_et_al.md`)

---

## 🚀 Tutorial de Execução do Pipeline

O projeto utiliza o gerenciador de pacotes e ambientes ultrarrápido **`uv`**.

### 1. Clonar o Repositório e Instalar Dependências
```bash
git clone https://github.com/serbal193/fire-risk-zoning.git
cd fire-risk-zoning
uv sync
```

---

### 2. Executar o Tratamento de Dados (Fase 01)
Execute os scripts de tratamento sequencialmente:
```powershell
# 1. Processar e agrupar hotspots de satélite + amostragem anual balanceada
uv run python 01_tratamento/01_processar_hotspots.py

# 2. Processar variáveis topográficas (Elevação, Declividade, Aspecto)
uv run python 01_tratamento/03_processar_topografia.py

# 3. Processar índices de vegetação Landsat (NDVI e NDMI)
uv run python 01_tratamento/04_processar_indices_vegetacao.py

# 4. Processar precipitação CHIRPS e cálculo do SPI
uv run python 01_tratamento/05_processar_precipitacao_spi.py

# 5. Processar distâncias euclidianas a estradas (DR) e áreas urbanas (DS) no centróide
uv run python 01_tratamento/06_processar_distancias_infraestrutura.py

# 6. Processar uso e cobertura da terra (MapBiomas)
uv run python 01_tratamento/07_processar_uso_cobertura.py
```

---

### 3. Executar a Modelagem e Validação Preditiva (Fase 03)
```powershell
# 1. Análise histórica exploratória espaço-temporal dos focos (2013-2025)
uv run python 03_modelagem/01_analise_historica.py

# 2. Treinar e validar a Rede Naive Bayes Categórica (Chen et al., 2021)
uv run python 03_modelagem/02_treinar_naive_bayes.py

# 3. Executar PCA (Corte 1/15), Biplot e Regressão Logística Contínua (Labres, 2021)
uv run python 03_modelagem/03_treinar_regressao_logistica_pca.py

# 4. Gerar os Mapas de Zoneamento de Risco em 100m (WarpedVRT & Mediana Temporal)
uv run python 03_modelagem/04_mapeamento_risco_zoning.py
```

---

## 📁 Estrutura de Diretórios e Saídas

```
fire-risk-zoning/
├── 01_tratamento/                     # Scripts de processamento espacial de variáveis
├── 03_modelagem/                      # Scripts de modelagem e validação
│   ├── 01_analise_historica.py
│   ├── 02_treinar_naive_bayes.py
│   ├── 03_treinar_regressao_logistica_pca.py
│   └── 04_mapeamento_risco_zoning.py
├── output/
│   ├── 01_processar_hotspots/         # Amostras anuais e conjuntos de treino/validação
│   ├── 03_modelagem/
│   │   ├── 01_analise_historica/      # Gráficos temporais e KDE espacial
│   │   ├── 02_treinar_naive_bayes/    # Matriz de confusão, ROC e CPTs
│   │   ├── 04_regressao_logistica/    # Gráfico de corte PCA, Biplot e Odds Ratio
│   │   └── 03_mapeamento_risco_zoning/# Rasters GeoTIFF (100m) e Painéis de Zoneamento
├── references/                        # Artigos, monografias e referências em Markdown
└── README.md                          # Documentação consolidada do projeto
```
