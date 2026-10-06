[CmdletBinding()]
param([string]$GamePath, [switch]$PrepareOnly)
$ErrorActionPreference = 'Stop'
if (-not $PrepareOnly -and (Get-Process -Name eu5 -ErrorAction SilentlyContinue)) {
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
# Compact release: reconstruct native cache streams in the extracted package.
# Only reads the installed game; never writes to Steam.
$cmPatchRoot = Join-Path $PSScriptRoot 'terrain_patch'
if (-not (Test-Path -LiteralPath $cmPatchRoot)) { $cmPatchRoot = Join-Path $PSScriptRoot 'build\terrain_patch' }
$cmManifestPath = Join-Path $cmPatchRoot 'manifest.json'
if (Test-Path -LiteralPath $cmManifestPath) {
    $cmManifest = Get-Content -LiteralPath $cmManifestPath -Raw | ConvertFrom-Json
    $cmNeedsGame = @($cmManifest.files | Where-Object {
        $cmCacheTarget = Join-Path $cmSource $_.path
        -not (Test-Path -LiteralPath $cmCacheTarget) -or (Get-Item -LiteralPath $cmCacheTarget -ErrorAction SilentlyContinue).Length -ne $_.final_size
    }).Count -gt 0
    if ($cmNeedsGame) {
        $cmGameCandidates = [Collections.Generic.List[string]]::new()
        if ($GamePath) { $cmGameCandidates.Add($GamePath) }
        $cmSteamRoot = (Get-ItemProperty -LiteralPath 'HKCU:\Software\Valve\Steam' -ErrorAction SilentlyContinue).SteamPath
        if ($cmSteamRoot) {
            $cmGameCandidates.Add((Join-Path $cmSteamRoot 'steamapps\common\Europa Universalis V\game'))
            $cmVdf = Join-Path $cmSteamRoot 'steamapps\libraryfolders.vdf'
            if (Test-Path -LiteralPath $cmVdf) {
                foreach ($cmMatch in [regex]::Matches((Get-Content -LiteralPath $cmVdf -Raw), '"path"\s+"([^"]+)"')) {
                    $cmLibraryPath = $cmMatch.Groups[1].Value.Replace('\\','\')
                    $cmGameCandidates.Add((Join-Path $cmLibraryPath 'steamapps\common\Europa Universalis V\game'))
                }
            }
        }
        $cmGame = $cmGameCandidates | Where-Object { Test-Path -LiteralPath (Join-Path $_ 'in_game\gfx\terrain2\terrain_cache\heightmap.bin') } | Select-Object -First 1
        if (-not $cmGame) { throw 'Could not find EU5. Run again with -GamePath pointing to the installed Europa Universalis V\game folder.' }
        # Check all source caches before assembling any output.
        foreach ($cmEntry in $cmManifest.files) {
            $cmVanilla = Join-Path $cmGame $cmEntry.path
            if ((Get-Item -LiteralPath $cmVanilla).Length -ne $cmEntry.source_size -or (Get-FileHash -LiteralPath $cmVanilla -Algorithm SHA256).Hash -ne $cmEntry.source_sha256) {
                throw "EU5 terrain cache does not match this release: $($cmEntry.path). Rebuild for your game version."
            }
        }
        foreach ($cmEntry in $cmManifest.files) {
            $cmVanilla = Join-Path $cmGame $cmEntry.path
            $cmCacheTarget = [IO.Path]::GetFullPath((Join-Path $cmSource $cmEntry.path))
            $cmSourceResolved = [IO.Path]::GetFullPath($cmSource).TrimEnd('\') + '\'
            if (-not $cmCacheTarget.StartsWith($cmSourceResolved, [StringComparison]::OrdinalIgnoreCase)) { throw 'Invalid cache output path.' }
            Copy-Item -LiteralPath $cmVanilla -Destination $cmCacheTarget -Force
            $cmOutput = [IO.File]::Open($cmCacheTarget, [IO.FileMode]::Append, [IO.FileAccess]::Write)
            $cmDelta = [IO.File]::OpenRead((Join-Path $cmPatchRoot $cmEntry.delta))
            try { $cmDelta.CopyTo($cmOutput) } finally { $cmDelta.Dispose(); $cmOutput.Dispose() }
            if ((Get-Item -LiteralPath $cmCacheTarget).Length -ne $cmEntry.final_size) { throw 'Terrain reconstruction length mismatch.' }
            if ((Get-FileHash -LiteralPath $cmCacheTarget -Algorithm SHA256).Hash -ne $cmEntry.final_sha256) { throw 'Terrain reconstruction checksum mismatch.' }
        }
    }
}
if ($PrepareOnly) { Write-Host "Prepared Cindermaw at $cmSource"; return }
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
Write-Host 'Fully restart EU5, use a separate playset with only this mod, and start a NEW campaign. Verify population, capital city and close-up terrain.'
