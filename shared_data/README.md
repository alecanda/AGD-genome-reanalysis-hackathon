# Shared mock data

`mock_talos_candidates.json` — synthetic, Talos-shaped variant prioritisation output for 3 mock cases (`CASE-0001`–`CASE-0003`). Used by Group Tracks 1, 2, and 3. Not real patient data.

Each case has: `phenotype_terms`, `previous_analysis_date`, and a list of `candidates`, each with rank, inheritance, zygosity, population frequency, in-silico score, ACMG-style classification, phenotype match count, `prioritization_reasons` (why it was flagged), `concerns` (caveats), and `evidence_links`.

Teams are free to:
- Add more cases/candidates
- Extend the schema (e.g. add compound-het pairing, SV candidates)
- Pull in real public reference data (ClinVar, gnomAD, OMIM, PanelApp) to enrich or validate against — the mock records above intentionally use real gene/disease pairs (ABCD1/ALD, PTPN11/Noonan, SCN1A/Dravet, etc.) so lookups against public databases return sensible results.

`../session2_group_hackathon/track4_triage_prioritization/data/mock_reanalysis_queue.csv` is a separate, case-level (not variant-level) dataset for the triage track.
