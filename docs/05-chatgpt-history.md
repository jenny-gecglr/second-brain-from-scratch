# 05. Import your ChatGPT history

Same method as [04](04-claude-history.md). The differences are the export and one extra risk: shared accounts.

## 1. Request the export
In [ChatGPT](https://chatgpt.com): your profile, Settings, **Data controls**, **Export data**. You get an email with a download link that expires, so download the zip promptly. ([UNVERIFIED] menu names and link lifetime: OpenAI changes them; the help page was not reachable when this kit was written.)

## 2. Store it untouched
```
raw/exports/chatgpt/<export-date>/
```

## 3. List titles
```powershell
python -I -X utf8 scripts/list_export_titles.py raw/exports/chatgpt/<export-date>/<file>.zip --out outputs/chatgpt-titles.md
```
A large history can have hundreds of conversations. Do not let an agent read them all. Work from the title table only, in groups.

## 4. Group, then decide
Ask the agent to group the titles (titles only), and decide TAKE / SKIP / LATER per group as in [03](03-scope-rule.md).

## Shared account warning
If anyone else ever used your ChatGPT account (a partner, a sibling, a colleague), their chats are in your export. **Mark those groups yourself.** Do not let the agent guess whose chat it is. Notes about another person go in a clearly named folder with `privacy: private`, or are skipped.

## Using ChatGPT history as the "second opinion"
Imported conversations can be useful as sources for rules and lessons. Treat them like any other source: summarise, label with `[SOURCED]` and the conversation title, and do not copy long passages.

## What a good result looks like
- A decision page listing the groups and the choices.
- One hub page per topic you took (for example "marketing", "language learning") that links the notes beneath it.
- A log line per import.
- Skipped groups exist only in the raw zip.
