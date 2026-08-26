# Sajtagent Platform

Sajtagent Platform is a clean version 2 of the ideas that work well in
Sajtmaskin. The goal is not to rewrite functioning behavior for its own sake.
The goal is to keep the useful parts while making ownership, contracts, agent
flows, and deployment boundaries substantially smaller and clearer.

SiteAgent names the complete web product. Its public first page is `/`, while
the building workspace is the **Builder** at `/builder`. `/siteagent` is kept
only as a compatibility redirect. This UI terminology does not require product
API routes such as `/api/siteagent/...` to be renamed.

## Repository layout

```text
sajtagent-platform/
├── sajtagent-site/             SiteAgent web product; separate Git repo
├── sajtagent-sprites/          Builder runtime; separate Git repo
├── control-panel/              Read-only local Streamlit control panel
├── scripts/                    Safe local maintenance routines
├── AGENTS.md                   Canonical guidance for all reviewers and agents
├── .cursor/rules/              Thin Cursor adapter to AGENTS.md
├── docs/                       Stable platform decisions
└── _reference/                 Disposable, non-authoritative working material
```

The outer repository tracks only platform-level governance and control-panel
code. It explicitly ignores the two nested product repositories. Never stage
or commit changes across those Git boundaries as one operation.

## Start the control panel on Windows

The reliable Python launcher on this machine is currently `py`. The bare
`python` command still resolves to the Microsoft Store alias in some terminals.

```powershell
py -m venv control-panel\.venv
.\control-panel\.venv\Scripts\python.exe -m pip install -r control-panel\requirements.txt
.\control-panel\.venv\Scripts\python.exe control-panel\app.py
```

The last command relaunches itself through Streamlit. Direct startup also works:

```powershell
.\control-panel\.venv\Scripts\python.exe -m streamlit run control-panel\app.py
```

The first version is deliberately read-only. It shows repository and platform
boundaries but does not deploy, mutate databases, execute customer code, or call
OpenAI.

## Start here

- [Architecture](ARCHITECTURE.md)
- [OpenAI client boundary](docs/openai-client-boundary.md)
- [Git and worktree workflow](docs/git-workflow.md)
- [Agent and reviewer instructions](AGENTS.md)
- [Reference-material warning](_reference/README.md)
