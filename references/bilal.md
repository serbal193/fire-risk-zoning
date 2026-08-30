pera Sos. 





**e** ee reer eee eee eeeee 

Check for 



<!-- Start of picture text -->
1.0<br>Low risk: Lower risk:<br>i minimal fuel moist canopy<br>40.8<br>4 Peak risk band<br>5. (~0.3-0.5)<br>§ 0.6<br>z<br>i=]<br>=<br>a£04<br>o<br>@2ar® 0.20.<br>ina]<br>9.093 0.0 0.2 0.4 0.6 0.8 1.0<br>NDVI<br><!-- End of picture text -->

_Ecological Informatics 91 (2025) 103435_ 

_M. Bilal_ 

baseline for the same time of year. For example, Dennison et al. (2005) showed that wildfire probability in Southern California increased significantly when NDWI dropped more than 15 % below its seasonal normal. Daily to weekly NDWI composites (e.g., from MODIS or VIIRS) can capture rapid drying or greening phases, which is ideal for operational fire monitoring, whereas monthly means are more suited for retrospective assessments or broad-scale planning. Seasonal NDWI drops, particularly in Mediterranean or monsoon-affected ecosystems, can provide early warning of fuel conditions transitioning toward extreme flammability. 

# iv. **Ecosystem-Specific Performance** 

NDWI’s reliability varies across biomes. In temperate forests, NDWI anomalies are strong indicators of canopy water stress and impending fuel drying (making it useful for fire danger warnings), but a dense canopy can saturate NDWI and mask drying of the understory or forest floor. In arid and semi-arid grasslands, NDWI is often already low due to sparse vegetation, so its dynamic range is limited; false positives may arise over bare soil or rock where NDWI _<_ 0 simply indicates lack of vegetation rather than high fire risk. In wetlands or riparian systems, NDWI remains persistently high and may not detect localized dry patches beneath dense canopies (essentially always signaling “low risk” ). In cropland regions, NDWI can fluctuate due to irrigation practices, leading to misleading signals if interpreted without context. As with NDVI, NDWI values should be cross-validated against land cover types and fuel models to accurately analyze their implications for fire risk. 

# v. **Practical Improvements and Integration** 

Given its limitations, NDWI should never be used alone in fire risk mapping. Its reliability improves significantly when it is (i) combined with NDVI (to distinguish vegetated areas that are green-and-wet vs. green-but-dry), (ii) cross-checked with soil moisture or drought indices, and (iii) applied with informed thresholds rather than generic ones. For example, one can combine NDWI and NDVI to flag areas of high biomass that are also unusually dry (low NDWI), which are of most significant concern. Furthermore, integrating NDWI with other layers, such as dead fuel moisture estimates or fire weather indices, can compensate for what NDWI misses; thermal indices (e.g., Land Surface Temperature, NBRT) to detect moisture-heat overlap; drought indices such as the KeetchByram Drought Index (KBDI), Standardized Precipitation Evapotranspiration Index (SPEI), or soil moisture proxies (Chuvieco et al., 2019), and masking layers (e.g., land use/land cover) to exclude non-burnable urban or bare zones. Ultimately, NDWI is a valuable proxy for live fuel water content, but must be contextualized with other data and interpreted correctly (inversely) to avoid the pitfalls of misclassification. 

equate to fire probability. While NBR can highlight areas of dense or vigorous biomass, it fails to reflect fuel dryness, ignition likelihood, or meteorological triggers necessary for fire. A region of lush, healthy vegetation (high NBR) might be presumed high-risk due to ample fuel, but if that vegetation is wet or the area lacks ignition sources, the actual fire risk remains low. Conversely, sparse but extremely dry vegetation can exhibit low NBR values yet be highly flammable. For example: 

- In humid tropical forests, NBR may remain high year-round ( _>_ 0.7) due to dense vegetation, yet fires are rare because fuel moisture is high; only under exceptional droughts or human disturbances would such areas ignite (Gabban et al., 2007). 

- In alpine meadows or boreal wetlands, high biomass can yield moderate NBR values, yet these landscapes are often insulated from fire by saturated soils, surface water, or microclimates (Xu et al., 2024a). 

- Conversely, arid grasslands with sparse but cured vegetation may show low NBR ( _<_ 0.1) but can burn readily due to extreme dryness and continuity of fine fuels. 

These examples highlight that NBR alone is a necessary but not sufficient indicator for estimating fire danger. The presence of biomass (which NBR captures) sets the stage for fire, but the probability of ignition and sustained burning depends on additional factors that NBR does not measure (fuel moisture, weather, ignition sources, etc.). 

# ii. **Over-Reliance on AUC and Localized Validation** 

In the case study by Sivrikaya et al. (2024), NBR achieved an Area Under the Curve (AUC) of 0.842 in predicting historical fire ignition points, outperforming NDVI, NDWI, and NBRT. While this high AUC suggests NBR was the best among those indices for that dataset, such metrics must be interpreted with caution. AUC evaluates model discrimination within a particular dataset and context, but it does not guarantee transferability across different regions or conditions. In Sivrikaya’s Mediterranean pine forest context, the high AUC likely reflects the specific situation where fire-prone periods coincide with dense, dry canopies—a circumstance favoring NBR’s performance. Koutsias et al. (2012) caution that using static vegetation indices without considering ignition mechanisms or seasonal fuel moisture dynamics can mislead fire planning. Overgeneralizing NBR’s effectiveness from one ecosystem to another (e.g., assuming the same thresholds or performance in tropical rainforests or alpine tundra) risks a false sense of security or misallocated resources. Thus, while AUC is a useful diagnostic, robust validation should include multi-ecosystem testing, confusion matrices, and, if possible, cross-validation on _unseen_ geographic regions to ensure a model’s generalizability beyond the original study area. 

