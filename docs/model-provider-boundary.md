# Model-provider and tool-authority boundary

Status: architecture direction, not an implemented client.

## Two different agent layers

Development subagents defined under `.codex/agents/` and `.cursor/agents/` help
Codex or Cursor edit and review these repositories. They use the model/session
configured in the developer tool. They are not bundled into SiteAgent, are not
deployed to Sprites, and do not use the product's OpenAI or Anthropic API keys.

Product agents are runtime code owned by `sajtagent-sprites`. They will use
Jakob's own server-side OpenAI and Anthropic accounts through explicit provider
adapters. Provider credentials belong in the runtime's secret configuration,
never in Git, the browser, `sajtagent-site`, Streamlit, prompts, logs, or tool
receipts.

## Reuse these principles

- Keep SiteAgent's product authority in its control plane and privileged
  execution in Sajtagent Sprites.
- Bind every run to server-owned `ProjectId`, `JobId`, and
  `WorkspaceRevision` values.
- Give the model only the tools allowed for this job and verify the grant again
  when each tool executes.
- Use isolated project workspaces, short-lived credentials, hard budgets,
  cancellation, idempotency, stale-write rejection, and auditable receipts.
- Release read capabilities before broad write capabilities. Keep edit and
  verify as one bounded operation when writes are enabled.
- Treat user prompts, imported files, logs, screenshots, dependencies, and web
  content as untrusted data that cannot expand authority.
- A build is successful only after deterministic checks and real preview
  evidence, not because a model or provider says it succeeded.

## Do not copy these Sajtmaskin assumptions

- `engine_versions.files_json` as the universal project representation;
- the exact `chatId`, `versionId`, `filesRevision`, or lineage contracts;
- `/api/openclaw/chat` and the older Chat Completions proxy flow;
- Quick Edit, Product Postcheck, RenderGate, ReleaseGate, or the persistent
  Render gateway;
- Sajtmaskin's database tables, branch model, component names, or model lanes.

The new neutral contract should center on `BuildJob`, `ToolGrant`,
`ToolReceipt`, `WorkspaceRevision`, and `BuildResult`.

## Provider location and API shape

The privileged OpenAI and Anthropic clients belong server-side behind
`sajtagent-sprites`. The browser, SiteAgent frontend, and Streamlit control
panel must never hold provider keys or call model tools directly.

Expose one small internal provider interface so tool authority, receipts,
budgets, cancellation, and terminal states remain provider-independent. A job
may select an allowed provider and model through server configuration, but a
model request may never grant itself broader tools. Provider fallback must be
explicit, observable, and budgeted rather than silently changing model or
behavior after an error.

```text
effective grant = platform policy
                intersect user mandate
                intersect job mode
                intersect runtime health limits
```

The model may choose from that effective grant, but it cannot widen it. Start
with sequential calls for mutating operations; parallel execution can be added
only where independence and retry safety are proven.

## Minimal first implementation

1. One server-side provider interface with separate OpenAI and Anthropic
   adapters; no provider-specific logic spread across UI routes.
2. Provider and model selected through server configuration rather than
   hard-coded prompts.
3. A small read tool set, followed by one bounded `apply patch -> check ->
   preview` path.
4. Explicit maximums for tool calls, model turns, wall time, changed bytes,
   repair attempts, and cost.
5. User-visible progress and tool receipts, but never private chain-of-thought.
6. Typed terminal results: `done`, `failed`, `cancelled`, `stale`, or
   `needs_user`.

Do not introduce a planner/reviewer/repair product-agent chain until
evaluations show that one bounded runtime loop is insufficient. The optional
Codex/Cursor integration reviewer is a development check and does not imply
such a product architecture.

Verify current official OpenAI and Anthropic documentation, account
availability, SDK versions, model support, and tool-call semantics when the
runtime adapters are implemented. This document deliberately does not lock the
platform to one provider, model name, or SDK version.
