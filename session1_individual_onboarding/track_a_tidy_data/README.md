# Track A — Tidy the data (individual, 30 min)

**Data:** `data/messy_variant_candidates.tsv` — a realistic-messy export of variant candidates across 3 patients: inconsistent casing (`abcd1` vs `ABCD1`, `pt-001` vs `PT-002`), trailing whitespace, inconsistent zygosity capitalisation, missing values, one candidate per row rather than one patient per row.

**Task**
1. Ask Claude to inspect the file first and describe what's inconsistent — don't jump straight to "fix it."
2. Get it to clean and normalise the data (consistent casing, trimmed whitespace, standardised zygosity/class values).
3. Reshape it: one row per **patient**, with their top candidate(s) summarised, sorted so the most clinically actionable patients are easiest to spot (e.g. by ACMG class).
4. Produce a short, clinician-readable summary — the kind of thing you could paste into a case-review note, not a raw table dump.

**Tips**
- Use the [agentic workflow cheat sheet](../../docs/claude_agentic_workflow_cheatsheet.md) — inspect → plan → implement → test → review → iterate.
- If using Claude.ai, ask for the result as an Artifact so you get an editable file, not just chat text.
- If using Claude Code, just point it at the file directly.

**Stretch goal (if you finish early)**
Cross-reference against `../../shared_data/mock_talos_candidates.json`, which has the same patients/genes in a richer, Talos-shaped format — see if you can merge the two views.