# iii. **Terrain, Soil, and Land Use Effects** 

# **4. Normalized burn ratio (NBR)** 

The Normalized Burn Ratio (NBR), calculated as (NIR – SWIR) / (NIR + SWIR), was originally developed to detect post-fire burn severity using satellite imagery (Key and Benson, 2006; Roy et al., 2006). The substitution of SWIR (shortwave infrared) in place of red reflectance (as in NDVI) allows NBR to detect changes in both vegetation density and moisture, making it sensitive to burned and charred surfaces. In post-fire — applications, the differenced NBR (dNBR) the change between pre— and post-fire NBR is widely used and validated. However, its pre-fire application, which is increasingly common for risk mapping, demands careful scrutiny. 

NBR, like NDVI, is subject to terrain-induced reflectance biases. Slope and aspect can cause differential solar illumination, altering SWIR reflectance and skewing NBR values (Ma et al., 2024). This is especially problematic in mountainous fire-prone regions, where south-facing slopes might show artificially low NBR (due to brighter, drier soil signals) compared to shaded north-facing slopes with identical fuel conditions. Moreover, land cover and land use can confound NBR-based risk maps. For instance, agricultural fields, urban green spaces, or recently – logged areas may show intermediate NBR values (~0.15 0.25) yet contain discontinuous or negligible wildland fuels. Without incorporating fuel type information or land-use overlays, such areas might be falsely labeled as moderate risk based solely on their NBR value. 

# i. **NBR as a Proxy for Biomass, Not Fire Probability** 

—much like NDVI—is often treated as an In pre-fire contexts, NBR indicator of abundant vegetation fuel, but fuel presence alone does not 

# iv. **Thresholding Challenges** 

Fire risk classification using NBR often depends on arbitrary or site- 

3 

> _M. Bilal                                                                                                                                                                                                                                           Ecological Informatics 91 (2025) 103435_ 

specific thresholds. In Sivrikaya et al. (2024), for example, zones with NBR _>_ 0.22 were designated as “extreme risk,” with lower NBR ranges defining lower risk classes. However, such fixed cutoffs lack ecological justification and are unlikely to hold across varying vegetation types and climates. One region’s “high-risk” NBR value could be normal background vegetation in another region. Instead, data-driven approaches like ROC curve optimization, quantile-based classification, or dynamic thresholding based on historical fire occurrences should be applied. In machine learning workflows, NBR is more effectively utilized as a continuous input feature rather than imposing hard class breaks; this enables the model to learn the nuanced risk contributions of NBR in combination with other variables. 

# v. **Strategies to improve NBR-based assessments** 

To enhance the accuracy and robustness of NBR in wildfire risk models, several improvements are recommended: (a) Pair NBR with direct fuel dryness indicators, such as thermal data (Land Surface Temperature), vapor pressure deficit (VPD), or an evaporative stress index, to distinguish between high biomass that is wet vs. high biomass that is dry. (b) Overlay ignition potential layers (lightning frequency, road networks, powerlines, camping areas) to factor in where ignitions are likely. (c) Combine NBR with NDWI or soil moisture datasets to better discriminate areas of high biomass that are actually moist (and thus lower risk) from those that are critically dry. (d) Apply land cover or fuel-type masks to exclude zones that have high NBR but low flammability (e.g., irrigated agriculture, wetlands). For instance, Chuvieco et al. (2019) propose a multi-layer model combining vegetation indices with drought indices and human accessibility factors, which achieved improved spatial accuracy in Mediterranean and South American fire risk mapping. In summary, NBR is a powerful proxy for vegetation density and continuity, particularly valuable in post-fire analysis and in ecosystems where fuel load is a limiting factor. But when applied to prefire risk mapping, it must be used with caution. On its own, NBR cannot capture fuel flammability, weather triggers, or human ignition patterns. — Integrating NBR with complementary variables including moisture indices, topography, ignition likelihood, and temporal trends—is essential to construct ecologically valid, spatially transferable, and operationally useful fire risk models. 

# **5. Normalized burn ratio thermal (NBRT)** 

The Normalized Burn Ratio Thermal (NBRT) extends the classic NBR by incorporating thermal infrared (TIR) information to account for surface temperature. The premise is straightforward: hot, vegetated areas under drought stress are more likely to ignite and sustain wildfire. NBRT formulations vary by sensor, but generally they augment the NBR calculation with a thermal band (Smith et al., 2005; Smith et al., 2007). By including a thermal component, NBRT attempts to bridge the gap between fuel quantity (as indicated by greenness) and fuel condition (dryness or heat stress). In theory, this provides a more complete indicator of fire risk than spectral reflectance alone. However, in practical applications—particularly at large scales—NBRT exhibits several limitations that require careful consideration. 

# i. **Thermal Confounders and False Positives** 

Thermal bands measure surface temperature, but high temperatures can arise from various non-vegetation features. For example, urban heat islands, asphalt roads, rocky outcrops, sparsely vegetated deserts, and bare soils may all exhibit elevated thermal signatures due to their physical properties (low albedo, high heat capacity) despite having little or no combustible biomass. These features can appear as “hotspots” on NBRT-derived risk maps, even in areas devoid of burnable fuel, leading to false positives. This phenomenon was observed in portions of the Sivrikaya et al. (2024) Mediterranean study area and was also noted by 

Lin et al. (2022) on Taiwan’s Dadu Plateau—demonstrating that NBRT can produce spurious high-risk signals in both semi-arid and subtropical landscapes. Similarly, large industrial structures (e.g., metal rooftops) or exposed rock escarpments can mimic NBRT risk hotspots without any ecological fire risk. 

