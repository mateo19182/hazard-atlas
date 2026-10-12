# Data storage and provenance

Store acquired material here. Raw files are immutable snapshots; create new records for new versions. Keep derived outputs separate and record their inputs and generation method.

- `raw/public/`: downloaded public source material. Public access does not establish redistribution rights.
- `raw/restricted/`: user-supplied or restricted material, including the paid Springer book and extracted text.
- `derived/`: computed datasets and maps, once produced.
- `manifest.json`: tracked paths, source IDs, acquisition times, checksums, file sizes and access notes.

Raw and derived files are ignored by Git. They remain in the local repository directory, but a Git remote alone will not back them up. Decide on private object storage or another backup before relying on a remote as the research archive. Avoid committing restricted material or applying a project license to third-party works.

The source catalogue includes leads that have not been acquired. It also includes superseded comfort-map research and product precedents for context. No national hazard raster collection has yet been downloaded.

Run `python3 scripts/verify_data.py` to check local manifest entries. Run `python3 scripts/snapshot_sources.py` to acquire or retry the selected small public reference snapshots. Inspect acquisition status afterwards. Source terms and technical completeness still require review.
