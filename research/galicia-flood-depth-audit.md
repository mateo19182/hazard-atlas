# Auditing Galicia's centimetre-scale flood depths

Checked 2026-10-12. The small Aqueduct values are present in the original source rasters. They are not introduced by our crop or display formatting. Their physical accuracy is unresolved, and the evidence does not justify treating all positive depth as equally meaningful flood extent.

## What we checked directly

The six stored Aqueduct rasters have scale 1 and offset 0. Three independent HTTP reads from the original historical global raster exactly reproduced local values, including 0.0111363186 m and 0.0201538689 m. The [provider's index](https://aqueduct.wridata.org/AqueductFloods20/index.html) explicitly specifies inundation depth in metres. There is no indication these are probabilities, centimetre-encoded integers or values needing another conversion.

The small values occur in large groups of exactly equal floats. In the unmasked bounding box, 543 pixels share 0.0111363186 m and 732 share 0.0201538689 m. All five future rasters retain groups of those sizes with different depths. Other repeated groups contain 1,271 and 905 pixels. This structure is already in the source, before our 10 km aggregation. It suggests model or terrain/downscaling structure, but does not identify a specific cause.

Using the existing Galicia boundary and a pixel-centre inclusion rule gives:

| Source | Positive-depth pixels | Pixels at 0 < depth ≤ 0.1 m | Pixels at depth > 0.1 m |
| --- | ---: | ---: | ---: |
| Historical WATCH | 3,962 | 1,254 | 2,708 |
| NorESM1-M 2050 | 3,940 | 2,521 | 1,419 |
| GFDL-ESM2M 2050 | 3,942 | 2,519 | 1,423 |
| HadGEM2-ES 2050 | 3,948 | 2,518 | 1,430 |
| IPSL-CM5A-LR 2050 | 3,953 | 2,522 | 1,431 |
| MIROC-ESM-CHEM 2050 | 3,933 | 2,519 | 1,414 |

These are pixel counts, not area-weighted regional estimates. Each raster has 45,591 valid pixels under this boundary rule. About 64% of future positive pixels have depths no greater than 10 cm. This makes the positive-depth footprint especially sensitive to interpretation. A count of wet pixels hides how much water the model predicts.

## What the method can explain, and what it cannot yet explain

The [Aqueduct technical note](https://files.wri.org/d8/s3fs-public/aqueduct-floods-methodology.pdf), appendix A.1.2, describes redistribution of flood volumes using height above nearest drainage and subbasins, starting at Strahler order six. It links the open-source wflow flood routine. Therefore neighbouring equal depths and dependence on the drainage/terrain representation are reasonable hypotheses to test. They are not confirmed explanations for these particular Galician pixels.

We inspected and saved the modeller's [downscaling driver](https://github.com/edwinkost/extreme_value_analysis/blob/master/downscaling_with_30min_option.py), [merge routine](https://github.com/edwinkost/extreme_value_analysis/blob/master/7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py), and [wflow flood library](https://github.com/edwinkost/wflow/blob/master/wflow-py/Scripts/wflow_flood_lib.py). The driver references the Aqueduct workflow. The library's `derive_HAND` computes terrain relative to drainage, and normally clips negative relative elevations to zero. `volume_spread` redistributes subcatchment volume across that relative terrain. The merge routine applies lake/reservoir masks. These are useful leads, but the downloaded branch has not been proven to be the exact code and configuration that generated the 2020 release. Do not claim a demonstrated bug, an intentional 1 cm floor, or a confirmed permanent-water explanation.

An exact diagnosis would require the corresponding terrain, drainage/HAND, subcatchment masks and generation configuration, or clarification from the data authors. No author contact was made. Raising a threshold does not repair the underlying map; it changes what we measure.

## Independent JRC data acquired

We acquired a matching Galicia bounding-box crop of the current [JRC European RP100 depth map](https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-EFAS/flood_hazard/), with its permanent-water and spurious-depth masks. All three are 3 arc seconds in EPSG:4326. No complete continental raster was downloaded.

The [README](https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-EFAS/flood_hazard/README.txt) identifies version 3.1.1 and explains that the spurious-depth mask includes small channels with modelled RP10 depth above 10 m and a 2 km buffer. It is a caution mask, not a declaration that every pixel is wrong. Permanent-water areas were used to patch the depth map. Preserve both masks in comparisons.

In the saved crop, JRC depth values start at approximately 0.1 m and all other pixels are nodata; there are no zero-depth pixels. Both masks contain ones and nodata. Consequently JRC's non-positive footprint cannot be treated as proof of modelled dry land or complete study coverage. Strict `>0.1 m` also differs from `>=0.1 m`, since it removes the first depth bin.

For a first spatial check, the fine JRC positive footprints were averaged into each Aqueduct pixel with all other JRC pixels represented as absence of a positive detection. This is only an overlap diagnostic. It does not recode those other pixels as confirmed dry land.

Of the 1,254 baseline Aqueduct pixels with depths up to 0.1 m inside Galicia:

- 243 contain some JRC RP100 positive footprint.
- JRC's positive footprint occupies an average 6.21% of the Aqueduct pixel area in this group.
- Its permanent-water mask occupies an average 1.23%, and its spurious-depth caution mask 7.66%.

These measurements do not support explaining the whole shallow group as permanent water. They also do not establish which flood map is right. Different channel networks, epochs, methods and coverage can produce non-overlap. The companion SNCZI comparison provides a third source of positive evidence.

## Action for the pilot

Keep Aqueduct as an experimental future signal, but stop using `depth > 0` alone to imply meaningful hazard severity. Show threshold sensitivity at 0, 0.1, 0.5 and 1 m, together with actual depths and source/version labels. A 0.1 m threshold can be a comparison choice; this audit has not validated it as the correct safety threshold.

Do not use apparent agreement among five climate-forcing members to imply independence of flood modelling. All five share the hydrological/downscaling framework and spatial inputs. Stable centimetre-scale footprints could survive every member while remaining sensitive to a shared modelling assumption.

Retain JRC's permanent-water and caution masks separately. Compare positive footprints with SNCZI and investigate a few named river reaches before restoring any overall lower-hazard ranking. Label unexplained non-overlap as disagreement, not false positives or false negatives.

## Reproducibility

- [JRC acquisition script](galicia-jrc-acquire.py) downloads documentation and extracts the three raster windows through HTTP range reads.
- [Diagnostic script](galicia-flood-depth-check.py) reproduces the pixel counts, JRC overlap and remote-source spot checks.
- [Artifact fragment](galicia-flood-depth-artifacts.json) records acquired files and local diagnostics with checksums.
- Detailed numerical output is `data/raw/public/galicia-flood-depth-audit/depth-statistics.json`.

The scripts require rasterio and NumPy; `uv run --with rasterio` supplies them. The diagnostic script depends on the previously acquired Aqueduct crops and Galicia boundary. It does not change the pilot build or main source catalogue.
