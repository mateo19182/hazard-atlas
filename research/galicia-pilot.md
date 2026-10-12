# Galicia 10 km pilot

The first computed experiment covers Galicia on a 10 km square grid clipped to the regional boundary. It keeps climate indicators and river flooding separate, with historical and mid-century values, changes and model spread. This is a way to inspect evidence before selecting a combined score.

## Open the results

- [Interactive local report](../data/derived/galicia/galicia.html)
- [Four climate maps](../data/derived/galicia/galicia-climate.png)
- [Cell values as CSV](../data/derived/galicia/indicators.csv)
- [Grid as GeoJSON](../data/derived/galicia/grid.geojson)
- [Input hashes and processing record](../data/derived/galicia/provenance.json)

These are generated local files, excluded from Git alongside the source datasets. Scripts and research notes are tracked. Reproduce after acquiring inputs with `uv run scripts/build_galicia.py`.

## What we could obtain

| Layer | Models and scenarios | Time windows | Current coverage |
| --- | --- | --- | --- |
| Annual maximum temperature | 11 CMIP6 models, SSP2-4.5 and SSP3-7.0 | 1971–2000, 2011–2040, 2041–2070 | 348 of 362 clipped cells |
| Longest heatwave | 11 CMIP6 models, SSP2-4.5 | Same climate windows | 348 cells |
| Longest dry spell | 11 CMIP6 models, SSP2-4.5 and SSP3-7.0 | Same climate windows | 348 cells |
| Annual maximum daily rainfall | 11 CMIP6 models, SSP2-4.5 and SSP3-7.0 | Same climate windows | 348 cells |
| River inundation footprint, RP100 | Aqueduct WATCH reference and five climate forcings, RCP4.5 | 1960–1999 and 2030–2069 | 321 cells |
| Coastal inundation | CoCliCo matched baseline and SSP2-4.5 sample | 2010 label and 2050 | A separate 30 by 30 km Rías Baixas sample; excluded from the regional map |

The climate cells with sufficient coverage contain approximately 98.9% of the boundary area; the river cells contain approximately 96.1%. This describes whether inputs meet our coverage rule, not independent validation of the models. Missing coastal cells remain visible. Six clipped border cells are smaller than 1 square kilometre, so check each cell's area before comparing footprints or interpreting extremes.

## Processing choices

The grid uses EPSG:3035, 10,000 m sides and an origin at zero in projected coordinates. The GISCO ES11 boundary is generalized at 1:1 million. Its clipped area is approximately 29,573 square kilometres. Climate source cells are 0.05 degrees; their overlaps with each Galicia-clipped cell determine area weights. This aggregates source detail rather than inventing finer resolution.

For each model and period, calculate an area-weighted mean of the source indicator. Require at least 80% valid source-area coverage. Then calculate model medians and the 10th and 90th percentiles. These percentiles describe the available model ensemble, not a statistical confidence interval. The source's average member is excluded as a separate model. The coverage threshold is a pilot choice that can change.

Climate changes subtract the same model's historical value before calculating the median change. River changes compare each future forcing with the single WATCH reference. RCP4.5 and SSP2-4.5 are kept as distinct scenarios, and the climate and river time windows are displayed separately.

River footprint is the area of positive depth divided by valid model-covered area within each cell. Two versions are included: depth greater than zero and depth greater than 0.1 m. They are sensitivity comparisons; 0.1 m is not an adopted damage or safety threshold. River nodata masks were checked and are identical across the six files. Flood defences are excluded, and smaller-stream, surface-water and coastal flooding are not represented by this river layer.

The climate variables are annual-filter climatologies. Their source metadata still uses generic monthly names for some variables. We have not reproduced the annual-to-climatology processing, so these results should not be described as record extremes over the whole 30-year window. See the [definition audit](galicia-indicator-definitions.md).

## First observations worth investigating

The maps suggest lower absolute extreme heat in northern Galicia and higher values in parts of the south and interior. Longest locally defined heatwaves have a different pattern, including some northern hotspots. This is a useful example of disagreement caused by what indicators measure. A long departure from a cool historical climate does not automatically imply the highest absolute temperature.

Dry-spell length and heavy rainfall also have different spatial patterns. Wetter western areas can still have substantial dry spells. None of these climate indicators alone provides a flood probability, water-security measure or complete hazard assessment.

The river source contains repeated positive depths of only around 1–2 cm in some coastal locations. Counting all positive values can produce very large footprint percentages. The report includes the 0.1 m comparison to expose that sensitivity. For example, cells E291_N245 and E293_N243 change from 100% mapped future footprint at any positive depth to 0% above 0.1 m. That is a threshold effect in this model, not evidence that those places are safe. Source artefacts, coastal treatment and permanent water need closer investigation before using this layer to identify lower-hazard places.

These observations are exploratory. There is no combined ranking. Wind, landslides, seismic hazards and a complete coastal-flood domain remain outside the computed pilot. The fire-weather extension is described below. The 1971–2000 baseline is historical, not a claim about current observed conditions.

## Reproduce

1. `python scripts/acquire_galicia.py` acquires the boundary, documentation and climate files, reusing existing snapshots.
2. `uv run --with rasterio --with pyproj python research/galicia-flood-acquire.py` acquires the river and coastal windows. Its separate artifact manifest records the requests.
3. `uv run scripts/build_galicia.py` generates the grid, per-cell values, per-model climate arrays, maps and report.
4. `python scripts/verify_data.py` checks locally registered input files against their hashes.

