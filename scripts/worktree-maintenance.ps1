[CmdletBinding()]
param(
    [switch]$Apply,
    [ValidateRange(1, 3650)]
    [int]$MinimumAgeDays = 14,
    [string[]]$RepositoryPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$platformRoot = Split-Path -Parent $PSScriptRoot
if (-not $RepositoryPath) {
    $RepositoryPath = @(
        $platformRoot,
        (Join-Path $platformRoot 'sajtagent-site'),
        (Join-Path $platformRoot 'sajtagent-sprites')
    )
}

function Invoke-Git {
    param(
        [Parameter(Mandatory)] [string]$Repository,
        [Parameter(Mandatory)] [string[]]$Arguments
    )

    $output = @(& git -C $Repository @Arguments 2>&1)
    $exitCode = $LASTEXITCODE
    [pscustomobject]@{ ExitCode = $exitCode; Output = $output }
}

function Get-NormalizedPath {
    param([Parameter(Mandatory)] [string]$Path)

    [IO.Path]::GetFullPath($Path).TrimEnd(
        [IO.Path]::DirectorySeparatorChar,
        [IO.Path]::AltDirectorySeparatorChar
    )
}

function Get-WorktreeRecords {
    param([Parameter(Mandatory)] [string]$Repository)

    $result = Invoke-Git -Repository $Repository -Arguments @('worktree', 'list', '--porcelain')
    if ($result.ExitCode -ne 0) {
        throw "Could not list worktrees for ${Repository}: $($result.Output -join [Environment]::NewLine)"
    }

    $records = @()
    $record = @{}
    foreach ($line in @($result.Output) + '') {
        if ([string]::IsNullOrWhiteSpace($line)) {
            if ($record.ContainsKey('worktree')) {
                $records += [pscustomobject]@{
                    Path     = [string]$record.worktree
                    Head     = [string]$record.HEAD
                    Branch   = [string]$record.branch
                    Locked   = $record.ContainsKey('locked')
                    Prunable = $record.ContainsKey('prunable')
                }
            }
            $record = @{}
            continue
        }

        $parts = $line -split ' ', 2
        $record[$parts[0]] = if ($parts.Count -gt 1) { $parts[1] } else { $true }
    }

    $records
}

function Get-GitHubSlug {
    param([Parameter(Mandatory)] [string]$RemoteUrl)

    if ($RemoteUrl -match '^(?:git@github\.com:|https://github\.com/)([^/]+/[^/]+?)(?:\.git)?$') {
        return $Matches[1]
    }
    $null
}

$cutoff = (Get-Date).ToUniversalTime().AddDays(-$MinimumAgeDays)
$candidateCount = 0
$removedCount = 0

foreach ($requestedPath in $RepositoryPath) {
    if (-not (Test-Path -LiteralPath $requestedPath -PathType Container)) {
        Write-Warning "Repository path does not exist: $requestedPath"
        continue
    }

    $topLevel = Invoke-Git -Repository $requestedPath -Arguments @('rev-parse', '--show-toplevel')
    if ($topLevel.ExitCode -ne 0) {
        Write-Warning "Not a Git repository: $requestedPath"
        continue
    }

    $repository = Get-NormalizedPath -Path ([string]$topLevel.Output[0])
    Write-Host "Checking $repository"

    $pruneArgs = if ($Apply) {
        @('worktree', 'prune', '--verbose')
    } else {
        @('worktree', 'prune', '--dry-run', '--verbose')
    }
    $prune = Invoke-Git -Repository $repository -Arguments $pruneArgs
    if ($prune.Output.Count -gt 0) {
        $prune.Output | ForEach-Object { Write-Host "  $_" }
    }

    $remote = Invoke-Git -Repository $repository -Arguments @('remote', 'get-url', 'origin')
    $githubSlug = if ($remote.ExitCode -eq 0) {
        Get-GitHubSlug -RemoteUrl ([string]$remote.Output[0])
    } else {
        $null
    }
    if (-not $githubSlug) {
        Write-Host '  Keeping linked worktrees: no supported GitHub origin.'
        continue
    }

    $fetch = Invoke-Git -Repository $repository -Arguments @('fetch', '--prune', 'origin')
    if ($fetch.ExitCode -ne 0) {
        Write-Host '  Keeping linked worktrees: origin could not be refreshed.'
        continue
    }

    $remoteMain = Invoke-Git -Repository $repository -Arguments @('rev-parse', '--verify', 'refs/remotes/origin/main')
    if ($remoteMain.ExitCode -ne 0) {
        Write-Host '  Keeping linked worktrees: origin/main is unavailable.'
        continue
    }

    foreach ($worktree in Get-WorktreeRecords -Repository $repository) {
        $worktreePath = Get-NormalizedPath -Path $worktree.Path
        if ($worktreePath -eq $repository -or $worktree.Prunable) {
            continue
        }
        if ($worktree.Locked -or -not (Test-Path -LiteralPath $worktreePath -PathType Container)) {
            Write-Host "  Keeping ${worktreePath}: locked or unavailable."
            continue
        }
        if (-not $worktree.Branch.StartsWith('refs/heads/')) {
            Write-Host "  Keeping ${worktreePath}: detached HEAD."
            continue
        }

        $branchName = $worktree.Branch.Substring('refs/heads/'.Length)
        if ($branchName -in @('main', 'master')) {
            Write-Host "  Keeping ${worktreePath}: protected branch $branchName."
            continue
        }

        $lastWrite = (Get-Item -LiteralPath $worktreePath).LastWriteTimeUtc
        if ($lastWrite -gt $cutoff) {
            Write-Host "  Keeping ${worktreePath}: newer than $MinimumAgeDays days."
            continue
        }

        $status = Invoke-Git -Repository $worktreePath -Arguments @('status', '--porcelain=v1', '--untracked-files=all')
        if ($status.ExitCode -ne 0 -or $status.Output.Count -gt 0) {
            Write-Host "  Keeping ${worktreePath}: working tree is not clean."
            continue
        }

        $merged = Invoke-Git -Repository $repository -Arguments @(
            'merge-base', '--is-ancestor', $worktree.Head, 'refs/remotes/origin/main'
        )
        if ($merged.ExitCode -ne 0) {
            Write-Host "  Keeping ${worktreePath}: commits are not all in origin/main."
            continue
        }

        $openPrJson = @(& gh pr list --repo $githubSlug --head $branchName --state open --limit 1 --json number 2>&1)
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  Keeping ${worktreePath}: GitHub PR state could not be verified."
            continue
        }
        $openPrs = @($openPrJson -join [Environment]::NewLine | ConvertFrom-Json)
        if ($openPrs.Count -gt 0) {
            Write-Host "  Keeping ${worktreePath}: branch has an open pull request."
            continue
        }

        $escapedPath = [Regex]::Escape($worktreePath) -replace '\\\\', '[\\\\/]'
        $activeProcesses = @(Get-CimInstance Win32_Process -ErrorAction Stop | Where-Object {
            $_.ProcessId -ne $PID -and $_.CommandLine -match $escapedPath
        })
        if ($activeProcesses.Count -gt 0) {
            Write-Host "  Keeping ${worktreePath}: an active process references it."
            continue
        }

        $candidateCount++
        if (-not $Apply) {
            Write-Host "  Candidate: $worktreePath ($branchName)."
            continue
        }

        $remove = Invoke-Git -Repository $repository -Arguments @('worktree', 'remove', '--', $worktreePath)
        if ($remove.ExitCode -eq 0) {
            $removedCount++
            Write-Host "  Removed: $worktreePath ($branchName)."
        } else {
            Write-Warning "Git refused to remove $worktreePath; it was kept."
        }
    }
}

if ($Apply) {
    Write-Host "Maintenance complete. Removed $removedCount of $candidateCount safe candidates."
} else {
    Write-Host "Dry run complete. Found $candidateCount safe candidates; nothing was removed."
}
