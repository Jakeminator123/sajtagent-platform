# Documentation index

Documents under this folder record accepted platform direction. They are more
authoritative than working notes, but executable code, tests, and contracts in
the repository that owns a feature remain the strongest source of truth.

## Accepted direction

- [Architecture](ARCHITECTURE.md) — product, runtime, and repository boundaries.
- [Migration from Sajtmaskin](migration-from-sajtmaskin.md) — what to reuse now,
  what must be proven, and what is deliberately deferred.
- [OpenAI client boundary](openai-client-boundary.md) — authority, tools, and the
  first bounded agent loop.
- [MCP and integration baseline](mcp-and-integrations.md) — verified developer
  tools, configuration placement, connection scope, and secret boundaries.
- [Sprites and OpenClaw proving runbook](sprites-runbook.md) — the first safe
  provider experiment and the unresolved controller-host decision.

## Ways of working

- [Change and PR workflow](workflow/README.md) — the default path from idea to a
  verified change without retaining accidental legacy paths.
- [Goal and agent workflow](agent-workflow.md) — repository-isolated worker
  roles and the recommended bounded `/goal` objective.
- [Git and worktrees](git-workflow.md) — branch policy and guarded maintenance.
- [Governance](governance/README.md) — future schemas, policies, and manifests.
- [Logging and telemetry](logg-and-telemetry/README.md) — observability ownership,
  redaction, and raw/readable views.

## Status labels

Use these labels at the top of design documents when the distinction matters:

- **Accepted direction** — safe to implement incrementally.
- **Proposal** — requires a decision or a small proving experiment.
- **Reference only** — historical or external material.
- **Superseded** — retained only to explain an older decision.

`NOTES.md` files are deliberately informal. Resolve a useful note by rewriting
the conclusion in the appropriate document; do not silently turn the note
itself into a contract.
