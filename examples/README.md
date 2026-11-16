# Filled example vault

Everything in this folder is **invented**. It shows what the vault looks like after a few real operations: a chat-import decision, a Drive folder map, one YouTube channel imported with its check report, a lesson, a rule and a private note.

How to use it:
1. Open this folder in Obsidian (**Open folder as vault**) and look at the graph and the pages.
2. Read `AGENTS.md` (section 0 is filled in), `wiki/INDEX.md` and `wiki/log.md` the way an agent does at the start of a session.
3. Run the doctor and compare with `outputs/vault-doctor/vault-doctor-report.md`:
```powershell
python -I -X utf8 tools/vault_doctor.py
```

The doctor report in `outputs/vault-doctor/` carries the date it was generated, which is later than the dates inside the example log.

Do not use this folder as your own vault. Start from `vault-template/`.
