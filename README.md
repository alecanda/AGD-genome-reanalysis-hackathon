# AI × Genomics Hackathon

A workshop package for an AI-assisted coding hackathon centred on Talos, rare-disease variant prioritisation and genome reanalysis.

## Core idea

The workshop is not primarily about teaching people to code.

It is about demonstrating that an AI coding agent can let clinical scientists and bioinformaticians build useful software in a short time that they would previously not have attempted.

## Setup and cheatsheet documentation
Please follow the guidelines in the [participant setup](/setup/participant_setup.md) **before** the event to get set up. This will ensure that no time is wasted on technical problems during the hackathon.

Additionally, have a read through the [Claude cheatsheet](/setup/claude_cheatsheet.md) for useful tips on working with Claude chat and Code.

## Session 1 — Individual onboarding

In Session 1, you will get a short, contained experience of using an AI coding agent. Both tracks use synthetic or public Talos-derived material, so you can focus on the workflow rather than on handling patient data.

- **Track A: Tidy the Talos data** — inspect a messy candidate table and turn it into a concise, clinician-readable summary. You will practise understanding unfamiliar data, choosing useful fields, and iterating on a practical output rather than trying to write perfect code.
- **Track B: Reskin the Talos report** — work with the real Talos output and make one useful presentation change to its HTML report. You will practise using Claude to analyse a file, identify areas fit for improvement, and testing a small change without altering the underlying variant interpretation.

Choose the track that suits your starting point: Track A begins with a data transformation task, while Track B takes you into modifying and extending the HTML, JavaScript and CSS code of the output of Talos.

## Session 2 — Team hackathon

In Session 2, work with your team on a small, working prototype that could make Talos or genome reanalysis more useful. Choose one of the challenges below, decide what a useful result would look like, and use Claude to help you build and demonstrate it. You do not need to build a complete product.

1. **[Talos Case Review](/session-2/challenge-1-case-review.md)** — improve the Talos HTML view for someone reviewing a case. You could focus on the case overview, phenotype summary, candidate table, evidence, filters, ranking explanations, links, visualisation, or export.
2. **[Why is this candidate interesting?](/session-2/challenge-2-explanation.md)** — build a component that explains an individual candidate using its gene, variant, rank, inheritance or reason, Talos evidence, phenotype evidence, supporting evidence, limitations, and source links. Make sure each explanation can be traced back to the data and does not make unsupported clinical claims.
3. **[Natural-language Talos](/session-2/challenge-3-natural-language.md)** — let a user ask questions about the Talos JSON output in plain English, such as "which candidates are de novo or have phenotype support?". Claude can interpret the question, and return the relevant results, but the actual result set should come from a deterministic query over the data.
4. **[Reanalysis triage](/session-2/challenge-4-reanalysis-triage.md)** — help a laboratory decide which unresolved cases to review first after a reanalysis cycle. You could use signals such as new candidates, updated gene-disease or ClinVar evidence, phenotype changes, and time since analysis. Show why each case was prioritised rather than presenting an unexplained score.
5. **[Open pitch](/session-2/challenge-5-open-pitch.md)** — propose and prototype another improvement to Talos, rare-disease diagnostics, or genome reanalysis. Start with a real user problem, make sure your idea meaningfully interacts with Talos or its outputs, and demonstrate a working proof of concept. It does not need to contain AI.

### Working with your team
**Workshop GitHub repository:**  
Please fork the repo, make a subdirectory for your team with a creative (and unlikely to be duplicated) name under `session-2/projects`. Please push your work here, including your final presentation and working prototype.

## Source material

The workshop deliberately uses the public Talos project and its test fixtures as the foundation. The upstream repository contains small VCF/pedigree/test JSON fixtures and the HTML report is assembled by Python/Jinja code.

Other source data not directly related to Talos have been synthetically generated for the purposed of this workshop.

## Data policy

No patient data is provided. Use synthetic/public data only.

## Funding and support
The AI x Genomics Hackathon at the Arbeitsgemeinschaft für Gen-Diagnostik e.V. Jahrestagung 2026 was supported by the following institutions, companies, and projects:
![image](/img/GHGA_full_Logo_orange.png)![image](/img/anthropic_logo.png)![image](/img/igsb_logo.png)