# ii. **Temporal Variability and Acquisition Biases** 

NBRT’s readings are sensitive to the timing of image acquisition, daily weather, and transient cloud/shadow effects. Time of day strongly influences surface temperature; a satellite overpass in the early morning will record lower thermal values than an afternoon overpass, potentially yielding very different NBRT maps for the same location. Likewise, recent weather events can skew NBRT: a passing cloud or recent rainfall will cool surfaces and suppress NBRT values even if the fuels are critically dry, whereas a brief heatwave could spike NBRT readings despite fuels still retaining moisture. These issues mean that single-date NBRT maps are inherently noisy. A region that appears “cool and safe” on a morning satellite image might become high-risk by late afternoon as surfaces heat up. This temporal sensitivity partially explains the underperformance of NBRT in Sivrikaya et al. (2024), where NBRT yielded the lowest AUC (0.812) of the four indices tested and marked only ~5 % of the study area as “extreme risk” (far less than NDVI or NBR). While such a conservative indicator might reduce false positives in some cases, it also risks _missing_ areas of flammable vegetation—especially in shaded or recently irrigated zones that were temporarily cool when the satellite passed. 

# iii. **Spatial Performance and niche strengths** 

Despite its pitfalls, NBRT has some situational advantages. In sunexposed shrublands and semi-arid scrub ecosystems, NBRT can excel at pinpointing critically dry fuels where other indices (e.g., NDVI) remain high due to persistent greenness. It is particularly useful in transitional zones (ecotones) between forest and grassland, where flammable understory builds up in open sunlight. Although NDVI might remain moderately high (indicating foliage presence), NBRT will capture the added heat stress of those drying fuels. NBRT can also be a valuable alert during short-term extreme heat events (e.g., drought combined with a heatwave or dry lightning conditions), when rapid surface heating precedes ignition. In these scenarios, NBRT provides a warning that purely reflectance-based indices would miss. Thus, NBRT has **situational value** – especially if used alongside fuel load indicators and real-time weather data – but it should not be treated as a universally reliable stand-alone metric. 

# iv. **Integration Strategies to Improve NBRT Use** 

To address NBRT’s limitations, it should never be used as a standalone risk indicator. We recommend the following integration approaches to harness NBRT’s strengths while compensating for its weaknesses: (a) Combine NBRT with a greenness index (NBR or NDVI): Ensure that a “hot” pixel also has sufficient biomass before interpreting it as high risk. An area with high NBRT but very low NBR/NDVI is likely a false alarm (hot bare ground). (b) Apply land-use/land-cover masks: Exclude or down-weight urban areas, rock outcrops, open water, and other non-fuel surfaces by using ancillary GIS layers; this prevents NBRT from flagging inherently nonflammable features. (c) Use multi-day thermal anomalies: Instead of a single image, compute NBRT anomalies over a week or use thermal anomaly products (e.g., MODIS or ECOSTRESS-based heat stress indices) to filter out ephemeral temperature spikes and focus on sustained heat indicative of drying fuels. (d) Fuse with meteorological and soil moisture data: Incorporate variables like VPD (vapor pressure deficit), soil moisture, or relative humidity to verify that elevated surface temperatures correspond to actual fuel dryness. Recent studies by Kondylatos et al. (2022) and Xu et al. (2024a) 

4 

_Ecological Informatics 91 (2025) 103435_ 

_M. Bilal_ 

have demonstrated the benefit of including NBRT as one layer in multiindex, machine learning models; these integrated models (in Mediterranean and boreal regions, respectively) achieved improved fire risk detection by treating NBRT as a dynamic feature adjusted for baseline climate and combined with other predictors. In summary, NBRT adds a useful thermal dimension to pre-fire risk mapping by flagging heatstressed vegetation. However, it is susceptible to misclassification due to non-vegetated hot surfaces, timing biases, and lack of fuel context. To avoid misleading outputs, NBRT must be interpreted within a multivariable framework, calibrated to regional conditions, and corrected using land cover, temporal anomaly, and fuel continuity information. When used in such a targeted manner, NBRT can complement—but not — replace traditional indices in a comprehensive wildfire risk assessment system. 

- **Temporal:** Capture dynamics through anomaly detection, moving averages, and seasonal composites to reflect fuel curing, drought onset, or unseasonal weather. 

- **Spatially contextualized:** Include terrain factors (slope, aspect), fuel types/loads, and human accessibility features (e.g., roads, powerlines) to refine where fires are likely and where they can spread. 

- **Probabilistic and adaptive:** Avoid rigid thresholds; employ statistical learning or threshold optimization to calibrate “high risk” for each ecosystem and season. 

- **Validated:** Rigorously test the framework with historical fire data 

- (ignitions and spreads) using cross-validation and by comparing against known fire events, to ensure it performs well under conditions beyond the training data. 

# **6. Comparative summary of spectral indices** 

# ii. **Recommended Data Layers** 

To facilitate comparison and emphasize each index’s niche and pitfalls, Table 1 summarizes the core characteristics, intended purposes, typical threshold interpretations, known limitations, and common misuses for NDVI, NDWI, NBR, and NBRT. This consolidated view (incorporating reviewer suggestions) provides a quick reference to how each index behaves and cautions to consider when using them for fire risk mapping. 

Each index provides valuable but _partial_ insight into wildfire risk. — Misapplication especially interpreting any single index as a stand— alone risk predictor can lead to severe errors in risk mapping. NDVI and NBR primarily focus on vegetation abundance, NDWI targets live fuel moisture, and NBRT responds to surface heat anomalies. None of them alone captures critical components like ignition probability, _dead_ fuel dryness, or fire weather conditions. 

