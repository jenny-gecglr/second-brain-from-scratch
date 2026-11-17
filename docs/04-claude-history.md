# 04. Import your Claude conversation history

Your past Claude chats hold decisions, rules and prompts you already paid for. This step turns them into notes without importing the noise.

## 1. Request the export
In [claude.ai](https://claude.ai): Settings, Privacy, **Export data**. You receive an email with a download link. Download the zip. (The author used these steps. Menu names change from time to time: [UNVERIFIED] for your current version, so look for "Export data" under privacy or account settings.)

## 2. Store it untouched
```
raw/exports/claude/<export-date>/   <- put the zip here, do not unzip into the wiki
```
Never edit it. Keep a copy of the zip's name and date in `wiki/log.md`.

## 3. List the titles (no content is read)
```powershell
python -I -X utf8 scripts/list_export_titles.py raw/exports/claude/<export-date>/<file>.zip --out outputs/claude-titles.md
```
The script reads `conversations.json` inside the zip and prints date, title and message count. If the layout is different from what it knows, it says so and stops. The layout was checked on synthetic data only, so confirm it on your real file.

## 4. Group and decide
Open `outputs/claude-titles.md` and ask the agent:
```text
Group these conversation titles into categories. Use titles only; do not open any conversation.
Show a table: group, how many conversations, example titles, and a suggested TAKE / SKIP / LATER.
Write nothing yet.
```
You decide each row (see [03 scope rule](03-scope-rule.md)). The agent writes your answers as a decision page.

## 5. Where each kind goes
| Kind of conversation | Where it goes |
|---|---|
| Off-topic but worth keeping | `conversations/<conversation-name>/` (one folder per chat, its own name) |
| Project instructions and "master prompts" | latest version verbatim in `raw/`, a short summary in `wiki/rules/` |
| Production chats (writing a script, naming a video, etc.) | NOT turned into notes. Only the **lessons, corrections and final rules** are extracted, with the project name written next to each |
| Chats you decided to SKIP | stay in the raw zip only |

## 6. Mark privacy
Any note under `conversations/` gets `privacy: private` or `privacy: internal` in its frontmatter. The doctor warns if the field is missing.

## 7. Update and log
Agent updates `wiki/INDEX.md`, appends to `wiki/log.md`, and runs the doctor. Only then is the import done.

## Why not import everything?
- Production chats are long and repetitive. The lasting value is the correction you made ("never open with a question") and the final prompt, not the 40 drafts.
- Chats often contain other people's data or things you typed in a hurry.
- A wiki that is 90 percent chat logs cannot be searched usefully.
