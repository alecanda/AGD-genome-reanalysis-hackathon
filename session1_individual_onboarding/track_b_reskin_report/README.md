# Track B — Reskin the report (individual, 30 min)

**Data:** `data/sample_report.html` — a bare-bones, table-only report for 3 mock patients (deliberately plain, so there's obvious room to improve it).

**Task**
1. Open the file in a browser first, look at it as-is.
2. Ask Claude to restructure/restyle it: e.g. colour-code rows by ACMG class, add a top-of-page summary ("3 patients, 2 with a top candidate of Pathogenic/Likely pathogenic"), collapse/expand per-patient sections, improve readability for a non-technical reader.
3. Keep iterating on *one* improvement at a time rather than asking for everything at once.

**Tips**
- Use the [agentic workflow cheat sheet](../../docs/claude_agentic_workflow_cheatsheet.md).
- If using Claude.ai, ask for it as an HTML Artifact so you get a live preview.
- If using Claude Code, just edit the file directly and open it in a browser to check.

**Stretch goal (if you finish early)**
Add a filter/sort control (e.g. by ACMG class or phenotype match), using data from `../../shared_data/mock_talos_candidates.json` instead of the hardcoded table — this is a small taste of what Group Track 1 does at larger scope.