# **7. Toward an integrated framework for wildfire risk mapping** 

The limitations of individual spectral indices outlined above underscore the need for multidimensional, integrative approaches that mirror the complex interplay of biophysical, climatic, topographic, and human factors driving wildfire occurrence. Rather than discarding spectral indices, we advocate for their strategic combination with other data layers, leveraging recent advances in machine learning, anomaly detection, and multi-sensor data fusion. Below, we propose a conceptual framework for integration and key strategies for implementation. 

# i. **Core Principles of the Framework** 

An effective pre-fire wildfire risk mapping system should be: 

- **Multi-layered:** Incorporate multiple spectral indices (NDVI, NDWI, NBR, NBRT) alongside other environmental and anthropogenic variables. 

Table 2 outlines _recommended data layers_ to combine in such a framework, categorized by type (spectral, meteorological, fuel, topography, anthropogenic) and providing examples of specific variables and data sources. 

# iii. **Example of integrative approaches** 

Recent studies offer templates for how multi-layer models outperform single-index approaches. For instance, Kondylatos et al. (2022) used a deep learning model (a convolutional neural network) to combine NDVI, LST, elevation, and drought indicators, resulting in significantly improved daily fire danger predictions in the Mediterranean region 

**Table 2** 

Recommended Data Layers for an Integrated Wildfire Risk Model. 

|Category|Suggested Variables|Sources|
|---|---|---|
|Spectral Indices|NDVI, NDWI, NBR, NBRT|Satellite imagery: Landsat,<br>MODIS, Sentinel-2|
|Meteorological/|Land Surface Temperature<br>(LST); Vapor Pressure Defcit<br>(VPD); Drought indices (eg|Reanalysis and climate data:<br>ERA5, CHIRPS; Remote|
|Drought|..,<br>KBDI, SPEI); Rainfall<br>anomaly; Wind speed|sensing: MODIS temperature<br>products|
|Fuel Type and<br>Load|Land cover classifcation;<br>Fuel models; Biomass density|Land cover maps: MODIS<br>MCD12Q1, ESA WorldCover;<br>National fuel databases|
|Topography|Elevation; Slope; Aspect|DEMs: SRTM, ASTER, or<br>LiDAR-derived terrain data|
||Road and trail density;|OpenStreetMap (roads, power|
||Powerline network;|infrastructure); Census or|
|Anthropogenic|Settlements/population|land-use data; Lightning|
|Factors|density; Historical ignition<br>points (e.g., lightning strikes,<br>campfres)|detection networks; Fire<br>incident databases (e.g.,<br>national fre history archives)|



## **Table 1** 

Summary of Key Spectral Indices Used in Pre-Fire Wildfire Risk Mapping. 

|Index|Formula|Primary Target|Strengths|Limitations|Common Misuse<br>|
|---|---|---|---|---|---|
|NDVI|(NIR–RED) / (NIR+<br>RED)|Green vegetation<br>cover (biomass<br>proxy)|Well-established; intuitive;<br>extensive historical<br>archives|Confounded by soil brightness, slope, and<br>view angle; does not measure fuel dryness<br>or type<br>|Treating high NDVI (_>_0.6) as high fre risk<br>regardless of moisture status (assuming<br>“greener=more dangerous”)|
|NDWI|(NIR–SWIR) / (NIR<br>+ SWIR)|Live canopy water<br>content|Strong indicator of<br>drought stress in green<br>vegetation<br>|Insensitive to dead fuels; noisy in sparsely<br>vegetated areas; values must be<br>interpreted inversely (wetness vs.<br>dryness)|Interpreting high NDWI (_>_0.12) as high fre<br>risk (inverting its meaning); failing to<br>account for irrigation or wetlands<br>|
|NBR|(NIR–SWIR) / (NIR<br>+ SWIR)|Biomass presence;<br>canopy vigor|Useful in post-fre<br>mapping; correlates with<br>fuel abundance|Not sensitive to fuel_condition_or ignition<br>likelihood; affected by terrain and soil<br>background|Assuming fuel quantity equals fammability;<br>applying one-size-fts-all NBR thresholds<br>across regions|
|NBRT|NBR integrated with<br>thermal band (sensor-<br>specifc)|Surface temperature<br>in vegetated areas|Captures heat stress;<br>highlights critically dry,<br>exposed vegetation|Susceptible to non-fuel heat (urban,<br>rock); subject to diurnal and weather-<br>related noise; requires biomass context|Misidentifying hot non-vegetated areas<br>(rooftops, bare ground) as high-risk; using<br>single images without temporal context|



5 

> _M. Bilal                                                                                                                                                                                                                                           Ecological Informatics 91 (2025) 103435_ 

compared to using NDVI or NBR alone. Nguyen et al. (2018) applied a Random Forest classifier integrating spectral indices with fuel type, topography, and weather data in tropical forests of Southeast Asia, and found the combined model far more accurate than any single-layer model. Xu et al. (2024a) employed long-term MODIS NDVI anomalies together with VPD and terrain layers to map fire-prone zones in Alberta’s boreal forests, emphasizing the importance of distinguishing fuel abundance from fuel _flammability_ . These examples underscore that _no_ — _one index or factor suffices_ the synergy of multiple data layers is key. 

# iv. **Conceptual Flow (Textual)** 

