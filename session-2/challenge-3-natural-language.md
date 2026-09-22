# Challenge 3 — Natural-language Talos

Build a prototype allowing a user to ask questions about Talos JSON in plain English.

Examples:
- Show me all candidates with phenotype support.
- Which candidates are de novo?
- Which candidates have ClinVar evidence?
- Show compound-heterozygous candidates.
- Which candidates have rare population frequency?

Recommended architecture:

    natural-language question
             ↓
       query interpretation
             ↓
       deterministic query
             ↓
          Talos JSON
             ↓
           results

The LLM should not invent the result set.
