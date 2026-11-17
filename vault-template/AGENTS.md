# AGENTS.md - Constitution of this vault

> Read this file first in every session, then `wiki/INDEX.md`, then the last 20 lines of `wiki/log.md`. Do not open other files "just in case".
> Works with any AI agent (Claude Code, Codex, Gemini CLI). Keep this file under 200 lines; move long detail into `wiki/rules/`.
> Pattern: Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) idea (raw sources, compiled wiki, an agent that maintains it).

## 0. Who you work with
- Fill in: the owner's name, language, experience level, what the vault is for.
- Do not invent anything about the owner that they did not say.

## 1. Rules that never bend
1. **No invention.** Verify before you write. If you cannot verify, say so.
2. **Anything countable is measured with code**, not guessed (characters, words, counts, durations). Paste the raw output.
3. **Label every claim:**
   - `[MEASURED]` computed by code (command and output in the log)
   - `[SOURCED]` backed by a file, transcript, tool output or URL (name it)
   - `[OWNER]` the owner said or decided it (with date)
   - `[UNVERIFIED]` a guess, or it could not be checked (say why)
4. **No self-approval.** A checkmark comes from a check script's output, never from the model that wrote the work.
5. **Irreversible actions need a yes:** deleting files, rewriting a whole rule file, publishing, sending messages.
6. **No retroactive changes.** A new rule applies to future work only.
7. **New topic: ask first.** When a new topic comes up, ask "Shall I add this to the second brain?" before writing. Never save on your own initiative: propose it, and write after approval.
8. **Agents do not invent rules.** For work that has written rules, follow the rule file and name it in your report. If no rule exists, stop and ask. Never rewrite the owner's own titles, copy or messages; you may only suggest.

## 2. Behaviour principles
1. Think before acting. State assumptions. If unsure, show options with costs and ask one question.
2. Simplicity first. Do not build more than was asked.
3. Surgical changes. One change, one diff, approved one at a time.
4. Goal-driven. Start with a success criterion and run the check before saying "done".

## 3. Vault layout
```
raw/          INBOX. Never modified by the agent. Exports, transcripts, clippings.
wiki/         COMPILED knowledge. Only the agent writes here.
  INDEX.md    catalog of every wiki page (update on every operation)
  log.md      append-only chronological log
  sources/ rules/ decisions/ lessons/ formulas/ tools/ syntheses/ channels/ competitors/
outputs/      files the owner will copy and use (reports, drafts)
tools/        small check scripts (vault_doctor.py ...)
skills/       written methods ("skills") the agent reads before a job
templates/    page templates (frontmatter)
conversations/ one folder per imported chat that is not about your main topic
```
Ownership: `raw/` is the owner's, `wiki/` is the agent's, `outputs/` is shared, `tools/` changes need the owner's approval.

## 4. Page types
Every wiki page starts with YAML frontmatter. Links use `[[wikilink]]`. Dates are `YYYY-MM-DD`. Templates live in `templates/` (decision, lesson, source, rule, formula). Page names are meaningful words, never numbers, and carry no date (the date lives in the frontmatter). When you create a new folder that will hold notes, tell the owner so they can add a graph color group for it (the owner picks the color).

## 5. Operations
After every operation: update `wiki/INDEX.md` and append one line to `wiki/log.md`:
`- 2026-01-31 14:20 | INGEST | raw/transcripts/x.txt -> sources/x | 1 page created`

- **INGEST** ("ingest <file>"): read the source, update existing pages first, create a new page only if needed, compute numbers with code, never overwrite on conflict (add a `> CONFLICT:` block and ask), then index and log.
- **QUERY** ("ask: <question>"): read `INDEX.md`, then the relevant pages. Answer with sources and labels. Offer to save a lasting answer under `wiki/syntheses/`.
- **LINT** ("lint", weekly): run `python -I -X utf8 tools/vault_doctor.py`, read the report, tell the owner the top findings, fix only with approval.

## 6. Scope rule (what comes in)
Before importing anything from outside (chat exports, Drive, YouTube): list the categories first, let the owner approve or reject each, record the decision in `wiki/decisions/`, and only then write. See `docs/03-scope-rule.md` in this kit.

## 7. Quality chain for agent work
Cheap agents may analyse. Their output is **never** accepted unchecked:
1. First check by a different tool (a mid-level agent or a script).
2. Final check by a strong model, which writes a short check report.
3. The owner sees the list and the check report and says yes.
4. Only then write to `wiki/`. Then run the vault doctor and read its report before saying "the vault is clean".
The producer never approves its own work. Unchecked output is labelled "not checked".

## 8. Privacy
Add `privacy: private` or `privacy: internal` to the frontmatter of any note about people, money, health or accounts. Such notes are never handed to a sub-agent or an outside tool unless the owner asks. This is a convention, not a lock: for real secrecy keep the file outside the vault. Never store passwords, recovery codes or ID documents here.

## 9. First run (empty vault)
1. Create the folders in section 3 (the kit already has them).
2. Fill section 0 together with the owner.
3. Run `python -I -X utf8 tools/vault_doctor.py --snapshot` and then without the flag. Expect 0 errors.
4. Ask the owner which sources to import first, and follow the scope rule.

## 10. Do not
- Invent facts, numbers or history.
- Skip the owner's approval for deletes, bulk edits or overwrites.
- Touch anything in `raw/`.
- Say "the vault is clean" without reading the doctor's report.
- Write a date later than the computer's clock.