From a workflow perspective, an integrated approach might follow this _conceptual pipeline_ : (i) _Data acquisition:_ Gather multi-source inputs (satellite indices, weather, topography, human footprint). (ii) _Preprocessing:_ Perform necessary calibrations (e.g., terrain correction of reflectance, resampling of coarse climate data to match high-res imagery, smoothing of time series with moving windows). (iii) _Feature engineering:_ Compute anomalies (e.g., NDWI deviation from 5-year norm), derive combined metrics (e.g., fuel aridity index blending NDVI and LST), or encode interactions (like slope-adjusted fuel load). (iv) _Modeling:_ Feed the prepared layers into a predictive model – this could range from statistical models (logistic regression, weighted indices) to machine learning (Random Forests, Gradient Boosted Trees) or deep learning (CNNs, LSTMs for time series) – to output a probabilistic fire risk map. (v) _Validation:_ Compare model outputs with observed fire occurrence or spread data, computing metrics like AUC, precision-recall, etc., and adjust model parameters accordingly. (vi) _Operational use:_ Translate the model probabilities into actionable classes or alerts, ideally with associated confidence measures, and implement a schedule for updating the inputs (e.g., daily weather updates, weekly satellite index updates). 

# v. **Practical and Operational Considerations** 

When building and deploying such models, a few practical points are worth highlighting: 

- **Dynamic thresholding:** Replace static threshold rules (e.g., NDWI _>_ 0.12) with thresholds tuned to specific conditions via ROC opti- 

- mization or similar. What constitutes “high risk” in one ecoregion or month may not be the same in another. 

- **Resolution matching:** Be mindful of the spatial resolution differences among layers (e.g., a 30 m Landsat NDVI vs. a 5 km ERA5 climate grid). Resample or aggregate data so that finer-resolution data aren’t being paired with overly coarse data in a misleading way. 

- **Real-time updates:** For early warning, use low-latency data sources. Geostationary satellites or daily polar orbiters (VIIRS, MODIS) can provide near-real-time indicators that feed into a continuously updated risk map, whereas higher-resolution products with longer revisit (Landsat/Sentinel) can be used for weekly or monthly assessments. 

- **Modularity and customization:** The framework should allow swapping or adding layers based on regional relevance and data availability. In some regions, lightning ignitions dominate (including lightning density); in others, human factors dominate (including population or land-use metrics). The model should be flexible enough to accommodate these differences. 

“best” The future of wildfire risk mapping lies not in picking a spectral index in isolation, but in developing robust, modular, and validated integrative frameworks. By fusing spectral, meteorological, — topographic, and anthropogenic layers using both classical statistical — methods and modern AI techniques researchers and practitioners can build adaptive systems for early fire detection and mitigation planning that are far more reliable and context-aware than any single-index map. 

# **8. Limitations** 

Despite the utility of spectral indices for pre-fire risk mapping, several significant limitations persist. One key issue is limited transferability across regions and ecosystems. Index thresholds or models calibrated in one landscape (e.g., Mediterranean pine forests) often fail when applied to different fuel types or climates without recalibration (Marino et al., 2024). Regional variations in vegetation, seasonality, and ignition patterns mean that a spectral indicator of risk in one area is not guaranteed to perform similarly elsewhere (Marino et al., 2024). Another problem is that common vegetation indices mainly capture live green canopy properties (greenness or moisture proxies) while overlooking other hazardous fuel components. They cannot effectively sense dry dead fuels, fine surface litter, ladder fuels, or undergrowth continuity beneath the canopy (Abdollahi and Yebra, 2025; Hao and Qu, 2007). In other words, an area might appear “safe” in the index due to a lush canopy, even if highly flammable dry debris lies below. Temporal and sensor-related biases further complicate index-based assessments. A single-date satellite image can be skewed by transient conditions – for example, recent rainfall can briefly raise vegetation moisture signals, or clouds and shadows can depress reflectance (Xu et al., 2024b). Likewise, sensor geometry and terrain introduce errors: differences in sun angle or steep topography can distort reflectance ratios (especially those involving SWIR bands) if proper topographic and illumination corrections are not applied (Chen et al., 2020). Such effects may cause an index to indicate spurious risk levels in shaded or sloped areas unless these biases are corrected. 

Anthropogenic and land-use factors can also confound spectral risk mapping. Irrigated agriculture, urban materials, or bare rock outcrops can produce spectral signatures that mislead risk indices (Liu et al., 2023). For instance, exposed soil or mineral surfaces often yield low – vegetation-index values (NDVI in the 0.1 0.2 range) similar to those of drought-stressed vegetation (Cherlinka, 2024). Without masking or down-weighting these non-fuel areas, an index algorithm might falsely flag them as high-risk simply because they appear “bare” or “dry” spectrally. Integrating multi-source data streams introduces additional challenges of scale and timing. Different inputs – e.g., daily coarseresolution meteorological indices versus 10–30 m satellite imagery – come at disparate resolutions and update intervals, and they must be carefully reconciled to avoid spurious correlations (Liu et al., 2024). Mismatches in spatial resolution or temporal frequency can otherwise generate artificial risk signals (for example, when a fine-scale vegetation map is paired with averaged climate data), so data are often resampled or aligned to a standard grid and timeframe (Liu et al., 2024). 

