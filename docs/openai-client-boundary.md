# OpenAI client and tool-authority boundary

Status: architecture direction, not an implemented client.

## Context

The historical review in the Codex task `Review OpenClaw branch plan` contains
useful security and agent-design ideas, but much of it was written for
Sajtmaskin's existing OpenClaw/OpenAI integration. This document deliberately
separates reusable principles from Sajtmaskin-specific implementation details.

## Reuse these principles

- Keep SiteAgent's product authority in its control plane and privileged
  execution in Sprite Agent.
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
  evidence, not because the model says it succeeded.

## Do not copy these Sajtmaskin assumptions

- `engine_versions.files_json` as the universal project representation;
- the exact `chatId`, `versionId`, `filesRevision`, or lineage contracts;
- `/api/openclaw/chat` and the older Chat Completions proxy flow;
- Quick Edit, Product Postcheck, RenderGate, ReleaseGate, or the persistent
  Render gateway;
- Sajtmaskin's database tables, branch model, component names, or model lanes.

The new neutral contract should center on `BuildJob`, `ToolGrant`,
`ToolReceipt`, `WorkspaceRevision`, and `BuildResult`.

## Recommended client location and API shape

The privileged OpenAI client belongs server-side behind `sajtagent-sprites`. The
browser and Streamlit control panel must never hold its API key or call model
tools directly.

Use the Responses API for reasoning, tool-calling, and multi-turn work. Define
small function tools with strict JSON schemas. Keep the model-visible catalog
separate from the server-authorized subset for the current job. A tool request
is a proposal; the server remains responsible for authentication,
authorization, validation, execution, and recording the result.

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

1. One server-side client interface, without model-specific logic spread across
   routes and UI components.
2. One default model selected through configuration rather than hard-coded in
   prompts.
3. A small read tool set, followed by a bounded `apply_patch -> check ->
   preview` path.
4. Explicit maximums for tool calls, model turns, wall time, changed bytes,
   repair attempts, and cost.
5. User-visible progress and tool receipts, but never private chain-of-thought.
6. Typed terminal results: `done`, `failed`, `cancelled`, `stale`, or
   `needs_user`.

Do not introduce a planner/reviewer/repair agent chain until evaluations show
that one bounded loop is insufficient.

## Current official guidance used for this decision

OpenAI's current model guidance recommends the Responses API for reasoning,
tool-calling, and multi-turn applications, shorter outcome-focused prompts,
structured outputs, and explicit success and stop criteria:

- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5

The function-calling guide recommends strict schemas and supports restricting
each request to an allowed subset of tools:

- https://developers.openai.com/api/docs/guides/function-calling

Verify current official documentation, account availability, and chosen model
support again when implementation begins. This document intentionally does not
lock the platform to a model name or SDK version.
