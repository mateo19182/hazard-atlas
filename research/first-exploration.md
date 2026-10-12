# First exploration

Start by finding out whether different sources tell a consistent story about the same places. Keep the first experiment small enough to inspect every result. A national composite can wait until we understand one useful disagreement.

## What existing work gives us

| Work | What we can learn | Next reading task |
| --- | --- | --- |
| [ThinkHazard](https://gfdrr.github.io/thinkhazard/) | Hazard-specific thresholds and global coverage | Check usable Spanish classifications and source dependencies |
| [UNICEF MHI](https://github.com/unicef/CCRR/tree/main/Multi_Hazard_Indicators/MHI) | A physical climate-hazard composite before downstream population analysis | Check which inputs we can reproduce and whether higher hazards always raise the index |
| [White et al. 2025](https://nhess.copernicus.org/articles/25/4263/2025/) | Review of 192 publications; distinguishes overlapping layers from interacting hazards | Follow references most relevant to comparing indicators and uncertainty |
| [Johansson et al. 2021](https://www.lunduniversity.lu.se/publication/7f333041-7b9b-4b80-87ee-ccf2b9d6a2f6) | Review of combining hazards for Sweden and the EXTREME-INDEX project | Read full report and trace resulting project work |

The two new reviews are reading leads, not evidence that our idea is novel. The Swedish report's summary already identifies normalization and weighting as central problems. A useful project can still come from making the evidence easier to compare and investigate.

## First candidate experiment

Compare river-flood extent at a 100-year return period using SNCZI and JRC. This is a proposed first exercise, not a decision to make flooding the whole project. It also does not establish which places have low overall hazard.

| Question | SNCZI | JRC European flood maps |
| --- | --- | --- |
| What is available? | Flood extent polygons, with separate mainland/Balearic and Canary downloads | Water-depth rasters for several return periods |
| Access checked | Official download listing | Public file directory and README |
| Spatial detail | Stated map scale 1:25,000 | 3 arc seconds, approximately 90 m |
| Key coverage issue | Only some rivers have mapped studies | Catalogue describes catchments larger than 150 square kilometres |
| Reuse information | Free use with specified MITECO attribution | Catalogue states CC BY 4.0 |
| Version to preserve | Listing updated June 2026; inspect archive metadata | README identifies v3.1.1, March 2026 |

Sources: [SNCZI download page](https://www.miteco.gob.es/es/cartografia-y-sig/ide/descargas/agua/zi-lamina.html), [JRC catalogue](https://data.jrc.ec.europa.eu/dataset/1d128b6c-a4ee-4858-9e34-6210707f3c81), [README](https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-EFAS/flood_hazard/README.txt) and [changelog](https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-EFAS/flood_hazard/CHANGELOG.txt).

The JRC directory exposes a roughly 308 MB 100-year raster, plus permanent-water and spurious-depth masks. The README warns about unusually high modelled depths in some small channels. Preserve those masks when acquiring the raster. The catalogue dates and file versions differ, so use file metadata and hashes to identify the actual input.

SNCZI lists roughly 0.98 GB for the mainland/Balearic 100-year archive. A polygon's absence does not establish that the location was studied and found dry. Finding a trustworthy study-coverage boundary is the first practical hurdle. Do not use the flood boundary itself as that boundary.

## Smallest useful output

1. Inspect one manageable river corridor with overlapping study coverage. The Ebro near Zaragoza is a candidate, subject to metadata checks. Retain a contrasting small-catchment case to expose coverage limitations.
2. Match the return period and inspect flood defences, flow assumptions, dates, raster thresholds and coordinate systems before calculating agreement.
3. Draw one comparison map with both mapped wet, SNCZI only, JRC only, neither mapped wet within confirmed shared coverage, and unknown coverage. Keep permanent water separate.
4. Write a short explanation for a few disagreement areas. Mark each explanation as documented, plausible or unresolved.

Only after that should we expand the comparison across Spain. If study coverage cannot be established, report positive flood detections and unresolved absence; do not manufacture a lower-hazard map.

No geospatial comparison has been run yet. This pass verified documentation and download routes and preserved reference snapshots; it did not acquire the large hazard layers.

## Ideas worth keeping open

- A disagreement map may be useful before any composite exists. Clicking a place could answer which sources disagree and what they actually measure.
- A shortlist could show places that remain relatively low under several plausible choices, alongside what would change that conclusion.
- Pairwise comparisons could explain why place A looks preferable to B, and where there is a trade-off. A single winner may be unnecessary.
- A place can remain a candidate when data are incomplete, but its unknowns must be visible rather than converted to reassuring green.

## Decision pending

The user now prioritizes future hazards, with present-day conditions still relevant. The flood comparison remains a baseline audit within a broader future-hazard investigation. The user selected around 2050 with a present-day baseline.

Hazard selection, final scoring, grid size and interface can stay open until this first comparison teaches us something.
