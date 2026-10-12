# Comparing places under future hazards

Research pass dated 2026-10-12. The user prioritizes future hazards while retaining present-day context. This is a research proposal, with no adopted score or preferred locations.

## The useful question

Which Spanish places remain relatively lower across the hazards we can measure, and which conclusions change when we change the source, model, scenario or indicator?

A flood comparison is a useful component, but too narrow as the project's only first output. Run it alongside a national future-climate comparison. Aim for a set of contrasting place profiles and a provisional map, then inspect surprising agreements and disagreements.

## Close precedents

| Study | What it already does | Implication for us | Review depth |
| --- | --- | --- | --- |
| [Forzieri et al. 2016, Multi-hazard assessment in Europe under climate change](https://link.springer.com/article/10.1007/s10584-016-1661-x) | Seven physical hazards, future periods, an Overall Exposure Index and Change Exposure Index. Explicitly separates hazard from vulnerability and settlements. | The idea of a European physical multi-hazard future index is established. | Main-text introduction and methods read; supplementary material and data not acquired. |
| [KC et al. 2020, journal volume 2021, Multi-hazard climate risk projections for the United States](https://link.springer.com/article/10.1007/s11069-020-04385-y) | County-scale 2040s multi-hazard risk, combining hazards with exposure and vulnerability. | A useful composite benchmark, although its final objective differs from ours. | Abstract and selected methods inspected; not reproduced. |
| [Stalhandske et al. 2024, Global multi-hazard risk assessment in a changing climate](https://www.nature.com/articles/s41598-024-55775-2) | Global flood and tropical-cyclone modelling in CLIMADA, matched climate realizations, different warming levels and recovery assumptions. | Shared drivers matter if we later make claims about concurrent events. | Abstract, introduction and discussion inspected; implementation not run. |
| [Khosravi and Ouarda 2026, Collapse of climatic refugia under compound climate hazards in the Middle East and North Africa](https://www.nature.com/articles/s44304-026-00213-8) | Future compound climate-state indices and erosion of historically milder areas under SSP scenarios. | Even the question of persistent lower-hazard refuges has close precedents. | Abstract and selected index definitions read; model training and supplementary validation not audited. |

Forzieri's framework is the most directly relevant new reading. It compares changes in frequencies of baseline extremes, uses 1981–2010 and three future windows, and rescales outputs to a common 1 km grid. Its original model inputs do not gain 1 km physical accuracy through that rescaling. It uses the older A1B scenario. Only one climate-model configuration is common across hazards, so it combines per-hazard medians and explores minima and maxima. Those combinations deserve care if reused as coherent future worlds.

The MENA paper calls its indices period-scale hazard states, not counts of simultaneous events. That distinction matters for us too. Adding standardized heat and dryness can describe an unfavorable profile without proving interaction or concurrent disasters.

Novelty remains unproven. A useful contribution to investigate is an open comparison of **which lower-hazard conclusions survive source and methodological changes**, with explanations tied to actual places. The algorithm alone is unlikely to be the contribution.

## Data routes worth using now

| Source | Candidate use | Access and limitations verified in this pass |
| --- | --- | --- |
| [C3S Atlas gridded dataset](https://cds.climate.copernicus.eu/datasets/multi-origin-c3s-atlas?tab=overview) | Heat, dry spells, drought indicators and heavy precipitation, with historical and future series. | Catalogue has 35 variables/indices, NetCDF4, CC-BY, version 2.5. CMIP6 is 1 degree; CORDEX-EUR-11 is 0.125 degree. Historical and RCP/SSP experiments exist, with availability varying by source. No data request executed. |
| [C3S fire-danger projections](https://cds.climate.copernicus.eu/datasets/sis-tourism-fire-danger-indicators?tab=overview) | Add fire-weather pressure to the future comparison. | European FWI projections span 1970–2098, using EURO-CORDEX and historical/RCP2.6/4.5/8.5 runs. Catalogue offers CC-BY. No files downloaded; model and island coverage still to inspect. |
| [ISIMIP repository](https://www.isimip.org/outputdata/isimip-repository/) | Later global expansion and impact-model comparisons. | Public dataset/file API and stable provenance links documented. Sector outputs include water and fire; a consistent matched subset and individual licenses still need an audit. |

C3S Atlas supplies days above 35 or 40 degrees C, tropical nights, consecutive dry days, SPI/SPEI and precipitation maxima. These give a practical climate-pressure comparison, not a complete natural-hazard inventory. Retain absolute levels beside changes. A cool place warming quickly can still be cooler than a hot place warming slowly.

FWI describes weather conducive to fire; it does not by itself describe ignition, fuel availability or a property's burn probability. Heavy rainfall is not flood inundation. SPI/SPEI measure departures from a reference climate, so they should not silently stand in for absolute water availability or household water security.

## A first experiment with more scope

1. Build a Spain-wide exploratory view of future heat and dry-spell/drought indicators. Include present-day reference conditions and a mid-century window. Start with the exact periods offered by accessible datasets and record differences.
2. Add fire weather if compatible model members and periods are available. In parallel, retain the detailed flood-source comparison as a separate layer. A present-day flood map must not acquire a future label by being shown next to 2050 climate projections.
3. Inspect around 15–20 deliberately contrasting places across Atlantic, Mediterranean, inland, mountain and island settings. Selection is for testing, not a claim that they are promising relocation destinations. Report any regional domain omissions explicitly.
4. Show the component values before any composite. Try pairwise comparisons: is A lower than B across all measured components, or is there a heat–flood–fire trade-off? Test a simple mean and worst-component view only as sensitivity exercises.
5. Recalculate the shortlist separately for available models and scenarios. Show which places persist and which flip, together with the input or assumption responsible. Summaries should name their denominator, such as the particular model runs tested. They are not probabilities that a place is safe.
6. Publish a short list of interesting findings, including failures: a supposed low-hazard place with missing coverage, two sources sharing a model, and a place whose apparent advantage disappears under another indicator.

A calendar window around 2050 is easy to discuss. A second view at common global warming levels would later help compare sources, but hydrology and coastal sea level can depend on the pathway and timing too. Do not equate an RCP with an SSP purely because their names share a forcing number. Use scenario families as approximate comparisons and disclose mismatches.

## Keep uncertainty intelligible

Separate disagreement about emissions, climate models, hazard models, sources, and our choices of normalization or weights. A single spread can hide all of them. Preserve climate-model identities when possible, so different hazard projections can be compared under a common driver. Shared models also mean several agreeing sources are not several independent confirmations.

For an initial map, colors might distinguish consistently lower, mixed trade-offs, consistently higher and insufficient information. The cutoffs are experiments, not accepted scientific categories. A place should keep its raw hazard profile even when its color changes.

The most relevant user decision is the time horizon: make mid-century the main view, or give mid- and late-century equal prominence? Hazard scope remains another choice: persistent heat/dryness belongs in this user's future-focused exploration, but should the headline eventually emphasize sudden disasters or include slow pressures equally? We can investigate sources while those choices remain open.

## Work still needed

Acquire small data samples and inspect actual coordinates, calendars, units, model membership and licenses. Read Forzieri's supplement. Test whether the same place order survives absolute versus local-relative definitions of heat and drought. Search specifically for robustness-based place selection before claiming novelty. No rankings, model results or preferred places were calculated during this literature pass.
