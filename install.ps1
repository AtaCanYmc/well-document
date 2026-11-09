<#
.SYNOPSIS
    well-document skill installer for Windows PowerShell and PowerShell Core.
.DESCRIPTION
    Installs well-document into supported AI agent skill directories on Windows.
.PARAMETER Target
    Custom destination path or agent flag (--antigravity, --claude, --cursor, --codex, --all).
.PARAMETER Antigravity
    Install to Google Antigravity / Gemini skill directory.
.PARAMETER Claude
    Install to Claude Code skill directory.
.PARAMETER Cursor
    Install to Cursor skill directory.
.PARAMETER Codex
    Install to OpenAI Codex skill directory.
.PARAMETER All
    Install to all detected AI agent directories.
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Target,
    [Alias("gemini")]
    [switch]$Antigravity,
    [switch]$Claude,
    [switch]$Codex,
    [switch]$Cursor,
    [switch]$All
)

$ErrorActionPreference = 'Stop'

Write-Host "==> well-document: AI Coding Assistant Skill Installer"

# Normalize CLI arguments if passed as flags in $Target
if ($Target) {
    switch ($Target.ToLowerInvariant()) {
        { $_ -in @("-antigravity", "--antigravity", "-gemini", "--gemini") } { $Antigravity = $true; $Target = $null }
        { $_ -in @("-claude", "--claude") } { $Claude = $true; $Target = $null }
        { $_ -in @("-codex", "--codex") } { $Codex = $true; $Target = $null }
        { $_ -in @("-cursor", "--cursor") } { $Cursor = $true; $Target = $null }
        { $_ -in @("-all", "--all") } { $All = $true; $Target = $null }
    }
}

# Determine source directory
$RepoDir = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
$SrcDir = Join-Path $RepoDir "skills\well-document"
$cleanupTemp = $null

if (-not (Test-Path -LiteralPath (Join-Path $SrcDir "SKILL.md"))) {
    Write-Host "==> Local skill files not found, downloading from repository..."
    $tempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("well-document-" + [System.IO.Path]::GetRandomFileName())
    $zipPath = Join-Path ([System.IO.Path]::GetTempPath()) ("well-document-" + [System.IO.Path]::GetRandomFileName() + ".zip")
    $cleanupTemp = @($tempDir, $zipPath)
    try {
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor [System.Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri "https://github.com/AtaCanYmc/well-document/archive/refs/heads/main.zip" -OutFile $zipPath -UseBasicParsing
        Expand-Archive -LiteralPath $zipPath -DestinationPath $tempDir -Force
        $SrcDir = Join-Path $tempDir "well-document-main\skills\well-document"
    }
    catch {
        Write-Error "Failed to download skill files: $_"
        return
    }
}

function Install-To {
    param(
        [string]$Dest,
        [string]$Name
    )
    Write-Host "==> Installing for ${Name}: $Dest"
    $refDest = Join-Path $Dest "references"
    if (-not (Test-Path -LiteralPath $refDest)) {
        New-Item -ItemType Directory -Path $refDest -Force | Out-Null
    }
    Copy-Item -LiteralPath (Join-Path $SrcDir "SKILL.md") -Destination (Join-Path $Dest "SKILL.md") -Force
    $refDir = Join-Path $SrcDir "references"
    $refFiles = Get-ChildItem -LiteralPath $refDir -Filter "*.md"
    foreach ($file in $refFiles) {
        Copy-Item -LiteralPath $file.FullName -Destination (Join-Path $refDest $file.Name) -Force
    }
}

$HomeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
$GeminiPath  = Join-Path $HomeDir ".gemini\antigravity\skills\well-document"
$ClaudePath  = Join-Path $HomeDir ".claude\skills\well-document"
$CursorPath  = Join-Path $HomeDir ".cursor\skills\well-document"
$CodexPath   = Join-Path $HomeDir ".codex\skills\well-document"
$DefaultPath = Join-Path $HomeDir ".skills\well-document"

try {
    if ($All) {
        Install-To -Dest $GeminiPath -Name "Google Antigravity / Gemini"
        Install-To -Dest $ClaudePath -Name "Claude Code"
        Install-To -Dest $CursorPath -Name "Cursor"
        Install-To -Dest $CodexPath  -Name "OpenAI Codex"
    }
    elseif ($Antigravity) {
        Install-To -Dest $GeminiPath -Name "Google Antigravity / Gemini"
    }
    elseif ($Claude) {
        Install-To -Dest $ClaudePath -Name "Claude Code"
    }
    elseif ($Cursor) {
        Install-To -Dest $CursorPath -Name "Cursor"
    }
    elseif ($Codex) {
        Install-To -Dest $CodexPath  -Name "OpenAI Codex"
    }
    elseif ($Target) {
        Install-To -Dest $Target -Name "Custom path"
    }
    else {
        # Auto-detect existing environments or fallback to default
        $installed = $false
        if (Test-Path -LiteralPath (Join-Path $HomeDir ".gemini")) {
            Install-To -Dest $GeminiPath -Name "Google Antigravity / Gemini"
            $installed = $true
        }
        if (Test-Path -LiteralPath (Join-Path $HomeDir ".claude")) {
            Install-To -Dest $ClaudePath -Name "Claude Code"
            $installed = $true
        }
        if (Test-Path -LiteralPath (Join-Path $HomeDir ".cursor")) {
            Install-To -Dest $CursorPath -Name "Cursor"
            $installed = $true
        }
        if (Test-Path -LiteralPath (Join-Path $HomeDir ".codex")) {
            Install-To -Dest $CodexPath -Name "OpenAI Codex"
            $installed = $true
        }

        if (-not $installed) {
            Install-To -Dest $DefaultPath -Name "Default Agent Directory"
        }
    }

    Write-Host "==> Installation complete. Skill active. Invoke with: well-document"
}
finally {
    if ($cleanupTemp) {
        foreach ($item in $cleanupTemp) {
            if (Test-Path -LiteralPath $item) {
                Remove-Item -LiteralPath $item -Recurse -Force -ErrorAction SilentlyContinue
            }
        }
    }
}
