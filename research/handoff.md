# Work handoff

Updated 2026-10-12. The user requested a wrap-up, GitHub push and public repository. Public source availability does not make the Tailscale explorer public or grant redistribution rights to third-party data. No project license has been selected.

## Current state

The working deliverable is a Spanish Galicia hazard explorer on 362 clipped 10 km cells. It shows separate indicators, historical and mid-century values, changes, available model spread and source comparisons. There is no validated composite score, stable lower-hazard shortlist or completed Spain-wide dataset.

- Four climate indicators use 11 models, with 348 covered cells. Most have SSP2-4.5 and SSP3-7.0; heatwave duration currently has SSP2-4.5 only.
- River flood footprints use five future forcings under RCP4.5, with 321 covered cells and a single historical WATCH reference.
- Two detailed fire-weather indicators cover 326 cells, using MRI-ESM2-0 under SSP2-4.5 only. Coarse FIRE-RES summer summaries remain separate regional context.
- Official SNCZI flood comparisons and the shallow-depth audit are complete as exploratory comparisons. Their disagreements remain unresolved.
- Coastal flooding is a small separate sample. Surface-water flooding, wind, landslides and seismic hazards are outside the computed pilot.

The static page is served by Tailscale at https://m19182.tail5196fa.ts.net/galicia from `data/derived/galicia/galicia.html`. No application backend is required. At wrap-up, no project acquisition or processing job was running.

## Verification at wrap-up

`python3 scripts/verify_data.py` passed for 157 registered local artifacts and 102 source records. The live page returned HTTP 200. The page, payload and source hashes matched `page-provenance.json`. All six existing Git commits were checked for common credential patterns and tracked raw/derived data; no matches were found. This was a targeted publication check, not a comprehensive security audit.

The scientific pipeline and browser interactions were not rerun during wrap-up. Earlier processing and browser checks are documented in [the pilot](galicia-pilot.md).

## Recommended next work

These are recommendations from the status assessment, not an approved final method or committed roadmap.

1. Investigate the three cells in [the flood comparison](galicia-flood-validation.md) where official positive flood area coexists with zero Aqueduct flood area. Check river representation, terrain and study assumptions. Aqueduct captures about 29% of covered official positive area at any positive depth; this is not an overall accuracy score. Do not use its zeros as evidence of safety.
2. Run a small robustness experiment on existing climate data. Compare which cells remain relatively low across models, scenarios and absolute versus locally relative indicators. Define the comparison and missing-data rules explicitly, preserve raw profiles and avoid double-counting related heat indicators. Keep unresolved flood results out of reassuring classifications.
3. Add matched fire-weather models before drawing ensemble conclusions from the finer fire layer.
4. Consolidate the build sequence and artifact-manifest registration, pin dependencies and retain repeatable scientific checks. Verify a separate backup of local data.
5. Expand beyond Galicia after the comparison produces useful, interpretable conclusions.

A recent observed baseline is still missing. The climate reference of 1971–2000 describes historical conditions, not present-day observations. Indicator aggregation from annual data to published climatologies has not been independently reproduced.

## Resume locally

Start with [the pilot and reproduction commands](galicia-pilot.md), [indicator definitions](galicia-indicator-definitions.md), [flood comparison](galicia-flood-validation.md) and [fire-weather notes](galicia-fire-weather.md).

- Verify local inputs with `python3 scripts/verify_data.py`.
- Rebuild presentation only with `python3 scripts/render_galicia.py`. This requires the saved `data/derived/galicia/report-data.json`.
- Recompute the main pilot with `uv run scripts/build_galicia.py`. Optional fire and flood comparisons require their own acquisition/build steps, documented in the pilot. Regenerate them if the grid changes.
- Inspect hosting with `tailscale serve status`.

A fresh clone does not contain raw inputs or generated reports. Local raw data occupy about 1.3 GB and derived data about 325 MB. GitHub does not back them up. Some fire acquisition depends on browser automation and temporary provider download links; cached inputs and their hashes are valuable for resuming.

## Keep the work manageable

Keep the static page and the separation between scientific processing and rendering. Defer global coverage, a large hazard catalogue and competing composite formulas until the first robustness experiment is useful. Scripts are small but densely formatted, and acquisition/processing is split between `scripts/` and `research/`; improve readability and coordination without introducing a framework.

Older briefs and access notes preserve research history and sometimes describe already completed work as future work. Use this handoff and the latest sections of the pilot for current status. Earlier suggestions about PCA, national expansion and alternative data sources remain tentative.
