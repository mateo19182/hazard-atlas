# Hazard atlas

Private research repository: [mateo19182/hazard-atlas](https://github.com/mateo19182/hazard-atlas).

Find places with consistently lower natural-hazard exposure, and explain where indicators disagree and why.

Spain is the first study area. Future hazards around 2050 are the priority, with present-day conditions as a baseline. Worldwide coverage is a possible later extension. This is an exploratory research repository: the question is clearer than the method, and both can evolve as we learn.

The starting idea is a national map whose colors summarize physical hazards. A useful result would distinguish places that remain relatively low across defensible methods from places whose ranking depends on a particular dataset or weighting choice. Population, property prices and wealth should not determine the headline comparison.

## Starting questions

- Which places consistently show lower hazard across independent sources and reasonable methods?
- Where do indicators disagree, and is the cause coverage, resolution, time period, hazard definition, normalization or aggregation?
- What can we conclude when sources agree but share the same underlying model?
- How much local detail survives a national overview?
- Which conclusions transfer from Spain to a consistent global comparison?

We have not established scientific novelty. Multi-hazard indices and sensitivity analysis already exist. A possible contribution is a reproducible comparison of sources and methods, plus a clear public explanation of where conclusions hold and where they change.

## Start here

- [Galicia 10 km pilot](research/galicia-pilot.md): computed maps, model comparisons and reproduction.
- [Interactive explorer on Tailscale](https://m19182.tail5196fa.ts.net/galicia): requires the owner's network connection.
- [Official flood comparison](research/galicia-flood-validation.md) and [shallow-depth audit](research/galicia-flood-depth-audit.md).
- [Future fire-weather research](research/galicia-fire-weather.md): native data, periods and access limitations.

- [Future comparison](research/future-comparison.md): broader research direction, close precedents and candidate experiments.
- [Future flood audit](research/flood-future-audit.md) and [present flood audit](research/flood-present-audit.md): access, assumptions and comparison opportunities.
- [Spanish climate data check](research/adaptecca-access-check.md): acquired heatwave projections and a reproducible inspection.

- [First exploration](research/first-exploration.md): a small proposed comparison, new reading leads and verified data-access routes.

- [Research brief](research/brief.md): current direction, possible experiments and open decisions.
- [Conversation backfill](research/history.md): how the project developed and what the user selected.
- [Reading notes](research/reading-notes.md): findings and critiques from the papers and implementations reviewed.
- [Source catalogue](research/sources.json): papers, datasets, tools, precedents and earlier leads.
- [Data guide](data/README.md): local storage, provenance and reuse status.
- [Acquisition manifest](data/manifest.json): downloaded files and checksums.

## Current state

The Galicia pilot computes four climate indicators, two single-model fire-weather indicators and river-flood footprints on 362 clipped 10 km cells, retaining historical baselines, mid-century projections and model spread. An interactive explorer is available locally and through the owner's Tailscale network. There is no validated composite score or completed national dataset. A source listed in the catalogue is not necessarily downloaded, reproducible or approved for redistribution.

## Repository layout

```
research/          Brief, reading notes, source catalogue and history
scripts/           Acquisition and verification utilities
data/raw/          Original source files, stored locally and ignored by Git
data/derived/      Reproducible outputs, stored locally and ignored by Git
data/manifest.json Tracked provenance and checksums for local files
```

Raw material belongs in this project directory, including restricted papers supplied by the user. Git tracks the research and provenance rather than automatically uploading third-party data. The GitHub remote contains code, research and provenance. Ignored raw and derived files still need a separate backup/storage arrangement.

Names, hazards, spatial units, formulas, technology, licensing and product direction remain open. No project-wide license has been chosen; third-party works retain their own terms.


## Page development

The Spanish atlas uses one map with hazard tabs, historical/future views, a cell detail panel and expandable source notes. Its source is in `web/`; it has no framework or external runtime assets.

`uv run scripts/build_galicia.py` computes the research outputs and saves `data/derived/galicia/report-data.json`. For layout or wording changes, run `python scripts/render_galicia.py` to rebuild the self-contained page from that saved payload. `page-provenance.json` records the payload and page-source hashes separately from the scientific processing record. Tailscale serves the generated `galicia.html` at the existing address.
