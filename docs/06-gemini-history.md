# 06. Import your Gemini history

Gemini history does not come as a single "conversations" file. You get it through **Google Takeout**.

## 1. Request the export
1. Go to https://takeout.google.com and sign in.
2. Click **Deselect all**.
3. Select only what you need: the Gemini activity ("My Activity" with the Gemini Apps filter) and Gems if you created any. Do not export your whole Google account.
4. Choose export once, zip, and create the export. You get an email when it is ready.
([UNVERIFIED] exact product names in Takeout: Google renames them. Pick the entries whose names contain "Gemini".)

## 2. Store it outside the vault, then copy the part you need
Keep the downloaded zip in a normal downloads folder, **not** inside the vault. Unzip it in a temporary folder outside the vault. Copy only the files you decided to keep into `raw/exports/gemini/<export-date>/`.

## 3. List what is there, then decide
The activity file is not shaped like the Claude or ChatGPT exports, so `list_export_titles.py` will say "layout not recognised". Ask the agent to list the **titles or first lines only**, group them, and show a TAKE / SKIP / LATER table. Example groups that came up in practice:

| Group | Typical decision |
|---|---|
| Cover or design work | TAKE (rules for later) |
| Master prompts and scripts from a tool you stopped using | SKIP (a bad experience should not become a rule) |
| Competitor or channel research | TAKE, compare with existing pages, no copies |
| Tool learning | TAKE what is not already in the wiki |
| Calendar, reminders, daily life | SKIP |
| Someone else's academic work | SKIP unless they agreed |

## 4. Gems and custom instructions
A Gem is a saved instruction. If it contains a master prompt you still use, keep the latest version verbatim in `raw/`, and write a short summary in `wiki/rules/`. If you no longer use it, skip it.

## 5. Notebooks (NotebookLM)
NotebookLM notebooks are **not** in Takeout. See [09 NotebookLM notebooks](09-notebooklm-notebooks.md).

## 6. Log and doctor
Update the index, append to the log, run `vault_doctor.py`.
