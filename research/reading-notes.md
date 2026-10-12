# Reading notes

These notes distinguish source descriptions from our interpretation. The catalogue records review depth; this is not a systematic literature review.

## Springer chapter supplied by the user

Pedra, Hernantes and Labaka, Assessing the Impact of Multi-hazard Events in Spain: A Clustering Index Framework, 2024, printed pages 233–251. DOI: https://doi.org/10.1007/978-3-031-74006-0_10

Read from the user-supplied full book. It uses more than 150,000 insurance claims from 2020–2021, AEMET observations, and flood, windstorm and sea-storm events. Robust scaling precedes K-means; elbow and silhouette analysis guide cluster selection. Event categories are averaged by province for single-hazard indices. A further clustering creates the combined index. Missing single-hazard scores are replaced by an average in that stage. Categories vary between years.

Our interpretation: this is a resilience-oriented event/loss analysis, not a suitable physical-hazard baseline for this project's current objective. Payouts depend on insured assets and coverage; two years poorly characterize rare events. Cluster separation does not independently validate danger or resilience. The paper associates meteorological magnitude with rapidity rather than directly measuring recovery time. Retain it as a methodological comparison, including the distinction between clusters and ordered scores.

## ThinkHazard

https://gfdrr.github.io/thinkhazard/

Reviewed documentation and classification methods. Provides global classifications for individual hazards, with intensity/frequency thresholds and administrative aggregation. A strong source for hazard-specific definitions and a global benchmark. It is not itself the combined physical score envisaged here.

Current and legacy documentation differ. Pin versions before reproduction. Review all thresholds and exceptions rather than treating institutional provenance as validation. Administrative aggregation can conceal spatial variation. The source catalogue and downloadable classifications need access and license audits.

## UNICEF Multi-Hazard Intensity

https://github.com/unicef/CCRR/tree/main/Multi_Hazard_Indicators/MHI

Read the README and inspected the construction notebook. This is a close implementation precedent: climate-hazard rasters become a continuous pixel index before population-weighted downstream analysis. Documentation describes 13 inputs at about 0.1 degrees, log transformation, standardization, six PCA components and scaling to 0–10. The notebook also clips standardized inputs and fills missing land values with zero.

Our questions: signed PCA-derived weights require monotonicity checks; explained variance is not hazard importance; multiple heat and drought indicators may affect family influence; missing values cannot universally be interpreted as zero. A latitude-longitude grid also raises an area-weighting question for global fitting. These are audit questions, not demonstrated failures of the published map. No reproduction has been run. Geological hazards are outside this MHI selection.

## European multi-hazard hotspots

Antofie et al., 2025: https://nhess.copernicus.org/articles/25/287/2025/

Reviewed article methodology and limitations. Combines hotspots of population/building exposure to six hazards at local administrative-unit scale. Useful for reproducibility and validation design. Exposure totals and spatial clustering differ from a pointwise physical-hazard score. The study distinguishes overlapping hazards from explicit modelling of interactions. Code and data are published.

## ESPON TITAN

https://database.espon.eu/indicator/2178/

Reviewed indicator documentation. Combines normalized flood, windstorm, drought, earthquake and landslide indicators using historical financial-loss weights. Missing coverage is flagged. It is a direct composite-map precedent, but its weighting target does not match our current independence-from-wealth preference.

## Other methodological references

FEMA National Risk Index combines expected loss with social vulnerability and resilience. INFORM combines hazards/exposure, vulnerability and coping capacity. They provide useful documentation patterns but answer different questions.

OECD/JRC's composite-indicator handbook supports explicit normalization, weighting and sensitivity analysis. ERICC-2025 is a Spanish synthesis for hazard coverage and relationships rather than a ready-made fine-scale index. CLIMADA and GEM are potential infrastructure/data sources; acquisition, fitness and reuse terms remain to be checked.

## Claim discipline

Do not infer the best method from a repository's existence, a paper's title or an institution's name. Distinguish an inspected implementation from a reproduced result. No novelty claim or ranking has yet been established.
