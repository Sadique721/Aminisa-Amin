# 🛡️ MANDATORY GIT IDENTITY & ROUTING POLICY
## Strict Separation Between Personal Projects and Corporate (KTPL) Systems

> **STATUS:** PERMANENT GLOBAL DIRECTIVE  
> **APPLIES TO:** ALL AGENTS, CONVERSATIONS, WORKSPACES & CLI SESSIONS

---

### 1. Architectural Concept & Separation of Concerns

The user operates in two strictly isolated domains:
1. **Personal / General Work (Default):** All open-source, personal projects, AI influencer systems (Aminsa Amin), and freelance / non-company repositories.
2. **Corporate Work (`D:\KTPL` only):** Dedicated corporate enterprise telecom/banking systems for KTPL.

Under **NO CIRCUMSTANCES** should credentials, repositories, commits, or pushes be mixed between these two domains.

---

### 2. Global Identity & Git Routing Matrix

| Scope / Location | Target Platform | Account / Identity | Pull Policy | Commit & Push Policy |
| :--- | :--- | :--- | :--- | :--- |
| **All Locations (DEFAULT)**<br/>*(Any path NOT in `D:\KTPL\`)* | **GitHub** | **`Sadique721`**<br/>`mdsadiqueamin721786@gmail.com` | Auto-pull from `Sadique721` remotes | **Autonomous Allowed**<br/>(Push/commit directly without blocking confirmation) |
| **Corporate IR**<br/>`D:\KTPL\IR\...` | **Bitbucket** | **`amin.sadique`** / Bitbucket | **Strictly Bitbucket**<br/>(Always pull latest from Bitbucket) | **MANDATORY 2-STEP CONFIRMATION**<br/>1. Show git diff & ask for review<br/>2. Explicit user approval required before push! |
| **Corporate USSD**<br/>`D:\KTPL\USSD\...` | **GitHub** | **`amin-keyanna`** | **Strictly `amin-keyanna`**<br/>(Always pull latest from `amin-keyanna`) | **MANDATORY 2-STEP CONFIRMATION**<br/>1. Show git diff & ask for review<br/>2. Explicit user approval required before push! |

---

### 3. Execution Rules & Workflow Automation

#### Rule A: Default / Personal Repositories (`Sadique721`)
* Any repository in `D:\current using file\...`, `C:\...`, or any folder outside `D:\KTPL\` belongs to **`Sadique721`**.
* Remote URLs must always target `https://github.com/Sadique721/<repo>.git` or `https://Sadique721@github.com/Sadique721/<repo>.git`.
* Commits and pushes can be executed autonomously with standard descriptive commit messages.

#### Rule B: Corporate `D:\KTPL\IR` (Bitbucket)
* When working in `D:\KTPL\IR`:
  1. **Pulling:** When the user says "pull" or requests updates, **ALWAYS** fetch and pull from the Bitbucket remote.
  2. **Committing / Pushing:** **NEVER auto-push.**
     - **Step 1:** Run `git status` and `git diff --stat`, summarize the exact changes to the user.
     - **Step 2:** Explicitly ask: *"Aapka IR code ready hai. Kya mai Bitbucket par commit aur push karu?"*
     - Only push after receiving explicit user confirmation.

#### Rule C: Corporate `D:\KTPL\USSD` (`amin-keyanna`)
* When working in `D:\KTPL\USSD`:
  1. **Pulling:** When the user says "pull" or requests updates, **ALWAYS** fetch and pull from `amin-keyanna` GitHub remote.
  2. **Committing / Pushing:** **NEVER auto-push.**
     - **Step 1:** Run `git status` and `git diff --stat`, summarize the exact changes to the user.
     - **Step 2:** Explicitly ask: *"Aapka USSD code ready hai. Kya mai amin-keyanna GitHub account par commit aur push karu?"*
     - Only push after receiving explicit user confirmation.

---

### 4. Git Config Template per Scope

```bash
# For Personal / Default (Sadique721):
git config user.name "Md Sadique Amin"
git config user.email "mdsadiqueamin721786@gmail.com"

# For KTPL IR (Bitbucket):
git config user.name "Sadique Amin"
git config user.email "amin.sadique@..."

# For KTPL USSD (amin-keyanna):
git config user.name "amin-keyanna"
```
