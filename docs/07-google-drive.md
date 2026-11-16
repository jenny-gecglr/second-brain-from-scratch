# 07. Bring in Google Drive, without copying your life

Drive usually holds a mix of useful documents and things that must never enter an AI tool: ID scans, invoices, recovery-code files. The method is **map first, open later**.

## Rule
The files stay in Drive. The vault gets (a) a **map** of what exists, and (b) notes written from the few documents you choose.

## Step 1. Connect Drive (optional)
You can read Drive from the agent in two ways:
- **A Google Drive connector** for Claude (set up in Claude's connector settings; you sign in to Google yourself).
- **Drive for desktop**, which shows Drive as a normal folder. Then the agent can read the files you point to, but also everything else in that folder, so point it at one folder only.

Either way, you do the Google sign-in. Do not hand a password to an agent.

## Step 2. Map the folders (names and counts only)
Ask:
```text
List the top-level folders of my Drive folder "<name>". For each: the name, the number of files,
the file types. Do NOT open any file and do NOT show file contents. Write nothing yet.
```
Save the result as one page in `wiki/tools/` (for example `drive-folder-map`): a table with columns folder, what is in it (from the name only, marked `[UNVERIFIED]`), decision.

## Step 3. Decide per folder or per file (TAKE / SKIP / LATER)
Use [03 scope rule](03-scope-rule.md). Typical outcome:

| Kind | Decision |
|---|---|
| Course notes, guides, PDFs you study | TAKE (summary or verbatim, as you choose) |
| Work templates and checklists | TAKE |
| Image folders (inspiration, highlights, photos) | SKIP: one line in the map is enough |
| ZIP archives | SKIP, never unzip unknown archives into the vault |
| ID, visa, civil documents | SKIP, never opened |
| Passwords or recovery codes | SKIP, a **security risk**: never stored in a vault |
| Credit or finance reports, invoices | SKIP |
| Health papers | SKIP unless you deliberately make a private health section |
| QR code PDFs, scans | SKIP |

The skipped categories are written down **by category name only** (never by file name), so that you are not asked again.

## Step 4. Import the chosen files
1. Download or copy each chosen file into `raw/notes/` (unchanged).
2. Ask the agent to write a note under `wiki/` (a summary, or a verbatim page if you want the exact text), with `[SOURCED]` and the Drive file name in the frontmatter.
3. Agents do not read images or videos here: a one-line description is enough.
4. Update the index, append to the log, run the doctor.

## Google files (Docs, Sheets)
Google Docs and Sheets are not ordinary files. Download them as `.docx` or `.xlsx` (or `.csv` for sheets) into `raw/notes/` before importing, or read them through the connector. Never edit the Google original from the vault.

## A file you decided never to import
Write one rule page, `wiki/decisions/never-import-<topic>`, naming the **category** (not the file). Every future session then knows not to read it.
