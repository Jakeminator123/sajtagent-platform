# Sprites and OpenClaw proving runbook

Status: proposal for the first controlled experiment, 2026-08-27.

## Deployment model

A Sprite is a persistent, isolated Linux cloud VM, not a Docker container. Its
filesystem persists while compute sleeps and wakes on demand. A normal Fly App
or Machine is a different product path that commonly starts from an image or
`fly launch`; do not use that command as a substitute for creating a Sprite.

Use this initial split:

- Vercel hosts `sajtagent-site`.
- Fly Sprites host isolated project workspaces and build/preview execution.
- `sajtagent-sprites` owns the controller contract and runtime integration.
- The controller's eventual hosting provider remains undecided until a real
  slice proves whether it needs a long-lived service, queue consumer, or only a
  narrow API. Render may host that controller later, but introducing it now
  would add a second runtime provider without solving the worker problem.

The hosted Sprites MCP is an operator/development interface. The production
browser must call SiteAgent, which calls a bounded controller API. It must not
receive Sprites OAuth authority or an organization token.

## Product edit and live-preview loop

Assign one persistent project Sprite to an active project by default. Sajtagent
may create a `BuildJob` against the current `WorkspaceRevision` when it chooses
the build Skill within the active standing mandate. A normal conversational
prompt creates no BuildJob. An in-scope build needs neither a second user
confirmation, a new Sprite, nor a Vercel deployment.

The OpenClaw product agent should be autonomous inside that assigned workspace:
it may inspect and edit project files, install allowed dependencies, run bounded
commands and checks, inspect logs, and start or restart the preview. Its system
message must include the project brief, current revision, accepted requirements,
available tools, limits, and definition of done. Prompt instructions alone are
not guardrails: the controller must enforce the effective grant on every tool
call and prevent access to other projects, Sprites, credentials, and control
plane code.

Run the project preview as a Sprite **Service** so it returns after a cold wake.
Use a short-lived **Task** while an agent job or build must remain active. The
service should expose one stable project preview endpoint while successive
verified revisions change what it renders.

Sprite URLs are organization-private by default and public mode has no built-in
end-user authentication. Therefore the Builder iframe should use a platform-
owned, authenticated preview-session URL that proxies to the private Sprite
service. SiteAgent authorizes the session; the gateway may run with the
controller if that is the smallest reliable place for HTTP streaming and
WebSocket proxying. Never place an organization token in the iframe, and do not
switch the whole Sprite to public merely to make embedding easy. The preview
gateway must authorize user plus project and support the HTTP/WebSocket behavior
required by the selected development server.

On build completion, return a typed `BuildResult` containing at least the new
`WorkspaceRevision`, preview-session reference, checks, changed-file summary,
terminal status, and receipts. A follow-up mutation may start another bounded
job on the same current revision and workspace; an ordinary reply remains in
the conversation. Neither path may rely on hidden model memory as the source of
truth.

## Git and publication boundary

- Keep a Git repository inside each project Sprite and commit every verified
  user-visible version. Do not commit half-applied intermediate tool actions.
- Prefer a private GitHub repository as the durable remote when a scoped
  SiteAgent GitHub App is available. It is a mirror/history boundary, not the
  active filesystem and not a reason to grant the Sprite broad GitHub access.
- Keep GitHub optional at job-execution time so a temporary provider outage does
  not destroy or block the current workspace. Queue or retry a failed mirror.
- Do not deploy to Vercel after every follow-up prompt. The live Builder preview
  comes from the Sprite. Publish a selected verified commit to Vercel only after
  explicit product/user intent; optional Vercel preview deployments are durable
  review milestones, not the inner edit loop.
- Developer MCP OAuth sessions are never product credentials. Production GitHub
  and Vercel actions use separately scoped server-side installations.

## Local state verified

- Fly CLI is installed.
- Sprite CLI is not currently installed.
- The official Sprites MCP is configured globally at
  `https://sprites.dev/mcp`; restricted Codex OAuth is verified. Cursor has the
  same endpoint configured and completes its own OAuth on first use.
- OpenClaw documentation MCP is available, but the `openclaw` CLI and an actual
  Gateway are not installed on this workstation.

The Sprite CLI is optional for the MCP-first experiment. If it is installed
later, follow the current official Windows instructions and verify with
`sprite --help`. Its user configuration belongs in
`%USERPROFILE%\.sprites\sprites.json`; a project-local `.sprite` selector is
user-specific and must remain ignored by Git.

## First safe experiment

Do not run these mutations merely because this document exists. The active
goal must explicitly authorize creating and later destroying a disposable
Sprite.

1. Use the restricted connector to list visible Sprites.
2. Create exactly one Sprite matching the approved OAuth prefix, for example
   `sajtagent-smoke-01`.
3. Inspect installed Node, Python, Git, and disk capacity.
4. Create a named checkpoint before installing or changing anything.
5. Clone or copy only a tiny fixture, not a customer project or the whole
   Sajtmaskin repository.
6. Register a private HTTP service and verify wake-on-request. Do not switch the
   URL to public access.
7. Exercise a short Tasks API heartbeat for one bounded background operation,
   then release it and verify it expires.
8. Apply or inspect a minimal outbound policy that permits only the required
   package, source, and model endpoints.
9. Capture commands, durations, receipts, failures, and cost-relevant state.
10. Destroy the disposable Sprite only after its evidence is saved and the
    active task explicitly authorizes deletion.

Success means the same filesystem survives a pause, a service returns after a
cold wake, a bounded task prevents premature pause while work is active, and a
network denial fails clearly. It does not mean the production architecture is
finished.

## Runtime primitives

- **Service:** brings a process such as a preview server back after a cold wake.
- **Task:** keeps the current run active while an agent or worker must finish;
  use a short expiry plus heartbeat and always clean it up.
- **Checkpoint:** filesystem rollback point before a risky change. It does not
  capture running processes or open connections, and restore is destructive.
- **Network policy:** outbound DNS allow/deny policy controlled from outside
  the Sprite. Default outbound access is unrestricted until a policy is
  applied.

## OpenClaw boundary

OpenClaw can provide a plugin-owned tool surface, but it is not itself a safe
multi-tenant authorization boundary. Its official security model assumes one
trusted operator boundary per Gateway. For mutually untrusted customer jobs,
use separate Gateway cells or put a deterministic controller in front of
separate workers so no shared agent can exercise another tenant's authority.

The first plugin should register only the smallest tools needed for one
read/edit/check/preview loop. Its manifest declares tool ownership, while the
controller remains responsible for tenant binding, job scope, expiry, budget,
idempotency, and audit receipts. Never expose the Gateway directly to the
browser.

Current official references:

- [Sprites remote MCP](https://docs.sprites.dev/integrations/remote-mcp/)
- [Sprites lifecycle and persistence](https://docs.sprites.dev/concepts/lifecycle/)
- [Sprites services](https://docs.sprites.dev/concepts/services/)
- [Keeping a Sprite running](https://docs.sprites.dev/keeping-sprites-running/)
- [Sprites checkpoints](https://docs.sprites.dev/concepts/checkpoints/)
- [Sprites networking](https://docs.sprites.dev/concepts/networking/)
- [OpenClaw plugin development](https://docs.openclaw.ai/plugins/building-plugins)
- [OpenClaw Gateway security](https://docs.openclaw.ai/gateway/security)
