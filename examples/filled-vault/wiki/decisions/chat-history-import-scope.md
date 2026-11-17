---
type: decision
date: 2026-03-02
scope: ["Claude and ChatGPT history import"]
supersedes: ""
status: active
---
## Decision (one sentence)
[OWNER] Import the cooking and newsletter chats; skip travel, family and shopping chats.

## Why
The vault is about the newsletter and learning. Family and travel chats mention other people and have no lasting value here.

## Scope
The export of 2026-03-02 and later exports.

## What does not change
The original export zip stays untouched in `raw/exports/`. Skipped chats exist only there.

Exception, decided by the owner on the same day: one travel chat is imported under `conversations/trip-planning-notes/` as an owner exception (TAKE), marked `privacy: private`.

Titles were listed with `scripts/list_export_titles.py`, grouped, and decided one group at a time. See [[tools/drive-folder-map]] for the same method applied to Drive.
