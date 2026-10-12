# Present-day flood source audit

Research pass: 12 October 2026. Future hazards are now the user's priority; this comparison supplies a present-day baseline and a way to investigate disagreement. No spatial comparison has been run.

## What changed since the first exploration

There is an official inventory of studied river segments, which helps with the coverage problem. It does not resolve it. There is also direct prior work comparing European JRC maps with Spanish official maps. We should reproduce and extend that comparison rather than call the overlay itself new.

## SNCZI coverage and interpretation

The [inventory of studied segments](https://www.miteco.gob.es/es/cartografia-y-sig/ide/descargas/agua/inventario-tramos.html) lists an 18.19 MB shapefile. These are river lines covering studies of DPH or flood risk, segmented at province boundaries. The page reports a 16 November 2018 update. Its historical coverage percentages must not be presented as current national coverage.

The inventory download is not yet usable through the tested route. Its linked `www.mapama.gob.es` archive failed TLS certificate verification in this environment; substituting the MITECO hostname returned 404. A guessed migrated GeoServer service also returned 404. Keep this as an access lead, not an acquired dataset.

A segment confirms a study existed somewhere along a river. It does not establish that every adjoining pixel was simulated for T100. A DPH study need not provide all return periods. We must inspect the attributes and study metadata before constructing a coverage mask. An arbitrary buffer would be an analysis choice, with sensitivity checks, not an official study boundary.

The [current download listing](https://www.miteco.gob.es/es/cartografia-y-sig/ide/descargas/agua/zi-lamina.html) provides national flood polygons, including separate Canary files. The existing first exploration records the T100 mainland/Balearic archive at roughly 0.98 GB. The data are free to reuse with MITECO attribution. Download-page dates describe the compilation; they do not prove a uniform hydrological baseline across studies.

There is a further source of apparent disagreement. The [third-cycle SNCZI guide](https://www.miteco.gob.es/content/dam/miteco/es/agua/temas/gestion-de-los-riesgos-de-inundacion/mapri/Documento%20metodol%C3%B3gico%20SNCZI%20rev3C.pdf), sections 3.4, 3.5 and 4.6.3, describes removing building pixels from depth rasters while filling building holes in extent polygons. It also allows decisions about retaining modelled tributaries in final mapped extents. The guide shows that published geometry incorporates cartographic judgement. A dry pixel can reflect map production rather than a physical conclusion. These are current instructions, not proof that every legacy study followed them. Prefer extent-to-extent comparisons first and inspect depth separately.

## JRC current product and version traps

The [catalogue](https://data.jrc.ec.europa.eu/dataset/1d128b6c-a4ee-4858-9e34-6210707f3c81) describes approximately 90 m depth grids for European and Mediterranean rivers with upstream catchments above 150 square kilometres. It identifies CC BY 4.0 and anonymous downloads. This is river flooding, not a complete flood product for small ravines, urban rainfall or the sea.

The [README](https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-EFAS/flood_hazard/README.txt) identifies version 3.1.1, dated 5 March 2026, and MERIT terrain plus EFAS v5 reanalysis inputs. Preserve both permanent-water and spurious-depth masks. The latter flags unusually deep results in smaller channels and includes a 2 km buffer. Its coordinate bounding box is not evidence that every island or catchment has modelled flooding.

The [changelog](https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-EFAS/flood_hazard/CHANGELOG.txt) records artefact corrections in March 2026. Version 3.1 improved coastline masking and checked that flood area grows with return period. A source carrying the same dataset DOI can therefore contain different flood footprints depending on acquisition date.

The [CEMS method page](https://confluence.ecmwf.int/spaces/CEMS/pages/340774762/CEMS-Flood+flood+inundation+maps) explains fitting extreme-value distributions to historical modelled discharge, subtracting estimated bankfull flow, and mosaicking local hydraulic simulations using maximum depth in overlaps. The global equivalent uses a larger 500 square kilometre catchment threshold. The page is dated 2023 and lists seven return periods while the current catalogue lists nine. Use current files to establish available periods, and treat the page as method context. Historical reanalysis hazard maps are not future projections merely because the download was updated in 2026.

## Existing comparison and defences

[Dottori et al. 2022](https://essd.copernicus.org/articles/14/1549/2022/) already validated an earlier JRC release against Spain and other countries. The paper attributes discrepancies partly to missing flood defences, channel simplifications and differences in the mapped river network. Large buffers used for comparison could count modelled flooding outside the reference studies as false alarms. Its 500 square kilometre threshold and validation scores belong to that older model and must not be assigned to v3.1.1. Reusing the DOI does not make the methods interchangeable.

The paper makes defences a plausible explanation to test, not a universal explanation for every mismatch. The current JRC guide does not establish a complete local defence representation. For SNCZI, check the individual hydraulic study before assigning a defence assumption.

MITECO's [defence inventory announcement](https://www.miteco.gob.es/es/prensa/ultimas-noticias/2021/05/el_miteco_publicaelinventariodeobrasdedefensafrenteainundaciones.html) describes mapped walls, embankments, levees and related structures. Their presence could help explain disagreement; it does not supply a verified protection standard or failure probability for every structure.

## Concrete next experiment

Run a small panel of contrasting Spanish river corridors rather than selecting one supposedly representative location. Candidate cases are the Ebro near Zaragoza, a Mediterranean catchment near Valencia, and a northern Atlantic river. Selection remains provisional until study metadata and source coverage are inspected.

1. Acquire T100 and T500 JRC depths with both masks, the SNCZI T100/T500 extents, and the study inventory. Preserve hashes and source dates. Inspect the inventory attributes before downloading more ancillary layers.
2. Match study IDs and river network, and document a comparison domain for each corridor. Separate confirmed coverage from inferred coverage. Where coverage remains unresolved, compare positive detections without claiming the remaining land is lower hazard.
3. Show overlap, SNCZI-only and JRC-only extents. Keep permanent water and known model artefacts visible. Inspect effects of rasterization and depth threshold rather than tuning them to maximize agreement.
4. Explain a handful of mismatches using study boundaries, tributaries, building treatment, terrain and defences. Label explanations as documented, plausible or unresolved.
5. Use the same locations for the future-flood research. Compare climate-related change only within a product with a consistent historical baseline and future model setup. A difference between a present SNCZI map and a future global map combines climate change with model differences.

This panel serves the broader question: which places remain lower hazard under several plausible sources and future scenarios, and which favourable rankings depend on a disputed assumption?

## Acquisition record

Four small reference snapshots were saved under `data/raw/public/flood-present-audit/`. Their URLs, sizes and SHA-256 hashes are in [flood-present-artifacts.json](flood-present-artifacts.json), pending integration into the shared manifest. No flood raster or polygon archive was acquired in this pass.
