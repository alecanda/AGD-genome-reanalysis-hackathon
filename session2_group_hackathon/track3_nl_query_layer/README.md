# Track 3 — Ask Talos output questions in plain English

**Core question:** can a clinician get a straight answer out of structured variant output without learning a query language or scrolling a giant table?

**Data:** [`../../shared_data/mock_talos_candidates.json`](../../shared_data/README.md).

**Example queries to support** (starting point, extend as you like):
- "Show me all candidates with a compatible inheritance pattern and a phenotype match over 50%."
- "Which patients have a Pathogenic or Likely pathogenic top candidate?"
- "List candidates with unresolved concerns."
- "Summarise Patient B's case in two sentences."

**Getting started**
1. Inspect the schema with Claude first.
2. Plan the architecture: are queries turned into structured filters over the JSON (safer, more auditable), or is the LLM reasoning freely over the raw data each time (more flexible, higher risk of a wrong answer sounding confident)? A hybrid (LLM parses intent → structured filter → LLM summarises the *actual* filtered result) is a strong middle ground worth considering.
3. Build a minimal interface — a simple chat box over the JSON is enough; don't over-invest in UI polish for this track, invest in getting answers *right*.
4. Test with a query where the honest answer is "no candidates match" — make sure your system says that rather than inventing one.

**Pitfall to avoid:** confident wrong answers. For a clinical tool, "I don't know" or "no matches" is a far better failure mode than a fabricated-sounding candidate. Judges will likely probe this directly.
