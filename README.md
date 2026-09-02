# Sajtagent Platform

Sajtagent Platform is the shared workspace for an independent, dynamic
site-creating agent. It understands the user's intent and the current site,
then intelligently selects Skills, capabilities, and tools to create, inspect,
verify, and improve websites precisely. Conversation is its natural control
interface, not its product identity. It selectively reuses proven technical
behavior without copying Sajtmaskin's product personality, card-and-process
experience, internal structure, or heavy LLM pipeline.

## Repository boundaries

This folder contains three independent Git repositories:

| Folder | Responsibility | Git repository |
| --- | --- | --- |
| `./` | Platform decisions, local control panel, and maintenance | `sajtagent-platform` |
| `sajtagent-site/` | SiteAgent web product and Builder | `sajtagent-site` |
| `sajtagent-sprites/` | Privileged agent, OpenClaw, and Sprite runtime | `sajtagent-sprites` |

The two child repositories are intentionally ignored by the platform repo. A
fresh clone of `sajtagent-platform` does not download them automatically; clone
each repository separately into the folder shown above.

## Start here

- [Architecture](docs/ARCHITECTURE.md)
- [Site-creating agent doctrine](docs/product-agent-doctrine.md)
- [Migration decisions](docs/migration-from-sajtmaskin.md)
- [Change and PR workflow](docs/workflow/README.md)
- [Model-provider boundary](docs/model-provider-boundary.md)
- [MCP and integration baseline](docs/mcp-and-integrations.md)
- [Goal and agent workflow](docs/agent-workflow.md)
- [Development environments](docs/development-environments.md)
- [Environment-variable ownership](docs/environment-variables.md)
- [Sprites and OpenClaw proving runbook](docs/sprites-runbook.md)
- [Documentation index](docs/README.md)
- [Agent instructions](AGENTS.md)

`_reference/` and every `NOTES.md` are working material. They may contain good
ideas, open questions, or stale assumptions, but they are not accepted
architecture until the decision has been rewritten under `docs/`.

## Local control panel

The first control panel is deliberately read-only:

```powershell
py -m venv control-panel\.venv
.\control-panel\.venv\Scripts\python.exe -m pip install -r control-panel\requirements.txt
.\control-panel\.venv\Scripts\python.exe control-panel\app.py
```

It reports repository state and architecture boundaries. It does not deploy,
write production data, execute customer code, or own the OpenAI client.
