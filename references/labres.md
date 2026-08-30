

<!-- Start of picture text -->
4<br>[B<br>~~<br>Ya ATiMIMO yy. oct><br>y ay) ME Sa Ses = AA<br>fey cf ISS : SS<br>Za<br>fyAh AIG A ges RMR<br>Sai, i : | oh Uae Heat<br>nips i iH ALLE A | | Pye<br>ice q al a ‘Bil We i = il<br>=— ;, =<br>=<br><!-- End of picture text -->

JOÃO FRANCISCO LABRES DOS SANTOS 

MODELAGEM DE VARIÁVEIS ANTRÓPICAS PARA A ESTIMATIVA DE PERIGO DE INCÊNDIOS FLORESTAIS PARA REGIÃO DE ESTEPE GRAMÍNEO LENHOSA NO ESTADO DO PARANÁ 

Monografia apresentada ao curso de Pós-Graduação em Prevenção e Combate aos Incêndios Florestais, Departamento de Ciências Florestais, Setor de Ciências Agrárias, Universidade Federal do Paraná, como requisito parcial à obtenção do título de Especialista. 

Orientador: Prof. Dr. Antonio Carlos Batista 

Coorientador: Prof. Dr. Alexandre França Tetto 

CURITIBA 

2021 



<!-- Start of picture text -->
ae i i MINISTERIO DA EDUCACGAO<br>AEE+Ty aia it SETOR DE CIENCIAS AGRARIAS<br>eee | se 3 See UNIVERSIDADE FEDERAL DO PARANA<br>iJ — ie PRO-REITORIA DE PESQUISA E POS-GRADUACAG<br>Free ire enter gr e pUG TSE TTS § CURSO DE POS-GRADUACAO PREVENCAO E COMBATE<br>AOS INCENDIOS FLORESTAIS - 40001016353E1<br><!-- End of picture text -->

## TERMO DE APROVACAO 

Os membros da Banca Examinadora designada pelo Colegiado do Programa de Pés-Graduagdo em PREVENCAO E COMBATE AOS INCENDIOS FLORESTAIS da Universidade Federal do Parana foram convocados para realizar a arguigao da Monografia de Especializagao de JOAG FRANCISCO LABRES DOS SANTOS intitulada: Modelagem de variaveis antrépicas para a estimativa de perigo de incéndios florestais para regiao de estepe gramineo lenhosa no estado do Parana , que apds terem inquirido o aluno e realizada a avaliacao do trabalho, sao de parecer pela sua PrPROY Aco ho rito de defesa. A outorga do titulo de especialista esta sujeita a homologagao pelo colegiado, ao atendimento de todas as indicagdes e correcdes solicitadas pela banca e ao pleno atendimento das demandas regimentais do Programa de Pés-Graduacao. 



<!-- Start of picture text -->
Curitiba, 15 de Marco de 2021. ; (<br>10 CARLO TISTA<br>Presidente da Banca Gkaminadora (UNIVERSIDADE FEDERAL DO PARANA}<br>Avaliador Externoa( ARTAMENTO ELOISA DEDE FREITASCIENCIAS MILANIFLORESTAIS UFPR)<br><!-- End of picture text -->

# <sup>GUIMARAKSKAMINSKI</sup> TATIANA<sup>CRISTINA</sup> lrouuveralA 

Avaliador Externo (UFPR / DEPARTAMENTO CIENCIAS FLORESTAIS) 

Av. Pref. Lothario Meissner, 632 - Campus Hl - Jardim Botanico - Curitiba - Parana - Brasil CEP &80 210-17 - Tal (41) 3360-4779 . Femail: tettn@isfnr br 

### **RESUMO** 

A ação antrópica é uma das principais causas de incêndios florestais no mundo. Estruturas como vias de acesso e propriedades são variáveis que representam o perigo de incêndios relacionado à presença humana. Para o manejo correto do fogo, se faz necessária a utilização de um índice de perigo eficiente. Buscando desenvolver ferramentas que subsidiem uma melhor gestão de território, o objetivo desse trabalho foi obter um índice de perigo antrópico baseado em variáveis geográficas, estatísticas e socioeconômicas. A escolha das variáveis independentes do modelo foi realizada por meio do método multivariado de análise de componentes principais. A variável dependente foi a espacialização de focos e ocorrências de incêndios com o uso da estimativa da densidade de Kernel adaptativa. A modelagem do índice de perigo antrópico se deu pela técnica de análise de regressão logística, separando aleatoriamente 60% da base de dados para ajuste e 40% para validação. A qualidade do ajuste foi avaliada por meio do pseudo-R² de Nagelkerke e pela análise da área sob a curva (ASC) característica do receptor (COR) e seu ponto de corte ótimo determinado pelo índice de união (IU) foi testado utilizando uma tabela de contingência para a obtenção dos valores de _skill score_ , acurácia (AC), probabilidade de detecção (POD) e probabilidade de falsa detecção (POFD). O modelo apresentou um pseudo R² de 46% e a análise ASC mostrou que o índice de perigo antrópico possui um poder de discriminação do perigo muito bom. O índice ajustado apresentou distribuição com tendência decrescente no número de pixels por classe e crescente no número de pixels com ocorrências por classe. Após o ajuste de classes de perigo, o índice apresentou um _skill score_ de 0,46, uma AC de 73,56%, uma POD de 79,55% e uma POFD de 29,9% para os 60% do ajuste. Para a validação o modelo apresentou uma AC de 76,6% e um _skill score_ de 0,47. O índice de perigo antrópico mostrou-se eficiente e recomenda-se seu uso devido aos resultados obtidos. 

Palavras-chave: teor de umidade; umidade de equilíbrio; _timelag_ ; _Grass Fuel Moisture Code_ . 

### **LISTA DE FIGURAS** 

|FIGURA 1 - TRIÂNGULOS DA COMBUSTÃO E COMPORTAMENTO DO FOGO. ...... 19|
|---|
|FIGURA 2 - ESQUEMA DA INTEGRAÇÃO DOS FATORES DE PERIGO. ..................... 25|
|FIGURA 3 - LOCALIZAÇÃO DA ÁREA DE ESTUDO ....................................................... 27|
|FIGURA 4 - VEGETAÇÃO DA ÁREA DE ESTUDO ........................................................... 28|
|FIGURA 5 - FLUXOGRAMA DA METODOLOGIA UTILIZADA. .................................... 29|
|FIGURA 6 - DENSIDADE DE KERNEL E DISTRIBUIÇÃO DAS OCORRÊNCIAS<br>REGISTRADAS. ............................................................................................ 38|
|FIGURA 7 - USO DO SOLO PARA ÁREA DE ESTUDO. ................................................... 40|
|FIGURA 8 - VARIÁVEIS CARTOGRÁFICAS. .................................................................... 41|
|FIGURA 9 - DENSIDADE DEMOGRÁFICA (A), RENDA (B) E TAXA DE<br>DESOCUPAÇÃO (C) .................................................................................... 42|
|FIGURA 10 -_BIPLOT_DA ANÁLISE DE COMPONENTES PRINCIPAIS ......................... 44|
|FIGURA 11 - CONTRIBUIÇÃO DAS VARIÁVEIS ORIGINAIS. ....................................... 45|
|FIGURA 12 - CURVA CARACTERÍSTICA DO RECEPTOR PARA O MODELO<br>AJUSTADO. .................................................................................................. 47|
|FIGURA 13 - PROPORÇÃO DE PREVISÕES CORRETAS E INCORRETAS DO ÍNDICE<br>ANTRÓPICO. ................................................................................................ 48|
|FIGURA 14 - ÍNDICE DE PERIGO ANTRÓPICO PARA REGIÃO DA ESTEPE<br>GRAMÍNEO-LENHOSA. .............................................................................. 49|
|FIGURA 15 - DISTRIBUIÇÃO DO NÚMERO DE OCORRÊNCIAS E PIXELS POR<br>CLASSE DE PERIGO PROPOSTA DE HELFMAN (A), AJUSTADO (B) E<br>PERCENTIL EM FUNÇÃO DO ÍNDICE (C). ............................................. 50|
|FIGURA 16 - ÍNDICE DE PERIGO ANTRÓPICO ................................................................ 52|



### **LISTA DE TABELAS** 

|TABELA 1 - VARIÁVEIS INDEPENDENTES IDENTIFICADAS. ..................................... 30|
|---|
|TABELA 2 - TABELA DE CONTINGÊNCIA UTILIZADA ................................................ 35|
|TABELA 3 - PORCENTAGEM DE OCORRÊNCIAS DE INCÊNDIOS POR CLASSE DE|
|USO DO SOLO. ............................................................................................. 43|
|TABELA 4 - AUTOVALORES E VARIÂNCIA PARA CADA COMPONENTE|
|PRINCIPAL. .................................................................................................. 43|



### **SUMÁRIO** 

|**1 INTRODUÇÃO ................................................................................................................... 16**|
|---|
|**2 OBJETIVO .......................................................................................................................... 17**|
|2.1 OBJETIVOS ESPECÍFICOS ............................................................................................. 17|
|**3 REVISÃO DE LITERATURA ........................................................................................... 18**|
|3.1 INCÊNDIOS FLORESTAIS .............................................................................................. 18|
|3.1.1 Condições favoráveis ....................................................................................................... 20|
|3.1.2 Agente causador .............................................................................................................. 21|
|3.2 ÍNDICES DE PERIGO ....................................................................................................... 23|
|3.2.1 Índices meteorológicos .................................................................................................... 23|
|3.2.2 Índices integrados ............................................................................................................ 24|
|**4 MATERIAL E MÉTODOS ................................................................................................ 27**|
|4.1 CARACTERIZAÇÃO DA ÁREA DE ESTUDO .............................................................. 27|
|4.2 PROCEDIMENTOS METODOLÓGICOS ....................................................................... 28|
|4.2.1 Variáveis independentes .................................................................................................. 29|
|4.2.2 Variável dependente ........................................................................................................ 32|
|4.2.3 Geração do modelo logístico ........................................................................................... 33|
|4.2.4 Avaliação da eficiência .................................................................................................... 34|
|**5 RESULTADOS E DISCUSSÃO ........................................................................................ 37**|
|5.1 VARIÁVEIS DO MODELO .............................................................................................. 37|
|5.2 AJUSTE E AVALIAÇÃO DA EFICIÊNCIA DO MODELO ........................................... 46|
|**6 CONCLUSÕES .................................................................................................................... 54**|
|**REFERÊNCIAS ..................................................................................................................... 55**|



16 

### **1 INTRODUÇÃO** 

O fogo, provocado de forma natural ou por ações do homem, é um importante agente de transformação em muitos ecossistemas. A proteção da vida, propriedade e recursos florestais requerem uma gestão cada vez mais eficaz dos incêndios florestais e um sistema de previsão bem estruturado é uma ferramenta fundamental para alcançar esse objetivo. 

Os sistemas de previsão consistem na avaliação e na integração de elementos que propiciam a ocorrência de incêndios, fornecendo índices quantitativos e numéricos sobre o comportamento do fogo. Essas informações alimentam um Sistema de Informações Geográficas que auxilia os gestores na alocação de recursos e proporcionam um aumento na eficiência da proteção do ecossistema de interesse. 

A padronização das escalas de perigo de incêndios e sua consequente integração se fazem necessárias para que um índice represente a probabilidade de ignição com base na relação característica do combustível x causas. Uma vez que os fatores intrínsecos ao material combustível (arranjo, continuidade, teor de umidade), as condições meteorológicas e as principais causas influenciam o início e a propagação de um incêndio. 

A estepe gramíneo-lenhosa, conhecida também como campos gerais ou campos sulinos, está inserida no contexto dos biomas Mata Atlântica e Pampa. É um ecossistema dependente do fogo para conservação de suas espécies e paisagem e possui histórico de utilização econômica como pastagens, com o uso do fogo para sua renovação. Portanto, esse estudo é uma sequência das pesquisas relacionadas ao estudo das variáveis de perigo de incêndios nessa região, mais especificamente no Parque Estadual de Vila Velha (PEVV), situado no estado do Paraná, Brasil. 

O parque é uma unidade de conservação de proteção integral e tem como objetivo principal a manutenção dos remanescentes de estepe gramíneo-lenhosa e apresenta um programa de manejo da vegetação por meio de queimas prescritas com objetivo de conservar e recuperar essa tipologia. 

Além do PEVV, a região dos campos gerais conta outras unidades de conservação como o Parque Nacional dos Campos Gerais (Ponta Grossa, Castro e Carambeí), a Floresta Nacional do Assungui (Campo Largo) e as Reservas Particulares do Patrimônio Natural da Meia Lua (Ponta Grossa), Fazenda Paiquerê (Ponta Grossa), do Tarumã (Palmeira e Campo Largo) e Caminho das Tropas (Palmeira). 

Esse trabalho visa a obtenção de um índice de perigo baseado nos agentes causadores que possibilite a integração com outros índices de perigo. 

17 

### **2 OBJETIVO** 

Obter modelos preditivos de perigo de incêndios florestais baseados em variáveis geográficas, estatísticas e socioeconômicas a fim de estimar a probabilidade de ocorrer incêndios florestais para região de estepe gramíneo-lenhosa circundante ao Parque Estadual de Vila Velha. 

### 2.1 OBJETIVOS ESPECÍFICOS 

- a) identificar as variáveis antrópicas relacionadas ao perigo de incêndios; 

