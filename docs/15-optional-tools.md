# 15. Optional tools (add them later, one at a time)

None of these are needed for the base vault. Add one only when you have a reason, and write a short tool note in `wiki/tools/` when you do (what you installed, where, how to remove it).

## graphify (knowledge graph from a folder)
- What: reads a folder of notes and builds a graph of concepts and links, with a report of the most connected ideas and the ones left alone. Each link is labelled as written in the text, inferred, or ambiguous.
- Package name on PyPI: `graphifyy` (two y). Install it in its **own isolated Python environment**, not into your system Python, and read its project page before using it.
- Use it on **small parts** of the wiki (it spends model tokens on the documents), never on `raw/` or private notes.
- Output goes to a **separate copy** first. Do not edit generated pages. Move a generated canvas only together with its notes (see lesson 3 in [13](13-lessons-and-pitfalls.md)).
- Use the report as a to-do list for missing cross links, not as new knowledge.

## Whisper (speech to text)
- What: turns audio into timed text or subtitles on your own PC, so audio and video can become sources.
- Install it **outside the vault** in its own Python environment. Test it on a short clip first and measure the speed on your PC before planning long files.
- Keep generated transcripts in `raw/transcripts/`, unedited.

## A second agent for checks
The quality chain works best with at least two different tools: one that produces and one that checks. Examples that are installable on a PC: Codex CLI (ChatGPT sign-in), the Gemini command-line tool, or any other model you have access to. Follow each vendor's install page and sign in yourself. Test the checker by giving it a known wrong number and see that it catches it.

## Scheduled tasks
A recurring agent job (weekly scan, daily summary). Keep each task's rules in a wiki page, make it log what it did, and make it prove what input it saw (see lesson 10).

## What to avoid adding
- Anything that wants to run in the background on all your folders.
- Tools that send your whole vault to a cloud service. Check what leaves your PC before you install.
