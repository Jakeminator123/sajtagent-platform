# Sajtagent Platform architecture

Status: initial platform decision, 2026-08-26.

## Product terminology and UI routes

**SiteAgent is the entire web product.** The Builder is one workspace inside
SiteAgent and must not be used as another name for the product.

| Route | Meaning |
| --- | --- |
| `/` | SiteAgent's public first page |
| `/builder` | The authenticated or interactive Builder workspace |
| `/siteagent` | Compatibility redirect to `/builder`, not a separate product |

Navigation, internal links, metadata, and product documentation should use
these meanings consistently. Product-owned API routes may continue to use
`/api/siteagent/...`; the clarification concerns the UI route.

## Product boundary

```text
Browser
   |
   v
SiteAgent ------- signed, scoped BuildJob --------> Sprite Agent / OpenClaw
   |                                                       |
   v                                                       v
Supabase                                             project Sprite
   |                                             build / test / preview
   v
Vercel publication
```

`sajtagent-site` owns SiteAgent's first page, Builder, authentication, projects,
chat, versions, product data, preview presentation, and release intent.

`sajtagent-sprites` owns privileged model orchestration, OpenClaw integration,
isolated project workspaces, tool execution, deterministic checks, and preview
runtime operations. It exposes a narrow server-to-server job API, not a public
general-purpose shell.

The root repository owns only cross-repository guidance and a local read-only
control panel. It is not another backend and must not become a third source of
runtime state.

## Thin-first delivery

The first useful system should be one complete, bounded path:

```text
user request -> BuildJob -> one agent loop -> tools -> checks -> preview
             -> typed BuildResult and verification evidence
```

Begin with a small tool surface and bounded retries. Add extra agents, models,
services, repositories, queues, manifests, or policy layers only after a real
requirement and a measured benefit exist.

## What to reuse from Sajtmaskin

Reuse behavior or code after verifying that its assumptions still fit:

- deterministic validation and real preview evidence;
- explicit versions/revisions and stale-write protection;
- server-owned permissions, budgets, audit receipts, and cancellation;
- good UI and control-panel patterns;
- known working integrations where adapting is smaller than rebuilding.

Do not automatically reuse Sajtmaskin's internal route names, database tables,
large prompt stack, model lanes, release gates, or full backoffice structure.
Sajtmaskin is a successful reference implementation, not the new platform's
runtime authority.

## Truth and reference material

The authority order is:

1. owning repository code, tests, and explicit runtime contracts;
2. accepted platform decisions in this repository;
3. current official service documentation;
4. `_reference/` as optional background only.

Customer workspaces live in isolated project Sprites, not as folders in this
repository. Secrets live in the service that needs them and never in the
browser, reference folder, model prompt, or root control panel.
