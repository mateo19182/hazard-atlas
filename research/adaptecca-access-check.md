# Spanish future climate data access check

The AdapteCCa THREDDS server provides downloadable future climate data. We acquired and opened one CMIP6 SSP2-4.5 heatwave-duration file, approximately 123 MB. This establishes a working data route for the research, not a result about lower-hazard places.

The file contains 11 climate-model members plus their average, four named periods, monthly/seasonal/annual filters and a 251 by 400 grid. It includes absolute values, anomalies and relative anomalies. Preserve individual members when comparing places; the average is not another independent model. The embedded license states CC BY 4.0. The portal also describes model-specific terms, particularly for CORDEX, so do not extend this file's license to every collection.

The heatwave measure is the maximum consecutive days above the local climatological 90th percentile. It is useful for persistent unusual heat, but is not an absolute temperature measure. Pair it with an absolute heat indicator before comparing a cool northern location with a hot southern one. The period coordinates are names such as `medium_future`; confirm their calendar bounds from documentation before labeling any map 2050.

The FAQ identifies a promising disagreement case: statistical CMIP6 and adjusted EURO-CORDEX projections can disagree on the direction of Mediterranean extreme-rainfall change. The portal links that uncertainty to regionalization and difficulty representing convection. Our proposed investigation is to compare those signals at the same places and periods, then examine whether flood-model conclusions change. Do not turn precipitation changes directly into inundation depths.

Sources: [FAQ](https://escenarios.adaptecca.es/faq), [data access](https://escenarios.adaptecca.es/data), [terms](https://escenarios.adaptecca.es/terminos), [heatwave catalogue](https://escenarios.adaptecca.es/thredds/catalog/peninsula/Proyecciones_CMIP6_en_rejilla/Climatologia/Temperatura/tasmaxhwdmax/catalog.xml). Copies and the NetCDF are in the acquisition manifest.

Reproduce the inspection with `uv run scripts/inspect_heat_sample.py`. It checks the input hash, extracts metadata and reads an annual field to confirm usable numerical data. Output is `data/derived/adaptecca-heat-sample-inspection.json`. It does not rank places. The grid rectangle is not a national boundary, and this sample does not include the separate Canary collection.