- b) Aplicar técnicas de análise multivariada para escolha das variáveis que explicam melhor o perigo de incêndios para a região; 

- c) Gerar a variável dependente (ocorrências de incêndios) de forma espacializada. 

- d) Utilizar técnicas de geoestatística e de regressão logística para obtenção do índice de causalidade; 

- e) Avaliar a eficiência do índice com base no histórico de ocorrências. 

18 

### **3 REVISÃO DE LITERATURA** 

### 3.1 INCÊNDIOS FLORESTAIS 

O termo incêndio florestal é comumente utilizado no Brasil para definir incêndios que atingem outros tipos de vegetação além das de porte florestal. Soares (1985) definiu incêndio florestal como um fogo incontrolado que se propaga livremente e consome os diversos tipos de material combustível existentes na floresta. 

Potencialmente todos os ecossistemas da Terra possuem um regime de fogo, um histórico que, de alguma forma, afetou a estrutura e a composição das espécies, sendo o fogo um agente biológico que mantém a viabilidade, estrutura e funcionamento equilibrado destes (MYERS, 2006). A influência humana no regime do fogo ocorre em várias vias, incluindo mudança no material combustível, seja na sua estrutura ou continuidade, bem como no uso do fogo em diferentes épocas do ano submetidas a variadas condições meteorológicas. As motivações para o uso do fogo variam consideravelmente desde guerra, gerenciamento hábil de recursos naturais (agricultura, pecuária, silvicultura e gestão da vida selvagem) a proteção de infraestrutura e áreas urbanas (BOWMAN _et al_ ., 2011). 

A ocorrência de incêndios naturais ao longo da história da vida terrestre de forma concomitante com o processo de domesticação do fogo permite concluir que, possivelmente, essa interação gerou efeitos evolutivos evidenciados nos ecossistemas (BOWMAN _et al_ ., 2009; BOWMAN _et al_ ., 2011;). Hardesty _et al_ . (2005) e Myers (2006) classificam os ecossistemas em quatro categorias: sensíveis ao fogo, independentes e dependentes do fogo e inclui ainda os influenciados pelo fogo. Os ecossistemas dependentes do fogo são aqueles que desenvolveram adaptações ao fogo, tornando-se resistentes e são beneficiados pela ação dele. A presença do fogo nesses locais é necessária para preservação das espécies nativas, os habitats dos animais e a paisagem. Porém existem locais onde as espécies não desenvolveram adaptações de resistência ao fogo. São os ecossistemas sensíveis ao fogo, isto é, mesmo com um incêndio de baixa intensidade, a mortalidade é alta. Os ecossistemas independentes do fogo são aqueles onde o fogo não é um dos agentes de maior importância e sua presença é quase desnecessária. Aqueles influenciados pelo fogo incluem os tipos de vegetação que se encontram em zonas de transição entre os dependentes e sensíveis ou independentes do fogo. 

A ocorrência e propagação dos incêndios florestais dependem de fatores que variam em função das características do ambiente, influenciando de forma distinta o fenômeno da combustão (BATISTA, 2000). 



<!-- Start of picture text -->
$ lo)%<br>> (oy<br>© ay<br>%<br>%, vvS<br>a) OX<br>ay XS<br>% + OS<br>BS Ss<br>Sa7 CocL.0<br>s<br>&<br>S$<br><!-- End of picture text -->

20 

### 3.1.1 Condições favoráveis 

Os elementos meteorológicos como: temperatura, umidade relativa, vento e precipitação são fatores decisivos na ignição e na propagação dos incêndios (BATISTA, 2000). O material combustível fino é o que responde de forma mais rápida às variações meteorológicas, variando sua temperatura e ganhando ou perdendo umidade com o ambiente (SOARES; BATISTA; TETTO, 2017). A variação nas condições atmosféricas determina em grande parte como os incêndios se comportam, quando e onde ocorrem, sendo essas variáveis as mais indicadas para o estabelecimento de índices de perigo de incêndios florestais (VÉLEZ, 2009). 

A estação de incêndios florestais geralmente está associada a época do ano em que a temperatura é maior e o período de seca prolongado (FIMIA, 2009). Portanto, as condições meteorológicas, além de determinar a duração da estação de incêndios, exercem influência sobre o desenvolvimento da vegetação, e, na quantidade e arranjo do material combustível (HEIKKILÄ; GRÖNQVST; JURVÉLIUS, 2007). 

A temperatura do ar exerce influência direta na quantidade de calor necessária para elevar o combustível à temperatura de ignição, isto é, sua inflamabilidade (SOARES; BATISTA; TETTO, 2017). Também possui efeito indireto sobre outros fatores como velocidade do vento, umidade relativa e umidade do combustível (SCHROEDER; BUCK, 1970) 

Outro fator de influência importante é o vento. Atrelado às condições de estabilidade atmosférica, o vento é o fator menos previsível, acelerando o processo de secagem do material combustível, principalmente a primeira fase, retirando a umidade presente no ar e a depositada sobre os combustíveis florestais (SOARES; BATISTA; TETTO, 2017). 

A umidade relativa é um indicador em porcentagem da saturação do ar a determinada temperatura e afeta diretamente o conteúdo de umidade do material combustível. Devido as propriedades higroscópicas do material combustível, existe uma troca contínua de vapor d’água com o ambiente desde que não haja influência da precipitação. Esse processo de ganho ou perda de água é regido pela umidade relativa do ar (HEIKKILÄ; GRÖNQVST; JURVÉLIUS, 2007; SOARES; BATISTA; TETTO, 2017; SCHROEDER; BUCK, 1970). 

Segundo Schroeder e Buck (1970), a quantidade de precipitação e sua distribuição ao longo do ano são fatores decisivos no controle e duração das temporadas de incêndios. Mesmo sendo um fator limitante para ocorrência de incêndios, sua influência evidente sobre o fogo acaba por subestimar seu efeito (SOARES; BATISTA; TETTO, 2017). Tetto _et al._ 

21 

(2012), ao analisarem a ocorrência de incêndios florestais de 2005 a 2010 para o estado do Paraná, constataram uma correlação negativa entre número de ocorrências e a precipitação (r= -0,77). Outro estudo realizado para os incêndios ocorridos na região de Telêmaco Borba, comprovou que o maior número de ocorrências de incêndio coincide justamente com o período de menor precipitação (TETTO _et al._ , 2015). 

Qualquer material orgânico, vivo ou morto, incorporado, sobre ou acima do solo, capaz de entrar em ignição e queimar pode ser tratado como combustível florestal. Suas características físicas e químicas determinam a possibilidade de ignição, sendo o ponto essencial para a proteção contra incêndios e o único com possiblidade de atuação preventiva direta (LARA, 2009; SOARES; BATISTA; TETTO, 2017). 

A quantidade de material combustível define se o fogo vai ou não se propagar, seu comportamento e a intensidade de calor liberada pelo processo de combustão (SOARES; BATISTA; TETTO, 2017). O arranjo e a continuidade desse material são fatores determinantes para a quantidade de oxigênio disponível para queima (BYRAM, 1959). Esses dois fatores, alterados de forma equivocada, somados com a estações de fogo severas, aumentam o tamanho, a severidade e a frequência dos incêndios florestais (MILLER _et al_ ., 2009; WESTERLING, 2016). 

O teor de umidade do material combustível é outra variável determinante na ocorrência de incêndios. Para Fuller (1991), é a umidade dos combustíveis mortos e finos que regula a capacidade de ignição e sustentação dos incêndios. A quantidade de água presente na biomassa vegetal, passível a entrar em processo de ignição, é chamada de teor de umidade do material combustível (WHITE, 2018). O conteúdo de umidade do material morto varia bastante, respondendo passivamente às variações meteorológicas, raramente atinge valores menores do que 2% e podendo atingir 300% após ocorrência de precipitação. O teor de umidade presente na vegetação viva possui menor variação, pois além da interação com o ambiente possui processos fisiológicos que estocam ou eliminam umidade na vegetação (SOARES; BATISTA; TETTO, 2017; PYNE, 1984). 

### 3.1.2 Agente causador 

Devido ao fato das causas dos incêndios serem muito variáveis, a FAO adotou uma classificação desenvolvida pelo Serviço Florestal dos Estados Unidos da América. Esse agrupamento tem mostrado bons resultados, contornando o problema da variabilidade e fornecendo dados comparáveis entre si em diversos países. Essa classificação define oito 

22 

grupos de causas: raios, incendiários, queimas para limpeza, fumantes, fogos de recreação, estradas de ferro, operações florestais e diversos (SOARES; BATISTA; TETTO, 2017). 

As principais causas de ocorrências dos incêndios florestais no Brasil são classificadas nos grupos de “incendiários” e “queimas para limpeza”, sendo as ocorrências causadas por “raios” 1,56% do total (SANTOS; SOARES; BATISTA, 2006). Machado _et al_ . (2017) constataram em estudo realizado no Parque Nacional Chapada dos Guimarães, que 46,9% das causas de ocorrências foram classificadas como “incendiários”, 22,2% como “queimas para limpeza” e 11,1% como “raios”. 

