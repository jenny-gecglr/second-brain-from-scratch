---
type: decision
date: 2026-03-04
scope: ["Google Drive import"]
supersedes: ""
status: active
---
## Decision (one sentence)
[OWNER] Only the "Recipes and newsletter" Drive folder is imported; image folders are mapped but not opened.

## Why
The folder holds the newsletter drafts and recipe notes. The photo folders add nothing a note can use.

## Scope
Drive as of 2026-03-04.

## What does not change
Files stay in Drive. The vault keeps the map ([[tools/drive-folder-map]]) and notes written from the chosen files. See also [[decisions/never-import-personal-documents]].
