# Development and runtime environments

Status: accepted platform convention, 2026-08-27.

## The three environments

| Environment | Default shell and paths | What it proves |
| --- | --- | --- |
| Jakob's development computer | Windows, PowerShell 7, paths such as `C:\Users\jakob\...` | Local setup, Git, Node, Python, and Windows-specific maintenance. |
| Optional compatibility shell | Git Bash on the same Windows computer | Convenient Bash/POSIX syntax for local development; it is not a real Linux VM. |
| Product worker | Linux inside a Fly Sprite, Bash, paths such as `/workspace/...` | Actual agent execution, services, Tasks, checkpoints, and previews. |

GitHub Actions and deployment builds should use Linux unless a workflow is
explicitly testing Windows behavior. The site and runtime must therefore remain
portable even though day-to-day development happens on Windows.

## Command notation

Never paste one shell's syntax into another without translating it. Label every
non-trivial command by environment.

PowerShell on the Windows host:

```powershell
Set-Location 'C:\Users\jakob\Documents\ChatGPT\sajtagent-platform'
$env:EXAMPLE = 'value'
```

Git Bash on the Windows host:

```bash
cd /c/Users/jakob/Documents/ChatGPT/sajtagent-platform
export EXAMPLE=value
```

Bash inside a Linux Sprite:

```bash
cd /workspace/project
export EXAMPLE=value
```

Git Bash is optional. Prefer PowerShell for Windows administration and local
commands. Use Git Bash when a script is intentionally Bash-compatible or when
rehearsing Linux-like command syntax. A successful Git Bash run does not replace
a Linux CI or Sprite smoke test.

## Portable code rules

- Application code remains TypeScript/JavaScript or Python; "Windows" and
  "Linux" here primarily describe shells, paths, process entrypoints, and
  filesystem behavior.
- Use Node/Python path APIs instead of joining paths with literal `\\` or `/`.
- Never hard-code a Windows drive path in code that runs in a Sprite.
- Never assume `.cmd`, `cmd.exe`, or PowerShell exists inside the Sprite.
- Treat Linux paths as case-sensitive. Imports and filenames must match exact
  casing even if Windows accepts a mismatch.
- Bash scripts intended for Linux use `#!/usr/bin/env bash`, UTF-8 without BOM,
  LF endings, and an executable Git mode.
- PowerShell scripts intended only for the Windows host use `.ps1` and CRLF.
- Prefer a portable TypeScript or Python script when the same operation must run
  on both Windows and Linux.

## Encoding and line endings

Every repository contains `.editorconfig` and `.gitattributes`:

- shared source, documentation, configuration, and Linux/runtime files use
  UTF-8 without BOM and LF;
- Windows-only `.ps1`, `.cmd`, and `.bat` entrypoints use CRLF;
- Git normalizes tracked text so a Windows checkout cannot accidentally ship a
  CRLF Bash script to Linux.

Do not run a repository-wide line-ending rewrite as part of unrelated work.
Apply the policy to new or touched files and review any normalization diff
before committing.

## Required verification

For a cross-platform change, report the environments actually tested:

1. Windows/PowerShell for local setup and developer commands.
2. Linux CI for builds and portable scripts.
3. A disposable Sprite smoke test for Sprite-specific behavior once cloud
   creation is explicitly authorized.

Passing on Windows alone does not prove the Sprite path. Passing in Git Bash
alone does not prove Linux. Conversely, Linux-only instructions are incomplete
for the developer unless an equivalent PowerShell command or an explicitly
labeled Git Bash requirement is provided.
