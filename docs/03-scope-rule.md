# 03. The scope rule: what comes in, what stays out

Every import in this kit (chat exports, Drive, YouTube, notebooks) follows the same five steps. The rule exists because the first impulse is "import everything", and that fills a second brain with noise, other people's data and things you never want an agent to read.

## The five steps
1. **List first.** Produce a list of categories (titles only, no content). Nothing is written yet.
2. **You decide.** For each category: TAKE, SKIP, or LATER. The agent never decides this.
3. **Record the decision** as a page in `wiki/decisions/` (template: `templates/decision.md`), with the date and the reason.
4. **Raw first.** Put the original export in `raw/` untouched. Compiled knowledge goes in `wiki/`.
5. **Approve before writing.** The agent shows you what it plans to write and waits for a yes. One line goes to `wiki/log.md`.

## What usually goes in
- Methods, rules and lessons you want to reuse
- Notes about your own projects and decisions
- Research you did and want to keep (as a summary with a source link)
- Tool notes (what worked, what broke, settings)
- Courses and videos you learned from (as rules and lessons, not as copies)

## What stays out (default, change only on purpose)
- Passwords, recovery codes, API keys, tokens
- ID, passport, visa and civil documents
- Bank, credit, tax, invoice and payroll records
- Health records
- Other people's data (family, friends, clients) unless they agreed
- Images, video and audio files (describe them in a note instead)
- Job-search drafts and one-off chats with no lasting value
- Anything you would not want an outside tool or a sub-agent to read

If a category is borderline, mark it `LATER` and decide when you know why you need it.

## A decision page, filled in
```markdown
---
type: decision
date: 2026-01-31
scope: ["chat history import"]
supersedes: ""
status: active
---
## Decision (one sentence)
Import work and learning chats; skip travel, health and family chats.

## Why
Keep the brain about my work. Personal topics do not belong in a tool other agents can read.

## Scope
Chat export of 2026-01-31 and later exports.

## What does not change
The raw export stays untouched in raw/exports/.
```

## A category table you can copy
| Group | Example | Decision | Note |
|---|---|---|---|
| A. Work methods | prompts, workflows | TAKE | |
| B. Research | competitor or topic studies | TAKE | summarise, keep source |
| C. Tool how-tos | how I set up X | TAKE | skip what is already in the wiki |
| D. Personal admin | travel, forms | SKIP | |
| E. Health, money | | SKIP | never |
| F. Other people's work | a relative's thesis | SKIP unless the owner says | privacy: private |

## Reopening a decision
Decisions can change ("I now want the research chats too"). Write a **new** decision page that says `supersedes: <old page>`, set the old one to `status: superseded`, and import under the new decision. Do not edit history.
