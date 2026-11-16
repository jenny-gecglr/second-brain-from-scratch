---
type: tool
topic: vault doctor, the structural health check
updated: 2026-03-01
---
# Vault doctor

`tools/vault_doctor.py` scans the whole vault and **reports** problems. It never edits, deletes or moves anything. The owner approves fixes one by one.

```
python -I -X utf8 tools/vault_doctor.py             # check and write the report
python -I -X utf8 tools/vault_doctor.py --snapshot  # record the expected state of raw/
python -I -X utf8 tools/vault_doctor.py --quiet     # summary lines only
```

Report: `outputs/vault-doctor/vault-doctor-report.md` (overwritten each run). Exit code 1 means at least one ERROR.

| Level | Checks |
|---|---|
| ERROR | broken `[[link]]`, empty (0 byte) file, file deleted or changed in `raw/`, canvas pointing to a missing note, future-dated entry |
| WARNING | unexpected file in the vault root, BOM, mojibake, missing frontmatter or `type:`, decision page missing a field, bad log line, imported chat note without `privacy:`, `AGENTS.md` over 200 lines |
| INFO | page not in `INDEX.md`, orphan page, same page name in two folders, density of `[UNVERIFIED]` |

Limit: it checks **structure only**. It cannot tell whether a fact is true. That is the job of the quality chain (see `AGENTS.md` section 7).
