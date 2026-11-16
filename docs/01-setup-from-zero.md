# 01. Setup from zero (Windows)

Goal: a working vault, opened in Obsidian, with an AI agent that has read the rules. Time: allow roughly an hour the first time (not measured). This guide was written and tested on Windows 11 with PowerShell. Mac and Linux are not tested (see the notes at the end).

## What you need, and what you do yourself

| Item | Why | Cost | You do it yourself |
|---|---|---|---|
| Obsidian | reads and edits the vault (plain markdown files) | check the Obsidian pricing page for current terms | download and install |
| Claude Code | the agent that maintains the wiki | needs a paid Claude plan or a Console account (the free plan does not include it) | sign-up, sign-in, payment |
| Python 3.8+ | runs the check scripts | free | install |
| Git for Windows | optional, lets Claude Code use a Bash shell | free | install |

Accounts, passwords, payment and sign-in codes are always yours. Never paste a password or an API key into the vault or into a chat with an agent.

## Step 1. Install Obsidian
1. Open https://obsidian.md/download and download the Windows installer.
2. Run it and finish the wizard.
3. Do not create a vault yet (step 4 does that).

## Step 2. Install Python
1. Download Python 3 from https://www.python.org/downloads/ and run the installer. Tick "Add python.exe to PATH".
2. Open PowerShell (Start menu, type `PowerShell`) and check:
```powershell
python --version
```
It must print `Python 3.x.x`. If Windows opens the Store instead, turn off the "App execution aliases" for Python in Settings, or reinstall with the PATH box ticked.

## Step 3. Install Claude Code
The official install page is https://code.claude.com/docs/en/setup (commands below were checked against it; they can change, so look there if one fails).

In PowerShell:
```powershell
irm https://claude.ai/install.ps1 | iex
```
Alternative with WinGet:
```powershell
winget install Anthropic.ClaudeCode
```
Close PowerShell, open a new window, then check:
```powershell
claude --version
claude doctor
```
Sign in by running `claude` once and following the browser prompt. If you prefer a graphical app, Anthropic also offers a Desktop app that includes Claude Code.

Optional: install Git for Windows from https://git-scm.com/downloads/win.

## Step 4. Create your vault from the template
1. Copy the folder `vault-template` from this repo to a place you choose, for example `C:\Users\YOU\Documents\MyVault`, and rename the copy to the name you like. Also copy this repo's `scripts` folder **into** that vault (so you have `MyVault\scripts\`). The commands in the guide are written to be run from the vault root and use `scripts\...` paths.
2. Open Obsidian, choose **Open folder as vault**, and select that folder.
3. You will see `AGENTS.md`, `CLAUDE.md`, `wiki/`, `raw/` and so on. If Obsidian asks about "Trust author and enable plugins", you can skip it: this vault needs no community plugins.

## Step 5. First run with the agent
1. In PowerShell go to your vault folder:
```powershell
cd "C:\Users\YOU\Documents\MyVault"
claude
```
2. Paste this first message:
```text
Read AGENTS.md, wiki/INDEX.md and the end of wiki/log.md. Then do the "First run" section of AGENTS.md:
run the vault doctor with --snapshot and then without, show me the result, and ask me the questions
needed to fill section 0 (who I am, my language, what this vault is for).
Do not write anything outside AGENTS.md section 0 until I approve.
```
3. Answer its questions. It should write section 0 of `AGENTS.md` and add one line to `wiki/log.md`.

## Step 6. Check that it works
```powershell
python -I -X utf8 tools/vault_doctor.py
```
Expected: `VAULT DOCTOR: ERROR 0 | WARNING 0 | INFO 0`. Open `outputs/vault-doctor/vault-doctor-report.md` to see the table.

If you get this, the base is done. Next: [02. Vault structure](02-vault-structure.md), then import your sources one by one (04 to 09).

## Troubleshooting
| Problem | Fix |
|---|---|
| `claude` is not recognized | close and reopen PowerShell; if still missing see the "Fix your PATH" page in the Claude Code docs |
| `irm` is not recognized | you are in CMD, not PowerShell |
| `python` opens the Microsoft Store | reinstall Python with "Add to PATH" ticked, or disable the app execution alias |
| Obsidian shows no files | you opened the parent folder; open the folder that contains `AGENTS.md` |
| Doctor prints mojibake or crashes on accents | always run with `-I -X utf8` exactly as shown |

## Notes on other systems
Everything in the vault itself (markdown, Python scripts) is system independent. Only the install commands and the backup script (`scripts/backup-vault.ps1`) are Windows specific. On Mac or Linux use the install commands on the official Claude Code page and a cron job or launchd for backups. These paths are **not tested** in this kit.
