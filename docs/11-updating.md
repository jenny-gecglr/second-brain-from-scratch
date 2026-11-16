# 11. Keeping the vault current

A second brain is only useful if it stays true. Updating is small, regular and always ends the same way: index, log, doctor.

## The closing routine (after every operation)
1. `wiki/INDEX.md` lists every new or changed page.
2. One line is appended to `wiki/log.md`: `- 2026-01-31 14:20 | INGEST | source -> pages | what changed`.
3. `python -I -X utf8 tools/vault_doctor.py`, and the report is **read**.

## Per source

| Source | How to update | What prevents duplicates |
|---|---|---|
| YouTube channel | run `youtube_list.py` again; only ids in `new_videos.txt` and `incomplete.txt` are processed | `_processed.json` resume file |
| Chat exports (Claude, ChatGPT) | request a new export, store it as a new dated folder in `raw/exports/`, list titles, import only conversations newer than the last import | the dated decision page records the last import |
| Gemini / Takeout | a new Takeout, same steps | same |
| Drive | re-run the folder map; compare counts with the stored map; open only new or changed files you choose | the map page |
| NotebookLM | re-list notebooks; add cards for new notebooks | the card list in `INDEX.md` |
| Your own rules | change one rule at a time through a decision page | `supersedes:` field |

## When a rule changes
- Add a new decision page with `supersedes:` and set the old one to `status: superseded`.
- A new rule applies from now on. Do not rewrite finished work unless you ask.
- In a long master prompt or rule file, never mention removed rules inside the file. History lives in decisions and the log.
- Keep the previous version of any master in `raw/` with the date.

## Weekly lint
Once a week (or after a big job) run the doctor, read the report, and ask the agent for a short summary: counts, top three findings, proposed fixes. Fix **with approval, one at a time**. Then run the doctor again and show the count dropped.

## Things that go stale
- `[UNVERIFIED]` claims older than 14 days: check them or delete them (this is manual: the doctor counts them but does not read their age).
- Tool notes: tools change, so date your tool notes (`updated:`).
- Rules that no check script can measure: ask "can code verify this?" If not, mark the rule as "not measured".

## Scheduled tasks (optional)
You can schedule a recurring agent task (for example a weekly niche scan) so that it appends results to a page. Rules for scheduled tasks: it writes only what its rule page allows, it logs every run, and anything it cannot verify is labelled `[UNVERIFIED]`. Decide which scheduled tasks to keep: not every old task deserves a place in the vault.
