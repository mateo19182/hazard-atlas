# Galicia flood comparison with official positive extents

Research date: 12 October 2026. This compares historical Aqueduct RP100 river flooding with official SNCZI T100 river-flood polygons. It does not validate the future climate response of Aqueduct.

## A working official data route

MITECO's [OGC API Features service](https://gis.miteco.gob.es/geoserver/ogc/features/v1/collections/agua:Zi_laminas_q100?f=json) supports bounded queries and pagination. The Galicia bounding box, west -9.35, south 41.75, east -6.7, north 43.85, matches 819 features. This avoids downloading the entire national archive. The full geometries and feature attributes are retained in the request snapshots.

MITECO's [download page](https://www.miteco.gob.es/es/cartografia-y-sig/ide/descargas/agua/zi-lamina.html) permits free reuse with attribution: Fuente: Ministerio para la Transición Ecológica y el Reto Demográfico.

[galicia-flood-validate.py](galicia-flood-validate.py) reproduces acquisition and calculation with `uv run research/galicia-flood-validate.py`. It preserves cached responses, checks pagination completeness and duplicate IDs, repairs invalid geometry if necessary, and records hashes. Raw responses are under `data/raw/public/galicia-snczi/`. The separate [artifact fragment](galicia-snczi-artifacts.json) records each request; the parent workflow integrates it into the shared inventory.

## What the comparison can establish

The official polygons identify mapped positive flood extents. They do not provide a boundary covering every studied-and-dry location. Therefore the comparison measures how much official positive area coincides with Aqueduct positive pixels. It also reports Aqueduct-only mapped area as a disagreement requiring investigation. Neither a false-positive rate nor overall map accuracy is justified.

Both products use the 100-year return period, but they differ in hydrology, terrain, historical window, river representation and local hydraulic assumptions. The national compilation contains study-level dates and methods rather than a single homogeneous model vintage. A planning cycle such as 2021–2027 or 2028–2033 is an administrative cycle, not a future climate scenario.

The method projects native Aqueduct pixels and SNCZI polygons to EPSG:3035 and computes their geometric area intersections within the existing Galicia boundary. It does not replace a fine polygon with its coarse-grid cell centre. Aqueduct's denominator includes finite, mapped pixels only. Regional capture uses official positive area covered by Aqueduct, with missing official-positive coverage reported separately. Per-cell outputs retain both all-official and covered-official denominators.

Official positive area divided by a 10 km cell's land area is a mapped-positive fraction. A zero remains unknown study coverage, not a lower-hazard classification. Aqueduct fractions for cells below 80% valid area are flagged so the report can retain the existing missing-data rule.

## Depth-threshold sensitivity

The Aqueduct extraction includes centimetre-scale positive depths across some northern coastal cells. A footprint defined as depth greater than zero counts these as flooded. We compare strictly greater than 0, 0.1, 0.5 and 1 metre to show this sensitivity. The thresholds change the question being asked, and are not competing calibrations selected to maximize agreement with SNCZI. Official polygons do not specify an equivalent depth cutoff.

The separate JRC/source-encoding audit investigates shallow positive depths and permanent-water handling. This comparison alone cannot explain those patterns or label them erroneous.

## Outputs

- `data/derived/galicia/flood-validation.json`: regional totals, study-attribute counts, source/grid hashes, and 362 matching cell IDs with positive-area and overlap values.
- `data/derived/galicia/snczi-t100-clipped.geojson`: official positive geometries clipped to Galicia, retaining attributes.

## Numerical results

All 819 bbox features were acquired without duplicate IDs. Of these, 766 have positive area within Galicia. Their dissolved mapped-positive extent is **258.98 km²**. Aqueduct has finite data over 252.12 km² of that extent; 6.86 km² falls outside its valid pixels. Official polygons occur in 206 of the 362 comparison cells.

| Aqueduct depth threshold | Aqueduct positive area, km² | Overlap with official positives, km² | Share of covered official positives captured |
| --- | ---: | ---: | ---: |
| >0 m | 2,481.67 | 74.09 | 29.39% |
| >0.1 m | 1,699.25 | 54.52 | 21.62% |
| >0.5 m | 653.45 | 47.74 | 18.94% |
| >1 m | 634.91 | 41.43 | 16.43% |

These regional totals use all finite native Aqueduct area inside Galicia, including the valid portions of comparison cells that fail the report's 80% display-coverage threshold. The capture denominator is the same 252.12 km² in each row. Raising the cutoff from zero to 0.1 m removes **31.53%** of Aqueduct's mapped-positive area. It also removes some overlap with official mapped positives, so the higher cutoff is not demonstrated to be more accurate.

The low positive-area agreement is substantial enough to investigate before using Aqueduct to identify favourable places. It does not prove the entire excess Aqueduct area is wrong. Official study coverage remains unknown outside the published positive polygons, and the source products differ in model setup and spatial detail.

Three adjacent inland cells are particularly useful follow-ups:

| Cell | Official positive area, km² | Aqueduct >0 positive area, km² | Approximate cell centre, longitude/latitude |
| --- | ---: | ---: | --- |
| E286_N228 | 23.90 | 0.00 | -7.729, 42.117 |
| E286_N227 | 17.64 | 0.00 | -7.703, 42.030 |
| E285_N227 | 9.35 | 0.00 | -7.821, 42.009 |

Each has effectively 100% finite Aqueduct area. The difference therefore cannot be dismissed as an ordinary nodata gap. Its cause remains unresolved. Next inspect the corresponding official river studies, represented Aqueduct river network, terrain and hydrological assumptions. These cells demonstrate why a modelled zero should not automatically receive a reassuring colour.

## Study metadata and checks

Among the 766 intersecting features, basin labels comprise Miño-Sil, 463; Galicia Costa, 282; Cantábrico Occidental, 13; and Duero, 8. These are feature counts, not independent studies or area weights. Hydraulic models include IBER, HEC-RAS 1D, INFOWORKS ICM and GUAD2D. Most terrain descriptions specify 1 or 2 m grids. Hypotheses include 508 natural-regime entries, 245 altered-regime entries and 13 natural-regime/geomorphology entries. Treat this as a mixed compilation.

The cycle field contains 350 cycle-1 features, 159 cycle-2, nine cycle-3 and 248 entries encoded as -9999. The last category is missing metadata, not a real cycle. Approval fields range from 2012 to 2025 and do not by themselves identify the climate baseline or terrain vintage.

The script repaired 26 invalid source geometries with GEOS `make_valid` before clipping. The source snapshots remain unchanged. Dissolving prevents overlapping official features from double-counting area. Exact overlay uses a spatial index of the dissolved polygon parts; no geometry simplification or raster-centre approximation is used.

All 31 raw artifacts passed size and SHA-256 checks. Summed cell official areas and threshold-specific intersection areas reconcile with independently accumulated regional areas within 0.001 km². The output records the Aqueduct raster hash and the grid hash. The report should reject a mismatched grid rather than silently attaching these values to different cells.

The [separate depth audit](galicia-flood-depth-audit.md) confirms that sampled shallow Aqueduct values match the original server data. Their cause is not established by this result.
