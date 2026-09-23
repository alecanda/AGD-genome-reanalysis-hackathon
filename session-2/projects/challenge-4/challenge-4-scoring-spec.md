# Reanalysis triage — composite scoring spec

Defines a points-based score for ranking the 300 cases in `synthetic_reanalysis_cases.tsv` by reanalysis priority. This is a spec only — no outcomes data was consulted, and nothing here has been implemented or tuned yet.

## Design principles

1. **Additive, capped components.** Each signal contributes points independently, but every component has a cap so no single repeated field (e.g. `new_candidates`) can dominate the score on its own.
2. **Diminishing returns, not linear.** Counts are capped low (2–5) because, for triage, the difference between "one strong hit" and "zero" matters far more than the difference between 3 and 4 hits.
3. **Missing data is flagged, not dropped or silently zeroed.** See [Missing data policy](#missing-data-policy).
4. **Already-solved cases are excluded**, not scored low — they aren't candidates for this cycle's reanalysis effort.

## Tier A — direct evidence of new molecular findings (highest weight)

| Field | Points | Cap |
|---|---|---|
| `clinvar_upgrades_to_plp` | 10 × count | max 3 counted (30 pts) |
| `new_clinvar_evidence` minus `clinvar_upgrades_to_plp` (reclassifications that aren't P/LP upgrades) | 4 × count | max 3 counted (12 pts) |
| `new_gene_evidence` | 6 × count | max 3 counted (18 pts) |
| `new_high_priority_candidates` | 6 × count | max 3 counted (18 pts) |
| `new_candidates` (weak signal on its own — can reflect pipeline/version churn rather than real change) | 1 × count | max 5 counted (5 pts) |

Rationale: a ClinVar upgrade to P/LP is the closest thing in this table to "this case might now be solvable," so it's weighted highest. `new_clinvar_evidence` is inclusive of the P/LP subset, so the two rows above subtract to avoid double-counting the same reclassified variant.

**Tier A subtotal cap: 60 points** (sum of the row caps above; not separately re-capped — the row caps are enough in practice).

## Tier B — analytic headroom (the original analysis had a gap)

### B1. Prior analysis completeness

| `prior_analysis_flag` value | Points | Rationale |
|---|---|---|
| `pipeline_error` | 10 | Analysis technically failed to run correctly — this cycle is effectively the first real attempt |
| `qc_fail` | 10 | Same as above — data never passed QC the first time |
| `partial_panel` | 7 | Ran, but against a restricted gene set |
| `no_parental_data` | 6 | Ran without parental data, so phasing/inheritance filtering was weaker |
| blank / `prior_analysis_complete == 1` | 0 | Prior analysis was complete — no headroom from this factor |

If `prior_analysis_complete` is `NA` and no flag is present, score this component 0 and add the case to the data-completeness flag list (see below) rather than guessing.

### B2. Phenotype expansion

`phenotype_changes` (new HPO terms since last analysis): **2 points per term, capped at 3 terms (max 6 points)**. New phenotype data can reorder candidate ranking even with no new variant evidence, but a large number of new terms doesn't linearly increase reanalysis value.

**Tier B subtotal cap: 16 points.**

## Tier C — free-text note classification

`note` is mostly administrative filler, but a minority of entries describe a genuinely new event. Classify the note against the fixed keyword lists below (case-insensitive substring match). If a note matches more than one "signal" phrase, take the **maximum**, not the sum — one real event is the actual signal, not the phrase count.

### Signal phrases (contribute points)

| Phrase (substring match) | Points | Why it matters |
|---|---|---|
| `parents now consented and sequenced` | 8 | Singleton/duo → trio upgrade: a real jump in analytic power |
| `second affected sibling now presenting` | 8 | New affected individual changes the phenotype/genetic evidence base |
| `research collaboration reported a second family` | 8 | External genetic evidence for the same gene |
| `matchmaker exchange match reported` | 8 | External genetic evidence via formal matching |
| `new consanguinity information` | 6 | Changes prior probability for recessive inheritance |
| `muscle biopsy results now available` | 6 | New orthogonal clinical evidence |
| `clinician requested review following new mri findings` | 6 | New clinical evidence prompted the request |
| `skin fibroblast rna study completed` | 6 | New functional evidence |
| `deep phenotyping completed at specialist clinic` | 5 | Refined phenotype data, sub-HPO-count-column-level detail |
| `clinician requested review ahead of family planning` | 4 | Clinical urgency, not new evidence — still worth surfacing |

### Administrative / no-signal phrases (0 points)

`routine`, `annual review`, `internal cohort`, `reviewed at mdt`, `part of research cohort`, `external referral`, `referred from clinical genetics`, `referred from paediatric neurology`, `no family history reported`, `prenatal history unremarkable`, `sample received from external lab`, `consanguineous family` (already-known family structure, distinct from the "new consanguinity information" phrase above), blank note.

Any note not matching a known phrase (signal or administrative) should be logged for manual review rather than silently scored 0 — the keyword list is very likely incomplete and should be expected to need extension once the real note text is scanned in the implementation step.

**Tier C cap: 8 points** (the max single-phrase value).

## Tiebreaker — time since last analysis

`current_analysis` (constant, 2026-09-01) minus `last_analysis`, converted to years: **0.5 points per year, capped at 5 points (10 years)**. This nudges older, longer-neglected cases upward without letting age dominate a case that has no other evidence for reanalysis — it exists to break ties among otherwise-similar scores, not to compete with Tier A/B/C.

## Case-status modifier

Applied multiplicatively to the summed score (Tier A + B + C + tiebreaker):

| `case_status` | Multiplier | Rationale |
|---|---|---|
| `unsolved` | 1.0 | Full priority pool |
| `partially_solved` | 0.85 | Already has a partial answer; still worth reanalysis but slightly less urgent than a fully unsolved case with the same evidence profile |
| `solved` | **excluded** | Not part of the ranking at all — set score to 0 and flag as `excluded_solved` in the output, don't rank it |

## Final formula

```
raw_score = TierA + TierB + TierC + AgeTiebreaker
final_score = raw_score × case_status_multiplier   (0 if case_status == "solved")
```

Rank all non-excluded cases by `final_score` descending. Ties broken by `last_analysis` ascending (older first).

## Missing data policy

| Situation | Handling |
|---|---|
| `hpo_term_count` = `NA` | Not used directly in scoring (only `phenotype_changes` is) — no action needed, but flag for visibility |
| `phenotype_changes` = `NA` | Treat as 0 for scoring; add case to `data_completeness_flags` |
| `new_high_priority_candidates`, `new_gene_evidence`, or similar count field = `NA` | Treat as 0 for scoring; add to `data_completeness_flags` |
| `prior_analysis_complete` = `NA` with no `prior_analysis_flag` | Score B1 as 0; add to `data_completeness_flags` — do not assume complete |
| `note` blank | Score Tier C as 0, no flag needed (blank is expected, not missing) |

No row is dropped for having `NA` values. Every case that has at least one `NA` in a scoring-relevant field should carry a `data_completeness_flags` list in the output (e.g. `["phenotype_changes"]`) so a reviewer can see which scores are based on incomplete information, per the README's instruction to handle missing values deliberately rather than by silent deletion.

## Output shape (for the implementation step)

For each non-excluded case: `case_id`, `tier_a_score`, `tier_b_score`, `tier_c_score`, `age_tiebreaker`, `case_status_multiplier`, `final_score`, `data_completeness_flags`, `matched_note_phrase` (for auditability). Sorted descending by `final_score`.

## Tunable parameters (called out explicitly for review before implementation)

- All point values and caps above are starting judgments, not derived from data (per the instruction not to consult outcomes yet).
- The `partially_solved` multiplier (0.85) is a guess and easy to argue with either direction.
- The Tier C keyword lists are built from the notes visible in a manual skim of the table and are very likely incomplete.
- The age-tiebreaker weight (0.5 pt/year, 5 pt cap) is deliberately small relative to Tier A/B so it only matters among near-ties.