Dentre os grupos definidos pela FAO, apenas os incêndios causados direta ou indiretamente por raios são considerados de origem natural, todas as demais são, direta ou indiretamente, de origem antrópica (SOARES; BATISTA; TETTO, 2017). Mesmo com uma menor importância, os incêndios causados por raios tendem a queimar áreas maiores quando comparados com os de origem humana, pois ocorrem em locais mais remotos o que dificulta a detecção e controle (WOTTON; MARTELL, 2005). 

Em muitos países, as atividades humanas são, de várias formas, as maiores responsáveis pelas ocorrências dos incêndios florestais (CHUVIECO _et al_ ., 2010). Apesar da importância dessas atividades, poucos trabalhos são realizados na quantificação do perigo representado pela ação do homem devido à complexidade da variação do comportamento humano no espaço e tempo (MARTÍNES; VEGA-GARCIA; CHUVIECO, 2009; CHUVIECO _et al_ ., 2010). 

Segundo Bouillon e Tedim (2019), o homem deve estar no centro do entendimento dos problemas relacionados aos incêndios florestais. Ainda segundo esses mesmos autores, é importante conhecer com precisão a população que vive no território afetado pelos incêndios, principalmente na interface urbano-florestal. 

De acordo com o Departamento de Agricultura e o Departamento de Interior dos Estados Unidos ( _United States Department of Agriculture -_ USDA e _United States Department of the Interior_ - USDI) (2001), a área de interface urbano-florestal (IUF) ocorre onde as estruturas estão imediatamente ligadas aos combustíveis florestais, com uma densidade de 7 estruturas por hectare e uma linha clara de demarcação entre as construções e os combustíveis florestais.Além da IUF, a área de intermix é caracterizada pela presença esparsa de construções (cerca de uma a cada 16 hectares), sem delimitação clara entre as estruturas e os combustíveis florestais, sendo esses contínuos por toda a área (USDA; USDI, 2001). 

Nesse sentido, a seleção de fatores antropogênicos tem sido o foco dos estudos na modelagem do perigo de incêndios como variáveis associadas às ocorrências causadas pela 

23 

atividade humana. Segundo Vélez (2009), a origem da maioria dos incêndios florestais se dá pelo uso incorreto do fogo, muitas vezes por negligência ou intencional. Essas duas categorias podem ser abordadas considerando a distância e a densidade rodo e ferroviária, linhas elétricas e áreas militares, enquanto os fatores associados ao uso recreativo das áreas estão ligados à presença da interface urbano-rural, hotéis e acampamentos (HOYO; MARTÍN; VEGA, 2008; CHUVIECO _et al_ ., 2010). 

### 3.2 ÍNDICES DE PERIGO 

### 3.2.1 Índices meteorológicos 

Para Soares, Batista e Tetto (2017), o conhecimento do grau de perigo diário é uma ferramenta útil na programação de prevenção e combate aos incêndios florestais. Índices de perigo são indicadores que refletem, antecipadamente, a probabilidade de ocorrer um incêndio, assim como a facilidade do mesmo se propagar, com base nas condições atmosféricas do dia ou de uma sequência de dias (SOARES, 1972). 

A estrutura que compõe os índices de perigo de incêndios meteorológicos é baseada nas variações de fatores relacionados às condições do tempo. Os fatores determinantes do grau de perigo podem ser divididos em duas categorias: permanentes (material combustível, tipologia florestal e relevo) e variáveis (condições meteorológicas). O primeiro grupo é recomendado para se estimar o comportamento do fogo e potencial dano, pois possui maior variação no longo prazo. O grupo dos fatores variáveis constitui uma base sólida na estimativa do grau de perigo, pois apresentam variação no curto prazo (NUNES, 2005; SOARES, 1984). 

Os índices de perigo de incêndio podem ser divididos em dois grupos: índices de ocorrência e de propagação. Os primeiros estimam se existem condições favoráveis ou não para o início da combustão. O segundo grupo incorpora fatores que influenciam o comportamento do fogo estimando as condições de propagação do mesmo (SOARES; BATISTA; TETTO, 2017). 

No Brasil, até o grande incêndio ocorrido no estado do Paraná em 1963, não havia conhecimento da utilização de índices de perigo. Pela dificuldade na obtenção de dados, a partir dessa data foram introduzidos os índices de Angstron e de Nesterov, que para seus cálculos apenas requerem temperatura, umidade relativa do ar e precipitação (SOARES; BATISTA; TETTO, 2017; SAMPAIO, 1999). 

Soares (1972) desenvolveu em 1972 utilizando dados da região central do Paraná, o primeiro índice de perigo de incêndio do país, a Fórmula de Monte Alegre (FMA), utilizada 

24 

em quase todo território nacional e em alguns países da América do Sul. Este índice, também cumulativo, utiliza a umidade relativa do ar, de forma direta, e a precipitação de forma indireta. Outro índice utilizado em diversas regiões do mundo é o Código de Umidade do Combustível Fino ( _Fine Fuel Moisture Code_ - FFMC) do Canadá, sendo um dos componentes primários do índice de perigo canadense. O código é calculado a partir de leituras meteorológicas realizadas às 12 h estima o teor de umidade do material combustível (VAN WAGNER, 1974). 

O índice de perigo de incêndios deve ser um dos fatores fundamentais para a realização de queimas controladas, pois quanto maior o grau de perigo, maior a probabilidade da queima se tornar um incêndio (SOARES; BATISTA; TETTO, 2017). 

### 3.2.2 Índices integrados 

Normalmente, os índices de perigo de incêndios se utilizam das condições atmosféricas para representar o grau de perigo diário. Esses índices possuem modelos matemáticos que a partir de variáveis meteorológicas estimam o valor do teor de umidade do material combustível, um dos fatores mais importantes na modelagem da ignição e comportamento do fogo (CHUVIECO; AGUADO; DIMITRAKOPOULOS, 2004). No entanto, as condições atmosféricas são apenas um dos componentes do perigo de incêndios e mesmo com o grande interesse nos índices meteorológicos, devido a sua operacionalidade, estes possuem dificuldades em encontrar escalas comuns para combinação com outras variáveis de perigo (CHUVIECO; AGUADO; DIMITRAKOPOULOS, 2004; CHUVIECO _et al_ ., 2010). 

Pode-se considerar que a probabilidade de ocorrer um incêndio provém da ocorrência de dois eventos: a presença de condições favoráveis e de um agente causador (fonte de fogo). Sendo os dois eventos independentes, pela regra do produto, a probabilidade de ocorrer incêndio pode ser expressa como (MAGALHÃES; LIMA, 2002; SOARES; BATISTA; TETTO, 2017): 



onde: 

### _P(F∩C) = probabilidade de ocorrer incêndio;_ 

_P(C) = probabilidade de haver condições favoráveis. P(F) = probabilidade de haver um agente causador;_ 



<!-- Start of picture text -->
Fontes de ignicado<br>Perigo de ignicao<br>Teor de umidade<br>do combustivel<br>PERIGO<br>Material<br>combustivel<br>propagacao<br>Condicées<br>meteorologicas<br><!-- End of picture text -->

26 

por quatro módulos: o já mencionado FWI, o sistema de previsão de ocorrência de incêndios ( _Fire Occurrence Prediction_ – FOP), o sistema de previsão do comportamento do fogo ( _Fire Behavior Prediction_ – FBP) e um sistema acessório que fornece dados e informações sobre o teor de umidade dos materiais combustíveis (ainda em desenvolvimento no Canadá) (LAWSON; ARMITAGE, 2008). 

Segundo Chuvieco, Aguado e Dimitrakopoulos (2004), uma das questões críticas no desenvolvimento de um índice sintético de perigo de incêndios é encontrar uma escala comum para representar todas as variáveis responsáveis pela ignição de maneira objetiva. Para que todas as variáveis possam ser integradas, elas devem ser expressas em uma mesma escala de perigo. Alguns autores como Martell, Otukol e Stocks (1987), Vega-García, Let e Adamowicz (1995), Hoyo, Martín e Vega (2008) e Martínez, Vega-García e Chuvieco (2009) propuseram a utilização de modelos logísticos para estimativa do perigo de incêndios baseada nas fontes de ignição, visando padronizar as escalas de perigo. No Brasil, White _et al_ . (2013) propôs um modelo logístico baseado em variáveis meteorológicas para a estimativa do perigo de incêndios florestais em plantios de eucalipto na costa norte da Bahia. 



<!-- Start of picture text -->
560000 580000 600000 620000 640000 660000<br>S &<br>So+ S o<br>N<br>is SS<br>, ” rc)S ~NR<br>S iS)<br>oS N Si]<br>S<br>~o<br><P S A 3<br>S ~<br>SoS o S)So S<br>aS<br>~o<br>SoSoSSs%~= S oo<br>aS o<br>~<br>31:1.300.000 =<br>S Sistema de coordenadas UTM - Fuso 22S S<br>= Datum - SIRGAS 2000 S<br>560000 580000 600000 620000 640000 660000<br><!-- End of picture text -->



<!-- Start of picture text -->
560000 580000 600000 620000 640000 660000 680000 700000<br>3 _~—~ Legenda 3<br>+ See ‘ een S<br>ere) NN) Ae Municipios<br>Oe Re ag TEE OR Drenagem<br>g ON EY Kae MO Massa de agua 3<br>CALE KTS S Vegetacao<br>2 ZSo on 5 re BE Floresta ombrofila mista ~<br>a , S/F, Sele ae HEE Estepe S<br>S NAA AS ROE Ey Ree y pan<br>=‘i A 1:1.100.000 | 3><br>Sistema de coordenadas UTM - Fuso 22 S<br>s Datum - SIRGAS 2000 x<br>=] foal<br>S8<br>=560000 580000 600000 620000 640000 660000 680000 700000 3<br><!-- End of picture text -->



<!-- Start of picture text -->
Grade UTM<br>Fontescartograficas estatisticase e 100x100metros Regsee.Focosee4 deeeouenenss calor.<br>spose Densidade de<br>Variaveis s0cio<br>a Lye Kernel<br>econémicas Espacializacgao :<br>SIG (adaptativo)<br>. Variaveisop ' Variaveldicot6micaaedependente<br>independentes<br>Anilise<br>de componentes<br>principais<br>Amostragem<br>aleatoria<br>Ajuste (60% Validagao<br>dos dados) (40% dos<br>dados)<br><!-- End of picture text -->



<!-- Start of picture text -->
Regressado<br>Logistica<br>Avaliagéo da<br>eficiéncia<br>Probabilidade<br>ocorréncia de<br>incéndio<br><!-- End of picture text -->

30 

Segundo a metodologia proposta por Hoyo, Martín e Veja (2008), foram identificadas 14 variáveis, sendo 11 de origem cartográfica e 3 do tipo estatística. As variáveis independentes cartográficas consistem na distância em quilômetros do ponto ignição/não ignição e as estatísticas seus respectivos valores de interpolação. A TABELA 1 a seguir apresenta os grupos de fatores e suas respectivas variáveis. 

