---
type: rule
scope: ["newsletter"]
source: "[[example-kitchen-channel]]"
updated: 2026-03-10
---
## Rule
1. Every recipe in the newsletter states how many pans and how many minutes.
2. A meal-prep recipe always names the day it was cooked and a "do not eat after day 4" note.

## Why
Readers said recipes with many pans were skipped (`[OWNER]`, 2026-03-10). The second rule comes from the meal prep video `[SOURCED]`.

## How to check it (code if possible)
Count the number of "pan" mentions and the minutes in each draft with a script; the agent only reads the result. Rule 2 is not measured by code yet: marked "not measured".
