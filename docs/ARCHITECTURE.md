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
User
  |
  v
SiteAgent / Builder on Vercel <--------------------> Supabase
  |
  | signed, scoped BuildJob
  v
Controller / OpenClaw -------- scoped tools ------> project Sprite
  ^                                                edit / test / preview
  +--------------- receipts + BuildResult ---------------+

Builder iframe <- authenticated preview route <- Sprite preview service

accepted revision -> durable Git remote -> explicit Vercel publication
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

## Interactive edit and preview loop

The normal Builder loop does not deploy to Vercel after every prompt:

1. SiteAgent stores the user message and creates a `BuildJob` bound to the
   current `WorkspaceRevision`.
2. The controller gives one OpenClaw agent enough project context and scoped
   tools to work independently inside the assigned project Sprite.
3. The agent edits the persistent workspace, runs checks, and updates a preview
   service in that Sprite.
4. SiteAgent authorizes an authenticated preview session and embeds its URL in
   the Builder iframe. It must not expose a raw organization token or make the
   whole Sprite public.
5. After health and acceptance checks, the controller returns a new
   `WorkspaceRevision`, `BuildResult`, preview URL, and tool receipts.
6. A follow-up prompt creates a new bounded job against that revision and edits
   the same project workspace, producing the next user-visible version.

The preview route should remain stable for the active project while its content
changes. Support proxied WebSockets for hot reload where practical; otherwise
reload the iframe when a verified workspace revision becomes ready. Progress
events and the rendered preview are separate streams.

The system message supplies role, project brief, current revision, accepted
requirements, tool contracts, and definition of done. It is guidance, not the
security boundary. Deterministic controller checks still enforce tenant,
workspace, paths, commands, network access, budgets, expiry, and stale writes.

## Workspace versions, GitHub, and Vercel

- The Sprite filesystem is the live workspace during an edit loop.
- Each successful agent turn creates a product version and a Git commit; risky
  operations may additionally use a Sprite checkpoint for rollback.
- A private GitHub repository is the preferred default durable remote when a
  scoped SiteAgent GitHub App installation is available. Push verified version
  commits, not every intermediate tool edit. Do not require an end user to have
  a GitHub account merely to start a project.
- GitHub is durable source history, not the live preview runtime. The product
  must retain a recovery path if GitHub is temporarily unavailable.
- Vercel is outside the fast edit loop. Publish only an explicitly selected,
  verified revision. A Vercel Preview Deployment may later provide a durable
  shareable milestone, but it does not replace the live Sprite preview.
- Product GitHub and Vercel credentials must come from scoped server-side
  integrations, never from a developer's Codex/Cursor MCP login.

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