TABELA 1 - VARIÁVEIS INDEPENDENTES IDENTIFICADAS. 

|Fatores|Variável|Descrição|Tipo|Unidade|
|---|---|---|---|---|
||Rodovias|Vias com tráfego intenso de veículos e<br>pessoas.|||
||Ruas|Vias residenciais com tráfego<br>médio/intenso de pessoas.|||
|Negligência e/ou<br>acidente|Estradas rurais<br>Ferrovia|Vias que cortam as zonas de intermix e<br>rural, não são asfaltadas. Aceiros e<br>estradas florestais entram nessa<br>classificação.<br>Os materiais que constituem os trens as<br>ferrovias podem ocasionar incêndios<br>florestais, além da constante manutenção<br>e proximidade com a vegetação.|Cartográfica|km|
||Rede elétrica|Linhas de alta tensão podem causar<br>incêndios através do simples contato<br>com a vegetação seca.|||
||Áreas urbanas|Área densamente povoada, pertencente<br>ao perímetro urbano.|||
||Interface|Componente da interface urbano-<br>florestal.|||
|Transformações<br>|Intermix|Componente da interface urbano-<br>florestal.|||
|socioeconômicas|Cultivos florestais|Áreas identificadas com maciços<br>florestais homogêneos|||
||Densidade<br>demográfica|<br>Número de habitantes por quilômetro<br>quadrado.|Estatística|hab/km²|
||Áreas recreativas|Campings e áreas de turismo rual|||
|Dissuasão da<br>ignição|Observação|Postos das polícias militar, ambiental e<br>rodoviária, bem como do corpo de<br>bombeiros.|||
||Unidades de<br>Conservação|Áreas protegidas|Cartográfica|km|
|Conflitos que|||||
|podem desencadear<br>um incêndio|Renda_per capta_<br>Desocupação|Renda média mensal por habitante<br>Porcentagem da população<br>economicamente ativa que se encontra<br>sem emprego.|Estatística|R$/hab<br>%|



Fonte: adaptado de Hoyo, Martín e Vega (2008), elaborado pelo autor (2021). 

31 

Foram confeccionados mapas temáticos com resolução de 100m x 100m (1 hectare) que permitiram a representação e a quantificação espacial das variáveis independentes vinculadas às atividades humanas. A identificação dessas variáveis baseou-se em análise de literatura referente a este tema (BATISTA, 2000; BATISTA; OLIVEIRA; SOARES, 2002; RIBEIRO _et al_ ., 2008; CHUVIECO _et al_ ., 2010; KOVALSYKI, 2016; MOREIRA; MENDES, SANTOS, 2020). Assim como a metodologia proposta por Hoyo, Martín e Veja (2008), tentou-se escolher, preferencialmente, as variáveis com caráter estrutural e relacionadas a elementos permanentes do território, pela facilidade de obtenção e constância ao longo do tempo. 

O grupo de fatores negligência e/ou acidentes englobam as malhas viária e elétrica presentes na região. Os vetores referentes a malha viária foram obtidos por meio de arquivos disponibilizados pelo IBGE (2019), através do projeto colaborativo de mapeamento _Open StreetMap_ (OSM) e por análises de imagens obtidas do satélite sino-brasileiro CBERS – 04A, com resolução espacial de 2 metros e composição colorida (bandas 01, 02, 03 e pancromática). 

O grupo relacionado de variáveis cartográficas relacionadas às transformações socioeconômicas (área urbana, interface e intermix) foram identificadas seguindo a classificação proposta por Kramer _et al._ (2019) por meio de uma classificação supervisionada do uso do solo feita em imagens do satélite _Landsat_ 8 de composição falsa cor (bandas 07, 06, 04 para áreas construídas e bandas 06, 05, 04 para vegetação). Esse satélite é equipado com o sensor multiespectral OLI ( _Operational Land Imager_ ) e fornece imagens de resolução espacial de 30 metros. 

Os pontos de dissuasão (observação) foram obtidos por meio da localização dos postos da Polícia Militar do Paraná (Força Verde e Corpo de Bombeiros) e da Polícia Rodoviária Federal. As áreas recreativas foram delimitadas com base na distribuição dos acampamentos e estâncias para turismo rural. 

Os vetores de áreas protegidas, incluídas no grupo dos conflitos que podem ocasionar incêndios florestais, foram obtidos através dos arquivos de Unidades Conservação de Proteção Integral do IBGE (2019) e pelo repositório da Secretaria Estadual do Meio Ambiente (SEMA) do estado do Paraná (2021). 

As variáveis do tipo estatística foram espacializadas pelo interpolador da distância inversa ponderada ( _Inverse Distance Weighted_ (IDW)). Esse método estima um valor para algum local não medido utilizando-se os valores amostrados no seu entorno, que terão um maior peso do que os valores mais distantes, ou seja, cada ponto possui uma influência no 

32 

novo ponto, que diminui na medida em que a distância aumenta. Desta forma, a influência de cada ponto é proporcional ao inverso de sua distância (VARGAS _et al_ ., 2018). 

Esse método foi escolhido para a interpolação da densidade demográfica, renda _per capta_ e taxa de desocupação, pois essas variáveis alcançam maiores valores nos centros urbanos e decrescem no sentido zona rural. Essa premissa baseia-se no modelo econômico proposto por Harris e Todaro (1970), no qual propõem que o equilíbrio econômico entre zona rural e cidade ocorre se houver desemprego na zona urbana. Isso ocorre pelo fato da renda ofertada nas cidades brasileiras (indústria e serviços) ser superior a existente no campo, gerando um fluxo migratório no sentido campo-cidade, reduzindo a população rural e aumentando o desemprego nas áreas urbanas (SANTOS; SILVEIRA, 2001; RUSSO; PERRÉ; ALVES, 2016). 

### 4.2.2 Variável dependente 

As variáveis dependentes são as respostas que se espera de um experimento, nesse trabalho são as ocorrências de incêndios. O banco de dados de ocorrências foi compilado com o registro de ocorrência de incêndios da Polícia Ambiental do estado do Paraná, referente ao Parque Estadual de Vila Velha, e com os registros de focos de calor obtidos por meio do satélite de referência do INPE (AQUA M-T) para o período de 2009 a 2017, totalizando 9 anos de observação. Essas fontes foram escolhidas por apresentarem a localização dos registros de ocorrências e focos. Para evitar a repetição de eventos, os dados foram filtrados conforme sua localização, data e horário de registro. 

Outro procedimento adotado para a redução da incerteza sobre o número e localização dos eventos de fogo, foi a retirada de focos que ocorreram em superfícies não vegetadas, assumindo que os incêndios se iniciam em áreas florestais (HOYO, MARTÍN, VEGA, 2008). 

Para se obter uma superfície contínua a partir dos pontos de ocorrências foi empregada a técnica de interpolação da estimativa de densidade de Kernel. Esta técnica consiste em posicionar uma probabilidade de densidade sobre cada ponto de ocorrência e estimar a densidade em cada interseção de uma malha sobreposta de pontos. A função quártica foi utilizada para a estimativa da densidade, bem como um raio de influência adaptativo ( _bandwitdh_ ). Esse processo possibilita maior flexibilidade na estimativa, pois o raio de influência se adapta conforme a concentração dos pontos (BERTOLLA, 2015). 

33 

Tendo em vista que a variável dependente de um modelo de regressão logística é do tipo dicotômica, os valores de densidade foram divididos em duas classes, que representam os valores 0 e 1. Para tal, foi utilizado o critério padrão de classificação por quebras naturais de Jenks (1977), que busca minimizar a variância dentro de cada classe. 

Após a geração da variável dicotômica espacializada, os dados matriciais obtidos foram convertidos para um vetor do tipo ponto com sua respectiva coordenada UTM. A partir destes foram extraídos os valores dos dados raster das variáveis estatísticas densidade demográfica, renda _per capta_ e taxa de desocupação. As distâncias de cada ponto em relação aos vetores das variáveis cartográficas foram obtidas por meio da ferramenta de análise _Nearest Neighbors Join_ do _software_ QGIS 3.16.2 Hannover. 

### 4.2.3 Geração do modelo logístico 

A ocorrência ou não ocorrência de um incêndio florestal é um exemplo de variável dicotômica e a forma mais apropriada de modelar esse tipo de dado é por meio da técnica de regressão logística. O modelo de regressão logística consiste em uma função de ligação que permite o ajuste de um modelo de regressão linear (simples ou múltipla) à uma variável binária (WILKS, 2011). Para esse estudo foi utilizada a função de ligação da família _logit_ definido pelas seguintes equações: 





Onde: 

_y =_ combinação de variáveis independentes; 

_Xn_ = variável independente; 

_βn_ = coeficientes da equação; 

_e_ = base do logaritmo natural (2,71828); 

_P_ = Probabilidade de ocorrer evento. 

Dentre os pressupostos assumidos pela regressão logística, existem alguns que cabem destacar. Modelos logísticos não assumem uma relação linear com a variável dependente e por outra parte, essa não necessita seguir uma distribuição normal, bem como ser homocedástica (WILKS, 2011). No entanto, como toda técnica de análise de regressão, a 

34 

segurança na predição de modelos logísticos é fortemente afetada pela multicolinearidade das variáveis independentes (NAKAMURA, 2013). 

Para evitar a inserção de variáveis que ocasionem o problema da multicolinearidade, se explorou a variância das variáveis independentes por meio da análise de componentes principais (ACP). A ACP consiste em uma análise multivariada que busca transformar um número _p_ de variáveis correlacionadas em variáveis não correlacionadas, as componentes principais. 

A variância de uma matriz de dados necessita de todas as suas _p_ variáveis para ser explicada. No entanto, a variabilidade desse sistema pode ser explicada por um número _n_ menor do que _p_ . ACP tem como objetivo reduzir o número de variáveis por combinações lineares das variáveis originais (componentes principais), resultando na rotação dos eixos do sistema. Essa técnica é muito utilizada na otimização de modelos para redução de variáveis independentes em análises de regressão (TABACHNICK; FIDEL, 2013). Foram escolhidas as componentes principais que melhor explicaram a variância dos dados seguindo o critério de Kaiser, no qual as componentes com autovalor superior a 1 devem ser escolhidas (TABACHNICK; FIDEL, 2013). Outro critério utilizado foi a seleção das variáveis que apresentaram a maior contribuição na explicação da variância dentro da primeira componente principal, pois essa consiste na combinação de todas as variáveis e explica a maior variância nos dados. 

O modelo do índice de perigo antrópico foi ajustado pelo método da máxima verossimilhança. 

### 4.2.4 Avaliação da eficiência 

O pseudo-R² de Nagelkerke foi avaliado e os valores estimados pelo índice de perigo antrópico forami submetidos à análise da Área Sob a Curva Característica de Operação do Receptor (ASC e COR), método muito utilizado para discriminar capacidade preditiva de modelos logísticos (JOLLIFFE; STEPHENSON, 2012; NAKAMURA, 2013). 

