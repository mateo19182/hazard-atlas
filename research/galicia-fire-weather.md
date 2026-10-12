# Future fire weather for the Galicia pilot

Research and acquisition, 2026-10-12. Fire weather is now an authorized addition to the pilot. It describes meteorological conditions conducive to fire, not ignition probability, burned area, fuel availability, suppression or property loss.

## Data acquired

The [FIRE-RES portfolio](https://zenodo.org/records/11083641) supplies actual future FWI data without credentials, under CC-BY-4.0. We extracted seven small NetCDF ensemble summer summaries from its 8.5 GB EU_DATA.zip using HTTP byte ranges. This avoids downloading unrelated daily climate data. The publisher describes the index folder as ensemble means, with historical 1995–2014, mid-century 2041–2060 and late-century 2081–2100 periods. Future scenarios are SSP1-2.6, SSP2-4.5 and SSP5-8.5.

Native files are in `data/raw/public/galicia-fire-weather/`. [acquire_fire_weather.py](../scripts/acquire_fire_weather.py) reproduces acquisition and writes `fire-res-provenance.json`, a standalone fragment for the shared manifest. ZIP CRC and file SHA256 are checked or recorded. The source record JSON, archive listing and alternative dataset README are preserved alongside them.

Direct file inspection found:

| Property | Observed value |
| --- | --- |
| Dimensions | time 1, latitude 79, longitude 143 |
| Coordinate names | time, lat, lon |
| Grid | Longitude spacing 0.5 degrees; latitude spacing roughly 0.5 degrees, slightly irregular |
| Variable | FWI, float32 |
| Variable description | ensemble mean FWI |
| Time coordinate in mid-century SSP245 file | 2041-06-01, a representative coordinate for a climatology, not one day's data |
| Native units attribute | Absent; FWI is dimensionless by index definition |
| Member dimension | Absent |
| Seasonal identification | JJA in the source filenames |

This is regional context at roughly 40–55 km, depending on latitude and direction. Drawing it on 10 km cells cannot add information. Display the native coarse grid separately. The summer-only summary misses potentially important fire weather during Galicia's other seasons.

Do not claim a five-member ensemble. Although the publisher describes five models overall, the EU_DATA archive's daily FWI members expose four names, with only three represented for SSP245. The small ensemble files contain no membership list or calculation history that resolves this discrepancy. Consequently, their model spread and exact averaging membership are not available from these summaries.

## Higher-resolution route under investigation

[Hetzer's dataset, version 1.1](https://zenodo.org/records/19792063), associated with [Hetzer et al. 2024](https://doi.org/10.1088/1748-9326/ad5b09), provides six downscaled CMIP6 models and four SSPs. The native spacing is 0.0703135 degrees. The authors describe it as approximately 9 km; angular grid spacing is not a constant 9 km square. Zenodo's API confirms CC-BY-4.0. The six names are ACCESS-CM2, CanESM5, CNRM-ESM2-1, EC-EARTH3, MPI-ESM1-2-HR and MRI-ESM2-0.

The current README links to public Dropbox transfers. Their expiry is shown as 2027-04-26. We verified the MRI-ESM2-0 SSP245 transfer is live and lists 86 annual daily-data TIFFs, 2015–2100, at roughly 338 MB each. This extends beyond the README's stated end date, so metadata and band calendars must be checked before use. The README describes 365 daily bands per annual file. The public UI has a download-only path without account registration; obtaining range-readable TIFF URLs and bounding the download to Galicia is the current next step.

The much smaller q95 summary bundle covers broad historical and future periods. It is not an established mid-century-only product and should not be used as a 2050 substitute. Matching the AdapteCCa 1971–2000 versus 2041–2070 windows would require more annual acquisition; this first fire experiment uses 1995–2014 versus 2041–2060.

## Other route checked

[C3S European fire-danger projections](https://cds.climate.copernicus.eu/datasets/sis-tourism-fire-danger-indicators?tab=overview) remains a strong alternative. It provides EURO-CORDEX-driven FWI under historical and RCP scenarios. Standard local CDS credential-file and environment-variable existence checks found none; no secret values were read or printed. We did not register an account or submit a CDS retrieval.

The [European Climate Data Explorer documentation](https://confluence.ecmwf.int/spaces/CKB/pages/453680707/Input+data+underpinning+the+European+Climate+Data+Explorer+Description+of+the+datasets+and+variables) identifies publicly described FWI products near 0.1 degrees, but presents inconsistent model counts across its overview and detailed sections. Downloaded-file membership would take precedence over a presumed count.

## Integration guidance

Keep the acquired coarse summer mean separate from the AdapteCCa 2041–2070 climate comparison. Use full period labels, native-grid information and a clear statement that model spread is unavailable. Do not treat it as independent of heat and dryness; FWI is calculated from related meteorological drivers. When higher-resolution daily data become usable, calculate each model's period summary before aggregating models and retain the member values. Neither dataset currently supports a probability that a Galicia location will burn.

Review depth: public catalogues, README, archive member list and downloaded NetCDF metadata inspected. One high-resolution TIFF header was subsequently inspected in the parallel acquisition audit below; daily calculations and author calculation code have not been audited. No fire-weather ranking or model validation was performed in this note.

## Preliminary regional comparison

The pilot build reports 27 native coarse cells with 97.4% valid shared-area coverage. Its area-weighted Galicia means are 9.4844 for 1995–2014, and 13.7043, 11.2560 and 11.7330 for 2041–2060 under SSP126, SSP245 and SSP585 respectively. These are preliminary regional summaries supplied by the build, not an independent validation in this note.

SSP126 has the highest future value in this particular product. Unequal or unresolved ensemble membership, internal variability and other processing choices could contribute. The scenario comparison does not isolate the causal effect of emissions. Preserve this unexpected result as a research question; do not reorder, smooth or recalibrate it to fit expectations.

## Higher-resolution access proof

The parallel acquisition audit obtained a public download-only URL for MRI-ESM2-0 SSP245 year 2050 and confirmed HTTP 206 byte-range access. Header inspection found a 557 by 711 TIFF with 365 float32 daily bands, NaN nodata and 0.0703135-degree spacing. The file has no CRS tag. Its geographic coordinate bounds agree with the publisher's European domain, but attaching EPSG:4326 is an explicit interpretation requiring documentation rather than a stored-file assertion.

The TIFF uses pixel-interleaved, LZW-compressed strips one row high. Reading a Galicia window across all bands is more efficient than issuing separate daily-band reads. A bounded annual crop is feasible; one year remains an access proof rather than a 30-year climate statistic. The completed paired historical and mid-century calculation is recorded below.

## First matched-model calculation

The completed bounded acquisition covers MRI-ESM2-0 alone, historical 1995–2014 and SSP2-4.5 2041–2060. [build_fire_highres.py](../scripts/build_fire_highres.py) requires all 40 annual crops before it writes an optional `fire-highres.json` for integration. It computes the annual mean FWI and the annual number of daily values strictly above 30, then averages each measure across 20 complete years. These use all seasons, which is preferable to assuming summer represents the full Galicia fire season.

The processor uses actual annual band counts, allowing 365 or 366. The 1996 source header contains 366 bands, contradicting the README's blanket 365-day description. The processor verifies that each file's count matches its calendar year's length; no leap years are dropped. Native pixels must have every daily value in every year in both periods. The same valid pixels are area-weighted into the existing 10 km Galicia cells, with an 80% minimum valid-area requirement. This preserves the distinction between no data and zero days above threshold.

Model count is one. Spread and ensemble quantiles remain null, and changes compare the same model in both periods. FWI >30 is a declared meteorological index threshold, not a calibrated probability of fire or a claim that all days below it are harmless. The calculation is a useful first local comparison but cannot establish agreement across climate models.


## Completed single-model results

All 40 annual crops were acquired and processed, covering 14,610 daily bands including ten leap years. The optional [high-resolution output](../data/derived/galicia/fire-highres.json) and [processing provenance](../data/derived/galicia/fire-highres-provenance.json) retain the existing pilot cell order and explicit single-model metadata.

326 target cells pass the 80% shared-area requirement. The source covers 97.4095% of the full Galicia grid area with complete data in both periods. Area-weighted means over valid source area within retained target cells are:

| Measure | 1995–2014 | 2041–2060, SSP2-4.5 |
| --- | ---: | ---: |
| Annual mean FWI | 5.0889 | 6.0599 |
| Annual days with FWI >30 | 3.1472 | 3.9306 |

Future cell values range from 3.4540 to 10.1533 for mean FWI and from 0 to 27.9479 days/year above 30. Fractional day counts result from averaging years and areas. These are projections from MRI-ESM2-0, not a multi-model conclusion. Comparisons against the coarse FIRE-RES summer means would mix season, model membership, source grid and processing choices; they do not isolate one source's bias.

Verification checked all 40 input hashes, 14,610 daily bands, geometry hash and target-cell order, coverage bounds, paired change arithmetic and null uncertainty fields. The result retains no near-term estimate or model spread. The headline project objective of locating places consistently lower across several hazard models remains open.
