**_sensors_** 





## _Article_ 

# **Wildfire Risk Assessment of Transmission-Line Corridors Based on Naïve Bayes Network and Remote Sensing Data** 

## **Weijie Chen**<sup>**1**</sup> **, You Zhou**<sup>**1,**</sup> ***, Enze Zhou**<sup>**2**</sup> **, Zhun Xiang**<sup>**2**</sup> **, Wentao Zhou**<sup>**1**</sup> **and Junhan Lu**<sup>**1**</sup> 

- 1 School of Electrical & Information Engineering, Changsha University of Science & Technology, Changsha 410114, China; chenweijie8558@163.com (W.C.); zhouwentao199734@163.com (W.Z.); L18924167973@163.com (J.L.) 

- 2 Electric Power Research Institute, Guangdong Power Grid, Guangzhou 510080, China; zhou_dky@163.com (E.Z.); xiang_dky@163.com (Z.X.) 

- Correspondence: zhouyou243@csust.edu.cn 

**Abstract:** Considering the complexity of the physical model of wildfire occurrence, this paper develops a method to evaluate the wildfire risk of transmission-line corridors based on Naïve Bayes Network (NBN). First, the data of 14 wildfire-related factors including anthropogenic, physiographic, and meteorologic factors, were collected and analyzed. Then, the relief algorithm is used to rank the importance of factors according to their impacts on wildfire occurrence. After eliminating the least important factors in turn, an optimal wildfire risk assessment model for transmission-line corridors was constructed based on the NBN. Finally, this model was carried out and visualized in Guangxi province in southern China. Then a cost function was proposed to further verify the applicability of the wildfire risk distribution map. The fire events monitored by satellites during the first season in 2020 shows that 81.8% of fires fall in high- and very-high-risk regions. 

#### ��������� **�������** 

**Citation:** Chen, W.; Zhou, Y.; Zhou, E.; Xiang, Z.; Zhou, W.; Lu, J. Wildfire Risk Assessment of Transmission-Line Corridors Based on Naïve Bayes Network and Remote Sensing Data. _Sensors_ **2021** , _21_ , 634. https://doi.org/10.3390/s21020634 

Received: 16 December 2020 Accepted: 14 January 2021 Published: 18 January 2021 

**Publisher’s Note:** MDPI stays neutral with regard to jurisdictional claims in published maps and institutional affiliations. 



