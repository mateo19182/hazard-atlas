# Galicia indicator definitions

Checked 2026-10-12 against the current AdapteCCa documentation. Scope is the proposed Galicia comparison at roughly 10 km, with mid-century priority. No scores calculated here.

## Period labels

The [data description, version 7.0, 13 June 2025, pages 6–7](https://escenarios.adaptecca.es/doc/datos.pdf?v=202506#page=6) defines:

| File period label | Calendar years | Recommended display |
| --- | --- | --- |
| reference | 1971–2000 | Historical reference, 1971–2000 |
| near | 2011–2040 | Near-term projection, 2011–2040 |
| medium | 2041–2070 | Mid-century, 2041–2070 |
| far | 2071–2100 | Late-century, 2071–2100 |

The same document identifies historical gridded observations and projections for mainland Spain with 1971–2000. Seasons are DJF, MAM, JJA and SON. Maps summarize climatologies over 30 years.

The [THREDDS guide, pages 10–11](https://escenarios.adaptecca.es/doc/thredds.pdf?v=202506#page=10) states that each future-scenario climatology file also contains the historical climatology. Annual historical files cover 1950–2014 and future files start in 2015. File coordinate names and storage calendars still require inspection; the table above describes climatic periods rather than asserting a Gregorian NetCDF calendar.

## Indicator meanings

Definitions follow [Table 2, page 13 of the data description](https://escenarios.adaptecca.es/doc/datos.pdf?v=202506#page=13). Machine identifiers are listed in the [THREDDS guide, page 6](https://escenarios.adaptecca.es/doc/thredds.pdf?v=202506#page=6); confirm each mapping against downloaded variable attributes.

| Identifier | Definition | Units |
| --- | --- | --- |
| tasmaxmax | Maximum daily maximum temperature, TXx | °C |
| tasmaxhwdmax | Longest heatwave, at least five consecutive days with maximum temperature above the reference 90th percentile | Days |
| prspellb1 | Longest consecutive sequence below 1 mm daily precipitation, CDD | Days |
| prmax24 | Maximum daily precipitation, Rx1day | mm/day |

## Interpretation for our experiment

Call the first panel historical reference, not present-day. A 1971–2000 baseline cannot describe the climate of 2026. Obtaining a recent observed climatology is a separate task. Label the future panel with its full 2041–2070 window; “2050” alone obscures that it represents decades rather than a forecast for one year.

Use TXx as the main absolute heat comparison and heatwave duration as a companion. A long locally unusual warm spell in a cool location can have a lower absolute temperature than a shorter spell elsewhere. Combining both as independently weighted hazards would double-count some heat information.

For annual climatologies, describe values as typical annual extremes over the period after confirming the file's aggregation. Do not call TXx the hottest temperature reached anywhere in the entire 30-year window. Likewise, a non-integer duration is consistent with averaging annual longest spells and model members; it is not a fractional observed event. The public definition alone does not establish the precise order of all aggregations in an arbitrary downloaded array.

CDD is a dry-spell indicator. It does not measure reservoir supply, soil moisture or household water scarcity. Rx1day is rainfall pressure. It does not measure river/coastal flood depth, drainage, runoff or flash-flood probability. Keep flood data separate.

The dry-spell table heading uses <1 mm, while its explanatory prose is less precise about equality. Use <1 mm in labels, record the discrepancy if reproducing the index, and check calculation code before claiming exact boundary equivalence. The heatwave definition does not specify every percentile-estimation detail, such as the calendar-day window; do not invent those details.

At roughly 10 km, retain source-cell values and the aggregation rule. Area averages can hide coastal or mountain extremes. Avoid implying address-level precision. These are proposals for clear interpretation, not a final scoring design.

Review depth: relevant sections of both official PDFs and the official FAQ read. No source calculation code or daily-data reproduction audited in this pass.
