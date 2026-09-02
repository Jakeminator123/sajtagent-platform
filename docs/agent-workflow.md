# Goal and agent workflow

Status: accepted working method, 2026-08-27.

## Development agents are not product agents

The roles in `.codex/agents/` and `.cursor/agents/` are optional development
helpers. They use the active Codex or Cursor session to edit or inspect code.
They are not shipped with SiteAgent and do not consume the product's OpenAI or
Anthropic API credentials.

The actual SiteAgent product agents will be implemented in
`sajtagent-sprites`, use Jakob's own server-side provider credentials, and run
through the bounded runtime/controller contract described in
`model-provider-boundary.md`.

Use one primary agent as coordinator and delegate by repository. Do not open
uncoordinated agents with broad prompts: all agents share the filesystem, so
two writers in the same repository can silently overwrite or invalidate each
other's evidence.

## Roles

| Role | Write scope | Purpose |
| --- | --- | --- |
| Primary agent | Platform root and integration decisions | Owns the goal, sequence, contracts, and final account of delivery. |
| `site_worker` / `site-worker` | `sajtagent-site` only | Implements the web product and Builder side of one vertical slice. |
| `sprites_worker` / `sprites-worker` | `sajtagent-sprites` only | Implements the privileged runtime side of that slice. |
| `integration_reviewer` / `integration-reviewer` | Read-only across all three repositories | Optional development-only check of the joined path; it is not a product agent. |

Codex definitions live under `.codex/agents/`; Cursor definitions live under
`.cursor/agents/`. The Codex concurrency cap is three spawned agents, matching
two independent writers plus one reviewer while the primary agent coordinates.

## Before starting `/goal`

This section governs development agents and operator infrastructure changes.
Its separate permissions do not introduce per-build confirmation inside an
active Sajtagent product mandate; that product authority is defined in
[the product-agent doctrine](product-agent-doctrine.md).

1. Complete restricted Sprites OAuth. In an interactive Codex CLI session, use
   `/mcp verbose`; from plain PowerShell, use `codex mcp list`. The connection
   was already verified on Jakob's current machine on 2026-08-27.
2. State whether the run may create one disposable Sprite. Creation, public
   exposure, restore, destruction, deployment, and database writes are separate
   permissions; do not infer one from another.
3. Choose one vertical outcome, not "build the whole platform". The recommended
   first outcome is one real Site request that becomes one signed build job,
   performs one bounded workspace change, produces one preview receipt, and
   reports a real failure when any boundary fails.
4. Resolve the exact Vercel project and Supabase project before allowing either
   integration to write. Existing Sajtmaskin connections are not defaults.
5. Record baseline failures separately so the goal does not claim to have
   caused or fixed unrelated debt.

## Recommended goal text

After the prerequisites above are satisfied, use a goal with this scope:

```text
Build and verify the first real Sajtagent vertical slice across the existing
three-repository workspace. Keep main as the standard branch and preserve all
unrelated local changes. The primary agent owns platform contracts and
coordination. Delegate sajtagent-site implementation only to site_worker and
sajtagent-sprites implementation only to sprites_worker; never let two writers
edit the same repository. Run integration_reviewer read-only after the real
path is connected.

The slice must accept one server-authorized project/job request, execute one
bounded read/edit/check/preview operation in an isolated worker, and return a
typed receipt with a real success or failure. Remove or explicitly gate any
simulated success on this path. Do not create, destroy, restore, expose, deploy,
or widen network access for cloud resources unless this goal separately and
explicitly authorizes that exact action. Do not reuse Sajtmaskin project
bindings by assumption.

Finish only when focused tests and a minimal end-to-end smoke test pass, and
report local, committed, pushed, deployed, and unverified state separately.
Always report branch and absolute worktree for every repository touched.
```

## Sequencing

1. The primary agent freezes a small cross-repository contract.
2. The two workers implement their own side in parallel.
3. The primary agent connects or reconciles the contract, without rewriting
   either repository wholesale.
4. The read-only reviewer traces the actual path and rejects false-green tests
   or simulated fallbacks.
5. The primary agent fixes bounded findings, verifies, and only then performs
   explicitly authorized Git or deployment actions.