Model uncertainty and generalizability are further limitations that demand transparency. Predictive risk models inherently carry error, and their performance can degrade outside the original calibration domain. Many current wildfire models are developed on region-specific datasets, which limits their broader applicability (Xu et al., 2024b). It is therefore critical that risk maps include validation metrics and even confidence layers indicating the reliability of the predictions (Ejaz and Choudhury, 2025). Reporting the model’s accuracy, uncertainty, and any assumptions helps users understand where the map is robust and where it should be interpreted with caution, especially if applied in new regions or conditions beyond the training data (Xu et al., 2024b). Finally, operational constraints affect the consistency of spectral risk monitoring. Data availability issues – such as missing satellite imagery due to orbital gaps or persistent cloud cover – and computational limitations can delay updates and create temporal gaps in risk maps (Chen et al., 2024). In practice, if critical inputs are missing or delayed, analysts must resort to conservative default assumptions (e.g., carrying forward the last known safe condition) and clearly communicate these uncertainties. Such stopgap measures are necessary to maintain an operational risk mapping system, but they underscore that real-world factors (cloudy weather, sensor downtime, processing capacity) can impact the frequency and reliability of wildfire risk assessments. (Chen et al., 2024). 

6 

_Ecological Informatics 91 (2025) 103435_ 

# **9. Conclusion and recommendations** 

The rising frequency and intensity of wildfires underscore the urgent need for reliable, context-aware fire risk assessment tools. While spectral indices like NDVI, NDWI, NBR, and NBRT each provide valuable information on vegetation density, moisture status, or surface heating, their use in stand-alone applications for pre-fire wildfire risk mapping is fraught with limitations. These indices are frequently misinterpreted, misapplied, or generalized across ecologically diverse landscapes without regard for regional climate, fuel types, ignition sources, or topographic complexity. No single index by itself captures all the critical dimensions of fire risk—especially fuel _flammability_ , dead fuel moisture, human ignition potential, and short-term weather anomalies. Accordingly, we advocate for multi-factor modeling frameworks (e.g., machine learning models) that integrate spectral indices with meteorological drought indices and human activity data to build more robust fire risk predictors. 

This letter has offered a comprehensive, evidence-based critique of four commonly used spectral indices, drawing on recent research across — varied ecosystems from Mediterranean pine forests and boreal landscapes to tropical rainforests and semi-arid grasslands. By integrating case studies, quantitative thresholds, and index-specific limitations, we _and_ the boundaries of each index’ clarified the scope s utility in pre-fire assessments. A recurring theme is the danger of misinterpreting index thresholds—for example, assuming a certain value denotes high risk without considering what that value actually means in terms of fuel moisture or ignition likelihood. Such misuse (as demonstrated in the NDWI case, where NDWI _>_ 0.12 was wrongly labeled “extreme risk”) can lead to false alarms or complacency, misallocation of firefighting resources, and flawed risk communication to stakeholders. 

Moreover, while individual indices may show moderate predictive power in specific environments (e.g., NBR performing well in the Mediterranean setting of Sivrikaya et al., 2024), no single index is universally reliable. Each index’s effectiveness is conditional on the ecosystem and season—for instance, NDVI and NBR tend to do well in fuel-limited scenarios, NDWI is crucial in drought-prone contexts, and NBRT adds value during heatwaves. But none, in isolation, accounts for the full picture. 

# _9.1. Recommendations for researchers and practitioners_ 

In light of our findings, we propose the following best-practice 

guidelines for pre-fire wildfire risk mapping: 

- **Do not rely on any single spectral index in isolation.** Use vegetation indices as _partial_ indicators within a broader assessment framework. Treat an index’s output as one piece of evidence that must be corroborated with other information (fuel conditions, weather, human factors) before drawing conclusions about fire risk. 

- **Incorporate temporal trends and anomalies.** Avoid single-date snapshots. Use time-series approaches like rolling averages, seasonal baseline comparisons, or z-score anomalies (e.g., standardized NDVI or NDWI) to detect when conditions are unusually conducive to fire. Often, it is the deviation from normal (a sudden drying) rather than an absolute index value that signals danger. 

- **Use ecologically grounded thresholds (or none at all).** Instead of applying arbitrary cutoffs (e.g., “NBR _>_ 0.2 = high risk”) everywhere, derive thresholds from the data (using ROC curves or similar) for each study area and season, or use continuous risk scores. Machine learning models can inherently find optimal breakpoints if appropriately trained, obviating the need for hard-coded thresholds. 

- **Fuse multiple indices with ancillary data.** As highlighted, combining layers is key. We recommend integrating spectral indices with: (i) Meteorological variables (temperature, VPD, drought indices, wind), (ii) Topographic variables (slope, aspect, elevation which affect microclimate and fuel moisture), (iii) Fuel and 

vegetation type maps (to distinguish grass vs. shrub vs. forest fuel dynamics), and (iv) Anthropogenic factors (proximity to roads, powerlines, settlements, historical fire ignition points). This multifactor fusion provides a more holistic view of risk. 

- **Leverage modern modeling techniques (when data allow).** Machine learning and ensemble models (e.g., Random Forests, Gradient Boosted Trees, Convolutional Neural Networks) are powerful for integrating diverse data layers. They can capture nonlinear interactions (e.g., how drought and fuel load together elevate risk in a way that isn’t obvious from either alone) and can provide feature importance insights to show which factors are driving predictions. These methods do require careful tuning and guarding against overfitting, but numerous studies show their promise in wildfire risk applications. 

- **Mask out non-burnable areas.** Use land cover data to exclude water bodies, urban cores, irrigated farmland, and other essentially non-flammable surfaces from analysis (or assign them a permanent low-risk rating). This prevents indices like NBRT or NDVI from misleadingly highlighting such areas. 

- **Tailor models to specific ecoregions.** There is no one-size-fits-all model for wildfire risk. A model developed in a Mediterranean climate should not be applied blindly to a boreal forest. Always calibrate and validate your risk model using historical fire data from the region of interest, and be cautious in extrapolating to new areas without additional validation. 

