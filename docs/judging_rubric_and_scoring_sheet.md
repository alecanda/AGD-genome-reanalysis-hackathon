# Judging Rubric & Scoring Sheet

Primary criteria are **Clinical Usefulness** and **Novelty/Creativity** — weighted highest because the goal of this hackathon is to surface genuinely useful, original ideas, not just polished engineering. Technical execution and communication matter but as secondary anchors.

## Scoring categories

| Category | Weight | What you're asking yourself |
|---|---|---|
| **Clinical usefulness** | ×3 | If a diagnostic scientist or clinician used this tomorrow, would it save them time, reduce error, or surface something they'd otherwise miss? Is it grounded in how real case review / reanalysis actually works? |
| **Novelty / creativity** | ×3 | Does this go beyond an obvious/generic implementation? Did the team make an interesting design choice, combine ideas in a new way, or take a genuinely open-ended approach (esp. relevant for Track 5)? |
| **Technical execution** | ×2 | Does it actually run? Is what's demoed real (even if rough), not a static mockup dressed up as a working system? Partial-but-real beats complete-but-faked. |
| **Problem understanding** | ×1.5 | Does the team correctly understand the underlying science/workflow (inheritance patterns, ACMG-style reasoning, what "reanalysis" actually involves)? Watch for confident-sounding but scientifically wrong output — common failure mode with LLM-assisted work. |
| **Communication** | ×1 | Is the 5-minute pitch clear? Could a judge unfamiliar with that specific team's rabbit hole understand what was built and why it matters? |

Score each category **1–5** (1 = not present/attempted, 3 = solid, 5 = excellent). Multiply by weight, sum for a weighted total out of **51.5**.

## Score anchors (use these to calibrate across very different tracks)

**Clinical usefulness**
- 1: No connection to a real clinical/diagnostic workflow
- 3: Plausibly useful, but a clinician would need to squint or add caveats
- 5: A diagnostic scientist in the room would want to actually try this

**Novelty**
- 1: Straightforward reproduction of something that already exists (e.g. Talos's report, unchanged)
- 3: Sensible extension or reasonable new angle on the problem
- 5: Genuinely surprised the judges, or reframed the problem in a useful way

**Technical execution**
- 1: Nothing runs; slides/description only
- 3: Runs on the demo data shown, with visible rough edges
- 5: Runs cleanly, handles at least one edge case gracefully

**Problem understanding**
- 1: Misuses genetics/inheritance/ACMG terms, or the "reasoning" is decorative rather than grounded
- 3: Core concepts used correctly, some simplification acceptable given time constraints
- 5: Nuanced, correctly flags its own scientific uncertainty rather than overclaiming

**Communication**
- 1: Judges can't tell what was built
- 3: Clear enough to follow, minor gaps
- 5: Sharp, memorable, makes the "why this matters" case in under 5 minutes

## Cross-track fairness notes for judges

- **Track 4 (triage/prioritisation)** is policy/algorithm-heavy with little UI — don't penalise it on "polish" relative to UI-heavy Track 1. Judge it on whether the prioritisation logic is defensible and well-reasoned.
- **Track 2 (explanation card)** is intentionally narrow in scope — a team that nails one component deeply should not be marked down versus a team that built a shallow version of everything in Track 1.
- **Track 5 (open pitch)** should be judged against the same rubric, not given a novelty bonus just for being open-ended — the novelty score should reflect the idea itself.
- If multiple groups pick the same track, compare within-track first, then normalise across tracks using the weighted total.

---

## Scoring sheet (one row per group)

| Group # | Track | Clinical usefulness (×3) | Novelty (×3) | Technical execution (×2) | Problem understanding (×1.5) | Communication (×1) | **Weighted total /51.5** | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | |
| 2 | | | | | | | | |
| 3 | | | | | | | | |
| 4 | | | | | | | | |
| 5 | | | | | | | | |
| 6 | | | | | | | | |
| 7 | | | | | | | | |
| 8 | | | | | | | | |

*(duplicate rows as needed for your final group count)*

### Per-judge worksheet (fill during each demo, 1 per group)

```
Group #: ____   Track: ____   Team members: ____________________

Clinical usefulness   [1 2 3 4 5]  notes: _______________________
Novelty/creativity    [1 2 3 4 5]  notes: _______________________
Technical execution   [1 2 3 4 5]  notes: _______________________
Problem understanding [1 2 3 4 5]  notes: _______________________
Communication         [1 2 3 4 5]  notes: _______________________

One thing I'd want to see next: _________________________________
```

### Tie-breaker order
1. Clinical usefulness score alone
2. Novelty score alone
3. Judges' quick discussion / re-vote (2 min max, don't let this drag out the ceremony)
