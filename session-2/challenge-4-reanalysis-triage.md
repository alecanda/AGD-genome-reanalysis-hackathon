# Challenge 4 — Reanalysis triage

A laboratory has thousands of unresolved genomes. It cannot manually review every case after every reanalysis cycle.

Build a prototype answering:

> Which cases should we review first, and why?

Use the synthetic case-level data provided (`/session-2/data/synthetic_reanalysis_cases.tsv`), or extend it. It contains 300 unresolved cases from a single reanalysis cycle. The column meanings are documented in the [session 2 data README](/session-2/README.md).

Potential signals:
- time since last analysis
- new candidates
- new gene-disease evidence
- new ClinVar evidence
- phenotype changes
- high-priority candidates
- quality/completeness of the previous analysis

Do not just produce a score. Make the reason for prioritisation understandable.

## Check whether it actually works

`/session-2/data/synthetic_reanalysis_outcomes.tsv` records what happened when each case was reviewed. Use it to **evaluate** your triage, not to build it — at the moment you decide what to review, you do not know the answer.

Once your prioritisation runs, ask how many of your top 20 cases were resolved, and whether that beats simply sorting by the oldest analysis date. A tool that cannot beat sorting by date has not learned and prioritised from all info in the case files properly.

## Worth thinking about

- Not every signal is equally predictive, and the most obvious column is not always the most useful one.
- A case analysed three weeks ago is unlikely to benefit from reanalysis, whatever else its numbers say.
- Some values are missing. Dropping those rows is a decision you need to make.
- The `note` column is free text. Some notes contain information that appears in no other column.
