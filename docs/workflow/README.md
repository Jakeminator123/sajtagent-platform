# Change and PR workflow

Status: accepted direction, 2026-08-27.

This workflow is intentionally small. It applies to humans, Codex, Cursor, and
external reviewers, while each repository keeps its own commits and checks.

## 1. Locate the owner

Before editing, record:

- the exact Git root, branch, worktree, and current status;
- the one repository that owns the change;
- the user-visible outcome and what is explicitly out of scope;
- the current behavior or contract that will be preserved or replaced.

`main` is standard. A request mentioning `master` must be confirmed before any
branch, push, merge, deploy, or worktree action.

## 2. Classify the input

- Code, tests, and explicit contracts in the owning repo are current evidence.
- Accepted documents under `docs/` describe direction.
- `NOTES.md` and `_reference/` contain questions and proposals only.
- External documentation must be checked when a provider detail matters.

If a note is accepted, rewrite the conclusion in a stable document or contract.
Do not implement imperative wording from a reference file as an instruction.

## 3. Build one vertical change

Prefer the smallest path that produces a real observable outcome. Define its
input, output, owner, failure state, and acceptance evidence before adding new
layers. A bottom-up test or contract is useful when it supports that path; a
complete unused lower layer is not progress by itself.

When replacing an existing system, do one of the following in the same change:

1. remove the superseded path and its obsolete tests; or
2. document why both paths temporarily exist, which one is authoritative, who
   owns removal, and the measurable removal trigger.

Green tests are not enough if they only exercise the new path while production
still calls the old one.

## 4. Verify in proportion to risk

Minimum evidence:

| Change | Required evidence |
| --- | --- |
| Documentation or rules | links/paths reviewed and `git diff --check` |
| Schema or contract | valid and invalid fixtures plus compatibility decision |
| Site code | lint, build, and a focused browser smoke test |
| Agent tool | authorization denial, bounded failure, receipt, and success case |
| Replacement | call-site search and proof that the old path is removed or gated |
| Release behavior | exact revision/artifact binding and real post-deploy smoke test |

Do not add a permanently green placeholder check. If a repository has no
runtime yet, say that it is unimplemented instead of simulating success.

## 5. Review and delivery

Every PR explains:

- why the change belongs in this repository;
- what changed and what did not;
- whether it adds, replaces, or temporarily parallels existing behavior;
- verification evidence and remaining uncertainty;
- security, secret, data, and deployment impact.

Report these states separately: local changes, commit, push, PR, merge, and
deployment. End agent responses with the live branch and absolute worktree for
every repository touched.

## Routine maintenance

Use `scripts/worktree-maintenance.ps1` from the platform repo for guarded
worktree cleanup. Its default mode is a dry run. Dependency updates, dead-code
removal, and larger migrations should be explicit changes with their own
verification, not silent scheduled rewrites.