Uma curva COR ideal para previsões perfeitas deve possuir área igual a 1, sendo análogo ao coeficiente de determinação (R²) para regressões lineares. No entanto a relação entre a precisão da previsão e o valor da ASC podem ser classificados da seguinte forma: 0,5 - 0,6 (fraca), 0,6 - 0,7 (média), 0,7 - 0,8 (boa), 0,8 - 0,9 (muito boa) e 0,9 - 1 (excelente) (HOSMER; LEMESHOW, 1980; POURGHASEMI, 2015). 

35 

O processo de ajuste do índice antrópico foi realizado utilizando a metodologia proposta por Helfman, Straub e Deeming _._ (1980) que busca um comportamento no qual o maior número de pixels classificados como ocorrência de incêndios se concentre na classe de perigo “Muito alto”. Esse método consiste em determinar o limite inferior de cada classe com base nos percentis das estimativas. Os valores propostos são os seguintes: 

- a) Muito alto:valor do índice que representa 97º percentil das estimativas; 

- b) Alto: valor do índice que representa 90º percentil das estimativas; 

- c) Médio: 50% do valor do índice que representa 90º percentil das estimativas; 

- d) Baixo: 25% do valor do índice que representa 90º percentil das estimativas; 

- e) Nulo: zero. 

A eficiência das previsões do índice foi avaliada utilizando método de verificação de 

previsões dicotômicas (JOLLIFFE; STEPHENSON, 2012). Esse método consistiu na construção de uma tabela de contingência que contém os valores observados e os valores previstos para ocorrências de incêndios florestais (TABELA 2). 

<u>TABELA 2 - TABELA DE CONTINGÊNCIA UTILIZADA</u> 

|**Evento**||**Observado**<br>**Total previsto**<br> <br>|
|---|---|---|
|||<br>**Incêndio**<br>**Não incêndio**|
|Previsto|Incêndio|_a_<br>_b_<br>_N2 = a+ b_|
||Não incêndio|_c_<br>_d_<br>_N4 = c+ d_|
|TotalObservado||_N1 = a +c_<br>_N3 = b +d_<br> _N= a +b +c +d_|



Nota: a = acertos; b = alarmes falsos; c = erros; d = negativos corretos; N = número total de amostras. Fonte: Sampaio e Soares (2000). 

Os critérios de avaliação de performance recomendadas por Jolliffe e Stephenson (2012) e Sampaio e Soares (2000) são os seguintes: 

- a) Acurácia ou porcentagem de sucesso (AC): trata-se da porcentagem de acertos na previsão em relação ao total observado dada pela fórmula (a + d) / N; 

- b) Probabilidade de detecção (POD): também conhecida como sensibilidade, é a proporção de ocorrências corretamente previstas, dada pela fórmula  a / (a + c); 

- c) Probabilidade de falsa detecção (POFD): também conhecida como 1- especificidade, é a proporção de não-ocorrências previstas incorretamente, obtida por meio da fórmula b / (d + b); 

- d) _Skill score_ (SS): proposto por Sampaio e Soares (2000), é a razão da diferença entre os acertos na previsão (G = a + d) e o número esperado de acertos (H  = N x (1 – p) * (1 – q) + N x p * q; onde: p = N1 / N e q = N2 / N) é a diferença entre o número de dias observados (N) e o número de acertos (SS = (G - H) / (N – H)). 



<!-- Start of picture text -->
UI = (POD — ASC| + |(1 — POFD) — ASC|)<br><!-- End of picture text -->

37 

### **5 RESULTADOS E DISCUSSÃO** 

### 5.1 VARIÁVEIS DO MODELO 

Foram registradas 758 ocorrências entre focos de calor e ocorrências de incêndios, entre focos de calor e ocorrências registradas, uma média de 84,22 incêndios por ano. Esse valor é menor do que o valor médio 397,5 ocorrências registradas por Kovalsyki _et al._ (2014) para Ponta Grossa de 2006 a 2014. Essa situação pode ser explicada pela diferença na compilação do banco de dados no qual os autores utilizaram o banco de dados do Corpo de Bombeiros do estado do Paraná, que não possui geolocalização na maioria das ocorrências. Outra possibilidade é a inclusão de ocorrências em vegetação dentro da área urbana, que contribuiu para o aumento da média anual de incêndios. 

O ano com maior número de registros foi 2011 com 119 ocorrências com redução para abaixo da média em 2012 (71 ocorrências) e retomada da tendência de subida a partir desse ano. Esses valores corroboram com os valores e tendência encontrados por Kovalsyki _et al._ (2014) e Santos (2020) para a mesma região. 

Os meses de agosto e setembro concentraram 52,30 % das ocorrências registradas, confirmando que a alta estação de incêndios abrange, principalmente, o período do inverno, como constatado por Vosgerau _et al._ (2006), Tetto _et al._ (2012), Kovalsyki _et al._ (2014) e Santos (2020). Segundo Deppe _et al._ (2004), outono, inverno e primavera são as estações com maior propensão a ocorrência de incêndios florestais no Paraná, pois trata-se de um período associado à baixa precipitação e ocorrências de geadas,que reduzem o teor de umidade do material combustível. 

A FIGURA 6 apresenta as ocorrências de incêndios espacializadas e o resultado da estimativa da densidade de Kernel. 



<!-- Start of picture text -->
7249000 7229000 7200000 7189000<br>n<br><I<br>22M=eao a&&= ro]_—3<br>ees TST es 2S<br>ST SEBS AT 25a<br>o | oe Ss = o<br>Ss ooOo=z Bvesecn S 2 Ss<br>S on a 2 & O<br>31/8 -L él Zee fe<br>+5<br>eS) &<br>6 5<br>os<br>BaoO<br>¢ Ss<br>ri &<br>} 1}<br>=:2<br>,a 3<br>Va<br>So Ss<br>So Sc<br>3<br>N=}a u nNwe<br>| 2<br>6 7 S<br>So \ ao<br>8S<br>a) i= wo<br>oO= 7No}<br>al vay<br>0000bZL 0000zZL 0000072 00008TL<br><!-- End of picture text -->

39 

Pode-se observar que as áreas de alta concentração de incêndios se localizam próximas às áreas urbanas e ao Parque Estadual de Vila Velha. Pelo critério de quebras naturais de Jenks (1977), os valores estimados da densidade de Kernel acima de 0,195 foram considerados como incidência de incêndios. 

Para uma melhor interpretação dos resultados, as FIGURAS 7, 8, 9A, 9B e 9C apresentam a espacialização das variáveis independentes avaliadas. 

A FIGURA 7 apresenta a classificação do uso do solo por meio das imagens obtidas do satélite _Landsat_ 8. Foram identificadas oito classes de uso do solo para a região, sendo elas: floresta ombrófila mista, estepe-gramíneo-lenhosa, _Pinus_ sp., _Eucalyptus_ sp., cultura temporária, solo exposto, pastagem e área construída. 

A floresta ombrófila mista foi a classe mais encontrada nesse levantamento, com 177.739,6 ha, corroborando com os resultados encontrados por Accioly (2013) para essa região. Foram classificados 89.638,7 ha na classe estepe gramíneo-lenhosa, enquanto os reflorestamentos de _Pinus_ sp. apresentaram 20.936,4 ha, abaixo dos 30.470,7 ha encontrados por Eisfeld e Nascimento (2015) para região. Esses mesmos autores mapearam os plantios de _Eucalyptus_ sp. para o estado do Paraná e encontraram 5.377,5 ha, acima dos 4.231 ha encontrados nesse estudo.  As culturas temporárias ocupam uma área de 66.196,7 ha e as pastagens 56.575,5 ha. A área total construída encontrada para os três municípios foi de 17,595,1 ha. 

A FIGURA 8 apresenta as variáveis cartográficas e as FIGURAS 9A, 9B e 9C as variáveis cartográficas avaliadas para a composição do modelo logístico. Sobre os aspectos socioeconômicos da região estudada houve uma mudança significativa na renda média dos habitantes de Ponta Grossa, que em 2000 era de R$ 1.041, 93 e subiu para cerca de R$ 2.800,00 em 2010 (IBGE, 2004; IBGE, 2011). Segundo Hilgemberg _et al_ . (2007) a renda mensal média dos habitantes de Palmeira era de R$ 914,17 e aumentou para R$ 2.285,80 em 2010. A densidade demográfica de Ponta Grossa saiu de 151 para 172,9 hab/km², indicando um crescimento populacional (IBGE, 2011). 

Um dado importante de se relatar é a mudança na contribuição de cada setor da economia para o Produto Interno Bruto (PIB) municipal. Em 2007, a agricultura contribuía com 6% do PIB de Ponta Grossa enquanto o setor de serviços contribuía com 35% e o industrial com 58%. Em 2010, a contribuição do setor agrícola caiu para 2,3%, o industrial para 35,5% e o setor de serviços saltou para 62,2% (HILGEMBERG _et al_ ., 2007; IBGE, 2011). Essa proporção corrobora com o modelo proposto por Harris e Todaro (1970) e pode ser confirmada com o fato de Ponta Grossa apresentar maior taxa de desocupação. 



<!-- Start of picture text -->
: 7240000 722004) TIMED TIROOOG :<br>g3 ,<br>Es cl<br>2 F 2 g<br>258<br>‘uy 36s 5 3 « F 2 32 5<br>a= = I — a ><br># 2 = & au av 8 <K = a =<br>|oO tan aswD fis es ii wm 25<br>a $82.5 Bs : eas<br>2 cP HESS BRE ee ee 2a<br>a= oe ancca&égé 28S re pee Ff<br>= és iaii Pia! Z<br>nee 7 ee Me a, a<br>Feet eee eee eet gee 2<br>—_—t het 2 on ie oe ay F iy ; a, 13<br>: ‘ et, ig<br>as me it ety - “Se “ 4 Bel . ieee “Fa<br>1 al i i ot ee 2) ee i Ss Sr ee gee be J ie<br>& a dete. eee a ee aeeA nate ae Ste s<br>ghee, CT a Pa tar | big A ee <b a Pee. oe eratae<br>7 J ge pegle ,<br>E Ye aea g<br>i.<br>OORT OOOOE EL DOOM L OOD0S1h<br><!-- End of picture text -->



<!-- Start of picture text -->
S 7240000 7220000 7200000 7180000 S<br>F< i om| | AR Aa<br>; eS as A<br>News re )<br>| rR. |<br>, ARG , Mee a@ ALK a<br>4 Y ING : re : é<br>-<br>0000¢7L 000077L 000007Z 0000812<br><!-- End of picture text -->



<!-- Start of picture text -->
560000 580000 600000 620000 640000 660000 680000 700000 720000 740000 760000<br>g<br>co]<br>~<br>So<br>a Legenda<br>g<br>Se [| Municipios<br>ag<br>2 (A) Densidade demografica<br>WN < 20 habkm?<br>=<br>1) 20 a 40 hab/km?<br>.<br>S<br>40 a 60 hab/km?<br>7<br>60 a 80 hab/km? a<br>&<br>I) 80 a 180 hab/km? S<br>WB 1145,1179 ~<br>8<br>(B) Renda S<br>MM < Rs 2.300,00 4<br>I) RS 2.300,00 a R$ 2.600,00 S<br>o<br>R$ 2.600,00 a R$2.700,00 :<br>"| R$ 2.700,00 a R$ 3000,00<br>MH > Rs 3.000,00 Co<br>2<br>(C) Desocup¢aox =<br>3 MN < 4.0%<br>| 4,0.25,0%<br>gSSe 5,0 a 6,0%<br>MB >6,0%<br>So<br>Ss<br>gS<br>So 1:1.450.000<br>~ Sistema de coordenadas UTM - Fuso 22S<br>Datum SIRGAS 2000<br>560000 580000 600000 620000 640000 660000 680000 700000 720000 740000 760000<br><!-- End of picture text -->

