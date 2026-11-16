---
name: vault-doctor
description: Health check for this Obsidian vault (broken links, empty files, changed raw files, future dates, privacy). Use after any bulk job, weekly, or when the owner says "lint", "doctor" or "check the vault". Read-only; fixes need approval.
---

# vault-doctor

## When
- After any bulk job (ingest, many pages written by agents, moving or deleting files).
- Weekly (`AGENTS.md` section 5, LINT).
- When something looks broken (empty graph node, missing page).

## Steps
1. Run from the vault root: `python -I -X utf8 tools/vault_doctor.py`
2. Read the newest report in `outputs/vault-doctor/`. Start with the summary table.
3. Tell the owner in plain words: how many ERROR, WARNING, INFO and the top 3 findings.
4. Propose fixes and wait for approval. The doctor fixes nothing.
5. After fixing, run it again and show that the error count dropped.
6. Append one line to `wiki/log.md`: `- YYYY-MM-DD HH:MM | LINT | vault_doctor: ERROR x, WARNING y`

## How to read findings
| Finding | Meaning | Action |
|---|---|---|
| Broken `[[link]]` | link to a page that does not exist | point it to the right page, or remove it (ask) |
| Empty file | created by accident | ask before deleting |
| `raw/` deleted or changed | raw must never change | STOP, tell the owner, restore from backup |
| Future date | written from a wrong clock | check the computer clock, fix with approval |
| Canvas target missing | canvas points to a missing note, makes empty nodes | move the canvas with its notes, or remove it |
| Orphan or not in INDEX | nothing links to it | add to `INDEX.md` or link from a related page |

## Limits
- Structure only. It does not check whether content is true.
- Refresh the raw snapshot (`--snapshot`) only after the owner deliberately adds raw files.
- The privacy field is a convention, not a lock.

## Do not
- Say "the vault is clean" without reading the report.
- Delete, move or bulk-fix without approval.
- Change anything inside `raw/`.
