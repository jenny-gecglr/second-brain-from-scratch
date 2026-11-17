<#
.SYNOPSIS
  Zip a vault into a dated archive and delete archives older than N days.

.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File backup-vault.ps1 `
    -Source "C:\path\to\MyVault" -Destination "D:\VaultBackups" -KeepDays 30

  Works with any destination folder, including a cloud-synced one
  (Google Drive for desktop, OneDrive, Dropbox) so the backup leaves this PC.
#>
param(
    [Parameter(Mandatory = $true)][string]$Source,
    [Parameter(Mandatory = $true)][string]$Destination,
    [int]$KeepDays = 30,
    [string]$LogFile = (Join-Path $env:LOCALAPPDATA 'vault-backup.log')
)
$ErrorActionPreference = 'Stop'

try {
    if (-not (Test-Path -LiteralPath $Source)) { throw "Source not found: $Source" }
    $destRoot = Split-Path -Qualifier $Destination -ErrorAction SilentlyContinue
    if ($destRoot -and -not (Test-Path -LiteralPath $destRoot)) {
        throw "Destination drive not found: $destRoot (is the sync app running?)"
    }
    if (-not (Test-Path -LiteralPath $Destination)) { New-Item -ItemType Directory -Path $Destination | Out-Null }

    $name = Split-Path -Leaf $Source
    $zip  = Join-Path $Destination ("{0}_{1}.zip" -f $name, (Get-Date -Format 'yyyy-MM-dd'))
    $tmp  = Join-Path $env:TEMP ("{0}_{1}.zip" -f $name, [guid]::NewGuid())

    # Build the archive in TEMP first, so a half-written zip never replaces a good one.
    # .NET zip ignores file attributes, so hidden files (desktop.ini, .obsidian) are included too.
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [IO.Compression.ZipFile]::CreateFromDirectory($Source, $tmp, [IO.Compression.CompressionLevel]::Optimal, $false)
    Move-Item -LiteralPath $tmp -Destination $zip -Force

    Get-ChildItem -LiteralPath $Destination -Filter ("{0}_*.zip" -f $name) |
        Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$KeepDays) } |
        Remove-Item -Force

    Add-Content -LiteralPath $LogFile ("{0}  OK  {1}" -f (Get-Date -Format 's'), $zip)
    Write-Output "Backup OK: $zip"
}
catch {
    Add-Content -LiteralPath $LogFile ("{0}  ERROR  {1}" -f (Get-Date -Format 's'), $_.Exception.Message)
    throw
}
