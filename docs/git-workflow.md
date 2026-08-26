# Git and worktree workflow

## Branch policy

`main` is the standard branch for every Sajtagent repository. A request that
mentions `master` is ambiguous and must be confirmed before an agent changes,
pushes, merges, deploys, or creates a worktree from that branch.

Every agent response that performs repository work ends with the live branch
and absolute worktree path for each repository touched. Local changes, commits,
pushes, pull requests, and deployments are reported as separate states.

## Safe automatic maintenance

`scripts/worktree-maintenance.ps1` performs a dry run by default. The scheduled
task invokes it weekly with `-Apply -MinimumAgeDays 14`.

The routine automatically prunes stale Git metadata and removes a linked
worktree only when all of these conditions are true:

- it is not the repository's primary worktree;
- it is at least 14 days old, clean, unlocked, and not running a process;
- its branch is neither `main` nor `master`;
- all commits are already contained in the latest `origin/main`;
- GitHub confirms that the branch has no open pull request.

If any check cannot be completed, the worktree is kept. Local branches are not
deleted automatically. Run a preview at any time:

```powershell
pwsh -File scripts/worktree-maintenance.ps1
```

Run the guarded cleanup manually:

```powershell
pwsh -File scripts/worktree-maintenance.ps1 -Apply -MinimumAgeDays 14
```

Install or refresh the weekly Sunday 03:00 task with:

```powershell
pwsh -File scripts/install-worktree-maintenance-task.ps1
```
