# Galicia flood access check

Checked 2026-10-12. The current research scope is Galicia, approximately 10 km comparison cells, with conditions around 2050 and a historical reference. We now have actual numerical flood data for this scope. These are model outputs, not a validated map of safe places.

## What is available locally

All rasters are under `data/raw/public/galicia-flood/`. Downloads used HTTP range reads, so we did not acquire global or continental rasters. The [artifact fragment](galicia-flood-artifacts.json) records eleven saved files with hashes. The [acquisition script](galicia-flood-acquire.py) reproduces the requests using `uv run --with rasterio --with pyproj python research/galicia-flood-acquire.py`.

| Source | Files acquired | Scope |
| --- | --- | --- |
| Aqueduct river flooding | Historical WATCH plus five climate models for RCP4.5, 2050, all RP100 | Bounding box west -9.35, south 41.75, east -6.7, north 43.85. This includes Galicia and some neighbouring land and sea; clip to the Galicia boundary before regional summaries |
| CoCliCo coastal flooding | Undefended RP100 baseline 2010 and SSP2-4.5 2050 | Matched 30 by 30 km windows around -8.85, 42.5 in Rías Baixas, including part of Ría de Arousa. An access sample, not Galicia-wide coastal coverage |

### River rasters

[Source download index](https://aqueduct.wridata.org/AqueductFloods20/index.html). Files use `galicia-bbox-inunriver_*.tif`. The five future climate models are NorESM1-M, GFDL-ESM2M, HadGEM2-ES, IPSL-CM5A-LR and MIROC-ESM-CHEM. Each saved raster has 318 columns and 252 rows in EPSG:4326 at 30 arc seconds. Pixel width on the ground differs from pixel height and varies with latitude. Reprojecting to a 10 km equal-area grid is reasonable for broad comparison, but it does not improve the input detail.

All six rasters share 57,393 non-nodata cells in the bounding box. Those cells include distinct zeros and positive depths. This confirms that the source encodes zero depth separately from nodata, unlike the coastal sample below.

| Bounding-box raster | Positive-depth cells | Zero-depth cells |
| --- | ---: | ---: |
| Historical WATCH | 4,717 | 52,676 |
| 2050 NorESM1-M | 4,687 | 52,706 |
| 2050 GFDL-ESM2M | 4,693 | 52,700 |
| 2050 HadGEM2-ES | 4,695 | 52,698 |
| 2050 IPSL-CM5A-LR | 4,706 | 52,687 |
| 2050 MIROC-ESM-CHEM | 4,681 | 52,712 |

These counts are an encoding check for an unmasked rectangle. They do not establish a trend for Galicia. Count differences also ignore changing depths and pixel areas.

The [Aqueduct methodology](https://files.wri.org/d8/s3fs-public/aqueduct-floods-methodology.pdf) identifies the historical river simulation as 1960–1999, and the 2050 slice as 2030–2069. The historical filename says `1980`; calling it present-day requires that qualification. Hazard maps omit flood defences. One hydrological model driven by five climate models supplies an ensemble of climate forcings, not five independent flood-modelling systems. Smaller rivers and pluvial flooding remain outside this comparison. A zero is modelled zero depth for that event and represented river network. It is not evidence of no flood hazard.

### Coastal rasters

The [CoCliCo item for 2050](https://minio.dive.edito.eu/project-coclico/coclico-stac-edito/cfhp_all/items/UNDEFENDED_MAPS/100/SSP245/2050.json) exposes a tile covering western Galicia. The actual header confirms 25 m pixels, EPSG:3035, float32 depth in metres, and nodata -9999. The [baseline item](https://minio.dive.edito.eu/project-coclico/coclico-stac-edito/cfhp_all/items/UNDEFENDED_MAPS/100/None/2010.json) provides matching data. Both item snapshots were saved.

The matched samples each contain 1,440,000 pixels. Baseline has 20,210 positive-depth pixels and 2050 has 21,190. Every other pixel is nodata; neither sample contains zeros. We therefore cannot classify those other pixels as surveyed dry land. The window includes water as well as land and cannot supply an inundated fraction of the local land area without another mask and a better understanding of the model domain. These samples prove that Galicia's coast has accessible future depth values.

The [collection](https://minio.dive.edito.eu/project-coclico/coclico-stac-edito/cfhp_all/collection.json) declares CC BY 4.0. Its undefended case still contains barriers represented in the terrain. Keep protection scenarios separate. Other metadata errors described in the [earlier audit](flood-future-audit.md) remain relevant: standard STAC geometry carries projected coordinates, and a band field incorrectly says 30 m. Use the raster georeferencing.

## Suggested contribution to the 10 km research map

For river flooding, calculate the fraction of modelled land in each Galicia-clipped cell with positive RP100 depth. Label it explicitly as Aqueduct modelled inundated fraction. Retain valid-area coverage, the baseline, all five future members, and their range. Area weighting should use projected area or geodesic pixel area. Do not let ocean, nodata, or cells outside Galicia enter the denominator. A 0.1 m depth threshold could be examined as a sensitivity check; adopting it changes the indicator and should be recorded.

The coastal samples should remain a separate access experiment for now. A future Galicia-wide coastal layer could report positive flood detections, but lower-hazard classification needs a documented model-domain mask. Combining the river and coastal layers by averaging their raw depths would confuse different processes and coverage.

No RCP8.5 river layers were acquired in this pass. The five-member RCP4.5 spread explores climate-model disagreement within one emissions scenario. It does not cover scenario uncertainty. Current data are adequate to start a labelled 2050 screening experiment while this remains explicit.
