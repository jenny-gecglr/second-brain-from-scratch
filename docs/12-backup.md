# 12. Backup and restore

Your vault is plain files, so backup is easy. The part people skip is proving the backup can be restored.

## What to protect against
| Risk | Example | Protection |
|---|---|---|
| Accidental deletion or overwrite | an agent or a shell alias deletes pages | daily dated zips, kept 30 days |
| Disk failure or lost PC | | the zip is stored in a cloud-synced folder, not only on the disk |
| Silent damage | a file turns empty or changes unnoticed | the doctor (empty files, and raw files that changed since your last `--snapshot`) |

Run the commands below from the **vault root**, after copying the `scripts` folder into the vault (see [01](01-setup-from-zero.md), step 4). If a path contains spaces, wrap it in quotes (in the `schtasks` line use `\"` around such paths).

## Step 1. Pick a destination that leaves this PC
A folder inside Google Drive for desktop, OneDrive or Dropbox. The script writes a normal zip to that folder and the sync app uploads it. Check that the sync app is running.

## Step 2. Run the script once by hand
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\backup-vault.ps1 `
  -Source "C:\Users\YOU\Documents\MyVault" -Destination "D:\VaultBackups" -KeepDays 30
```
It builds the zip in the temp folder first and only then moves it to the destination, so a half-written zip never replaces a good one. It deletes archives of this vault older than `-KeepDays`. It writes a one-line log to `%LOCALAPPDATA%\vault-backup.log` (success or error).

Note: `Compress-Archive` can fail on very large vaults (a single archive over about 2 GB) or on files another program has locked. If that happens, close Obsidian and retry, or use another zip tool.

## Step 3. Test the restore (do this once, then monthly)
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\test-restore.ps1 `
  -Source "C:\Users\YOU\Documents\MyVault" -Destination "D:\VaultBackups"
```
It unzips the newest archive to a temp folder, compares file counts with the live vault and runs the doctor on the copy, then deletes the copy. If counts differ a little (you edited since the backup) that is fine; large differences are not.

## Step 4. Schedule it (daily at 21:00)
```powershell
schtasks /Create /SC DAILY /ST 21:00 /TN "VaultBackup" /TR "powershell -NoProfile -ExecutionPolicy Bypass -File C:\path\to\scripts\backup-vault.ps1 -Source C:\path\to\MyVault -Destination D:\VaultBackups"
```
Check it exists with `schtasks /Query /TN "VaultBackup"`. Remove it with `schtasks /Delete /TN "VaultBackup" /F`. The task runs only when the PC is on; if your PC is usually off at 21:00, pick a time when it is on. Look at `vault-backup.log` now and then to see that runs succeed.

## Restoring
1. Close Obsidian.
2. Unzip the archive you want into a **new** folder (do not unzip over your live vault).
3. Open the new folder in Obsidian, run the doctor, compare, then copy back only what you need.

## What the backup does not cover
- Things stored outside the vault (your Drive originals, raw exports you kept elsewhere).
- Tool settings and logins (agent configuration, sign-ins). Keep a short note of what you installed, in `wiki/tools/`, so a new PC can be rebuilt from this repo's setup guide.
- Never change the backup script or its schedule without telling yourself why; write the reason in a decision page.