**Copyright:** © 2021 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license (https:// creativecommons.org/licenses/by/ 4.0/). 

**Keywords:** wildfire; risk assessment; Naïve bayes; transmission-line corridors 

## **1. Introduction** 

Due to the inhomogeneous distribution of energy resources and power loads in China, a large number of overhead transmission lines pass through forests and mountains to achieve an optimal allocation of power resources [1,2]. Wildfires are prone to occur in transmission-line corridors during the high-incidence periods. If a wildfire occurs under an overhead transmission line, the high temperature and smoke in wildfire would reduce the insulating strength of air gap drastically and induce a trip fault of transmission line. In addition, the reclosing usually fails under wildfire conditions with continuous high temperature, which seriously endangers the reliable operation of power grid [3–5]. 

To improve the wildfire prevention capability of transmission lines, scholars carried out much research, including distribution analysis of widfire occurrence [6,7], transmissionline trip mechanisms caused by wildfire [8,9], fire-spot monitoring algorithms [10–13] and wildfire risk assessment methods [14–16]. Remote sensing satellite is an economical and effective way to monitor wildfires in transmission-line corridors continuously. After identifying the flame strength of wildfire, the tripping risk would be evaluated by comparing the height of fire and transmission line [17,18]. However, this method needs numerous land-surface and environmental parameters to estimate the possible height of wildfire. Once a wildfire occurs near the transmission lines, it may cause a trip within tens of minutes. Furthermore, multiple wildfires usually occur simultaneously during the period of the Spring Festival, Qingming Festival, and autumn harvest in China. It is difficult for operation and maintenance personnel to rush the field and put out the fire in time. Therefore, it is necessary to assess occurrence probability of wildfire to propose differentiated wildfire prevention strategies. 

_Sensors_ **2021** , _21_ , 634. https://doi.org/10.3390/s21020634 

https://www.mdpi.com/journal/sensors 

2 of 16 

_Sensors_ **2021** , _21_ , 634 

The wildfire risk assessment was initially proposed by forest and fire departments to supporting decisions or policies for general fire, forest management, and fire suppression. Forestry departments in the US and Canada evaluated the large-scale wildfire risk by combining meteorological factors [19,20]. Nevertheless, these meteorology-based assessment methods cannot meet the requirement of spatial accuracy for transmission-line corridors due to the geographical differences. In 2016, State Grid Corporation of China issued a standard of drawing guidelines (DG) for region distribution map of wildfires near overhead transmission lines. In this standard, fire-spot densities and vegetation burning hazard grades are introduced to construct a risk assessment matrix [21]. However, the wildfire occurrence risk is affected by multi-dimension factors [22]. Besides meteorology and vegetation, physiographic and human-related factors are believed to have an important role in affecting wildfire occurrences [23]. Unfortunately, due to the complexity of wildfire occurrence there is still no physical model that could assess wildfire risk with specific variables. 

Bayesian network is an effective approach to estimate uncertainty in risk evaluation in terms of the likelihood of risks and hazards [24]. In this paper, we aim to propose a wildfire risk assessment model based on Naïve Bayes Network (NBN) and remote sensing data. The region of Guangxi province which locates in southern China, is selected as the study area. A total of 14 sub-categories of wildfire-related factors including anthropogenic, physiographic, and meteorologic factors are collected. Then the spatial data are divided into grids of 1 km _×_ 1 km to meet the spatial accuracy requirement of power grid. Considering the historical wildfire occurrences, the grids are divided based on whether there have been wildfires. After the importance evaluation by the relief algorithm, an NBN-based model is built with the optimal factor subset to map the wildfire risk distribution of Guangxi province. The wildfire risks are then divided into four levels based on the wildfire occurrence probability. In addition, a cost function is proposed to evaluate the applicability of wildfire risk map. 

## **2. Study Area and Data Collection** 

## _2.1. Study Area_ 

Guangxi province is in South China with the latitude of 20<sup>_◦_</sup> 54<sup>_′_</sup> –26<sup>_◦_</sup> 24<sup>_′_</sup> and the longitude of 104<sup>_◦_</sup> 28<sup>_′_</sup> –112<sup>_◦_</sup> 04<sup>_′_</sup> . The total area is 237,600 square kilometers. It is located on the southeastern edge of the Yunnan–Guizhou Plateau. In addition, the terrain is high in the northwest and low in the southeast. The region of Guangxi province is dominated by subtropical and tropical monsoon climate, in which the precipitation is synchronous with high temperature. With a large forest area, Guangxi is vulnerable to wildfire disasters due to its changeable climate, complex topography, and various vegetation. 

## _2.2. Wildfire-Related Factors_ 

## 2.2.1. Anthropogenic Factors 

Based on survey, more than 90% of wildfires are linked directly or indirectly to intentional and unintentional human activities [25]. It mainly includes productive fires such as wasteland and slash burning, and non-productive fires such as smoking in the wild and incensing on the grave [26]. To represent the influence of human activities, five kinds of anthropogenic sub-factors, which are Distance to Roads (DR), Distance to Settlements (DS), Population Density, Gross Domestic Product (GDP) and Historical Fire-Spot Density, are selected. 

Human settlements and roads are the main areas of human activities, in where there are more human-caused fires. Population density reflects the regional population aggregation. A high population density generally corresponds to more human activities and consequently high probability of wildfire occurrence [27]. However, this law may be only suitable to explain the fire events in forests and rural areas. In large urbans, the higher population density may cause the less fire occurrence due to lack of fuels [28]. GDP represents the economic status of regions, which affects the human’s fire habits. The data of 

3 of 16 

_Sensors_ **2021** , _21_ , 634 

roads, settlements, population density were downloaded from the website of the Resource and Environment Science and Data Center (RESDE) with a resolution of 1 km _×_ 1 km. In addition, the DR and DS of grids were calculated by using ArcGIS 10.4. 

Historical Fire-Spot Density represents the spatial distribution of wildfires in the past few years. It is related to not only human activities but also other meteorological and physiographic factors. The database of historical fire-spots was monitored by polar orbiting meteorological satellites from 2010 to 2019, which is provided by the National Meteorological Center. The fire-spot data during 2010–2014 is used to calculate the Historical Fire-Spot Density of grids, whereas the remains (from 2015 to 2019) are used to train and test the NBN model. To calculate the Historical Fire-Spot Density, the study area is divided into grids of 2.5 km _×_ 2.5 km first. Then the fire-spots from 2010–2014 were allocate into grids based on their longitude and latitude. In addition, the final Historical Fire-Spot Density of grids was obtained by using Kriging interpolation method from the resolution of 2.5 km _×_ 2.5 km into 1 km _×_ 1 km. 

## 2.2.2. Physiographic Factors 

The physiographic factors include the land cover and landscape parameters of grids. The land cover factors are consisted of the Land-Usage Type, Vegetation Type, Fuel Load and Normalized Difference Vegetation Index (NDVI), whereas the landscape parameters are average Elevation, Slope, and Aspect of underlying surface. 

The vegetations provide the fuel basis for wildfires’ development. Different types of vegetations differ from their burning capacity in fire ignition and spread. Wildfires prone to ignite and spread rapidly at woodlands, shrubberies and meadows [29]. Therefore, the Land-Usage Type and Vegetation Type are taken to describe the flammability of the underlying surface. To construct the NBN model, the Land-Usage Type and Vegetation Type of study area are classified into four levels according to their flammability, which are shown in Tables 1 and 2, respectively. The Fuel Loading is represented by the drying weight of fuel per unit area, which affects the spread velocity and flame intensity of fires. The NDVI represents the coverage of surface vegetation. It is another representative parameter about fuel contents on the underlying surface. 

**Table 1.** Classification of Vegetation Types. 

|**Level**|**Description**|
|---|---|
|1|Desert, Swamp, Cultivated plants|
|2|Meadow, Grassland, Alpine vegetation|
|3|Broad-leaved forest, Shrub|
|4|Coniferous forest, theropencedrymion|



**Table 2.** Classification of Land-Usage Types. 

|**Level**|**Description**|
|---|---|
|1|Paddy feld, Dry land, Water area, Unused<br>land, Urban-rural fringe, Industrial and mining<br>land, Residential land|
|2|Meadow, Grassland, Alpine vegetation|
|3|Broad-leaved forest, Shrub|
|4|Coniferous forest, Theropencedrymion|



Complex topography influences not only the distribution of vegetations, but also the spreading behavior of fires directly. The elevation brings differences of temperature and humidity to affect the composition of vegetations. Moreover, human population tends to cluster at the region with low elevation and gentle slopes, which increases the fire activities. In addition, the slope also has a direct impact on the spreading speed of wildfires [30]. The increase of slope leads to the faster surface runoff, which is beneficial to the drying of 

4 of 16 

_Sensors_ **2021** , _21_ , 634 

vegetations. Slope aspect determines the amount of solar radiation, therefore the humidity of atmosphere and vegetations. 

The data of Fuel Loading was obtained from the National Meteorological Center. In addition, other land cover factors and landscape parameters were downloaded from RESDE. All the data resolution are 1 km _×_ 1 km. 

## 2.2.3. Meteorologic Factors 

Annual Precipitation and Temperature which have great influences on vegetation growth are selected as the meteorologic factors. In the high precipitation regions, the growth of vegetations is flourishing, which provides fuel conditions for wildfires to burn. However, the reduced transpiration in these areas increases the humidity of vegetation and reduces the flammability. The water-holding capacity of soils and air humidity are also increased. The fires’ ignition and spread are therefore restrained. The higher temperature in forests generally benefits plant growth. In addition, the increase of temperature also accelerates the transpiration of vegetations, which promoting the rapid drying of vegetations. The data of Annual Precipitation and Annual Temperature were obtained from the RESDE, with a resolution of 1 km _×_ 1 km. 

## _2.3. Sample Preparation and Pre-Processing_ 

The influencing degree of wildfires in transmission-line corridors varies with the distance. Generally, the fire that is 1 km away from the transmission-line is regarded as the highest risk, whereas the fire that is 3 km away is assumed to be no impact on the operation of transmission-line [31]. To meet the spatial accuracy requirement, the study area is divided into 1 km _×_ 1 km grids. Then all the wildfire-related factors are allocated into grids. Specifically, the grids which have monitored fire-spots from 2015–2019 are taken as the fire samples. Considering the ignition, spread, and extinction of wildfire last for several hours, those monitoring fire-spots within 4 h and 3 km are regarded as a same fire-spot. Meanwhile, a same number of the non-fire samples are sampled randomly from the rest grids of 3 km away from the grids of the fire samples. 

Compared to processing continuous factors, the Bayesian model has a higher efficiency and better robustness for discrete factors [24]. Therefore, the equal frequency method integrating empirical knowledge was used to discretize the factors. The standards of factor discretization are shown in Table 3. 

**Table 3.** Factor discretization standards. 

|**Factors**|**Discrete Intervals**|
|---|---|
|GDP (10,000 yuan/km<sup>2</sup>)<br>Fuel load(t/km<sup>2</sup>)<br>NDVI|(0, 194), (194, 400), (400, 638), (638,∞)<br>(0, 1), (1, 1.3), (13, 23.3), (23.3,∞)<br>(0, 0.8), (0.8, 0.86), (0.86, 0.90), (0.90, 1]|
|Population density (people/km<sup>2</sup>)<br>Elevation (m)<br>|(0, 91.9), (91.9, 144.7), (144.7, 303.1), (303.1,∞)<br>(0, 145), (145, 295), (295, 575), (575,∞)|
|Fire-spot density (unit/(100 km<sup>2</sup>_·_year))<br>Annual precipitation (mm)|(0, 1), (1, 2.4), (2.4, 4.5), (4.5,∞)<br>(0, 173.1), (173.1, 195.1), (195.1, 209.6), (209.6,<br>∞)|
|Annual temperature (<sup>_◦_</sup>C)<br>Slope (<sup>_◦_</sup>)<br>Aspect (<sup>_◦_</sup>)<br>DS (m)|(0, 19.9), (19.9, 21.5), (21.5, 22.8), (22.8,∞)<br>(0, 3.3), (3.3, 10), (10, 18.3), (18.3, 90]<br>North (0<sup>_◦_</sup>, 45<sup>_◦_</sup>)_∪_(315<sup>_◦_</sup>, 360<sup>_◦_</sup>), East (4 5<sup>_◦_</sup>, 135<sup>_◦_</sup>),<br>South (135<sup>_◦_</sup>, 225<sup>_◦_</sup>), West (225<sup>_◦_</sup>, 315<sup>_◦_</sup>)<br>(0, 356.5), (356.5, 635.7), (635.7, 1041.8), (1041.8,<br>∞)|
|DR (m)|(0, 832.6), (832.6, 2043.7), (2043.7, 3860.3),<br>(3860.3,∞)|

















































































































































































































<!-- Start of picture text -->
DS i GDP<br>[ <356.5 <n oee [4 <194<br>MM 356.5-- 635.7 | ag M@ 194- 400- 400 400<br>[1 635.7-- 1041.8 AG es [1 400- 638- 638 638<br>MH >1041.8 ae. ME >638 *<br><!-- End of picture text -->



<!-- Start of picture text -->
DS i GDP<br>[ <356.5 <n oee [4 <194<br>MM 356.5-- 635.7 | ag M@ 194- 400- 400 400<br>[1 635.7-- 1041.8 AG es [1 400- 638- 638 638<br>MH >1041.8 ae. ME >638 *<br><!-- End of picture text -->



































































































































































































<!-- Start of picture text -->
Land-usage go Ae A ; ar ae<br>rl t See Fuelload ae Se<br>oe tas gee @<! on dl i Se<br>3 er [7 13-233 PP ake<br>m4 < M@ >23.3 aioe<br><!-- End of picture text -->













































































































<!-- Start of picture text -->
[1] 0.86- 0.9 (1) 295- 575<br>mi >0.9 Mi >575<br><!-- End of picture text -->















































































<!-- Start of picture text -->
Slope Aspect<br>[1 <3.3 [1 North<br>M™ 3.3-10 HH East<br>[J 10-183 [| South<br>mi >18.3 / Ml West sides<br><!-- End of picture text -->



<!-- Start of picture text -->
Slope Aspect<br>[1 <3.3 [1 North<br>M™ 3.3-10 HH East<br>[J 10-183 [| South<br>mi >18.3 / Ml West sides<br><!-- End of picture text -->



<!-- Start of picture text -->
;<br>“k on tatty he a<br>|<br>Annual precipitation : ; Annual temperat ire ie ie es 1s : ay<br>MM 1730.7 - 1950.6 () 19.9-21.5 oe pe pea<br>[1 1950.6-2095.6 (7) 21.5 - 22.8 a) of a<br>MM >2095.6 ME >22.8 ee<br>®@<br>De)<br>D(x |<br>De) D& |<br><!-- End of picture text -->



8 of 16 

_Sensors_ **2021** , _21_ , 634 

The basic steps of the relief algorithm are as follows: 

- (1) Take a sample _Si_ randomly from the dataset _D_ = ( _S_ 1, _S_ 2, . . . , _Sn_ ). 

- (2) Go through the dataset and find the closest same-class sample _Si_<sup>_NH_</sup> and different-class sample _Si_<sup>_NM_</sup> of the _Si_ . 

- (3) Calculate the distance _D_ ( _xj_ , _Si_ , _Si_<sup>_NM_</sup> ) between the closest samples about a certain factor _xj_ . If the factor _xj_ is a discrete variable, 



else, 



In this study, the most of factors are continuous variables, except the Vegetation Type and Land-Usage Type. 

(4) Update the weight of factor _xj_ after multiple sampling 



where _ωj_ and _ω_<sup>_∗_</sup> _j_<sup>are the initial and updated weight, respectively.</sup><sup>_m_is the number of</sup> random sampling. The calculated weights of the 14 wildfire-related factors are listed in Table 4. 

**Table 4.** Weights of wildfire-related factors based on the Relief. 

|**Wildfre-Related Factor**|**Weight**|
|---|---|
|DS|0.1265|
|Vegetation Type|0.1227|
|DR|0.1182|
|Annual precipitation|0.1043|
|Fire-spot density|0.0997|
|Land-Usage Type|0.0922|
|Elevation|0.0873|
|NDVI|0.0789|
|Aspect|0.0554|
|Fuel load|0.0376|
|Population density|0.0297|
|Annual temperature|0.0245|
|Slope|0.0134|
|GDP|0.0096|



Based on relief algorithm, the DS, Vegetation Type, and DR shows the most three important impacts on distinguishing the fire and non-fire samples. This is mainly because of the plentiful of fire activities near the living and transportation regions of populations. In addition, the type of vegetation affects the ignition and spread of wildfires. Population Density, Annual Temperature, Slope, and GDP are the least four important factors. The population in Guangxi province is concentrated in the regions of cities, whereas the rest large parts of region are subtropical forests. In urban area, it is hard to inflame due to the lack of fuels and timely fire-fighting behavior. On the other hand, in sparsely populated forests, the happen probability of wildfire is also low due to the low human activities. The wildfire is likely to be happened at the interfacial region of forests and human settlements, which leads the population and GDP to fade into insignificance in this study. The study area is the provincial power grid in southern of China with a small temperature difference. Thus, the average temperature has little influence on the wildfire occurrence. 

9 of 16 

_Sensors_ **2021** , _21_ , 634 

## **4. Naïve Bayes Network-Based Wildfire Risk Assessment** 

## _4.1. Bayes Theorem and Independence Assumption_ 

Bayes’ theorem was initially proposed by Thomas Bayes in the 18th century. It expresses the relationship between the conditional probabilities of two events statistically [34]. It has been widely used in uncertain fields such as disaster prediction, medical diagnosis, speech recognition, and so on. The Bayes’ theorem is as follows: 



where _P_ ( _Xi_ ) is the priori probability which are obtained from the past experience or data distribution. _P_ ( _Y|Xi_ ) is the probability of event _Y_ occurring under the condition of known event _Xi_ . _P_ ( _Xi|Y_ ) is the probability of _Xi_ when the result _Y_ is known. Based on this theorem, the probabilities of wildfire-related factors and then the wildfire occurrence probability under certain conditions could be estimated statistically. However, the estimation of joint probability _P_ ( _Y|Xi_ ) is difficult due to the limited number of samples. Therefore, the Naïve Bayes Network (NBN), in which the factors are assumed to be independent with each other, is used to model the risk of wildfire occurrences. Even through it sacrifices the interaction of factors but still gets an acceptable performance of model in many applications. 

## _4.2. Model Construction_ 

The construction of a Bayes network includes the structure learning and the parameter learning. Due to the independence assumption, the structure of NBN is simplified into a directed acyclic graph with factor nodes connecting to a class node. In addition, the parameter learning process is as follows: 

- (1) Sample preparation from the grids. The fire samples are the grids where fire-spots have been monitored by satellites in the years from 2015 to 2019. A total of 20,348 fires were recorded. In addition, a same number of non-fire samples were extracted randomly excluding buffer zones of 3 km around the fire samples. Then the samples were graded according to the discretization standards in Table 3. The training subset was randomly chosen from 70% of the samples, the remaining samples were used as the testing subset to evaluate the model’s performance. In addition, the spatial distribution of samples in the testing subset are shown in Figure 3. 

- (2) By using the training subset, the probabilities of factors are obtained under fire and 



where _xij_ is the _i_ th wildfire-related factor fall in _j_ th level; and _nij_ is the number of _xij_ . _k_ represented the discretization level of factors. _P_ ( _xij_ �� _Y_ = 0) and _P_ ( _xij_ �� _Y_ = 1) are the probabilities of _xij_ for the girds with non-fires and fires, separately. (3) The conditional probability _P_ ( _Y_ = 1 _|x_ 1, _x_ 2, . . . , _xn_ ) and _P_ ( _Y_ = 0 _|x_ 1, _x_ 2, . . . , _xn_ ) of samples in the testing subset were calculated based on the Bayes’ theorem. In addition, the final wildfire occurrence probability _P(Y)_ was obtained after normalization. 



- (4) To test and optimize model’s performance, the value of 0.5 was selected as the threshold to divide the samples into two classes: “Prone to fire” and “Prone to nonfire”. The least important factors were then eliminated in turn to study the influence of factors composition on the model’s performance. 

10 of 16 

_Sensors_ **2021** , _21_ , 634 

































































**Figure 3.** Samples of testing subset in the Guangxi province. 

## _4.3. Model Assessment_ 

The confusion matrix is used to evaluate the assessment performance of NBN model. It compares the predicted fire tendency of the testing subset with the actual wildfire events to measure the following four indexes, as shown in Table 5. 

**Table 5.** 

|**Samples in Testing Subset**|**Predicte**|**d Results**|
|---|---|---|
||**Prone to Fire**|**Prone to Non-fre**|
|Actual events<br>Fire|_TP_|_FN_|
|Non-fre|_FP_|_TN_|



_TP_ : True Positive, represents the number of fire events correctly predicted as “Prone 

_TN_ : True Negative, indicates the grids where are non-fire and that were identified as “Prone to non-fire”, correctly. 

_FN_ : False Negative, reflects the fire events that were identified as “Prone to non-fire”, mistakenly. 

_FP_ : False Positive, recounts the grids where are non-fire but that are predicted to be 

It is obviously that larger shares of _TP_ and _TN_ indicate a better predicted performance of model. Therefore, the indexes of _Accuracy Pa_ , _Recall Pr_ , _Precision Pp_ and a more balanced index _F_ -score are introduced on the basis of the confusion matrix. 



where _β_ reflect the attention degree of power grids on fault tolerance. Considering the wildfire would induce outage of transmission lines, bring huge economic losses, and even casualties, this study takes _β_ as 3. 

As mentioned in Table 4, the weights of wildfire-related factors have been evaluated by using relief algorithm. Then the NBN models were re-trained and re-tested by eliminating the least important wildfire-related factor one by one. The assessment performances of models are shown in Figure 4. 

11 of 16 

_Sensors_ **2021** , _21_ , 634 



<!-- Start of picture text -->
0.90<br>Pa<br>Pr<br>0.85 Pp<br>0.81229 F -score<br>0.80<br>0.75<br>0.70<br>0.65<br>0.60<br>14 12 10 8 6 4<br>Factor number<br>Ratio<br><!-- End of picture text -->

**Figure 4.** Variation of assessment indexes with wildfire-related factors. 

With the reduced number of wildfire-related factors, the impact of noise, which is bring by unimportant factors, on the model is gradually reduced, which leading to the improvement of _Accuracy Pa_ and _Precision Pp_ . The _Accuracy Pa_ is only 70.14% when all 14 wildfire-related factors are used. It reaches the maximum of 75.93% when the number of factors is reduced to six. The _Recall Pr_ and _F_ -score remain about 81% until the used factor number less than six. However, the performance of NBN model deteriorates significantly when the number of wildfire-related factors reduces from six to five, indicating that the remaining factors have greatest impacts on the wildfire occurrence. 

The _F_ -score reaches the highest value of 81.23% when eight wildfire-related factors are used. The results of confusion matrix are listed in Table 6. 81.92% of actual fire events in the testing subset are predicted correctly. The eight wildfire-related factors include three anthropogenic factors (DS, DR, Elevation and Fire-spot density), three physiographic factors (Vegetation Type, land-Usage Type, and NDVI) and only one meteorological factor (Annual Precipitation). The composition of important wildfire-related factors indicates an important role of human activities in increasing the risk of wildfires. Based on survey, more than 90% of wildfires in Guangxi province are human-caused, deliberately and unintentionally. 

**Table 6.** 

|||**Predicted Results**||
|---|---|---|---|
||**Prone to Fire**|**Prone to**<br>**Non-fre**|**Total**|
|Fire|4839|1161|6000|
|Actual events<br>Non-fre|1641|4359|6000|
|Total|6480|5520|—|
|_Accuracy Pa_||76.65%||
|_Recall Pr_||80.65%||
|_Precision Pp_||74.68%||
|_F_-score||81.23%||



## **5.** 

To guide the wildfire prevention of transmission corridors, the wildfire occurrence probability is calculated in all 1 km _×_ 1 km grids of the study area. The wildfire risks of grids are then divided into four levels based on the probability: Low-(0% _≤ p_ < 25%), Medium(25% _≤ p_ < 50%), High-(50% _≤ p_ < 75%) and Very-high-( _p ≥_ 75%) risk. The conditional probability distribution of wildfire-related factors and an example of probability inference for grids are shown in Figure 5. The remarkable difference of conditional probability 

12 of 16 

_Sensors_ **2021** , _21_ , 634 

distribution gives a visualized explanation of why and how these wildfire-related factors <u>affect wildfre occurrence.</u> 



<!-- Start of picture text -->
Fire  Non-fire<br>DS Vegetation type DR Annual precipitation<br>4 4 4 4<br>3 3 3 3<br>2 2 2 2<br>1 1 1 1<br>0.0 0.1 0.2 0.3 0.4 0.5 0.0 0.1 0.2 0.3 0.4 0.5 0.0 0.1 0.2 0.3 0.4 0.5 0.0 0.1 0.2 0.3 0.4 0.5<br>Probability Probability Probability Probability<br>DS Vegetation type DR Annual precipitation<br>4 4 4 4<br>3 3 3 3<br>2 2 2 2<br>1 1 1 1<br>0.0 0.1 0.2 0.3 0.4 0.5 0.0 0.1 0.2 0.3 0.4 0.5 0.0 0.1 0.2 0.3 0.4 0.5 0.0 0.1 0.2 0.3 0.4 0.5<br>Probability Probability Probability Probability<br>Fire-spot density Land-usage type Elevation NDVI<br>4 4 4 4<br>3 3 3 3<br>2 2 2 2<br>1 1 1 1<br>0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.0 0.1 0.2 0.3 0.4 0.5 0.0 0.1 0.2 0.3 0.4 0.5 0.0 0.1 0.2 0.3 0.4 0.5<br>Probability Probalibity Probability Probability<br>Fire-spot density Land-usage type Elevation NDVI<br>4 4 4 4<br>3 3 3 3<br>2 2 2 2<br>1 1 1 1<br>0.0 0.1 0.2Probability0.3 0.4 0.5 0.0 0.1 0.2Probability0.3 0.4 0.5 0.0 0.1 Probability0.2 0.3 0.4 0.5 0.0 0.1 Probability0.2 0.3 0.4 0.5<br>4 4 4 4 3 2 3 4 4 2 3 2<br>2 4 4 3 3 3 1 4 4 4 1 3<br>90% 91% 90%<br>4 4 4 4 3 2 4 4 4 4 1 2<br>(DS) (vegetation type) (DR) (Annual precipitation) 24% 65% 92%<br>4 4 4 2 2 3 3 3 3 2 2 4<br>91% 65% 47%<br>2 4 4 1 4 4 2 4 2 2 4 3<br>(Wildfire occurrence probability)<br>4 4 3 4 4 4 2 4 4 4 4 1<br>(Fire-spot density) (Land-usage type) (Elevation) (NDVI)<br>Classification Classification Classification Classification<br>Classification Classification Classification Classification<br>Classification Classification  Classification Classification<br>Classification Classification Classification Classification<br><!-- End of picture text -->

**Figure 5.** Conditional probability distribution of wildfire-related factors and an example of probability inference. 

The NBN-based wildfire risk distribution of Guangxi province is mapped by using the ArcGIS software (Figure 6a). For comparison, another wildfire risk distribution map is drawn according to the DG of State Grid Corporation of China (Figure 6b) [21]. In addition, a total of 527 fire events, which were monitored by remoting satellite during the first season in 2020, allocate on the maps. 































<!-- Start of picture text -->
;<br><!-- End of picture text -->



















































































































14 of 16 

_Sensors_ **2021** , _21_ , 634 

more costs for wildfire rescue and management. To balance the contradiction of prediction precision and management cost, a cost index -score is proposed. 



where _ki_ are the maintenance cost for the region with the _i_ th risk level; The maintenance costs of different risk levels need further studies in power grid cases, and are simplified to 1, 2, 4, 8 for the low-risk, medium-risk, high-risk, and very-high-risk regions, respectively. _Si_ is the area proportion of the ith risk region. In addition, _fi_ represents the misjudgment cost when the wildfires are happened in the _i_ th risk level. If a fire happened in the low-risk and medium-risk region, it is likely to be enlarged and bring disaster cost due to negligence of management. Thus, _fi_ are set as 8, 8, 2, and 0 for simplicity. The _R_ -score of NBN-based map is 6.15, which is lower than that of DG-based map (6.62). The reduced cost also indicates the applicability of NBN-based map. 

## **6. Conclusions** 

This study develops a spatial framework to assess and map wildfire risk of transmissionline corridors by integrating remote sensing data. The proposed NBN-based wildfire risk assessment combines empirical knowledge and machine learning into the discretization of input factors, construction of conditional probabilities of wildfire-related factors, and mapping of wildfire risk distribution. NBN as a core algorithm is used to infer the probabilities of wildfire occurrence. The remote sensing data including a total of 14 sub-categories of wildfire-related factors is assembled to construct NBN model. Based on the relief algorithm, the number of key wildfire-related factors is reduced into 8, indicating human activities and fuels at underlying surface play more important roles in wildfires occurrence. This spatial framework was implemented in a case study of Guangxi province in the south of China. In addition, a cost index, R-score, is proposed to reflect the maintenance costs and misjudgment costs. The results show that the NBN-based wildfire risk map has a higher prediction precision and lower costs for power grids than the traditional method. 45.35% of new monitored fire events distribute at the very-high-risk regions. The visual wildfire risk distribution can assist decision maker of power grids to optimize both supplies and staff resources and make strategies for responding damage control in the future. 

**Author Contributions:** Funding acquisition, Z.X.; Investigation, E.Z.; Methodology, W.Z.; Project administration, Y.Z.; Software, W.Z.; Supervision, Z.X.; Writing—original draft, W.C.; Writing—review & editing, Y.Z. and J.L. All authors have read and agreed to the published version of the manuscript. 

**Funding:** The research was funded by the Science and technology projects funded by China Southern Power Grid Corporation for supporting this research under Contract No. GDKJXM20198386, by the Changsha University of Science and Technology Professional Master’s Innovation Project SJCX202045, by the Changsha University of Science and Technology Academic Master’s Research and Innovation Project CX2020SS56, by the Hunan Province Natural Science Foundation of China under Grant No. 2019JJ50658, and by the Scientific Research Foundation of Hunan Education Department under 

### **Institutional Review Board Statement:** No statement. 

**Informed Consent Statement:** Not applicable. 

### **Data Availability Statement:** No statement. 

**Acknowledgments:** The authors would like to thank Sanyi Sui from the Changsha University of Science and Technology for his helpful suggestions. The authors also would like to thank the anonymous reviewers for their constructive suggestions and comments. 

15 of 16 

_Sensors_ **2021** , _21_ , 634 

## **References** 

1. Shi, S.; Yao, C.; Wang, S.; Han, W. A Model Design for Risk Assessment of Line Tripping Caused by Wildfires. _Sensors_ **2018** , _18_ , 1941. [CrossRef] [PubMed] 

2. Guo, Y.; Chen, R.; Shi, J.; Wan, J.; Yi, H.; Zhong, J.J.I.G. Determination of the power transmission line ageing failure probability due to the impact of forest fire. _IET Gener. Transm. Distrib._ **2018** , _12_ , 3812–3819. [CrossRef] 

3. Wu, T.; Ruan, J.; Zhang, Y.; Chen, C.; Pu, Z.H.; Wang, G.L. Study on the statistic characteristics and identification of AC transmission line trips induced by forest fires. _Power Syst. Prot. Control_ **2012** , _40_ , 138–143. 

4. Li, P.; Huang, D.; Pu, Z.; Ruan, J. Study on DC Voltage Breakdown Characteristics of Gap under Fire Conditions. In Proceedings of the Annual Report Conference on Electrical Insulation and Dielectric Phenomena, Shenzhen, China, 20–23 October 2013; pp. 338–341. 

5. Fonseca, J.; Tan, A.; Silva, R.; Monassi, V.; Assuncao, L.; Junqueira, W.; Melo, M. Effects of agricultural fires on the performance of overhead transmission lines. _IEEE Trans. Power Deliv._ **1990** , _5_ , 687–694. [CrossRef] 

6. Chou, Y.H.; Minnich, R.A.; Salazar, L.; Power, J.; Dezzani, R.J. Spatial autocorrelation of wildfire distribution in the Idyllwild quadrangle, San Jacinto Mountain, California. _Remote Sens._ **1990** , _56_ , 1507–1513. 

7. Sakellariou, S.; Cabral, P.; Caetano, M.; Pla, F.; Painho, M.; Christopoulou, O.; Sfougaris, A.; Dalezios, N.; Vasilakos, C. Remotely Sensed Data Fusion for Spatiotemporal Geostatistical Analysis of Forest Fire Hazard. _Sensors_ **2020** , _20_ , 5014. [CrossRef] [PubMed] 

8. El-Zohri, E.H.; Abdel-Salam, M.; Shafey, H.M.; Ahmed, A. Mathematical modeling of flashover mechanism due to deposition of fire-produced soot particles on suspension insulators of a HVTL. _Electr. Power Syst. Res._ **2013** , _95_ , 232–246. [CrossRef] 

9. You, F.; Zhang, Y.; Chen, H.X.; Zhang, L.H.; Zhu, J.P.; Zhou, J.J. Preliminary studies on flashovers of high-voltage transmission lines induced by wildfires by field survey and experimental tests. _Procedia Eng._ **2013** , _52_ , 557–565. [CrossRef] 

10. Giglio, L.; Descloitres, J.; Justice, C.O.; Kaufman, Y. An enhanced contextual fire detection algorithm for MODIS. _Remote Sens. Environ._ **2003** , _87_ , 273–282. [CrossRef] 

11. Giglio, L.; Csiszar, I.; Restás, Á.; Morisette, J.T.; Schroeder, W.; Morton, D.; Justice, C.O. Active fire detection and characterization with the advanced spaceborne thermal emission and reflection radiometer (ASTER). _Remote Sens. Environ._ **2008** , _112_ , 3055–3063. [CrossRef] 

12. Chiang, S.H.; Ulloa, N.I. Mapping and Tracking Forest Burnt Areas in the Indio Maiz Biological Reserve Using Sentinel-3 SLSTR and VIIRS-DNB Imagery. _Sensors_ **2019** , _19_ , 5423. [CrossRef] 

13. Barmpoutis, P.; Papaioannou, P.; Dimitropoulos, K.; Grammalidis, N. A Review on Early Forest Fire Detection Systems Using Optical Remote Sensing. _Sensors_ **2020** , _20_ , 6442. [CrossRef] 

14. Choobineh, M.; Ansari, B.; Mohagheghi, S. Vulnerability assessment of the power grid against progressing wildfires. _Fire Saf. J._ **2015** , _73_ , 20–28. [CrossRef] 

15. Sánchez, Y.; Martínez-Graña, A.; Santos Francés, F.; Mateos Picado, M. Mapping Wildfire Ignition Probability Using Sentinel 2 and LiDAR (Jerte Valley, Cáceres, Spain). _Sensors_ **2018** , _18_ , 826. [CrossRef] 

16. Sadasivuni, R.; Cooke, W.; Bhushan, S. Wildfire risk prediction in southeastern Mississippi using population interaction. _Ecol. Model._ **2013** , _251_ , 297–306. [CrossRef] 

17. Lu, J.; Liu, Y.; Xu, X.; Yang, L.; Zhang, G.; He, L. Prediction and early warning technology of wildfire nearby overhead transmission lines. _High Volt. Eng._ **2017** , _43_ , 314–320. 

18. Dian, S.; Cheng, P.; Ye, Q.; Wu, J.; Luo, R.; Wang, C.; Hui, D.; Zhou, N.; Zou, D.; Gong, X. Integrating wildfires propagation prediction into early warning of electrical transmission line outages. _IEEE Access_ **2019** , _7_ , 27586–27603. [CrossRef] 

19. Deeming, J.E. _National Fire-Danger Rating System_ ; Rocky Mountain Forest and Range Experiment Station, Forest Service: Fort Collins, CO, USA, 1972; Volume 84. 

20. Wang, X.; Wotton, B.M.; Cantin, A.S.; Parisien, M.A.; Anderson, K.; Moore, B.; Flannigan, M.D. cffdrs: An R package for the Canadian forest fire danger rating system. _Ecol. Process._ **2017** , _6_ , 5. [CrossRef] 

21. State Grid Corporation of China. Drawing Guidelines for Region Distribution Map of Wildfires Near Overhead Transmission Lines. 2016. Available online: http://www.doc88.com/p-3837473228466.html (accessed on 21 October 2017). 

22. Costafreda-Aumedes, S.; Comas, C.; Vega-Garcia, C. Human-caused fire occurrence modelling in perspective: A review. _Int. J. Wildland Fire_ **2018** , _26_ , 983–998. [CrossRef] 

23. Rodrigues, M.; Jiménez, A.; de la Riva, J. Analysis of recent spatial–temporal evolution of human driving factors of wildfires in Spain. _Nat. Hazards_ **2016** , _84_ , 2049–2070. [CrossRef] 

24. Albuquerque, M.T.D.; Gerassis, S.; Sierra, C.; Taboada, J.; Martín, J.; Antunes, I.M.H.R.; Gallego, J.R. Developing a new Bayesian Risk Index for risk evaluation of soil contamination. _Sci. Total Environ._ **2017** , _603_ , 167–177. [CrossRef] [PubMed] 

25. Depicker, A.; De Baets, B.; Baetens, J. Wildfire ignition probability in Belgium. _Nat. Hazards Earth Syst. Sci._ **2020** , _20_ , 363–376. [CrossRef] 

26. Lu, J.; Zhou, T.; Wu, C.; Li, B.; Tan, Y.; Zhu, Y. Fault statistics and analysis of 220 kV and above power transmission line in province-level power grid. _High Volt. Eng._ **2016** , _42_ , 200–207. 

27. Dlamini, W.M. A Bayesian belief network analysis of factors influencing wildfire occurrence in Swaziland. _Environ. Model. Softw._ **2010** , _25_ , 199–208. [CrossRef] 

28. Archibald, S.; Roy, D.P.; van Wilgen, B.W.; Scholes, R.J. What limits fire? An examination of drivers of burnt area in Southern Africa. _Glob. Chang. Biol._ **2009** , _15_ , 613–630. [CrossRef] 

16 of 16 

_Sensors_ **2021** , _21_ , 634 

29. O’Donnell, A.J.; Boer, M.M.; McCaw, W.L.; Grierson, P.F. Vegetation and landscape connectivity control wildfire intervals in unmanaged semi-arid shrublands and woodlands in Australia. _J. Biogeogr._ **2011** , _38_ , 112–124. [CrossRef] 

30. Saglam, B.; Bilgili, E.; Dincdurmaz, B.; Kadiogulari, A.I.; Kücük, Ö. Spatio-Temporal Analysis of Forest Fire Risk and Danger Using LANDSAT Imagery. _Sensors_ **2008** , _8_ , 3970–3987. [CrossRef] 

31. Lu, J.; Liu, Y.; Wu, C.; Zhang, H.; Zhou, T. Study on satellite monitoring and alarm calculation algorithm of wild fire near transmission lines. _Proc. Csee_ **2015** , _35_ , 5511–5519. 

32. Parisien, M.A.; Moritz, M.A. Environmental controls on the distribution of wildfire at multiple spatial scales. _Ecol. Monogr._ **2009** , _79_ , 127–154. [CrossRef] 

33. Kira, K.; Rendell, L.A. The Feature Selection Problem: Traditional Methods and a New Algorithm. In Proceedings of the Tenth National Conference on Artificial Intelligence, San Jose, CA, USA, 12–16 July 1992; pp. 129–134. 

34. Liu, R.; Chen, Y.; Wu, J.; Gao, L.; Barrett, D.; Xu, T.; Li, L.; Huang, C.; Yu, J. Assessing spatial likelihood of flooding hazard using naïve Bayes and GIS: A case study in Bowen Basin, Australia. _Stoch. Environ. Res. Risk Assess._ **2016** , _30_ , 1575–1590. [CrossRef] 

