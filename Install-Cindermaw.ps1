[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
if (Get-Process -Name eu5 -ErrorAction SilentlyContinue) {
    throw 'Close Europa Universalis V before installing this demo.'
}
$cmSource = Join-Path $PSScriptRoot 'cindermaw_demo'
if (-not (Test-Path -LiteralPath $cmSource)) {
    $cmSource = Join-Path $PSScriptRoot 'build\cindermaw_demo'
}
$cmMetadataPath = Join-Path $cmSource '.metadata\metadata.json'
if (-not (Test-Path -LiteralPath $cmMetadataPath)) { throw 'Cannot find the built Cindermaw mod next to this installer.' }
$cmMetadata = Get-Content -LiteralPath $cmMetadataPath -Raw | ConvertFrom-Json
if ($cmMetadata.id -ne 'alex.cindermaw_demo') { throw 'Unexpected source mod ID; installation stopped.' }
$cmDocuments = [Environment]::GetFolderPath('MyDocuments')
if ([string]::IsNullOrWhiteSpace($cmDocuments)) { throw 'Windows did not return a Documents folder.' }
$cmModRoot = [IO.Path]::GetFullPath((Join-Path $cmDocuments 'Paradox Interactive\Europa Universalis V\mod'))
$cmTarget = [IO.Path]::GetFullPath((Join-Path $cmModRoot 'cindermaw_demo'))
if ([IO.Path]::GetDirectoryName($cmTarget) -ne $cmModRoot) { throw 'Invalid installation target.' }
if (Test-Path -LiteralPath $cmModRoot) {
    if ((Get-Item -LiteralPath $cmModRoot).Attributes -band [IO.FileAttributes]::ReparsePoint) {
        throw 'The mod folder is a link; use manual installation into its intended destination.'
    }
}
New-Item -ItemType Directory -Path $cmModRoot -Force | Out-Null
if (Test-Path -LiteralPath $cmTarget) {
    if ((Get-Item -LiteralPath $cmTarget).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'The existing target is a link; installation stopped.' }
    $cmOldMeta = Join-Path $cmTarget '.metadata\metadata.json'
    if (-not (Test-Path -LiteralPath $cmOldMeta)) { throw 'Existing folder has no Cindermaw metadata; installation stopped.' }
    if ((Get-Content -LiteralPath $cmOldMeta -Raw | ConvertFrom-Json).id -ne 'alex.cindermaw_demo') { throw 'Existing folder belongs to another mod; installation stopped.' }
    # Backups are outside the mod scan directory so they cannot appear as duplicate mods.
    $cmBackupRoot = [IO.Path]::GetFullPath((Join-Path $cmDocuments 'Paradox Interactive\Europa Universalis V\cindermaw_backups'))
    New-Item -ItemType Directory -Path $cmBackupRoot -Force | Out-Null
    $cmBackup = [IO.Path]::GetFullPath((Join-Path $cmBackupRoot ('cindermaw_demo_' + (Get-Date -Format 'yyyyMMdd_HHmmss_fff'))))
    if ([IO.Path]::GetDirectoryName($cmBackup) -ne $cmBackupRoot) { throw 'Invalid backup target.' }
    Move-Item -LiteralPath $cmTarget -Destination $cmBackup
    Write-Host "Previous Cindermaw preserved at $cmBackup"
}
Copy-Item -LiteralPath $cmSource -Destination $cmTarget -Recurse
Write-Host "Installed Cindermaw development demo at $cmTarget"
Write-Host 'Use a separate playset with only this mod and start a new campaign. Runtime/terrain verification is still required.'
