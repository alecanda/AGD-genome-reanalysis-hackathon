# Participant Technical Setup

## Choose the setup that matches your experience

We deliberately support two ways of working. You do **not** need to install a full programming environment just to participate. Due to time constraints, unfortunately it won't be feasible to help with technical challenges on the day. We strongly recommend to choose the right path below based on you experience and skill level.

### Path A — Users with no programming experience: Claude Platform / Claude App

**Recommended if you have little or no programming experience, or do not already use VS Code/another IDE.**

Participants are recommended to participate using the Claude Console (https://platform.claude.com/). You do not need to install Claude Code, VS Code, Git, or a terminal environment for the introductory exercises.

**Note:** Claude Chat (https://claude.ai/) is a separate system to Claude Platform even with the same email. The Claude credits supplied for the hackathon (details below) are for Console, given as API credit. It does not top up a Claude Chat Pro/Max subscription. Therefore, we suggest setting up an account with the Console even if you already use Claude Chat.

### Path B — Users with programming and Claude Code experience

**Recommended if you already have coding experience and use VS Code or a similar editor.**

Use Claude Code when you are comfortable with a terminal, code editor, Git/GitHub, and an existing codebase.

Recommended software:
- VS Code or another editor
- Git
- Claude Code
- GitHub account

You do **not** need to install this path just because you are attending. However, participants following this path should still have a Claude Console login and should redeem hackathon credits on this platform.

---

# Claude event credits (everyone)

Anthropic will provide **$100 of API credit per participant**, subject to the event claim limit.

The event claim link will be distributed closer to the event and is intentionally not included in this document yet.

**[CLAIM LINK — TO BE ADDED CLOSER TO THE EVENT](https://example.com/event-claim-link)**

### Before the event

Please create/sign in to your Claude Console (https://platform.claude.com/) account **before 23 September** so email verification does not delay you at the start of the workshop.

You can use an existing account. If you have never used Claude Console before, the claim process will guide you through creating a Console account using your existing email.

### Claiming the event credit

**If you have access to more than one Claude Console organisation, check which organisation is active **before claiming**. The credit will be added to the active organisation.**

1. Follow the claim link.
2. Sign in to your Anthropic account.
![image](/img/console_signin.png)
3. Select "Individual" on the screen "How will you use the Claude API?"
![image](/img/type.png)
4. Skip the initial buy credits step.
![image](/img/skip_credits.png)
5. Fill in the application page for "AGD 2026 Rare-Disease Reanalysis Hackathon (Uni Bonn / TUM) Credits"
![image](/img/agd_credits.png)
6. Wait for you $100 credit to appear in you dashboard (can take up to 2 hours)
![image](/img/credits_in_profile.png)

> **Important:** The event credit is **API credit in Claude Console**. It is not a credit/top-up for a Claude Pro or Max subscription.

The credit is valid for **90 days from the moment it is claimed**. The organisers will therefore distribute the claim link at/near the event rather than weeks in advance.

---

# Claude Code (Path B participants)
## ⚠️ Claude Code users: make sure you use the hackathon credits and not personal credits

### Before the event
Install Claude Code, either the terminal tool, VS Code integration, standalone app or any combination of the above. 
Follow detailed instructions for installation for your system here: https://code.claude.com/docs/en/overview

After installation and claiming the event credit:

### via a terminal
1. In Claude Code (run `claude` in a terminal), run `/login`.
2. Select **Anthropic Console account (API usage billing)** then **Sign in with your Console account**.
![image](/img/code_terminal_login.png)
![image](/img/code_terminal_login2.png)
3. **Do NOT select:** “Claude account with subscription”.
4. Select **default** workspace and authorise this when the browser opens for login.
![image](/img/default_workspace.png)
5. Run `/status` to check which account/billing method is active.

If you select the subscription option, Claude Code can continue using your personal Claude plan and **will not use the hackathon API credits**.

After the hackathon, run `/login` again to switch back to your normal subscription.

### via VS Code
1. Click the Claude Code icon in the top right tool bar, or type `/login` in the already open Claude Code side panel.
![image](/img/vs_login.png)
2. Choose **Anthropic Console**.
3. Allow opening of the external link.
4. Follow prompts for login and authorisation.
---

# Working with your team

The workshop is designed for teams of approximately four people, combining clinical scientists and bioinformaticians. We suggest that one experienced bioinformatician takes the role of technical steward, handling the final project repository, data, and files.

## Shared project workspace

The workshop GitHub repository is the main shared workspace for team projects.

**Workshop GitHub repository:**  
[WORKSHOP GITHUB REPOSITORY](https://github.com/drewjbeh/AGD-genome-reanalysis-hackathon/tree/main)

Please fork the repo, make a subdirectory for your team with a creative (and unlikely to be duplicated) name under `session-2/projects`. Please push your work here, including your final presentation and working prototype.

---

# Talos setup

The hackathon uses a **pinned Talos 11.0.x environment**.

The organisers will provide prepared Talos 11.0.2 outputs and workshop data so participants do not need to spend the hackathon setting up the complete Talos pipeline.

More technically experienced participants who want to work directly with Talos source code can use the following Talos 11.0.1 release: https://github.com/populationgenomics/talos/releases/tag/v11.0.1.

**Docker/Nextflow and a complete local Talos pipeline are **optional**, not prerequisites.**

---

# Data and AI safety

**Do not use patient-identifiable or confidential clinical data with Claude.**

The hackathon will provide synthetic/public data. Do not paste patient identifiers, confidential clinical reports, unpublished confidential patient data, credentials, passwords, API keys, or other secrets into Claude. **The organisers of the hackathon are not liable for any data privacy breaches related to participants using sensitive data with any AI-based agent or tool.**

---

# If you get stuck

There will be on-site support, including help from the Anthropic team with Claude account setup, Claude Console, event credit claiming, Claude Code installation, login/authentication, and basic troubleshooting.

For the hackathon itself, do not spend a large part of your session building infrastructure from scratch. Start with the provided materials and get something working first.

## Quick checklist

### Everyone
- [ ] Anthropic/Claude account created or tested
- [ ] Email verification completed before the event
- [ ] Event claim link used when released
- [ ] $100 Console API credit claimed
- [ ] Correct Console organisation checked
- [ ] GitHub account available
- [ ] Workshop GitHub repository accessible

### Claude Console participants
- [ ] Claude Console accessible
- [ ] No further technical setup required

### Claude Code participants
- [ ] VS Code or similar editor
- [ ] Git installed
- [ ] Claude Code installed
- [ ] Claude Code logged into **Anthropic Console account (API usage billing)**
- [ ] `/status` checked