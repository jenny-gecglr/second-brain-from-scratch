# 09. NotebookLM notebooks you already have

If you used NotebookLM before this vault existed, you probably have notebooks full of sources. They are not in Google Takeout, so you bring them in by hand or through the agent.

## Step 1. List the notebooks
Ask the agent (with the NotebookLM tool connected, see [08](08-youtube-data.md)):
```text
List all my NotebookLM notebooks: title, number of sources, and one line on the topic.
Do not read the sources yet.
```
The count may surprise you: there are often more notebooks than you remember.

## Step 2. Decide per notebook
TAKE, SKIP or LATER, using [03](03-scope-rule.md). Skip notebooks about other people (a relative's study notebook) and notebooks about regulated personal topics unless you deliberately want them in a private section.

## Step 3. One source card per taken notebook
Card contents (use `templates/source.md`):
- the notebook name and its source types,
- the key points the notebook produced (use its summary and Q&A),
- the rules and lessons that follow, with links,
- what you did not take and why.
Put cards in `wiki/sources/notebooklm/`. Group them by topic in `INDEX.md` instead of making a heading just for NotebookLM.

## Step 4. Check and log
Quality chain, then index, log, doctor.

## If the tool will not connect
- Sign in again with the tool's own login command (Google sign-in is always yours).
- As a last resort the agent can work through a browser extension, which is slower and costs more, so ask first.