- **Document uncertainty and model performance.** Especially for operational use, provide confidence measures with risk maps. For example, produce a “high-risk probability” map but also supply the AUC or expected false alarm rate, and identify areas where the model is extrapolating beyond the range of its training data (indicating lower confidence). This transparency helps fire managers trust and appropriately use the outputs. 

- **Maintain spatial and temporal consistency.** Ensure that all input layers align (e.g., same projection and resolution) and that any timesensitive inputs are matched to the period of analysis (e.g., don’t mix a 5-year-old fuel map with current NDVI data without checking for changes). Misalignments can create spurious risk signals. 

- **Promote open science and interoperability.** Whenever possible, share the code, data, and parameters of your risk mapping approach. This facilitates peer review, replication in other regions, and incremental improvements by the community. It also enables combining datasets across borders for tackling wildfires as the regional and global challenge that they are. 

# _9.2. Final remarks_ 

In conclusion, we echo and reinforce the sentiment that wildfire danger cannot be reliably mapped by vegetation indices alone. These indices, however sophisticated or popular, capture only slices of a much — larger puzzle. The complexity of fire ecology spanning live and dead fuels, ignition patterns (natural and human), microclimate variability, — and land management practices demands composite models reflecting this complexity. As data availability grows (with new satellites, sensors, and crowd-sourced information) and computational tools evolve, we now have the opportunity to transition from static, single-index maps to dynamic, data-rich predictive systems. Realizing this vision will require interdisciplinary collaboration, better integration of remote sensing with field data, and a commitment to tailoring solutions to each landscape’s unique characteristics. We hope this synthesis serves not only as a caution against simplistic approaches but also as a constructive path forward. By bridging spectral index insights with ecological understanding and modern data science, the wildfire research and management community can develop next-generation risk mapping tools that meet the urgency of a changing climate and an increasingly fire-prone world. 

7 

> _M. Bilal                                                                                                                                                                                                                                           Ecological Informatics 91 (2025) 103435_ 

# **CRediT authorship contribution statement** 

**Muhammad Bilal:** Writing – review & editing, Writing – original draft, Visualization, Validation, Supervision, Software, Resources, Project administration, Methodology, Investigation, Funding acquisition, Formal analysis, Data curation, Conceptualization. 

# **Declaration of competing interest** 

The authors declare that they have no known competing financial interests or personal. 

# **Acknowledgements** 

This research is supported by the funding project INAE2502, awarded by the Center for Aviation & Space Exploration at King Fahd University of Petroleum and Minerals (KFUPM) in Saudi Arabia. The author also expresses gratitude for the valuable financial assistance provided by the Deanship of Research at KFUPM. 

# **Data availability** 

Data will be made available on request. 

# **References** 

Abdollahi, A., Yebra, M., 2025. Challenges and opportunities in remote sensing-based fuel load estimation for wildfire behavior and management: a comprehensive review. Remote Sens 17. 

Chen, R., Yin, G., Liu, G., Li, J., Verger, A., 2020. Evaluation and normalization of topographic effects on vegetation indices. Remote Sens 12. 

Chen, Y., Morton, D.C., Randerson, J.T., 2024. Remote sensing for wildfire monitoring: insights into burned area, emissions, and fire dynamics. One Earth 7, 1022–1028. Cherlinka, V., 2024. NDVI FAQ: All you Need to Know About Index. EOS Data Analytics. Chuvieco, E., Mouillot, F., van der Werf, G.R., San Miguel, J., Tanase, M., Koutsias, N., García, M., Yebra, M., Padilla, M., Gitas, I., Heil, A., Hawbaker, T.J., Giglio, L., 2019. Historical background and current developments for mapping burned area from satellite earth observation. Remote Sens. Environ. 225, 45–64. 

Dennison, P.E., Roberts, D.A., Peterson, S.H., Rechel, J., 2005. Use of normalized difference water index for monitoring live fuel moisture. Int. J. Remote Sens. 26, 1035–1042. 

Ejaz, N., Choudhury, S., 2025. A comprehensive survey of the machine learning pipeline for wildfire risk prediction and assessment. Eco. Inform. 90. 

Flannigan, M., Cantin, A.S., de Groot, W.J., Wotton, M., Newbery, A., Gowman, L.M., 2013. Global wildland fire season severity in the 21st century. For. Ecol. Manag. 294, 54–61. 

Gabban, A., San-Miguel-Ayanz, J., Viegas, D.X., 2007. On the suitability of the use of normalized difference vegetation index for forest fire risk assessment. Int. J. Remote Sens. 27, 5095–5102. 

- Gao, B.-C., 1996. NDWI—A normalized difference water index for remote sensing of vegetation liquid water from space. Remote Sens. Environ. 58, 257–266. 

García, M.J.L., Caselles, V., 1991. Mapping burns and natural reforestation using thematic mapper data. Geocarto Int. 6, 31–37. 

Hao, X., Qu, J., 2007. Retrieval of real-time live fuel moisture content using MODIS measurements. Remote Sens. Environ. 108, 130–137. 

Huang, S., Tang, L., Hupy, J.P., Wang, Y., Shao, G., 2020. A commentary review on the use of normalized difference vegetation index (NDVI) in the era of popular remote sensing. J. For. Res. 32, 1–6. 

- Huete, A.R., Post, D.F., Jackson, R.D., 1984. Soil spectral effects on 4-space vegetation discrimination. Remote Sens. Environ. 15, 155–165. 

Iban, M.C., Sekertekin, A., 2022. Machine learning based wildfire susceptibility mapping using remotely sensed fire data and GIS: a case study of Adana and Mersin provinces, Turkey. Eco. Inform. 69. 

