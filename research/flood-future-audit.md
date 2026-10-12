# Future flood sources: first audit

Research date: 2026-10-12. Future hazards are the user's priority, with present conditions retained as a reference. This audit checks access and suitability; it does not validate predictions or rank places.

## What I would investigate first

A Spain-wide search for places that remain lower-hazard across futures is feasible enough to investigate now. Flooding needs separate river, coastal and rainfall-driven layers. Two useful routes are already accessible: Aqueduct for global future river flooding and CoCliCo for detailed European coastal projections. They have very different strengths. Keep their outputs separate until their coverage and assumptions are understood.

A useful research output would show three things for each candidate place: current hazard, projected future hazard, and whether its relative position survives changing the source or scenario. A place with modest projected change can still have high absolute hazard. Neither a large increase from a tiny baseline nor a small increase from a dangerous baseline should dominate interpretation automatically.

## Source audit

| Source | Physical quantity and futures | Role and access status |
| --- | --- | --- |
| [Aqueduct Floods v2](https://aqueduct.wridata.org/AqueductFloods20/index.html) | River and coastal inundation depth in metres; historical, 2030, 2050, 2080; RCP4.5 and RCP8.5 | Global comparison route. Actual GeoTIFF download links verified, documentation saved; large rasters not downloaded |
| [CoCliCo flood collection](https://minio.dive.edito.eu/project-coclico/coclico-stac-edito/cfhp_all/collection.json) | European coastal maximum depth and extent; 2010, 2030, 2050, 2100; SSP1-2.6, SSP2-4.5, SSP5-8.5 and high-end options | Strong open coastal candidate. STAC saved, raster header read, small Spanish raster window acquired |
| [Valencian PIMA Adapta](https://dadesobertes.gva.es/dataset/pima-adapta-impactos-escenarios-de-inundacion) | Coastal inundation for current and future sea levels | Regional comparison candidate with eight direct TIFF downloads. Metadata and directory saved; raster contents not examined |
| [Fathom Global Flood Map](https://api-docs.fathom.global/data/dynamic_layers.html) | River, rainfall-driven and coastal flood depths, climate-conditioned through 2100 | Commercial comparison lead. Public API documentation checked; no licence or data acquired |
| [Copernicus sea-level indicators](https://cds.climate.copernicus.eu/datasets/sis-water-level-change-indicators-cmip6?tab=overview) | Water-level indicators, historical and future through 2050 under SSP5-8.5 | Supporting coastal driver. These are not land-inundation maps |

### Aqueduct: useful global ensemble, coarse local detail

The [download index](https://aqueduct.wridata.org/AqueductFloods20/index.html) supplies separate future river files for five climate models, rather than just an ensemble mean. Return periods include 2, 5, 10, 25, 50, 100, 250, 500 and 1,000 years. Coastal variants distinguish subsidence assumptions and percentiles. Preserve filenames and the October 2020 river bias-correction release.

The [methodology](https://files.wri.org/d8/s3fs-public/aqueduct-floods-methodology.pdf), sections 3 and A.1, uses PCR-GLOBWB 2 hydrology at 5 arc minutes with inundation downscaling to 30 arc seconds. River baseline simulations cover 1960–1999; labels 2030, 2050 and 2080 correspond to 2010–2049, 2030–2069 and 2060–2099. The tool's 2010 baseline label should not be mistaken for recent flood climatology. Coastal baseline tide/surge data cover 1979–2014. Hazard layers exclude flood defences; protection enters downstream risk calculations. Use hazard rasters, not affected people, GDP or damages. One hydrological model with several climate forcings does not capture all structural uncertainty.

[Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/WRI_Aqueduct_Flood_Hazard_Maps_V2) exposes `WRI/Aqueduct_Flood_Hazard_Maps/V2` and describes roughly 1 km pixels. It explicitly cautions against property-level inundation interpretation. [WRI's FAQ](https://www.wri.org/aqueduct/faq) describes CC BY 4.0 sharing with attribution and registration; preserve the applicable terms before redistribution.

### CoCliCo: actual coastal rasters, with metadata problems worth catching

The collection declares CC-BY-4.0 and names IHCantabria as producer. Its summaries distinguish no defence and low/high policy protection. The latter use regional protection assumptions, not surveyed protection at every site. Default scenario maps use the median; high-end includes low-confidence processes at the 83rd percentile. Scenario/year combinations need enumeration; a collection summary is not evidence that every combination exists.

[One verified item](https://minio.dive.edito.eu/project-coclico/coclico-stac-edito/cfhp_all/items/UNDEFENDED_MAPS/100/SSP245/2050.json) supplies public COG assets for undefended, 100-year, SSP2-4.5, 2050 conditions. Header inspection confirmed EPSG:3035, 25 m pixels, float32 and nodata -9999. Item metadata claims 30 m in a band field and puts projected coordinates into standard STAC geometry fields. Use actual raster georeferencing; do not trust generic STAC spatial filtering here. The collection called `floodmaps` is a different static sea-level visualization; the wanted collection is `cfhp_all`.

The [handbook](https://www.openearth.nl/coclico-workbench/Datasets/) describes process-based flooding, elevation, roughness, hydrodynamics and climate inputs. Its available ensemble descriptions should not be assumed to describe every raster. Audit subsidence, model coverage, baseline assumptions and defences in the linked technical report before comparative analysis. Spain's islands and autonomous cities require explicit coverage checks.

### Valencian PIMA Adapta: promising third view for one coast

The [official catalogue](https://dadesobertes.gva.es/dataset/pima-adapta-impactos-escenarios-de-inundacion) lists current 100/500-year events; RCP4.5 at 2050 and 2100; and RCP8.5 at 2100, each at both return periods. It identifies a Creative Commons Attribution licence. The [public TIFF directory](https://descargas.icv.gva.es/dcd/05_medioambiente/07_riesgos_cclimatico/PIMA/pima_impactos_inun/) contains all eight files. Example: `0507_pima_impactos_inun_escenario3_f452050100.tif`.

This provides a concrete regional comparison with CoCliCo, but RCP4.5 and SSP2-4.5 are not interchangeable experiments. Resolve grid size, water-depth encoding, baseline, protection and underlying model lineage before treating differences as independent evidence. The catalogue alone does not answer these questions.

### Rainfall-driven flooding remains an access gap

Fathom's [documented API](https://api-docs.fathom.global/data/dynamic_layers.html) has 1-arc-second layers, years 2011–2100, return periods 5–1,000, and defended/undefended river and coastal options plus defended pluvial. Access is subject to licence restrictions. [Wing et al. 2024](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2023WR036460) describes the model scientifically. An accessible paper does not grant redistribution rights to the maps.

This pass did not locate and validate an openly downloadable, Spain-wide future pluvial inundation layer. That is a research gap, not proof none exists. Future heavy-rainfall indices could support screening, but rainfall intensity is not a replacement for runoff, drainage and water-depth modelling. Do not paint unmapped urban pluvial hazards green.

## A more ambitious first experiment

1. Retain the present-day SNCZI/JRC river comparison as a quality check while adding Aqueduct's baseline and 2050 ensemble. Inspect whether places appear lower-hazard because of coarse resolution, missing smaller rivers, or a different climate baseline.
2. In parallel, compare coastal futures using CoCliCo across Spain's covered coasts. Test current, 2050 and 2100, with median and available high-end assumptions kept visible. Use the Valencian PIMA maps for a regional comparison after checking shared inputs.
3. Summarise candidate areas by absolute depth/extent and changes, plus the fraction of tested assumptions under which they remain below an explicit threshold. Report this as agreement across tested cases, not a probability that the place is safe.
4. Keep undefended physical hazard as the initial comparison, with protected variants as a separate sensitivity experiment. The user has not yet decided how much protection should count in the main interpretation.
5. Avoid a flood-only 'safest places' list. Combine the flood findings with separate future heat, fire and drought research before considering any overall shortlist.

World expansion is plausible through Aqueduct, and possibly licensed Fathom if it later proves worthwhile. Europe-specific coastal detail would remain an additional layer, with its coverage visible. A uniform global score must not silently reward countries with sparse mapping.

## What was actually saved

See [artifact fragment](flood-future-artifacts.json). Saved eight primary-source documents or metadata snapshots, a local raster access record, and a small CoCliCo raster window around the Valencian coast. The window was extracted through HTTP range reads, not a complete continental download. Its purpose is to prove accessible numerical data and inspect encoding. It does not establish a location's flood status or source quality. Raw artifacts live outside Git under `data/raw/public/future-flood-audit/`.

## Decisions to revisit after inspecting the data

The user selected around 2050 with a present-day baseline. End-of-century results can serve as an optional stress test. A second decision is whether protection should improve the headline assessment or remain separate. No new scoring formula is needed to begin these comparisons.
