# MCP and integration baseline

Status: accepted tooling baseline, verified 2026-08-27.

MCP configuration is a developer-tool concern, not a product runtime contract.
Account-specific connections belong in each developer's global configuration;
tokens and OAuth artifacts never belong in Git. The product must use its own
bounded server-side APIs and credentials at runtime.

## Verified local availability

| Capability | Placement | Current state | Sajtagent rule |
| --- | --- | --- | --- |
| OpenAI developer documentation | Global Codex and Cursor MCP, `openai-docs` | Configured and callable | Use for current OpenAI and Codex behavior. |
| OpenClaw documentation | Global Codex and Cursor MCP, `openclaw-docs` | Configured and callable | Documentation only; it is not an OpenClaw Gateway. |
| Versioned library/cloud documentation | Global Codex and Cursor MCP, `context7` | Configured and callable | Prefer it for current SDK and service documentation. |
| Fly Sprites operator tools | Global Codex and Cursor MCP, `sprites` | Configured at `https://sprites.dev/mcp`; Codex OAuth verified, Cursor authenticates separately on first use | Keep restricted access, a Sajtagent-specific name prefix, and a small Sprite cap. |
| GitHub | Codex GitHub plugin | Callable as `Jakeminator123` | Confirm the exact repository before writes. |
| Vercel | Codex Vercel plugin | Callable for team `jakeminator123s-projects` | Resolve the exact Sajtagent project before writes or deployment. |
| Supabase | Codex Supabase plugin and read-only MCPs | Callable, but no project is yet accepted as Sajtagent's database | Never infer the database from a convenient existing project. |

The global Codex configuration also contains a Vercel MCP scoped to the
separate Sajtmaskin project. It remains useful for that project but is not a
valid Sajtagent connection. Do not use its project scope here. The generic
`user-vercel` entry was not logged in during this verification; the installed
Vercel plugin was independently callable.

## Why these are global

- Codex user configuration lives in `~/.codex/config.toml`.
- Cursor user configuration lives in `~/.cursor/mcp.json`.
- Both products support project-level configuration, but a committed project
  file would duplicate these cross-project documentation tools and could
  override a developer's safer global settings.
- Project-level MCP configuration is appropriate only for a portable,
  secret-free server that is genuinely part of this project's workflow.

The committed `.codex/` and `.cursor/agents/` files configure agent roles, not
account credentials. No API key, bearer token, OAuth token, database URL, or
project secret may be committed there.

## Sprite connector policy

This policy governs the developer/operator MCP connection. It is separate from
the product agent's server-enforced standing project mandate described in
[the product-agent doctrine](product-agent-doctrine.md).

Use the official endpoint `https://sprites.dev/mcp`. During OAuth:

1. choose a restricted token;
2. use a prefix such as `sajtagent-` or `mcp-sajtagent-`;
3. keep the initial maximum at five Sprites or fewer;
4. require explicit approval for create, destroy, restore, public exposure, and
   network-policy expansion;
5. never expose this operator connector to the SiteAgent browser.

The remote MCP can create and manage Sprites, execute commands, inspect or
restore checkpoints, manage services, and change outbound network policy.
Those are real external mutations. A restricted token limits blast radius but
does not make destructive calls harmless.

## Verification

For Codex:

```text
/mcp verbose
```

or from PowerShell:

```powershell
codex mcp list
codex mcp get sprites
```

For Cursor, open **Settings -> Tools & MCP**, confirm the same server names,
and complete OAuth for `sprites` if Cursor requests its own login. Restart or
open a new agent session if a newly added server is not discovered in the
current session.

Authoritative references:

- [Sprites remote MCP](https://docs.sprites.dev/integrations/remote-mcp/)
- [Sprites quickstart](https://docs.sprites.dev/quickstart/)
- [OpenClaw building plugins](https://docs.openclaw.ai/plugins/building-plugins)
- [OpenClaw Gateway security](https://docs.openclaw.ai/gateway/security)
- [Cursor MCP configuration](https://cursor.com/help/customization/mcp)
- [OpenAI MCP and connectors](https://developers.openai.com/api/docs/guides/tools-connectors-mcp)
- [Codex developer commands](https://learn.chatgpt.com/docs/developer-commands)