43 

<u>TABELA 3 - PORCENTAGEM DE OCORRÊNCIAS DE INCÊNDIOS POR CLASSE DE USO DO SOLO.</u> 

|**Classe**|**Nº de ocorrências**|**%**|
|---|---|---|
|Estepe gramíneo-lenhosa|277|36,54|
|Floresta ombrófila mista|211|27,84|
|Cultura Temporária|133|17,55|
|Pastagem|81|10,69|
|_Pinus_sp.|41|5,40|
|_Eucalyptus_sp.|15|1,98|
|**Total**|**758**|**100**|



Fonte: INPE (2021), elaborado pelo autor (2020). 

A estepe gramíneo-lenhosa foi a classe mais atingida pelas ocorrências de incêndios, com 36,54% seguida da floresta ombrófila mista com 27,84%. A classe menos atingida foi a de reflorestamento com _Eucalyptus_ sp. com 15 registros, totalizando 1,98% do total. Os valores encontrados para floresta ombrófila mista são semelhantes aos 31,10% para área de “mata” e os de estepe gramíneo- lenhosa com os 30,30% para áreas de “vegetação rasteira” encontrados por Vosgerau _et al._ (2006). Kovalsyki _et al._ (2014) também encontrou valores próximos de ocorrências em “vegetação rasteira” com 40 %. 

A TABELA 4 a seguir contém as estatísticas de autovalores e variância para cada componente principal (CP). 

TABELA 4 - AUTOVALORES E VARIÂNCIA PARA CADA COMPONENTE PRINCIPAL. 

|**CP**|**Autovalor**|**Variância**|**Acumulada (%)**|
|---|---|---|---|
|1|5,54|36,95|36,95|
|2|2,79|18,61|55,56|
|3|2,11|14,09|69,65|
|4|1,06|7,07|76,72|
|5|0,89|5,96|82,68|
|6|0,73|4,85|87,53|
|7|0,49|3,24|90,76|
|8|0,36|2,40|93,16|
|9|0,27|1,79|94,95|
|10|0,24|1,60|96,56|
|11|0,18|1,22|97,77|
|12|0,14|0,92|98,69|
|13|0,10|0,65|99,34|
|14|0,07|0,48|99,82|
|15|0,03|0,18|100,00|



Fonte: elaborado pelo autor (2021). 

Pelo critério de Kaiser, apenas as CPs que apresentaram autovalor acima de 1 são recomendadas para a continuidade da análise. Logo, as componentes principais 1, 2, 3 e 4 devem ser utilizadas e o restante descartado. Com os resultados obtidos é possível observar que a primeira componente apresentou 36,95% da variância total dos dados, enquanto a 



<!-- Start of picture text -->
1<br>UCs<br>e<br>0.8 Renda<br>e<br>0,6 Cultivos florestais e Area. recreativa<br>e<br>Desocupaciio Densidade. e<br>0.4 ° e Ferroviaaaa<br>e<br>0.2 Rede elétrica<br>e<br>aM9 Interface:<br>oO . e<br>Area Urbana @<br>Fetrad ;<br>0.2 stradase rurais Dissuasioe°<br>Ruas<br>-0.4 Intermix_ @podovia<br>e<br>-0.6<br>-0.8<br>-1<br>-1 -0.8 -0.6 -0.4 -0.2 0 0,2 04 0,6 0,8 1<br>CP1<br><!-- End of picture text -->



<!-- Start of picture text -->
18<br>16<br>14<br>12<br>10<br>8<br>=. ~ o-oo<br>+--+ +--+.<br>‘<br>4<br>2<br>0<br>s & Pot ss Ss Ss . cS °es ee Ss SF ses<br>pe ~ s res & e ” » s<br>e we Vos Os<br>fe<br><!-- End of picture text -->

y = —0,3793395 — 0,1577199AU + 0,0141263DI/S + 0,0581409/F — 0,1249078RU 

+ 0,2785750RV — 0,0463450FV + 0,1105361/M 

7 PERIGO = 100 ( (1 + ~~,~~ e-)) ) 



<!-- Start of picture text -->
3 0,6 a<br>0 Ol 02 03 O4 O55 06 0,7 O08 09 1<br>1-Especificidade<br><!-- End of picture text -->



<!-- Start of picture text -->
560000 580000 600000 620000 640000 660000 680000 700000<br>S Ss)<br>Legenda<br>+><br>&[] Municipios—— S<br>= || Negativo correto | |8<br>NS<br>gFalso negativo S<br>I) Positivo correto<br>S 3<br>SoN BB Falso alarme SS<br>aa o<br>i=] —<br>S A x<br>fora) S<br>“4os 1:1.100.000 S-<br>Sistema de coordenadas UTM- Fuso 22S<br>s Datum - SIRGAS 2000 =<br>560000 580000 600000 620000 640000 660000 680000 700000<br><!-- End of picture text -->



<!-- Start of picture text -->
S 7240000 7220000 7209000 7189000 g<br>op)<br>N<br>N<br>i] 2<br>8 2Ss iza)<br>x 5 Ss S<br>s}}/§ = s Sar m aun- ek Re a<br>= 5) 2 moccoeSr82 oOBeesSoo SCS e,PSn < S<br>S So ‘o = —) oO S<br>me] ui Li <A mn Sa<br>TSO 000 O00 <i<br>T5%<br>u 668<br>, d Oo s<br>, OS<br>BaoO<br>ion]<br>5<br>Na) . — 7<br>N<br>Ss<br>K<br>Nor No}<br>a<br>}<br>é<br>CSS “ . So@<br>a4<br>: Ss -<br>c—) ; <_< ScSe<br>ow ww<br>Sc cS<br>a) wy<br>OOOUPTL O000TTL O0000TL 00008TL<br><!-- End of picture text -->



<!-- Start of picture text -->
°<br>50<br>40<br>& 30<br>20<br>10<br>0<br>Nulo Baixo Médio Alto Muito Alto<br>@Pixeis com ocorréncia—_& Pixel por classe<br>35<br>*°<br>25<br>20<br>Ss<br>co<br>15<br>10<br>5<br>0<br>Nulo Baixo Médio Alto Muito Alto<br>@Pixeis com ocorréncia —_& Pixel por classe<br>100<br>90 87°<br>80<br>0 el '<br>= 60<br>= 51°<br>i H !<br>2 ' ' |<br>* 40 ! | !<br>20<br>10<br>0 H H H H<br>0 0,2 04 0,6 0,8 l<br>indice de perigo antropico<br><!-- End of picture text -->

51 

Pode se observar que os percentis propostos por Helfman, Straub e Deeming (1980) desajustam a distribuição de pixels com ocorrência e de pixels por classe. No entanto, o mesmo autor recomenda que os limites de classes devem ser determinados pelo manejador florestal e baseados na sua experiência com relação ao local. Para esse estudo os percentis escolhidos para limites inferiores foram zero para a classe “nulo”, 25º para a classe “baixo”, 51º para classe “médio” (ponto de corte), 71º para classe “alto” e 87º para “muito alto” (FIGURA 15C). Esse ajuste permitiu alcançar a premissa de Helfman, Straub e Deeming (1980). Tetto _et al._ (2010) realizaram este mesmo procedimento para o ajuste dos valores das classes de perigo da FMA e consideraram as seguintes condicionantes: i) minimizar o número de dias no período, nas classes de perigo “Alto” e “Muito alto”; e ii) maximizar a correlação entre a ocorrência de incêndios e as classes “Alto” e “Muito alto”. 

Alguns autores como Nunes _et al._ (2010) afirmam que a melhor distribuição do número de pixels por classe seja decrescente da classe “nulo” para a classe “muito alto”. Contudo, considerando que o ponto de corte divide as estimativas em ocorrência e não ocorrência de incêndios há de se supor que esse valor represente o “centro” da escala e que um maior número de dias se concentre nas classes “baixo” e “médio” e decresça sentido “nulo” e “muito alto”. 

Wendling _et al._ (2012) afirmaram que a distribuição ideal da quantidade de dias por classe de perigo deve seguir uma distribuição normal, Viegas _et al._ (2004) apontaram que a quantidade de dias esperada na classe “muito alto” não deve exceder 5%. Alexander (2008) ao revisar as classes do FWI para a região de savana na Nova Zelândia, relatou que as classes de perigo “Baixo”, “Moderado”, “Alto” e “Extremo” devem seguir a distribuição de frequência decrescente de 45%, 30%, 20% e 5%, respectivamente. No entanto, Andrews e Bradshaw (1997), Andrews, Loftsgaarden e Bradshaw (2003) e de Jong _et al._ (2016) confirmaram que a distribuição de pixels por classe de perigo aproxima-se da normalidade. 

A FIGURA 16 apresenta o índice de perigo antrópico espacializado com base na divisão de classes. 



<!-- Start of picture text -->
S>7249000 7229000 7200000 7189000 S—<br>g<br>Nn<br>N<br>N<br>a<br>° =}<br>wn 2 py<br>2 Qo. a)<br>& 3s <j ><br>S & a =sS<br>28 & e 9 aN<br>S SB € Sleep = N S<br>S= Sso>2 eHPZ2HNBs BPxHeB45 ee)Sa < S=<br>E]| 0 F Sa0 [gs<br>SUéil ui <a<br>& XAG EG<br>~ OD<br>=v !<br>5° &<br>Se<br>ae)<br>gao<br>3<br>Sp)<br>S o fo]S<br>5=<br>aSo aQSo<br>SS<br>=<br>S<br>oO eo<br>oS cS<br>S<br>wy woEs<br>S S<br>S<br>ww al<br>0000P7L 000077L 000007L 000081L<br><!-- End of picture text -->

53 

O índice de perigo antrópico alcançou um desempenho muito bom na discriminação de pixels com ocorrência de incêndios apresentando parâmetros de avaliação iguais ou superiores aos encontrados na literatura, possibilitando o planejamento de ações de prevenção e combate. 

Cabe salientar que a equação logística apresentada nesse estudo já converte a probabilidade de incêndios para porcentagem e, como esse índice futuramente poderá ser integrado com outro índice baseado em variáveis meteorológicas, essa conversão não é necessária. Como a resolução da espacialização foi de 100 metros (1 ha) por pixel é de suma importância novo ajuste e determinação de quais variáveis independentes serão incluídas no modelo para a representação do índice de perigo antrópico em maior escala. 

54 

### **6 CONCLUSÕES** 

Com base nos resultados obtidos a metodologia para determinação do perigo devido à presença humana mostrou-se adequada. Os parâmetros obtidos demonstraram um desempenho muito bom do índice de perigo antrópico quando comparado com outros trabalhos. 

