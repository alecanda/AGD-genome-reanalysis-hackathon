# Track 4 — Which cases should we reanalyse?

**Scenario:** a diagnostic lab has 5,000 unsolved genomes. They can't manually reanalyse everything. Build a system that decides which cases deserve reanalysis first — and be ready to explain *why* your strategy is defensible, not just what it outputs.

**Data:** `data/mock_reanalysis_queue.csv` — 10 mock cases (extend/synthesise more if useful) with columns:
- `date_last_analysed`
- `phenotype_terms`
- `num_candidates_at_last_analysis`
- `num_unresolved_variants`
- `new_gene_disease_assoc_since_last_analysis`
- `new_clinvar_evidence_since_last_analysis`
- `phenotype_changed_since_last_analysis`
- `age_at_last_analysis`
- `clinical_trajectory_notes` (free text)
- `previous_analysis_quality_score` (1–5, higher = more thorough original analysis)

**This is the least UI-heavy track on purpose** — the interesting work is the *strategy*, not the front-end. A team that produces a clearly-reasoned ranking with a short written justification can outscore a team with a fancier dashboard and a weaker rationale.

**Getting started**
1. Inspect the CSV with Claude — discuss as a team (clinicians + bioinformaticians) which signals *should* matter most, before writing any ranking code. This discussion is itself valuable output — capture it for your pitch.
2. Plan a scoring/ranking approach. Options to consider (not prescriptive):
   - A weighted score combining multiple signals
   - A rules-based triage (e.g. "flag if new gene-disease association AND unresolved variants > 0")
   - Separate "quick win" vs "deep dive" queues
3. Implement, run it over the mock queue, and sanity-check: does the resulting order actually make clinical sense to the clinicians on your team?
4. Be ready to defend trade-offs — e.g. should a case with a **regressing** clinical trajectory (`CASE-1009`) always outrank one with more new evidence but a **stable** trajectory (`CASE-1002`)? There's no single correct answer; the rubric rewards a well-reasoned position.

**Pitfall to avoid:** a ranking that's technically sophisticated but that the clinicians on your own team wouldn't actually endorse. Sanity-check with them, not just with the data.
