<#
.SYNOPSIS
  Prove a backup works: unzip the newest archive into a temp folder,
  compare file counts with the live vault, and run the vault doctor on the copy.
  A backup you have never restored is only a hope.

.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File test-restore.ps1 `
    -Source "C:\path\to\MyVault" -Destination "D:\VaultBackups"
#>
param(
    [Parameter(Mandatory = $true)][string]$Source,
    [Parameter(Mandatory = $true)][string]$Destination
)
$ErrorActionPreference = 'Stop'

$name = Split-Path -Leaf $Source
$zip = Get-ChildItem -LiteralPath $Destination -Filter ("{0}_*.zip" -f $name) |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $zip) { throw "No archive found in $Destination" }

$tmp = Join-Path $env:TEMP ("restore_test_" + [guid]::NewGuid())
try {
    Expand-Archive -LiteralPath $zip.FullName -DestinationPath $tmp -Force
    $live = (Get-ChildItem -LiteralPath $Source -Recurse -File -Force).Count
    $copy = (Get-ChildItem -LiteralPath $tmp -Recurse -File -Force).Count
    Write-Output ("Archive : {0} ({1:N1} KB)" -f $zip.Name, ($zip.Length / 1KB))
    Write-Output ("Files   : live {0} | restored {1}" -f $live, $copy)
    if ($live -ne $copy) { Write-Warning "File counts differ. Files may have changed since the backup, or some were skipped." }

    $doctor = Join-Path $tmp 'tools\vault_doctor.py'
    if (Test-Path -LiteralPath $doctor) {
        Push-Location $tmp
        try { python -I -X utf8 tools/vault_doctor.py } finally { Pop-Location }
    } else {
        Write-Warning "tools\vault_doctor.py not found in the restored copy."
    }
}
finally {
    if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Recurse -Force }
}
