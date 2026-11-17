# 08. Pull knowledge from YouTube channels and videos

Goal: learn from a channel without watching it, keep your strong (expensive) model's usage low, and end with linked notes you approved.

## The idea in one picture
```
channel or video link
   -> script lists the videos (yt-dlp)               [code, no model]
   -> NotebookLM reads the transcripts, writes       [heavy reading is offloaded]
      summaries, rules, workflows
   -> a cheap model files and pairs the results      [cheap model, no transcripts rewritten]
   -> a checker model verifies numbers and names     [see 14, quality chain]
   -> you see the list and a check report, and say yes
   -> only then notes are written to wiki/
```

## Tools
| Tool | Role | Install |
|---|---|---|
| `yt-dlp` (https://github.com/yt-dlp/yt-dlp) | lists a channel, gets titles, views, durations, descriptions | `pip install yt-dlp` then `python -m yt_dlp --version` |
| NotebookLM | reads transcripts, produces summaries and verbatim transcripts | a Google account; the `nlm` command-line tool (project `notebooklm-mcp-cli`) can drive it from the agent. Install it as that project's own README describes (not tested here), then sign in with `nlm login`; you sign in to Google yourself |
| a cheap model | sorting and filing only | whichever you have (a small Claude model, Gemini, etc.) |
| a strong model | the final check and the list shown to you | your main agent |

Commands used in the tested setup (NotebookLM CLI 0.16.x, November 2026; they can change):
```text
nlm notebook query <notebook> "<question>"        ask a question across the sources
nlm source list <notebook> --json                 list sources and their ids
nlm source content <source-id> -o <file>          save the verbatim transcript to a file
```

## Step 1. List the videos (code, no model)
```powershell
python -I -X utf8 scripts/youtube_list.py "https://www.youtube.com/@ChannelName" raw/transcripts/ChannelName
```
This writes `videos.json` (id, title, views, duration), an empty `_processed.json` (the resume file), `new_videos.txt` and `incomplete.txt`. The fast listing has **no upload dates and no descriptions**; Step 2 and Step 3b get them with a second pass.

## Step 2. Choose which videos
| Channel size | Rule |
|---|---|
| 80 videos or fewer | take all |
| more than 80 | the 80 most viewed of the last 6 months, plus the 50 most viewed of all time, without duplicates, at most 130 in total; a second model checks "did a clearly important video get missed?" |
| Shorts (list them separately with `--tab shorts` and their own out_dir, e.g. `python -I -X utf8 scripts/youtube_list.py "https://www.youtube.com/@ChannelName" raw/transcripts/ChannelName-shorts --tab shorts`) | compare their median views with the long videos; **you** decide include or exclude per channel |

The "last 6 months" rule needs upload dates, which the fast listing does not have. Get them with a second pass for the candidates, one video at a time:
```powershell
python -m yt_dlp --skip-download --no-warnings --print "%(id)s %(upload_date)s" "https://www.youtube.com/watch?v=VIDEO_ID"
```
(prints the id and the date as `YYYYMMDD`). Let a script loop over the ids, not the model.

Show the list to the owner before going further.

## Step 3. Transcripts, verbatim
Put all videos of one channel in **one** NotebookLM notebook named after the channel. For a single video that belongs to no channel you follow, look for a suitable existing notebook by topic first, open a new one only if none fits, and show the owner which video goes to which notebook. Save each transcript to `raw/transcripts/<channel>/` with `nlm source content -o`. **No model rewrites, translates or shortens a transcript.** If a video has no transcript, mark it `unavailable` in the resume file (`--mark ... unavailable`) and show it to the owner in the list. Never invent a summary for it.

## Step 3b. Description links and chapter titles (code, no model)
For each chosen video fetch the description with a second pass (`--print "%(description)s"` in the same `yt_dlp` command as above) and let a script:
- extract the links into one `links` file, with the video title next to each link. Relevant ones go into the summary; researching a link is a separate job that you approve first;
- pull the chapter lines ("0:00 Intro", "2:14 Setup ...") into their own file. They are used to check that the summary's structure matches the video.
Optionally collect the most liked comments (they sometimes correct the video). Try this on one video first, and label what you get `[UNVERIFIED]`.

## Step 4. Summaries (labelled)
Ask NotebookLM, notebook by notebook, for: hook, main thesis, sections, tools and models, lessons, call to action, narrative patterns, and a step-by-step workflow if there is one. A NotebookLM summary is **not** verbatim: label it "NotebookLM summary".

NotebookLM reads speech only. Code, screens and tool UIs shown in a video are missing. For important videos you can ask a model that can watch video to fill the gap, and mark that part `[UNVERIFIED]` until you check it.

## Step 5. Resume file
`_processed.json` records each video id with a status: `added`, `transcript`, `summary`, `checked`, or `unavailable` (no transcript could be fetched). After each step the agent (or you) records it:
```powershell
python -I -X utf8 scripts/youtube_list.py --mark raw/transcripts/ChannelName VIDEO_ID transcript
```
The file is only as accurate as these marks: a video nobody marked is treated as new. If a quota limit or an error stops the job, list again: `incomplete.txt` shows the videos that have not reached `checked` or `unavailable` (continue those first) and `new_videos.txt` the ones never started. A later run on the same channel only handles those two lists.

## Step 6. Check, list, approve
Run the [quality chain](14-quality-chain.md). Then the agent shows:
- the videos and their groups (context clusters),
- the rules and workflows found,
- links found in descriptions (relevant ones only),
- anything that could not be processed,
- the check report.
Ask the one question: "Write these notes to the wiki?" Until the owner says yes, only `raw/` may be filled.

## Step 7. Write
After a yes:
```
wiki/sources/<channel>/            hub page for the channel + one card per video or cluster
wiki/lessons/<channel>/            one lesson page per cluster
wiki/rules/<channel>/              one rule page per cluster + a combined rules page
wiki/formulas/                     storytelling patterns (titles, hooks, calls to action) as patterns only
```
The hub page ("ball", in graph terms) links every page of the channel, so the graph shows a connected cluster. Check for overlap with existing rules before writing: link to the existing page instead of repeating it, and show contradictions to the owner separately.

Then update `INDEX.md`, append to `log.md`, add a graph color for the new folder, run the doctor.

## If a tool will not work
- Say so and stop. Do not invent a result.
- NotebookLM tool not connected: sign in again with its own login command (the Google sign-in is yours).
- Last resort: the agent can drive the website through a browser extension. It is slow and expensive, so the agent must ask you first.

## Things you do not do
- Do not let a model rewrite a transcript.
- Do not send private notes (privacy: private or internal) to an outside model.
- Do not import thumbnails or images; describe them.
- Do not copy a competitor's titles, hooks or signature metaphors. Learn the structure, write your own.
- Do not retry endlessly when a quota is hit; say so and stop.
