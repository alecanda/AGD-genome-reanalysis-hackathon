# Session 1B — Reskin the Talos report

## Mission

Start with the real Talos output, and make one visual/presentation change to the HTML report.
Data needed for this challenge is located in this directory, and includes:
* [Example HTML report](/session-1/track-b/example_report_2026-09-17.html): this file should be edited as the goal of this challenge.
* [Example json output](/session-1/track-b/example_json_2026-09-17.json): for reference only. This data is already embedded in the HTML. 

### Starter ideas

1. Add a compact case-summary panel.
2. Make candidate categories visually easier to distinguish.
3. Improve the prominence of inheritance/reason information.
4. Add a clearer evidence section.
5. Improve the visual hierarchy of the candidate table.
6. Add an export or copy-to-clipboard action.
7. Pick your own annoyance and fix it.

### Safety / interpretation rule

Do not change Talos's underlying variant interpretation or claim that a visual colour represents an ACMG classification unless it actually does. Presentation changes should remain presentation changes.

### Suggested first prompt

> Inspect this Talos HTML report. I want to make the report easier for a clinical geneticist to review. First explain how the current report is assembled and structured. Do not modify anything yet.

From here, describe your suggested implementation, expected output, and visual appearance. Claude may even suggest some obvious ideas after using the prompt above.