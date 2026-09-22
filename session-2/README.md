# Session 2 (group hackathon) data

All data for session 2 is located in [`/session-2/data/`](/session-2/data/).
Individual challenge descriptions:
* [Challenge 1 — Talos Case Review](/session-2/challenge-1-case-review.md)
* [Challenge 2 — Why is this candidate interesting?](/session-2/challenge-2-explanation.md)
* [Challenge 3 — Natural-language Talos](/session-2/challenge-3-natural-language.md)
* [Challenge 4 — Reanalysis triage](/session-2/challenge-4-reanalysis-triage.md)
* [Challenge 5 — Open pitch](/session-2/challenge-5-open-pitch.md)
* [Challenge 6 — HPO annotation tool](/session-2/challenge-6-hpo-annotation.md)

## Challenges 1 - 3

These challenges can all be completed using either, or a combination of, the example multi-variant report and json results files from Talos v11.0.1:
* `multi_variant_report_2026-07-27.html`
* `multi_variant_results_2026-07-27.json`

## Challenge 4

Synthetic case-level data for the reanalysis-triage challenge. It is intentionally artificial and must not be presented as clinical evidence:
* `synthetic_reanalysis_cases.tsv`

## Challenge 6

No data is supplied for this challenge. Download the HPO annotation files yourself from https://hpo.jax.org/data/annotations (CC BY 4.0):
* `phenotype.hpoa` — disease-level annotations: for each OMIM, ORPHANET or DECIPHER disease, the HPO terms curated for it, with frequency, onset and evidence code.
* `genes_to_phenotype.txt` / `phenotype_to_genes.txt` — the same annotations viewed per gene.

These files map diseases and genes to HPO term IDs. They do not contain the ontology itself, so they carry no term labels, synonyms or parent/child relationships. For term search and hierarchy, download `hp.json` or `hp.obo` from https://hpo.jax.org/data/ontology.

## Important data policy

No patient data is supplied by the workshop. Participants must not upload patient-identifiable or otherwise confidential clinical data to Claude or the workshop repository.

Public and synthetic data are encouraged.
