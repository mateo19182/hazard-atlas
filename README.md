# Hazard atlas

Find places with consistently lower natural-hazard exposure, and explain where indicators disagree and why.

Spain is the first study area. Worldwide coverage is a possible later extension. This is an exploratory research repository: the question is clearer than the method, and both can evolve as we learn.

The starting idea is a national map whose colors summarize physical hazards. A useful result would distinguish places that remain relatively low across defensible methods from places whose ranking depends on a particular dataset or weighting choice. Population, property prices and wealth should not determine the headline comparison.

## Starting questions

- Which places consistently show lower hazard across independent sources and reasonable methods?
- Where do indicators disagree, and is the cause coverage, resolution, time period, hazard definition, normalization or aggregation?
- What can we conclude when sources agree but share the same underlying model?
- How much local detail survives a national overview?
- Which conclusions transfer from Spain to a consistent global comparison?

We have not established scientific novelty. Multi-hazard indices and sensitivity analysis already exist. A possible contribution is a reproducible comparison of sources and methods, plus a clear public explanation of where conclusions hold and where they change.

## Start here

- [Research brief](research/brief.md): current direction, possible experiments and open decisions.
- [Conversation backfill](research/history.md): how the project developed and what the user selected.
- [Reading notes](research/reading-notes.md): findings and critiques from the papers and implementations reviewed.
- [Source catalogue](research/sources.json): papers, datasets, tools, precedents and earlier leads.
- [Data guide](data/README.md): local storage, provenance and reuse status.
- [Acquisition manifest](data/manifest.json): downloaded files and checksums.

## Current state

Research and source collection only. There is no implemented atlas, validated composite score or completed national dataset. A source listed in the catalogue is not necessarily downloaded, reproducible or approved for redistribution.

## Repository layout

```
research/          Brief, reading notes, source catalogue and history
scripts/           Acquisition and verification utilities
data/raw/          Original source files, stored locally and ignored by Git
data/derived/      Reproducible outputs, stored locally and ignored by Git
data/manifest.json Tracked provenance and checksums for local files
```

Raw material belongs in this project directory, including restricted papers supplied by the user. Git tracks the research and provenance rather than automatically uploading third-party data. A future remote needs a separate backup/storage arrangement for ignored files.

Names, hazards, spatial units, formulas, technology, licensing and product direction remain open. No project-wide license has been chosen; third-party works retain their own terms.
