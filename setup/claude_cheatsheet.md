# Choosing the right Anthropic tool

Anthropic provides several ways to work with Claude. Start with the least technical option that can do the job, then move to a more powerful tool when you need repeatability, access to local files, or multiple steps.

### Choosing the right model

Each participant has **$100 in credits** for this workshop. More capable models can use those credits surprisingly quickly, especially with large files, long conversations, repeated retries, or agent tasks that make many tool calls. A complex model is also often overengineered for a simple task.

See the [Anthropic guide](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) to selecting a model Helpful rules of thumb:
- Start with the fastest or most economical suitable model for summarising, reformatting, extracting fields, straightforward questions, and small code changes.
- Use a more capable model when the task involves ambiguous requirements, difficult reasoning, a large or unfamiliar codebase, multi-step planning, or debugging that simpler models cannot resolve.
- Test your prompt on a small representative sample before sending a full dataset or running a long agent workflow.
- Use a cheaper model for routine first passes, then reserve a stronger model for the difficult cases or a final review.
- See the [current model descriptions and pricing](https://platform.claude.com/docs/en/about-claude/pricing) in the Console. A stronger model may produce better reasoning, but it does not replace checking the output or validating scientific claims.

### A quick decision rule

- Choose **Claude chat** for a one-off question, document, or small file task with no coding.
- Choose **Claude Console** when you want to test an API prompt, process many inputs consistently, or build an application or tool-using agent.
- Choose **Claude Code** when the work involves a local codebase, terminal commands, tests, or editing files.

You can combine them: use chat to clarify a problem, Console to prototype a repeatable prompt or API workflow, and Claude Code to integrate that workflow into a tested project.


| Tool | Best for | What it can do |
| --- | --- | --- |
| **Claude chat** | Questions, writing, explanation, summarising, and small transformations | Work with text and uploaded files in a conversation; ask follow-up questions; produce text, tables, or other downloadable results |
| **Claude Console** | Testing prompts, working with the API, and building repeatable workflows or agents | Try prompts with files and tools, compare outputs, create reusable prompts, and build an application or agent that can call tools and run several steps |
| **Claude Code** | Inspecting and changing a software repository or running a local data workflow | Read a codebase, inspect local files, run commands and tests, edit or create files, and iterate with you while keeping the work in the repository |

These tools use the same underlying Claude family but have different interfaces and permissions. A chat conversation does not automatically have access to your computer. Claude Code does not automatically know what you intend to change. Console applications can be given access to files, tools, and other services only when you explicitly configure them.

### Claude chat: simple tasks without technical setup

Use Claude chat when you want help with a self-contained task and do not need Claude to inspect a local project or run commands. Upload a document, spreadsheet, image, or small data file, describe the desired output, and review the result in the conversation.

Useful examples:
- "Summarise this report in five bullet points and list anything that needs checking."
- "Compare these two tables and identify rows that differ. Do not guess at missing values."
- "Rewrite this explanation for a non-technical audience, keeping the scientific meaning unchanged."

The basic pattern is **input -> instruction -> review -> refinement**. State the format you want back, show an example when possible, and ask Claude to identify uncertainty instead of filling gaps. For large or sensitive files, check the account, workspace, and organisation's data-handling policies before uploading them. Do not treat an unverified response as a clinical or scientific conclusion.

### Claude Console: from a prompt to an agent

Use the [Anthropic Console](https://platform.claude.com/) when you want to experiment with the API or turn a successful prompt into a repeatable workflow. The Console is aimed at developers and technical users, but you can start with the browser-based Workbench before writing application code.

#### Start with a file-processing task

For a simple **file input -> processing -> output** workflow:

1. Create or sign in to your Anthropic Console account and open the Workbench.
2. Choose a current Claude model and write a clear system instruction describing the role, constraints, and output format.
3. Provide a representative input file or sample content. Tell Claude whether it should quote the source, return structured JSON, produce a table, or write a new file.
4. Test the prompt with normal cases, messy cases, and an empty or unexpected input. Inspect the actual outputs rather than judging only the prompt.
5. Save the working prompt. Use the Console's code-generation or API examples to call it from a script when you need the same process repeatedly.

For example, a prompt for a candidate table might say:

> Read the attached TSV. Preserve every input row. Normalise whitespace and obvious spelling variants, but do not change variant coordinates or clinical claims. Return a TSV with the original value, normalised value, and a reason for each change. Flag ambiguous rows for human review.

This is enough for a one-off experiment. A script or application is useful when you need the same output for many files, logging, retries, validation, or integration with another system. Keep the API key in an environment variable or secret manager; never commit it to a repository or paste it into a prompt.

#### Build a more complex agent

Move from a prompt to an agent when the task requires several decisions or actions, such as finding relevant files, calling a database or web service, checking results against rules, and producing a report. An agent is an application that gives Claude access to a defined set of tools and lets it decide which tool to use at each step.

A sensible build sequence is:

1. Define the job, the permitted inputs, the required output, and the actions Claude must never take.
2. Start with one narrow tool, such as "read this file" or "look up this record," and return structured results.
3. Add validation after each important step. The application, not just the model, should check schemas, required fields, permissions, and allowed ranges.
4. Require confirmation before destructive, external, or clinically consequential actions.
5. Test with representative, adversarial, and incomplete inputs. Log the prompt, tool calls, errors, and final result without exposing sensitive data unnecessarily.

Console experiments are not automatically production systems. Before sharing an agent, review access controls, cost limits, rate limits, privacy requirements, error handling, and how a human can inspect or override its decisions. Consult the current Anthropic API and tool-use documentation because model names, limits, and SDK details change over time.

### Claude Code: inspect and change a codebase

Use Claude Code when the task depends on files in a local repository, shell commands, tests, or changes across multiple files. It is especially useful for adding functionality, fixing a bug, understanding unfamiliar code, or running a data-processing workflow where the inputs and outputs live on your computer.

Getting started:

1. Install Claude Code using the current instructions at [code.claude.com/docs](https://code.claude.com/docs/en/overview), then authenticate when prompted.
2. Open a terminal in the repository or project directory and start Claude Code.
3. Begin with an inspection request. For example: "Inspect this repository and find where the Talos HTML report is generated. Do not modify anything yet. Explain which files are relevant."
4. Ask for a small plan, then approve an implementation. Be explicit about files, constraints, and whether Claude may run commands or edit files.
5. Ask Claude to run the narrowest relevant tests or example command, inspect the output, and show you the changes for review.

Claude Code's normal loop is **inspect -> plan -> implement -> test -> review**. It can read local files and make edits, but it still needs your direction about the intended behaviour. Start a fresh session in the correct directory, avoid granting access to unrelated sensitive folders, and review commands and diffs before accepting changes. For genetics or clinical work, treat generated interpretation as an aid to review, not as an independent clinical decision.

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
