<#
.SYNOPSIS
    Syncs canonical workspace skills from .agents/skills/ to Claude Code and/or user-global agent skill directories.

.DESCRIPTION
    Mirrors or links each skill folder (containing SKILL.md) from <repo>/.agents/skills/ into:
      - Project scope (default): <repo>/.claude/skills/
      - Global scope (-Global):  ~/.claude/skills/, ~/.agents/skills/, ~/.codex/skills/

    Operates per-skill so existing unrelated skills in global directories are preserved.

.PARAMETER Global
    Sync into user-global skill directories (~/.claude/skills, ~/.agents/skills, ~/.codex/skills)
    instead of project-local .claude/skills/.

.PARAMETER Target
    Filter target directories. Valid values: auto, claude, agents, codex, all.
    Default is 'auto' ('claude' for project scope; 'all' for -Global).

.PARAMETER Mode
    Link/copy strategy: auto (junction -> symlink -> copy), junction, symlink, or copy.
    Default is 'auto' (uses directory junctions on Windows, which require no Admin/Developer Mode).

.PARAMETER Force
    Overwrite existing skill entries in target directories if they already exist.

.PARAMETER Clean
    Remove only skill entries in target directories whose names match .agents/skills/*.

.PARAMETER DryRun
    Preview planned actions without creating, modifying, or deleting anything on disk.

.EXAMPLE
    .\scripts\sync-skills.ps1
    Links .agents/skills/* into .claude/skills/* for Claude Code in this repository.

.EXAMPLE
    .\scripts\sync-skills.ps1 -Global -DryRun
    Previews syncing all 47 skills to ~/.claude/skills, ~/.agents/skills, and ~/.codex/skills.

.EXAMPLE
    .\scripts\sync-skills.ps1 -Mode copy -Force
    Copies all skills into .claude/skills/, replacing any existing copies.
#>
[CmdletBinding()]
param(
    [switch]$Global,

    [ValidateSet('auto', 'claude', 'agents', 'codex', 'all')]
    [string]$Target = 'auto',

    [ValidateSet('auto', 'junction', 'symlink', 'copy')]
    [string]$Mode = 'auto',

    [switch]$Force,
    [switch]$Clean,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$SourceDir = Join-Path $RepoRoot '.agents\skills'

if (-not (Test-Path -LiteralPath $SourceDir -PathType Container)) {
    throw "Source skills directory not found: $SourceDir"
}

$Skills = @(
    Get-ChildItem -LiteralPath $SourceDir -Directory |
    Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md') -PathType Leaf } |
    Sort-Object Name
)

if ($Skills.Count -eq 0) {
    throw "No skills (folders containing SKILL.md) found in: $SourceDir"
}

$HomeDir = [Environment]::GetFolderPath('UserProfile')
if (-not $HomeDir) { $HomeDir = $HOME }

$DestDirs = @()
if ($Global) {
    $effectiveTargets = if ($Target -in @('auto', 'all')) { @('claude', 'agents', 'codex') } else { @($Target) }
    foreach ($t in $effectiveTargets) {
        switch ($t) {
            'claude' { $DestDirs += Join-Path $HomeDir '.claude\skills' }
            'agents' { $DestDirs += Join-Path $HomeDir '.agents\skills' }
            'codex'  { $DestDirs += Join-Path $HomeDir '.codex\skills' }
        }
    }
} else {
    $effectiveTargets = if ($Target -eq 'auto') { @('claude') } elseif ($Target -eq 'all') { @('claude', 'codex') } else { @($Target) }
    foreach ($t in $effectiveTargets) {
        switch ($t) {
            'claude' { $DestDirs += Join-Path $RepoRoot '.claude\skills' }
            'codex'  { $DestDirs += Join-Path $RepoRoot '.codex\skills' }
            'agents' { Write-Warning "Project target 'agents' is already the canonical source ($SourceDir); skipping." }
        }
    }
}

if ($DestDirs.Count -eq 0) {
    Write-Output "No target directories selected. Nothing to do."
    exit 0
}

function Remove-ExistingEntry {
    param([string]$Path)
    $item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    if (-not $item) { return }
    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
        # Remove junction/symlink itself without recursing into link target
        [System.IO.Directory]::Delete($Path, $false)
    } else {
        Remove-Item -LiteralPath $Path -Recurse -Force
    }
}

$ScopeLabel = if ($Global) { 'global' } else { 'project' }
$ActionLabel = if ($Clean) { 'clean' } else { "sync ($Mode)" }
Write-Output "Source: $SourceDir ($($Skills.Count) skills)"
Write-Output "Scope:  $ScopeLabel | Action: $ActionLabel$(if ($DryRun) { ' [DRY-RUN]' })"

foreach ($destRoot in $DestDirs) {
    $created = 0
    $skipped = 0
    $removed = 0
    $fallbackCopies = 0

    Write-Output ""
    Write-Output "Target: $destRoot"

    if ($Clean) {
        if (-not (Test-Path -LiteralPath $destRoot -PathType Container)) {
            Write-Output "  (not present; nothing to clean)"
            continue
        }
        foreach ($skill in $Skills) {
            $dst = Join-Path $destRoot $skill.Name
            if (Test-Path -LiteralPath $dst) {
                if ($DryRun) {
                    Write-Output "  [dry-run] remove $dst"
                } else {
                    Remove-ExistingEntry -Path $dst
                }
                $removed++
            }
        }
        Write-Output "  Cleaned: $removed skill(s)"
        continue
    }

    if (-not (Test-Path -LiteralPath $destRoot -PathType Container)) {
        if ($DryRun) {
            Write-Output "  [dry-run] mkdir $destRoot"
        } else {
            New-Item -ItemType Directory -Path $destRoot -Force | Out-Null
        }
    }

    foreach ($skill in $Skills) {
        $src = $skill.FullName
        $dst = Join-Path $destRoot $skill.Name

        if ([string]::Equals($src, $dst, [StringComparison]::OrdinalIgnoreCase)) {
            $skipped++
            continue
        }

        if (Test-Path -LiteralPath $dst) {
            if (-not $Force) {
                $skipped++
                continue
            }
            if (-not $DryRun) {
                Remove-ExistingEntry -Path $dst
            }
        }

        if ($DryRun) {
            $created++
            continue
        }

        switch ($Mode) {
            'junction' {
                New-Item -ItemType Junction -Path $dst -Target $src | Out-Null
                $created++
            }
            'symlink' {
                New-Item -ItemType SymbolicLink -Path $dst -Target $src | Out-Null
                $created++
            }
            'copy' {
                Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
                $created++
            }
            'auto' {
                try {
                    New-Item -ItemType Junction -Path $dst -Target $src | Out-Null
                    $created++
                } catch {
                    try {
                        New-Item -ItemType SymbolicLink -Path $dst -Target $src | Out-Null
                        $created++
                    } catch {
                        Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
                        $created++
                        $fallbackCopies++
                    }
                }
            }
        }
    }

    if ($DryRun) {
        Write-Output "  [dry-run] would sync: $created | already present (skip; use -Force to replace): $skipped"
    } else {
        $extra = if ($fallbackCopies -gt 0) { " ($fallbackCopies copied via fallback)" } else { '' }
        Write-Output "  Synced: $created$extra | Skipped (already present): $skipped"
    }
}
