# Session 2 (group hackathon) data

All data for session 2 is located in [`/session-2/data/`](/session-2/data/).
Individual challenge descriptions:
* [Challenge 1 — Talos Case Review](/session-2/challenge-1-case-review.md)
* [Challenge 2 — Why is this candidate interesting?](/session-2/challenge-2-explanation.md)
* [Challenge 3 — Natural-language Talos](/session-2/challenge-3-natural-language.md)
* [Challenge 4 — Reanalysis triage](/session-2/challenge-4-reanalysis-triage.md)
* [Challenge 5 — Open pitch](/session-2/challenge-5-open-pitch.md)

## Challenges 1 - 3

These challenges can all be completed using either, or a combination of, the example multi-variant report and json results files from Talos v11.0.1:
* `multi_variant_report_2026-07-27.html`
* `multi_variant_results_2026-07-27.json`

## Challenge 4

Synthetic case-level data for the reanalysis-triage challenge. It is intentionally artificial and must not be presented as clinical evidence:
* `synthetic_reanalysis_cases.tsv` — 300 unresolved cases from a single reanalysis cycle dated 2026-09-01
* `synthetic_reanalysis_outcomes.tsv` — what happened when each case was actually reviewed

### Using the outcomes file

`synthetic_reanalysis_outcomes.tsv` is for **evaluating** your triage, not for building it. In a real lab you do not know these outcomes at the moment you decide what to perform reanalysis, that is the whole problem. Build your prioritisation from the case table, then use the outcomes to check how well it worked.

A good evaluation asks: of the top 20 cases your tool surfaces, how many were resolved? How does that compare with simply sorting by the oldest analysis date?

`review_outcome` takes four values: `solved`, `candidate_for_followup`, `no_change`, and `not_reviewed_already_solved`.

### Data dictionary — `synthetic_reanalysis_cases.tsv`

| Column | Meaning |
|---|---|
| `case_id` | Unique case identifier |
| `case_status` | `unsolved`, `partially_solved`, or `solved` at the start of this cycle |
| `first_analysis` | Date the case was first analysed |
| `last_analysis` | Date of the most recent previous analysis |
| `current_analysis` | Date of this reanalysis cycle (constant) |
| `sequencing_type` | `exome` or `genome` |
| `family_structure` | `singleton`, `duo`, or `trio` at the last analysis |
| `hpo_term_count` | Number of HPO terms currently recorded |
| `phenotype_changes` | New HPO terms added since the last analysis |
| `candidate_count` | Total candidate variants in the current output |
| `new_candidates` | Candidates not present at the last analysis |
| `new_high_priority_candidates` | Candidates now in a high-confidence category, including existing ones newly promoted |
| `new_gene_evidence` | Candidates whose gene–disease association has strengthened |
| `new_clinvar_evidence` | Candidates with any ClinVar reclassification |
| `clinvar_upgrades_to_plp` | Subset of the above reclassified specifically to Pathogenic / Likely Pathogenic |
| `prior_analysis_complete` | `1` if the previous analysis ran to completion, `0` if not |
| `prior_analysis_flag` | Why the previous analysis was incomplete: `qc_fail`, `partial_panel`, `pipeline_error`, `no_parental_data` |
| `note` | Free-text laboratory note. Mostly administrative, but some notes record real events |

Missing values are encoded as `NA` and appear in several columns. Decide deliberately how to handle them — dropping incomplete rows is a choice with consequences.

## Important data policy

No patient data is supplied by the workshop. Participants must not upload patient-identifiable or otherwise confidential clinical data to Claude or the workshop repository.

Public and synthetic data are encouraged.