A utilização de métodos multivariados como a análise de componentes principais mostrou resultados satisfatórios na escolha de variáveis independentes para o modelo. As variáveis socioeconômicas apresentaram bom ajuste com a variável dependente. Contudo, recomenda-se continuidade nos estudos para padronização de variáveis, pois a técnica de regressão logística permite a utilização de variáveis categóricas. 

O método de espacialização pela estimativa da densidade de Kernel mostrou-se acertado, pois reduziu a incerteza com relação à localização dos focos e ocorrências de incêndios. 

Por fim, recomenda-se o uso do índice de perigo antrópico para a região da estepe gramíneo-lenhosa e como componente de um índice de perigo integrado de incêndios. 

55 

### **REFERÊNCIAS** 

ACCIOLY, P. **Mapeamento dos remanescentes vegetais arbóreos do estado do Paraná e elaboração de um sistema de informações geográficas para fins de análise ambiental do estado** . 2013. 127 f. Tese (Doutorado em Engenharia Florestal) Universidade Federal do Paraná, Curitiba. 

ALEXANDER, M.E. **Proposed revision of fire danger class criteria for forest and rural areas inNew Zealand** . 2nd Edition. National Rural Fire Authority, Wellington, in association with Scion, Rural Fire ResearchGroup, Christchurch. 62 p., 2008. 

ALVARES, C. A.; STAPE, J. L.; SENTELHAS, P. C.; GONÇALVES, J. L. M.; SPAROVEK, G. Köppen’s climate classification map for Brazil. **Meteorologische Zeitschrift** , v. 22, n. 6, p. 711 – 728, 2013. 

ANDREWS, P. L.; BRADSHAW, L. S. **FIRES: Fire Information Retrieval and Evaluation System: A program for fire danger rating analysis** . US Department of Agriculture, Forest Service, Intermountain Research Station, 1997. 

ANDREWS, P. L.; LOFTSGAARDEN, D. O.; BRADSHAW, L. S. Evaluation of fire danger rating indexes using logistic regression and percentile analysis. **International Journal of Wildland Fire** , v. 12, n. 2, p. 213-226, 2003. 

BATISTA, A. C. Mapas de risco: uma alternativa para o planejamento de controle de incêndios florestais. **Floresta** , Curitiba, v. 30, n. 1, p. 45 - 54, 2000. 

BERTOLLA, J. M. **Técnicas de análise de dados distribuídos em áreas** . 2015. 46 f. Dissertação (mestrado) - Universidade Estadual Paulista Júlio de Mesquita Filho, Instituto de Biociências de Botucatu, 2015. 

BORGES, T. S., FIEDLER, N. C., SANTOS, A. R., LOUREIRO, E. B., MAFIA, R. G. Desempenho de alguns índices de risco de incêndios em plantios de eucalipto no norte do Espírito Santo. **Floresta e Ambiente** , v. 37, n. 92, p. 535 - 543, 2017. 

BOUILLON, C.; TEDIM, F. Fires at the urban-forest interface: methodological and management issues. **Os incêndios florestais: em busca de um novo paradigma: II Diálogo entre Ciência e Utilizadores** , 2019. 

BOWMAN D. M.; BALCH J. K.; ARTAXO P.; BOND W. J.; CARLSON J. M.; COCHRANE M. A.; D'ANTONIO C. M.; DEFRIES R. S.; DOYLE J. C.; HARRISON S. P.; JOHNSTON F. H.; KEELEY J. E.; KRAWCHUK M. A.; KULL C. A.; MARSTON J. B.; MORITZ M. A.; PRENTICE I. C.; ROOS C. I.; SCOTT A. C.; SWETNAM T. W.; VAN DER WERF G. R.; PYNE S. J. Fire in the Earth system. **Science** , Washington, v. 324, p. 481 – 484, 2009. 

BOWMAN D. M.; BALCH J. K.; ARTAXO P.; BOND W. J.; CARLSON J. M.; COCHRANE M. A.; D'ANTONIO C. M.; DEFRIES R. S; JOHNSTON F. H.; KEELEY J. E.; KRAWCHUK M. A.; KULL C. A.; MACK, M.; MORITZ M. A.; PYNE, S.; ROOS C. I.; SCOTT A. C.; SODHI, N. S.; SWETNAM T. W. The human dimension of fire regimes on Earth. **Journal of Biogeography** , v. 38, n. 8, p. 2223 - 2236, 2011. 

56 

BROWN, A. A.; DAVIS, K. P. **Forest fire** : control and use. 2.ed. New York: McGraw Hill, 1973. 686 p. 

BYRAM, G.M. Combustion of forest fuels. In: DAVIS, K.P. **Forest fire:** control and use. New York: Mc Graw Hill, 1959. 

CHUVIECO, E.; AGUADO, I.; YEBRA, M.; NIETO, H.; JAVIER SALAS, J.; MARTÍN, M. P.; VILAR, L.; MARTÍNEZ, J.; MARTÍN, S.; IBARRA, P.; LA RIVA, J.; BAEZA, J.; RODRÍGUEZ, F.; MOLINA, J.R.; HERRERA, M. A.; ZAMORA, M. Development of a framework for fire risk assessment using remote sensing and geographic information system technologies. **Ecological Modelling** , v. 221, p. 46 – 58, 2010. 

DE JONG, M.C; WOOSTER, M.J.; KITCHEN, K.; MANLEY, C.; GAZZARD, R.; MCCALL, F.F. Calibration and evaluation of the Canadian Forest Fire Weather Index (FWI) System for improved wildland fire danger rating in the United Kingdom. **Nat. Hazards Earth Syst. Sci** , v. 16, n. 1, p. 1217 – 1237, 2016. 

DE VARGAS, T.; GOMES; M. G., BELLADONA, R.; ADAMI, M. V. D. Aplicação do Interpolador IDW para Elaboração de Mapas Hidrogeológicos Paramétricos na Região da Serra Gaúcha. **Scientia cum Industria** , v. 6, n. 3, p. 38-43, 2019. 

DEPARTAMENTO DE AGRICULTURA DOS ESTADOS UNIDOS (USDA); DEPARTAMENTO DE INTERIOR DOS ESTADOS UNIDOS (USDI). Urban wildland interface communities within vicinity of Federal lands that are at high risk from wildfire. **Federal Register** , v. 66, n. 3. p. 751–777, 2001. 

DEPPE, F.; PAULA, E. V.; MENEGHETTE, C. R.; VOSGERAU, J. Comparação dos índices de risco de incêndio florestal com focos de calor no estado do Paraná. **Floresta** , Curitiba, v. 34, n. 2, p. 119 – 124, 2004. 

DUANE, A.; PIQUÉ, M.; CASTELLNOU, M.; BROTONS, L. Predictive modelling of fire occurrences from different fire spread patterns in Mediterranean landscapes. **International journal of wildland fire** , Washington DC, v. 24, n. 3, p. 407 - 418, 2015. 

FAO – Food and Agriculture Organization. **Manejo del fuego: principios y acciones estratégicas. Directrices de caráter voluntario para el manejo del fuego** . Documento sobre el manejo del fuego n. 17: Roma. 70p. 2007. 

FIMIA, J. C. M. Fatores meteorológicos. In: VÉLEZ, R. (Ed.). **La defensa contra incendios forestales** : fundamentos y experiências. Madrid: Mcgraw-Hill; 2009. 

FULLER, M. **Forest fires** : An introduction to wildland fire behavior, management, firefighting, and prevention. Nova Iorque: Wiley Nature Editions, 1991. 

GODOY, M. M.; MARTINUZZI, S.; KRAMER, H. A.; DEFOSSÉ, G. E.; ARGAÑARAZ, J.; RADELOFF, V. C. Rapid WUI growth in a natural amenity-rich region in central-western Patagonia, Argentina. **International Journal of Wildland Fire** , [S.I.], v. 28, p. 473-484, 2019. 

HARDESTY, J.; MYERS, R. L.; FULKS W. Fire, ecosystems, and people: a preliminary assessment of fire as a global conservation issue. **The George Wright Forum** , Hancock, v. 22, n. 4, p. 78-87, 2005. 

57 

HEIKKILÄ, T. V.; GRÖNQVST, R.; JURVÉLIUS, J. **Wildland fire management** : handbook for trainers. Helsinki, 2007. 

HELFMAN, R. S.; STRAUB, R. J.; DEEMING, J. E. **User's guide to AFFIRMS: time-share computerized processing for fire danger rating** . Intermountain Forest and Range Experiment Station, 1980. 

HILGEMBERG, E. M.; HILGEMBERG, C. T.; STEGE, A.; TOLEDO, A.; SILVA, T. Perfil Sócio-Econômico de Ponta Grossa. **Revista Economia & Tecnologia** , v. 3, n. 4, 2007. 

HOSMER, D. W.; LEMESHOW, S. Goodness of fit tests for the multiple logistic regression model. **Communications in statistics-Theory and Methods** , v. 9, n. 10, p. 1043-1069, 1980. 

HOYO, L. V.; MARTÍN, M. P.; MARTÍNEZ-VEGA, J. Empleo de técnicas de regresión logística para la obtención de modelos de riesgo humano de incendio forestal a escala regional. **Boletín de la A.G.E** . 2008. 

IBGE. **Organização do território** . 2019. Disponível em: < https://www.ibge.gov.br/geociencias/organizacao-do-territorio.html>. Acesso em: 05 nov. 2020. 

INSTITUTO ÁGUA E TERRA (IAT). **Dados e informações geoespaciais temáticos** . 2020. Disponível em: < http://www.iat.pr.gov.br/Pagina/Dados-e-Informacoes-GeoespaciaisTematicos>. Acesso em: 20 dez. 2020. 

INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). **Base de informações do censo demográfico de 2010** : resultados do universo por setor censitário. Rio de Janeiro, 2011. 

___________. COORDENAÇÃO DE POPULAÇÃO; INDICADORES 

SOCIAIS. **Indicadores sociais municipais: uma análise dos resultados da amostra do censo demográfico 2000: Brasil e grandes regiões** . IBGE, 2004. 

___________. **Organização do território** . 2019. Disponível em: < 

https://www.ibge.gov.br/geociencias/organizacao-do-territorio.html>. Acesso em: 05 nov. 2020. 

INSTITUTO NACIONAL DE PESQUISAS ESPACIAIS (INPE). **Programa queimadas** . Disponível em: < http://queimadas.dgi.inpe.br/queimadas/bdqueimadas#exportar>. Acesso em: 20 dez. 2020. 

JENKS, G. F. Optimal data classification for choropleth maps. **Department of Geographiy, University of Kansas Occasional Paper** , 1977. 

KOVALSYKI, B. **Zoneamento de risco para o Parque Estadual de Vila Velha e seu entorno.** 76 f. Dissertação (Mestrado em Engenharia Florestal) - Setor de Ciências Agrárias, Universidade Federal do Paraná, Curitiba, 2016. 

KOVALSYKI, B.; TETTO, A. F.; BATISTA, A. C.; SOUSA, N. J.; TAKASHINA, I. K. Avaliação da eficiência da Fórmula De Monte Alegre para o município de Ponta Grossa – PR. **Enciclopédia Biosfera** , Goiânia, v. 10, n. 19, p. 208 - 218, 2014. 

