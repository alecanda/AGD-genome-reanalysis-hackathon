# Track 2 — "Why does Talos think this is interesting?"

**Core question:** what should a diagnostic scientist actually see when reviewing one prioritised candidate?

**Data:** [`../../shared_data/mock_talos_candidates.json`](../../shared_data/README.md) — use the `prioritization_reasons`, `concerns`, `phenotype_match`, `inheritance`, and `evidence_links` fields.

**Target shape** (adapt freely — this is a starting sketch, not a spec):

```
ABCD1
Rank: #2  |  Inheritance: X-linked  |  Phenotype: 8/12 terms matched

Why prioritised?
✓ Phenotype similarity
✓ Compatible inheritance
✓ Rare variant
✓ Predicted loss-of-function
✓ Known disease association

Potential concerns
⚠ Phenotype match is incomplete
⚠ Variant classification uncertain

[Show evidence]
```

**Design decision to make explicitly (this is the actual point of the track):** should this be generated **deterministically** (a template filled directly from the structured fields — auditable, reproducible, "boring" but trustworthy) or **LLM-generated prose** (reads more naturally, but needs guardrails against overclaiming or inventing reasoning not actually present in the data)? You could also build both and let a judge compare them side by side — that's a legitimate, interesting demo in itself.

**Getting started**
1. Inspect the JSON schema with Claude — map out exactly which fields feed which part of the card.
2. Plan: deterministic, LLM-generated, or both?
3. Build the card for one candidate first (e.g. ABCD1), then generalise to all candidates across all 3 mock cases.
4. If going the LLM route: test what happens when the underlying evidence is weak (e.g. the `PEX1` or `MYH7` candidates) — does your explanation honestly reflect the uncertainty, or does it oversell the candidate?

**Pitfall to avoid:** an LLM-generated explanation that sounds confident regardless of how weak the underlying evidence actually is. A judge asking "would you trust this concern-flagging on a weak candidate?" is a very likely question.
