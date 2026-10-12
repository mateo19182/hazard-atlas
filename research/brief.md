# Research brief

## Current direction

Find relatively lower-hazard places and investigate disagreement between indicators. Start with a Spain-wide overview, including islands and autonomous cities where coverage permits. Treat worldwide expansion as a design consideration rather than a promised release.

The user selected physical natural-hazard exposure independent of wealth or population size. In technical reporting, distinguish hazard from exposure of people/assets, vulnerability and realized risk. No place should be described as universally safe.

## Working research design

1. Inventory source definitions, coverage, date, resolution, units, return periods, missing values, dependencies and rights.
2. Reproduce the closest existing methods before proposing another index. ThinkHazard and UNICEF MHI are priority baselines; ESPON and the European multi-hazard hotspot study are useful comparisons.
3. Compare sources within each hazard before comparing composite indices. Align scope and units; document differences that cannot be harmonized.
4. Hold inputs fixed while comparing aggregation choices, then hold the method fixed while changing sources. This helps separate causes of disagreement.
5. Identify locations with stable classifications across a specified set of defensible alternatives. Report the alternatives and their coverage. Agreement alone does not establish truth.
6. Validate against independent evidence appropriate to each hazard. Avoid optimizing a physical-hazard index against wealth-dependent insured losses.

Possible baselines include threshold-based hazard counts, an equal-weight family average, a root-mean-square composite and the highest component. These are candidates, not accepted formulas. PCA is another benchmark, subject to monotonicity and interpretability checks. A disagreement score, rank interval or classification stability measure also needs a definition before use.

## Evidence and scoring questions

- Keep missing, outside-domain, below-threshold and true zero distinct.
- More datasets for a hazard should not automatically increase its influence.
- Increasing hazard intensity should not reduce the composite under otherwise fixed inputs.
- Source agreement can reflect shared inputs, rather than independent corroboration.
- Shared drivers and cascading hazards need examination; do not invent interaction bonuses or joint probabilities.
- Do not confuse a percentile with a disaster probability.
- Do not infer fine precision by resampling coarse data.
- Changes in category can reflect a changed baseline or source rather than changed physical hazard.

## Geographic design to investigate

A regular grid could support the main view, with municipal summaries and detailed source overlays. Grid size is undecided. Test aggregation effects, small hotspots and boundary sensitivity. Global comparisons should use fixed physical transformations or an explicitly fixed reference population of locations. Country-relative percentiles may be an additional presentation layer.

A consistent global baseline and clearly distinguished local refinements are a promising architecture. Simply replacing global data inside Spain could introduce artificial differences at borders.

## Candidate hazards

Flooding, wildfire, earthquakes, ground instability, extreme heat, drought, severe wind, volcanic hazards and tsunamis. Flood subtypes and correlated indicators should be organized deliberately. Inclusion of slow hazards in the headline view remains open. Availability and fitness of data must determine what can actually be assessed.

## Possible contribution

Measure how source and method choices change conclusions about lower-hazard places. Publish reproducible comparisons, explanations of disagreements and uncertainty-aware maps. The novelty claim still requires a focused literature review. Existing indices already combine hazards, and sensitivity analysis is established practice.

## Next experiments

- Audit ThinkHazard data downloads and source terms.
- Reproduce the UNICEF MHI construction on accessible inputs; inspect missing-data assumptions, signed PCA weights, input multiplicity and area weighting.
- Choose one hazard with two comparable sources and test disagreement across Spain.
- Define a small set of shared hazards, then compare three candidate maps using identical inputs.
- Audit results in contrasting Spanish regions, including the Canaries, coasts, mountains and inland areas.
- Write down failures and unresolved disagreements before selecting a public score.

No specific launch date, commercial model, final formula or implementation stack is committed.