58 

KRAMER, H. A.; MOCKRIN, M. H.; ALEXANDRE, P. M.; RADELOFF, V. High wildfire damage in interface communities in California. **International journal of wildland fire** , v. 28, n. 9, p. 641-650, 2019. 

LARA, C. H. El concepto de inflamabildad. In: VÉLEZ, R. (Ed.). **La defensa contra incendios forestales** : fundamentos y experiências. Madrid: Mcgraw-Hill; 2009. 

LAWSON, B.D.; ARMITAGE, O.B., editor. **Weather guide for the Canadian Forest Fire Danger Rating System** . Edmonton: Natural Resources Canada Canadian Forest Service; 2008. 

LOPES, L. M. S. A. **Os incêndios florestais na interface urbano-florestal. Caracterização em 2017 e medidas de autoproteção nos aglomerados. O exemplo de Vieira de Leiria** . 2018. Tese de Doutorado. Universidade de Coimbra. 

MAACK, R. **Mapa fitogeográfico do Estado do Paraná** . Instituto de Biología e Pesquisas Tecnológicas, Paraná (Brasil). Servico de Geologia e Petrografia Instituto Nacional do Pinho, Paraná (Brasil), 1950. 

MACHADO, A. P. M.; BATISTA, A. C.; SOARES, R. V.; BIONDI, D.; BATISTA, A. P. B. Incêndios florestais no Parque Nacional da Chapada dos Guimarães-MT entre 2005 e 2014. **Nativa** , Sinop, v. 5, n. 5, p. 355 - 361, 2017. 

MAGALHÃES, M., N.; LIMA, A. C. Ped. **Noções de probabilidade e estatística** . Editora da Universidade de São Paulo, 2002. 

MARTELL, D. L.; OTUKOL, S.; STOCKS, B. J. A logistic model for predicting daily people-caused forest fire occurrence in Ontario. **Canadian Journal of Forest Research** , v. 17, n. 5, p. 394-401, 1987. 

MARTÍNEZ, J.; VEGA-GARCIA, C.; CHUVIECO, E. Human-caused wildfire risk rating for prevention planning in Spain. **Journal of Environmental Management** , v. 90, n. 2, p. 1241 – 1252, 2009. 

MILLER, J. D.; SAFFORD, H. D.; CRIMMINS, M.; THODE, A. E. Quantitative evidence for increasing forest fire severity in the Sierra Nevada and southern Cascade Mountains, California and Nevada, USA. **Ecosystems** , v. 12, n. 1, p. 16-32, 2009. 

MOREIRA, P. A. G.; MENDES, T. A.; SANTOS, D. F. Avaliação de locais potenciais para instalação de torres de observação para prevenção de risco de incêndios florestais. **Ciência Florestal** , v. 30, n. 4, p. 1266-1282, 2020. 

MYERS, R. L. **Convivendo com o fogo** : manutenção dos ecossistemas e subsistência com o manejo integrado do fogo. TNC: USA, 2006. 28p. 

NAKAMURA, Karina Gernhardt. **Multicolinearidade em modelos de regressão logística** . 2013. Tese de Doutorado. Universidade de São Paulo. 

NUNES, J. R. S. **FMA**<sup>**+**</sup> **- um novo índice de perigo de incêndios para o estado do Paraná – Brasil.** 169 f.Tese (Doutorado em Ciências Florestais) - Setor de Ciências Agrárias, Universidade Federal do Paraná, Curitiba, 2005. 

59 

NUNES, J. R. S.; FIER, I. S. N.; SOARES, R.V.; BATISTA, A. C. Desempenho da Fórmula de Monte Alegre (FMA) e da Fórmula de Monte Alegre Alterada (FMA<sup>+</sup> ) no Distrito Florestal de Monte Alegre. **Floresta** , Curitiba, v. 40, n. 2, p. 319 - 326, 2010. 

OLIVEIRA, D. S. **Zoneamento de risco de incêndios florestais no norte de Santa Catarina.** 2002 124f. Dissertação (Mestrado em Engenharia Florestal) Universidade Federal do Paraná, Curitiba. 

PREFEITURA MUNICIPAL DE CAMPO LARGO. **Campo Largo** . 2021.Disponível em: <https://campolargo.atende.net/#!/tipo/pagina/valor/11>. Acesso em: 20 dez. 2020. 

PREFEITURA MUNICIPAL DE PONTA GROSSA. **Ponta Grossa** . 2021.Disponível em: <https://pontagrossa.pr.gov.br/pontagrossa>. Acesso em: 20 dez. 2020. 

PYNE, S. J. **Introduction to wildland fire** : fire management in the United States. Nova Iorque: Wiley-Interscience, 1984. 

registros de incêndios florestais do estado do Paraná no período de 1991 a 2001. RIBEIRO, L.; KOPROSKI, L. P.; STOLLE, L.; LINGNAU, C.; SOARES, R. V. BATISTA, A. C. 2008. Zoneamento de Riscos de incêndios florestais para a fazenda experimental do Canguiri, Pinhais (PR). **Revista Floresta** , Curitiba, v.38, n.3, set. 2008. 

RUSSO, L. X.; PERRÉ, J. L.; ALVES, A. F. Diferencial de Rendimento entre trabalhadores rurais e urbanos: uma análise para o Brasil e suas regiões. **ENCONTRO NACIONAL DE ECONOMIA** , v. 44, 2016. 

SALAS, J.; CHUVIECO, E. Geographic information systems for wildland fire risk mapping. **Wildfire** , Washington, v. 3, n.2, p. 7-13, jun. 1994. 

SAMPAIO, O. B. **Análise de quatro índices na previsão de incêndios florestais** . 177 f.Tese (Doutorado em Ciências Florestais) - Setor de Ciências Agrárias, Universidade Federal do Paraná, Curitiba, 1999. 

SANTOS, J. F. L. **Estimativa do teor de umidade da estepe gramíneo-lenhosa para uso em índices de perigo de incêndios florestais** . Dissertação(Mestrado em EngenhariaFlorestal) - Universidade Federal do Paraná,Curitiba, 2020. No prelo. 

SANTOS, M.; SILVEIRA, M. L. **O Brasil: território e sociedade no início do século XXI** . 2001. 

SCHROEDER, M. J.; BUCK, C. C. **Fire weather** : a guide for application of meteorological information to forest fire control operations. Washington DC: US Forest Service, 1970. 

SECRETARIA ESTADUAL DO MEIO AMBIENTE DO ESTADO DO PARANÁ (SEMA). **_Geoserver_ .** Disponível em: <http://geoserver.pr.gov.br/geoserver/sema_iap/>. Acesso em: 05 nov. 2020. 

SEGER, C. D. **Material combustível e comportamento do fogo em vegetação de estepe gramíneo-lenhosa na RPPN Caminho das Tropas, Palmeira, Paraná.** 197 f. Tese (Doutorado em Ciências Florestais) - Setor de Ciências Agrárias, Universidade Federal do Paraná, Curitiba, 2015. 

60 

SOARES, R. V. **Incêndios florestais** : controle e uso do fogo. Curitiba: FUPEF, 1985. 

SOARES, R. V. Índice de perigo de incêndio. **Floresta** , Curitiba, v. 3, n. 3, 19-40, 1972. 

SOARES, R. V. **Prevenção e controle de incêndios florestais** . ABEAS, 1984. 

SOARES, R. V; BATISTA, A. C.; TETTO, A. F. **Incêndios florestais** : controle, efeitos e uso do fogo. Curitiba, 2017. 

TABACHNICK, B.G.; FIDELL, L.S. **Using multivariate statistics** . 6. ed. Pearson: New York. 2013. 

TETTO A. F, BATISTA A. C., SOARES R. V. Ocorrência de incêndios florestais no estado do Paraná, no período de 2005 a 2010. **Floresta,** Curitiba, v. 42, n. 2, p. 391 – 398, 2012. 

TETTO, A. F.; BATISTA A. C., SOARES R. V.; NUNES, J. R. Comportamento e ajuste da fórmula de Monte Alegre na Floresta Nacional de Irati, Estado do Paraná. **Scientia Forestalis** , v. 38, n. 87, p. 409-417, 2010. 

TETTO, A. F.; SOARES, R. V.; BATISTA, A. C.; WENDLING, W. T. Incêndios florestais atendidos pela Klabin do Paraná no período de 1965 a 2009. **Cerne** , Lavras, v. 21, n. 3, p. 345 – 351, 2015. 

VAN WAGNER, C.E. **Structure of the Canadian forest fire weather index** . Canadian Forestry Service. Ontario: 1974. 32p. (Information Report PS-X-58). 

VEGA-GARCIA, C.; WOODARD, P. M.; TITUS, S. J.; ADAMOWICZ, W. L.; LEE, B. S. A logit model for predicting the daily occurrence of human caused forest-fires. **International Journal of Wildland Fire** , v. 5, n. 2, p. 101-111, 1995. 

VÉLEZ, R. Factores ambientales: los índices meteorológicos de peligro. In: VÉLEZ, R., (Ed.). **La defensa contra incendios forestales** : fundamentos y experiências. Madrid: Mcgraw-Hill; 2009. 

VIEGAS, D. X.; REIS, R. M.; CRUZ, M. G.; VIEGAS, M. T. Calibração do Sistema Canadiano de Perigo de Incêndio para aplicação em Portugal. **Silva Lusitana** , Lisboa, v.12, n.1, p. 77– 93, 2004. 

VOSGERAU, J. L.; BATISTA, A. C.; SOARES, R. V.; GRODZKI, L. Avaliação dos WENDLING, W. T.; SOARES, R. V.; BATISTA, A. C.; TETTO, A. F. Danger degrees adjustment for the Monte Alegre Fórmula (FMA). **WIT Transactions on Ecology and The Environment** , Lavras, v. 158, n. 1, p. 199 – 209, 2012. 

WESTERLING, A. L. Increasing western US forest wildfire activity: sensitivity to changes in the timing of spring. **Philosophical Transactions of the Royal Society B: Biological Sciences** , v. 371, n. 1696, p. 20150178, 2016. 

WHITE, B. L. A. Modelos matemáticos de previsão do teor de umidade dos materiais combustíveis florestais finos e mortos. **Ciência Florestal** , Santa Maria, v. 28, n. 1, p. 432 - 445, 2018. 

61 

WHITE, B. L. A.; RIBEIRO, G. T.; SOUZA, R. M. O uso do BehavePlus como ferramenta para modelagem do comportamento e efeito do fogo. **Pesquisa Florestal Brasileira** , Colombo, v. 33, n. 73, p. 73-84, 2013. 

WHITE, B. L. A.; WHITE, L. A. S.; RIBEIRO, G. T.; FERNANDES, P. A. M. Development of a fire danger index for eucalypt plantations in the northern coast of Bahia, Brazil. **Floresta** , v. 43, n. 4, p. 601-610, 2013. 

WILKS, D. S. **Statistical methods in the atmospheric science** :3rd ed. Oxford, 676 p, 2011. 

WOTTON, B. M.; MARTELL, D. L. A lightning fire occurrence model for Ontario. **Canadian Journal of Forest Research** , v. 35, n. 6, p. 1389-1401, 2005. 

