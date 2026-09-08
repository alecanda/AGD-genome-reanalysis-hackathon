# Track 1 — Redesign the report for real clinical case review

**Core question:** what would make this report actually usable during an actual clinical case review session — not just readable, but something a diagnostic scientist would keep open while making a decision?

**Data:** [`../../shared_data/mock_talos_candidates.json`](../../shared_data/README.md) (3 mock cases, multiple candidates each).

**Possible components** — pick 2–4, don't try to build all of them shallowly:
- **Case overview** — patient, phenotype terms, previous analysis date, at-a-glance status
- **Phenotype summary** — which HPO terms matched vs. didn't, visually
- **Candidate table** — sortable/filterable, not just a static dump
- **Evidence panels** — expand a candidate to see why it's ranked where it is
- **Filters** — by ACMG class, inheritance, phenotype match, rank
- **Ranking explanations** — surface `prioritization_reasons` / `concerns` clearly (this overlaps with Track 2 — feel free to borrow/build together if your rooms end up adjacent)
- **External links** — wire up the `evidence_links` (ClinVar, gnomAD, OMIM) so they're one click away
- **Visualisation** — e.g. phenotype match as a bar, candidates plotted by rank vs. confidence
- **Export** — one-click "copy as case note" or PDF/print view

**Getting started**
1. Inspect `mock_talos_candidates.json` with Claude first — understand the schema before building UI around it.
2. Plan which 2–4 components you're building and why those, specifically — this is your pitch's clinical-usefulness argument.
3. Build iteratively, testing against all 3 mock cases as you go (not just the one you eyeballed first).

**Pitfall to avoid:** building something that looks impressive but wouldn't survive contact with a real case reviewer — keep asking "would a clinician actually trust/use this row, or does it need a caveat we haven't shown?"
