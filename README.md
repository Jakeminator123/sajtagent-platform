# Sajtagent Platform

Sajtagent Platform is the shared workspace around a thinner, clearer version 2
of the ideas that work well in Sajtmaskin. The goal is to reuse proven behavior
without copying the old product's internal structure or heavy LLM pipeline.

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
- [Migration decisions](docs/migration-from-sajtmaskin.md)
- [Change and PR workflow](docs/workflow/README.md)
- [OpenAI client boundary](docs/openai-client-boundary.md)
- [MCP and integration baseline](docs/mcp-and-integrations.md)
- [Goal and agent workflow](docs/agent-workflow.md)
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
