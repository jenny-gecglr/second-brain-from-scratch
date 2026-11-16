---
type: lesson
date: 2026-03-08
scope: ["Windows PowerShell"]
---
## What happened
A helper function was named `rd`. In Windows PowerShell `rd` is an alias of `Remove-Item`, so calling it deleted pages instead of running the helper.

## Evidence
`[SOURCED]` pages were found empty and the doctor listed them under "Empty (0 byte) file" and "Broken wikilink".

## Result
Pages were restored from the backup zip (chapter 12 of the guide explains the backup).

## Which rule it became
Never name a function with an alias name. Give helpers long names. This is also chapter 13 of the guide.
