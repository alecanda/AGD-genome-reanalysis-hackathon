# Participant Technical Setup

Please choose the path that matches your experience:

### Path A — Users with no programming experience

**Recommended if you have little or no programming experience, or cannot install anything on your device**

You can participate using the Claude Console (https://platform.claude.com/). You do not need to install Claude Code, VS Code, Git, or a terminal environment for the introductory exercises.

**Note:** Claude Chat (https://claude.ai/) is a separate system to Claude Platform. The Claude credits supplied for the hackathon (details below) are for Console, given as API credit.

### Path B — Users with programming and Claude Code experience

**Recommended if you already have coding experience and use VS Code or a similar editor, and feel comfortable with a terminal and Git.**

Recommended software:
- VS Code or another editor
- Git
- Claude Code
- GitHub account

---

# Claude event credits (everyone)

Anthropic provides **$100 of API credit per participant**.



### Before the event

Please create or sign in to your Claude Console (https://platform.claude.com/) account **before the hackathon starts** so email verification does not delay you at the start of the workshop. You can also use an existing account.

Here is a tutorial for getting the necessary Claude Credits. Note that the credit will be added to the active account/organisation.

### Claiming the event credit on Sep 23

1. Follow the claim link. It will be distributed at the registration desk on-side.
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

The credit is valid for **90 days from the moment it is claimed**.

---
# PATH A: Claude Console

Please continue reading at the section **Working with your team**. You can skip the Claude Code setup step required for Path B.

# PATH B: Claude Code
## ⚠️ Claude Code users: make sure you use the hackathon credits and not personal credits

### Before the event
Install Claude Code, either the terminal tool, VS Code integration, standalone app or any combination of the above. 
Follow detailed instructions for installation for your system here: https://code.claude.com/docs/en/overview

After installation and claiming the event credit:

### via a terminal
1. In Claude Code (run `claude` in a terminal), run `/login`. If you are already signed in, run `/logout` first.
2. Select **Anthropic Console account (API usage billing)**. **Do NOT select:** “Claude account with subscription”
![image](/img/code_terminal_login.png)
3. Select **Sign in with your Console account**.
![image](/img/code_terminal_login2.png)
4. Select **default** workspace and authorise this when the browser opens for login.
![image](/img/default_workspace.png)
5. Run `/status` to check which account/billing method is active.

After the hackathon, run `/logout`, then `/login` again to switch back to your normal Claude account with subscription.

### via VS Code
1. Click the Claude Code icon in the top right tool bar, or type `/login` in the already open Claude Code side panel.
![image](/img/vs_login.png)
2. Choose **Anthropic Console**.
3. Allow opening of the external link.
4. Follow prompts for login and authorisation.
---

# Working with your team

The workshop is designed for teams of approximately four people, combining clinical scientists and bioinformaticians. We suggest that **one experienced bioinformatician takes the role of technical steward, handling the final project repository, data, and files.**

## Shared project workspace

The workshop GitHub repository is the main shared workspace for team projects.

**Workshop GitHub repository:**  
[https://github.com/drewjbeh/AGD-genome-reanalysis-hackathon/tree/main](https://github.com/drewjbeh/AGD-genome-reanalysis-hackathon/tree/main)

1. Please fork the repo (button near the top right)
![image](/img/fork_repo.png)
2. Keep the suggested name, leave "Copy the main branch only" checked, and click "Create fork".
You find a copy of the repository in your own Github account, which you can either edit in the browser, or clone on your local machine, edit, and push changes
4. Create a subdirectory for your team with a creative (and unlikely to be duplicated) name under `session-2/projects`. Please push your work here, including your final presentation and working prototype.

---

# Talos setup

The hackathon uses a **pinned Talos 11.0.1 environment**.

The organisers will provide prepared Talos 11.0.1 outputs and workshop data so participants do not need to spend the hackathon setting up the complete Talos pipeline.

More technically experienced participants who want to work directly with Talos source code can use the following Talos 11.0.1 release: https://github.com/populationgenomics/talos/releases/tag/v11.0.1. This can be done using the following command, for example:
```
git clone git@github.com:populationgenomics/talos.git --branch v11.0.1
```
---

# Data and AI safety

**Do not use patient-identifiable or confidential clinical data with Claude.**

The hackathon provides synthetic/public data. Do not paste patient identifiers, confidential clinical reports, unpublished confidential patient data, credentials, passwords, API keys, or other secrets into Claude. **The organisers of the hackathon are not liable for any data privacy breaches related to participants using sensitive data with any AI-based agent or tool.**

---

# If you get stuck

There will be on-site support, including help with Claude account setup, Claude Console, event credit claiming, Claude Code installation, login/authentication, and basic troubleshooting.

For the hackathon itself, do not build infrastructure from scratch. Start with the provided materials and get something working first.

## Quick checklist

### Everyone
- [ ] Anthropic/Claude account created or tested
- [ ] Email verification completed before the event
- [ ] Event claim link used when released
- [ ] $100 Console API credit claimed
- [ ] Correct Console organisation checked
- [ ] GitHub account available
- [ ] Workshop GitHub repository accessible

### Path A: Claude Console participants
- [ ] Claude Console accessible
- [ ] No further technical setup required

### Path B: Claude Code participants
- [ ] VS Code or similar editor
- [ ] Git installed
- [ ] Claude Code installed
- [ ] Claude Code logged into **Anthropic Console account (API usage billing)**
- [ ] `/status` checked
