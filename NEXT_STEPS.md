# Next build step

This v0.1 package is a design/data scaffold, not yet the final event bundle.

Before the conference we should:

1. Pin the exact Talos release used at the event.
2. Run that release with its official test fixtures and capture an actual generated HTML report.
3. Add a richer synthetic multi-candidate Talos result based on the same schema.
4. Validate that the Session 1B starter modification can be run in a clean Talos checkout.
5. Build an old/new Talos result pair with realistic reanalysis metadata (`first_seen`, `evidence_last_updated`) for Challenge 4.
6. Add deterministic answer/test fixtures for the NL-query challenge.
7. Add example solution branches for instructors/judges, kept out of participant view.
8. Add a 1-page emergency setup guide for participants arriving without Claude Code/VS Code configured.