- Key, C.H., Benson, N.C., 2006. Landscape Assessment: Ground Measure of Severity, the Composite Burn Index; and Remote Sensing of Severity, the Normalized Burn Ratio, Ogden, UT. 

Kondylatos, S., Prapas, I., Ronco, M., Papoutsis, I., Camps-Valls, G., Piles, M., Fern´andezTorres, M.A., Carvalhais, N., 2022. Wildfire danger prediction and understanding<sup>´</sup> with deep learning. Geophys. Res. Lett. 49. 

Koutsias, N., Arianoutsou, M., Kallimanis, A.S., Mallinis, G., Halley, J.M., Dimopoulos, P., 2012. Where did the fires burn in Peloponnisos, Greece the summer of 2007? Evidence for a synergy of fuel and weather. Agric. For. Meteorol. 156, 41–53. 

Lin, C.-Y., Shieh, P.-Y., Wu, S.-W., Wang, P.-C., Chen, Y.-C., 2022. Environmental indicators combined with risk analysis to evaluate potential wildfire incidence on the Dadu plateau in Taiwan. Nat. Hazards 113, 287–313. 

Liu, W., Guan, H., Hesp, P.A., Batelaan, O., 2023. Remote sensing delineation of wildfire spatial extents and post-fire recovery along a semi-arid climate gradient. Eco. Inform. 78. 

Liu, X., Zheng, C., Wang, G., Zhao, F., Tian, Y., Li, H., 2024. Integrating multi-source remote sensing data for Forest fire risk assessment. Forests 15. 

Ma, Y., He, T., McVicar, T.R., Liang, S., Liu, T., Peng, W., Song, D.-X., Tian, F., 2024. Quantifying how topography impacts vegetation indices at various spatial and temporal scales. Remote Sens. Environ. 312. 

Marino, E., Ya´nez, L., Guijarro, M., Madrigal, J., Senra, F., Rodríguez, S., Tom˜ ´e, J.L., 2024. Transferability of empirical models derived from satellite imagery for live fuel moisture content estimation and fire risk prediction. Fire 7. 

Moreira, E.P., Valeriano, M.D.M., Sanches, I.D.A., Formaggio, A.R., 2016. Topographic effect on spectral vegetation indices from Landsat tm data: is topographic correction necessary? Boletim Ciˆenc. Geod´es. 22, 95–107. 

Moritz, M.A., Parisien, M.-A., Batllori, E., Krawchuk, M.A., Van Dorn, J., Ganz, D.J., Hayhoe, K., 2012. Climate change and disruptions to global fire activity. Ecosphere 3, 1–22. 

Nguyen, N.T., Dang, B.-T.N., Pham, X.-C., Nguyen, H.-T., Bui, H.T., Hoang, N.-D., Dieu, T.B., 2018. Spatial pattern assessment of tropical forest fire danger at Thuan Chau area (Vietnam) using GIS-based advanced machine learning algorithms: a comparative study. Eco. Inform. 46, 74–85. 

Reszka, P., Fuentes, A., 2014. The great Valparaiso fire and fire safety Management in Chile. Fire. Technol 51, 753–758. 

Roy, D.P., Boschetti, L., Trigg, S.N., 2006. Remote sensing of fire severity: assessing the performance of the normalized burn ratio. IEEE Geosci. Remote Sens. Lett. 3, 112–116. 

Sivrikaya, F., Günlü, A., Küçük, O., Ürker, O., 2024. Forest fire risk mapping with<sup>¨</sup> Landsat 8 OLI images: evaluation of the potential use of vegetation indices. Eco. Inform. 79. 

Smith, A.M.S., Wooster, M.J., Drake, N.A., Dipotso, F.M., Falkowski, M.J., Hudak, A.T., 2005. Testing the potential of multi-spectral remote sensing for retrospectively estimating fire severity in African savannahs. Remote Sens. Environ. 97, 92–115. Smith, A.M.S., Drake, N.A., Wooster, M.J., Hudak, A.T., Holden, Z.A., Gibbons, C.J., 2007. Production of Landsat ETM+ reference imagery of burned areas within southern African savannahs: comparison of methods and application to MODIS. Int. J. Remote Sens. 28, 2753–2775. 

Tucker, C.J., 1979. Red and photographic infrared linear combinations for monitoring vegetation. Remote Sens. Environ. 8, 127–150. 

Xu, E., Wei, M., Li, T., Lei, V., Gao, J., Wang, N., He, Y., Bloor, M., 2024a. Assessing burn severity and vegetation restoration in Alberta’s boreal forests following the 2016 Fort McMurray wildfire – a remote sensing time-series study. Sustain. Environ. 10. Xu, Z.L., Jonathan, Sibo, Cheng, Xue, Rui, Yu, Zhao, Hongjie, He, Linlin, Xu, 2024b. Wildfire Risk Prediction: A Review. 

Yebra, M., Dennison, P.E., Chuvieco, E., Riano, D., Zylstra, P., Hunt, E.R., Danson, F.M., ˜ Qi, Y., Jurdao, S., 2013. A global review of remote sensing of live fuel moisture content for fire danger assessment: moving towards operational products. Remote Sens. Environ. 136, 455–468. 

Muhammad Bilal<sup>a,b,*</sup> a _Architecture and City Design Department, College of Design and Built Environment, King Fahd University of Petroleum & Minerals, Dhahran, Saudi Arabia_ b _Center for Aviation & Space Exploration, KFUPM, Dhahran, Saudi Arabia_ 

- Corresponding author at: Architecture and City Design Department, College of Design and Built Environment, King Fahd University of Petroleum & Minerals, Dhahran, Saudi Arabia. 

- _E-mail address:_ muhammad.bilal@kfupm.edu.sa. 

8 

