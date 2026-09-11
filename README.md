# AI × Genomics Hackathon — Talos

A workshop package for an AI-assisted coding hackathon centred on Talos, rare-disease variant prioritisation and genome reanalysis.

## Core idea

The workshop is not primarily about teaching people to code.

It is about demonstrating that an AI coding agent can let clinical scientists and bioinformaticians build useful software in a short time that they would previously not have attempted.

## Session 1 — Individual onboarding

Two tracks:

- Track A: tidy/reformat Talos-derived candidate data
- Track B: modify the real Talos HTML report

## Session 2 — Team hackathon

1. Talos Case Review
2. Why is this candidate interesting?
3. Natural-language Talos
4. Reanalysis triage
5. Open pitch

## Source material

The workshop deliberately uses the public Talos project and its test fixtures as the foundation. The upstream repository contains small VCF/pedigree/test JSON fixtures and the HTML report is assembled by Python/Jinja code.

This workshop repository should reference a pinned Talos release for the event rather than tracking `main` during the workshop.

## Data policy

No patient data is provided. Use synthetic/public data only.
