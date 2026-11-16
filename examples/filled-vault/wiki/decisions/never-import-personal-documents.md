---
type: decision
date: 2026-03-02
scope: ["all imports"]
supersedes: ""
status: active
---
## Decision (one sentence)
[OWNER] These categories are never imported, opened or summarised: ID and visa papers, passwords and recovery codes, bank and tax records, invoices, health papers.

## Why
An AI tool or a sub-agent must never see them. A vault is a convention, not a lock, so the safe place for these files is outside it.

## Scope
Every source: chat exports, Drive, YouTube, notebooks.

## What does not change
The category names are written here, never the file names. If such a file shows up in a list, the agent says "never imported" and moves on.
