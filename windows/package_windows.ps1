<#
.SYNOPSIS
  Build and package FilmCraft TH (Thai localized) for Windows 11 / 10.

.DESCRIPTION
  Produces in dist/thai (and optionally windows/):
    FilmCraft-TH-<version>-windows-<arch>-portable.zip  (Portable version: exe + cli + thai catalog)
    FilmCraft-TH-<version>-windows-<arch>.msi           (Windows Installer via WiX v5, if available)

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File windows/package_windows.ps1
  powershell -ExecutionPolicy Bypass -File windows/package_windows.ps1 -SkipBuild
#>
param(
  [ValidateSet('x64', 'x86', 'arm64')] [string] $Arch = 'x64',
  [switch] $SkipBuild
)

$ErrorActionPreference = 'Stop'
$SearchDir = $PSScriptRoot
while ($SearchDir -and -not (Test-Path (Join-Path $SearchDir 'Cargo.toml'))) {
  $SearchDir = Split-Path $SearchDir -Parent
}
if (-not $SearchDir) { throw "Could not locate repository root (Cargo.toml)" }
$Root = $SearchDir

$Version = '0.17.0-th.1'
$MsiVersion = '0.17.0'

$Dist = Join-Path $Root 'dist\thai'
$TargetDir = if ($env:CARGO_TARGET_DIR) { $env:CARGO_TARGET_DIR } else { Join-Path $Root 'target' }
New-Item -ItemType Directory -Force -Path $Dist | Out-Null

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " Building FilmCraft TH $Version for Windows $Arch" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Validate Thai catalog
Write-Host "==> Validating Thai catalog..." -ForegroundColor Yellow
& python (Join-Path $Root 'tools\thai\validate_catalog.py')
if ($LASTEXITCODE -ne 0) { throw "Thai catalog validation failed" }

# 2. Build binaries if requested
$BinDir = Join-Path $TargetDir 'release'
if (-not $SkipBuild) {
  Write-Host "==> Compiling FilmCraft (release)..." -ForegroundColor Yellow
  cargo build --release --locked -p filmcraft -p filmcraft-cli
  if ($LASTEXITCODE -ne 0) { throw "cargo build failed" }
}

$FilmcraftExe = Join-Path $BinDir 'filmcraft.exe'
$FilmcraftCliExe = Join-Path $BinDir 'filmcraft-cli.exe'

if (-not (Test-Path $FilmcraftExe)) {
  throw "Binary not found at $FilmcraftExe"
}

# 3. Create Portable Package
$PackageName = "FilmCraft-TH-$Version-windows-$Arch-portable"
$StageDir = Join-Path $TargetDir "windows-package\$PackageName"
Remove-Item -Recurse -Force $StageDir -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $StageDir | Out-Null

Copy-Item $FilmcraftExe, $FilmcraftCliExe $StageDir

Set-Content -Encoding ascii -Path (Join-Path $StageDir 'portable.txt') -Value @(
  'FilmCraft TH portable: preferences, presets, logs and crash recovery are kept in the data folder'
  'next to filmcraft.exe. Delete this file to use %APPDATA%\FilmCraft instead.'
)

foreach ($doc in 'README.md', 'LICENSE', 'NOTICE', 'LICENSE-MIT', 'LICENSE-APACHE') {
  $p = Join-Path $Root $doc
  if (Test-Path $p) { Copy-Item $p $StageDir }
}

$ZipPath = Join-Path $Dist "$PackageName.zip"
Remove-Item -Force $ZipPath -ErrorAction SilentlyContinue
Write-Host "==> Creating portable zip: $ZipPath" -ForegroundColor Yellow
Compress-Archive -Path "$StageDir\*" -DestinationPath $ZipPath

# 4. Create MSI Installer if WiX is available
$WixCmd = Get-Command wix -ErrorAction SilentlyContinue
if ($WixCmd) {
  Write-Host "==> Building Windows Installer (.msi) via WiX..." -ForegroundColor Yellow
  $MsiPath = Join-Path $Dist "FilmCraft-TH-$Version-windows-$Arch.msi"
  $DocsDir = Join-Path $StageDir 'font-licences'
  New-Item -ItemType Directory -Force -Path $DocsDir | Out-Null

  $wxsPath = Join-Path $Root 'packaging\windows\filmcraft.wxs'
  if (Test-Path $wxsPath) {
    try {
      wix build $wxsPath -arch $Arch -ext WixToolset.UI.wixext `
        -d "Version=$MsiVersion" -d "BinDir=$StageDir" -d "IconPath=$(Join-Path $Root 'assets\app-icon\filmcraft.ico')" `
        -d "DocsDir=$DocsDir" -d "HasCraftFontLicences=0" `
        -o $MsiPath
      Remove-Item -Force -ErrorAction SilentlyContinue ([IO.Path]::ChangeExtension($MsiPath, '.wixpdb'))
      Write-Host "==> Created MSI: $MsiPath" -ForegroundColor Green
    } catch {
      Write-Warning "WiX build skipped or failed: $_"
    }
  }
} else {
  Write-Host "==> WiX v5 not found; skipping MSI installer generation." -ForegroundColor Gray
}

Write-Host "==========================================" -ForegroundColor Green
Write-Host " Build and Packaging Complete!" -ForegroundColor Green
Write-Host " Output files in: $Dist" -ForegroundColor Green
Get-ChildItem -Path $Dist | Format-Table Name, Length, LastWriteTime
