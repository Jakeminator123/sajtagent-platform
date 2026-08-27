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
