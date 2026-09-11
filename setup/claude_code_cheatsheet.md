# Claude Code quick-start pattern

A useful agent workflow is:

1. Inspect
2. Plan
3. Implement
4. Run/test
5. Inspect the result
6. Iterate
7. Review the changes


**Don't do this:** *"Write Python code to parse this file."*
**Do this instead:** treat Claude like a capable collaborator you loop with, not a one-shot code generator.

## 1. Inspect
Before asking for code, get Claude to actually look at your data/report first.
- "Here's a sample of the file — what format is this, and what looks messy or inconsistent?"
- "Open this HTML report and describe its structure before we change anything."
- Paste in a *real* example, not a description of one. Claude works much better from the actual thing than from your summary of it.

## 2. Plan
Ask for a plan before code. This catches misunderstandings early, when they're cheap to fix.
- "Before writing anything, outline your approach in 3–5 steps."
- "What would you need to know from me to do this well?"
- If the plan looks wrong, say so *now* — redirecting a plan is much faster than debugging code built on a wrong assumption.

## 3. Implement
Let Claude write/edit the actual files, not just paste snippets into chat.
- In Claude Code: let it read the real files, run commands, and edit in place.
- In Claude.ai: use Artifacts so you get a working file you can iterate on, not a wall of text to copy-paste.
- Ask for one coherent chunk at a time rather than "build the whole thing" — easier to review, easier to course-correct.

## 4. Test
Don't just eyeball the output — ask Claude to check its own work.
- "Run this on the sample data and show me the actual output."
- "What would break this? Try an edge case."
- For anything touching genetics/variant logic: "Are you confident about the biology here, or guessing?" — Claude can overclaim; asking directly gets you a more honest answer.

## 5. Review
You're still the reviewer. Read the diff, read the output, don't just trust a green checkmark.
- "Explain why you made this choice" — if the explanation doesn't hold up, that's a signal.
- Check numbers/claims against the actual data, especially anything clinical.

## 6. Iterate
Treat the first working version as a draft, not the answer.
- "This works, but the output is hard to read — can we improve X specifically?"
- Small, targeted iterations beat re-prompting from scratch each time.

---

## Fast tips
- **Show, don't describe.** Paste real data/files rather than describing them from memory.
- **One step at a time beats one giant prompt.** Especially under time pressure — a working small piece is worth more than a broken big one.
- **Ask "why" and "are you sure."** Especially for anything scientific — it surfaces uncertainty Claude would otherwise gloss over.
- **If stuck, back up a step** rather than pushing forward — often the fix is in *inspect* or *plan*, not in more code.
- **It's fine to disagree with Claude's plan.** You know the clinical/biological context; say so early.

### Example

> Inspect this repository and find where the Talos HTML report is generated. Do not modify anything yet. Explain which files are relevant to adding a case-summary panel.

Then:

> Implement the smallest version of that feature. Keep existing behaviour intact and add/update tests where appropriate.

Then:

> Run the relevant tests or example command. If anything fails, diagnose the problem and fix it.

Then:

> Review your changes for unintended changes to Talos interpretation or output. Summarise what changed.
