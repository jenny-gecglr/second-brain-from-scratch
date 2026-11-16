# 13. Lessons and pitfalls (all of these happened)

Short, real, and each one became a rule or a check.

## 1. A shell alias deleted pages
In Windows PowerShell, `rd`, `rm`, `del` and `ri` are aliases of `Remove-Item`. A helper function that was named `rd` did not define a new command: it ran `Remove-Item` and reset or deleted files. Pages were emptied or deleted. They were restored from agent scratch parts and from the session record.
**Rule:** never name a function with an alias name. Give helpers long names. To move files use `[IO.File]::Move`. **Check:** the doctor reports empty files and broken links.

## 2. The computer clock was a day ahead
Dates were written from a wrong clock, a day in the future, in many files. **Rule:** never write a date later than the computer clock, and fix the clock first. **Check:** the doctor's "future-dated entry" error.

## 3. Empty graph nodes
A canvas copied without its notes made empty (0 byte) nodes in the graph; clicking one created an empty note in the vault root. **Rule:** move a canvas together with its notes, or not at all. **Check:** the doctor reports canvas targets that do not exist, and empty files.

## 4. `#00FF41` became a tag
A bare hex color in a note is read as a tag and makes an empty tag node. **Rule:** write colors in code format with backticks.

## 5. Numbered page names made unreadable graphs
Pages called `01-home`, `02-rules` show as `01-home` nodes. **Rule:** meaningful names, no numbers, no dates; the date lives in the frontmatter. Put the old name in `aliases:` when you rename.

## 6. Bulk graph output is not the vault
A knowledge-graph tool produced hundreds of generated pages. They are an index for discovery, not your notes. **Rule:** generate into a copy first; do not edit generated pages; never feed it private folders.

## 7. Cheap agents miscount
Numbers produced by cheap agents were wrong more than once (a figure attached to three cards that belonged to one; duplicate and blank rows). **Rule:** the quality chain in [14](14-quality-chain.md).

## 8. Long rule files get ignored
An `AGENTS.md` over 200 lines is not read carefully. **Rule:** keep it short; test each rule with "could the model know this without being told? If yes, delete it." Never leave two contradicting instructions.

## 9. Production chats are not knowledge
Forty drafts of a script are not a note. **Rule:** extract the corrections and the final rules, not the drafts.

## 10. A tool that "kept working" had stopped
A scheduled summary task reported "no new chats today" because it could not see a test chat that lived inside a project. **Rule:** a scheduled task must prove it saw its input (count the items it read), and a "nothing found" result is checked once by hand.

## 11. Big imports hide privacy risks
Shared accounts contain other people's chats; Drive contains documents you must never import. **Rule:** [03 scope rule](03-scope-rule.md): list first, decide, then write.

## 12. Publishing your own version is its own risk
A vault contains names, paths, emails and employers. **Rule:** see the README section "Publishing your own version".