The first pass verified grid-area conservation, coordinate alignment, data coverage, identical river masks, source hashes and complete model counts. The stricter flood-depth threshold never increases footprint, and every future median lies between its reported model percentiles. All report selectors and cell interactions were exercised in a headless browser without JavaScript errors. An independent review found the threshold issue above and prompted clearer river-change units and baseline wording.

Source descriptions and links are in [climate definitions](galicia-indicator-definitions.md) and [flood access findings](galicia-flood-access.md). Boundary source: [Eurostat GISCO NUTS 2024](https://gisco-services.ec.europa.eu/distribution/v2/nuts/nuts-2024-units.html).


## Flood and fire-weather extension

The private [GitHub repository](https://github.com/mateo19182/hazard-atlas) now stores the scripts, research and source manifests. The [live report on Tailscale](https://m19182.tail5196fa.ts.net/galicia) includes the new comparisons. Raw and generated data remain local and excluded from Git; the GitHub push is not a backup of these files.

The [official flood comparison](galicia-flood-validation.md) obtains SNCZI T100 fluvial polygons through MITECO's OGC API, preserving study attributes and checking complete pagination. It compares historical Aqueduct footprints at depth thresholds of 0, 0.1, 0.5 and 1 m. The report shows official positive extent, Aqueduct footprint and the fraction of covered official positives captured. A fixed 0–100% scale is used for Aqueduct fractions across thresholds. This is a positive-extent comparison, not an overall accuracy score: SNCZI study-domain coverage remains unknown. Planning-cycle dates are not future climate scenarios.

The [depth audit](galicia-flood-depth-audit.md) confirms that centimetre-scale depths occur in Aqueduct's original source, with no scaling or cropping error. Approximately 64% of future positive native pixels in the pixel-centre Galicia mask are no deeper than 10 cm. This is a diagnostic pixel count, not an area-weighted hazard estimate. JRC flood depth and water/caution masks provide another independent comparison. The precise cause of the shallow values remains unresolved.

The [fire-weather research](galicia-fire-weather.md) adds FIRE-RES June–August ensemble-mean FWI for 1995–2014 and 2041–2060, under SSP1-2.6, SSP2-4.5 and SSP5-8.5. Its approximately 0.5° cells are shown at native resolution in a separate panel. They cannot distinguish neighbouring 10 km cells. The NetCDFs do not identify their model members; differences between scenario means cannot be interpreted as isolated effects of emissions. FWI measures meteorological conditions favourable to fire, not ignition probability or burned area. Summer-only averages do not cover Galicia's full fire season.

Additional acquisition and processing commands:

- `uv run research/galicia-flood-validate.py` acquires official polygons and calculates the positive-extent comparison using the existing grid.
- `uv run --with rasterio python research/galicia-jrc-acquire.py` acquires independent JRC flood depths and masks.
- `uv run --with rasterio python research/galicia-flood-depth-check.py` runs source-depth and overlap diagnostics.
- `python scripts/acquire_fire_weather.py` acquires the coarse FIRE-RES summaries using bounded archive reads.
- After the optional comparisons have been generated, rerun `uv run scripts/build_galicia.py` to embed them in the self-contained report. Grid hashes must match; regenerate optional comparisons if the boundary or grid changes.


### Matched fire-weather climatologies on the 10 km grid

The finer Hetzer/FirEUrisk source now supplies an initial single-model comparison for MRI-ESM2-0 under SSP2-4.5: 1995–2014 versus 2041–2060. Forty bounded annual crops contain 14,610 daily bands in total, retaining leap days. Native resolution is 0.0703135°, approximately 6 by 8 km in Galicia. The source TIFFs have no CRS tag; interpreting their documented longitude/latitude grid as EPSG:4326 is recorded explicitly.

Two indicators enter the main 10 km selector: annual mean FWI and annual days with FWI strictly greater than 30. The threshold is applied to each native pixel and day before averaging years and spatial overlaps. Both periods must have every daily value on the same native pixel, and each target cell must meet 80% shared valid-area coverage. This leaves 326 mapped cells. Fractional days are spatial and climatological averages, not fractional observed fire events. This is an all-season indicator, distinct from the coarse June–August source above.

Across valid source area in the retained target cells, annual mean FWI increases from 5.09 to 6.06 and annual days above 30 from 3.15 to 3.93. These summarize one model, not a consensus forecast. No model percentiles or spread are reported. Exact values, windows, hashes and calendar checks are in `data/derived/galicia/fire-highres-provenance.json`.

To reproduce, install Playwright Chromium once with `uv run --with playwright playwright install chromium --only-shell`, then run `uv run research/galicia-fire9km-acquire.py`, `uv run scripts/build_fire_highres.py`, and finally `uv run scripts/build_galicia.py`. The acquisition script uses the public provider interface to obtain bounded range reads; temporary session headers and signed download links are kept outside the repository. Public transfer links may expire; the versioned source record links to the current provider README.


### Page presentation

The atlas is now in Spanish, with a single map and five hazard tabs. Future, historical and change views share the same cell selection. The layer selector retains official flood extents, historical Aqueduct threshold comparisons and source overlap. Coarse summer fire weather keeps its native grid. Source dates, units, single-model limits and missing-data distinctions remain visible; longer methods are expandable. Model-paired changes are labelled separately from differences between the displayed medians. CSV export contains the active layer's values and source.

The page can be rebuilt independently with `python scripts/render_galicia.py`. This changes presentation without recomputing the indicators.
