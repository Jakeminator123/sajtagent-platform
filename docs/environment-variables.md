# Environment-variable ownership

Status: accepted boundary, 2026-08-27.

Use one ignored `.env.local` per deployable or local component. Do not create a
shared platform-wide secret file: it would give the browser, control panel, and
runtime more authority than each one needs.

| Repository | Local file | May contain | Must not contain |
| --- | --- | --- | --- |
| Platform root | `.env.local` | Local control-panel overrides | Provider, database, Sprite, GitHub, or Vercel credentials |
| `sajtagent-site` | `.env.local` | Site URL, database connection, browser-safe Supabase values, narrowly scoped site integrations | OpenAI/Anthropic provider keys, Sprite organization token, OpenClaw token |
| `sajtagent-sprites` | `.env.local` | Model-provider keys, Sprite token, OpenClaw token, controller signing secret | Browser-exposed values or developer MCP OAuth sessions |

Tracked `.env.example` files contain names and safe defaults only. Every real
secret stays in an ignored local file for development and in the owning host's
secret store for preview/production.

## Current boundaries

- `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` belong only to
  `sajtagent-sprites/.env.local`.
- `SPRITE_TOKEN`, `OPENCLAW_GATEWAY_TOKEN`, and
  `SITEAGENT_CONTROLLER_SIGNING_SECRET` are server-only runtime credentials.
- The current site prototype reads Postgres connection strings and optional
  Vercel AI Gateway/GitHub credentials. Those do not authorize the future
  product agent and must be replaced incrementally by the accepted controller
  and GitHub App contracts.
- `NEXT_PUBLIC_*` values are shipped to the browser. They may contain public
  configuration only, never secrets.
- Database TLS policy belongs with the site database connection. Keep
  certificate verification enabled unless a documented environment requires a
  narrower exception.

## Connections that are not env files

- Developer Git pushes use the workstation's SSH agent and repository remote.
- Codex/Cursor Vercel, GitHub, Supabase, and Sprites MCP logins are developer
  OAuth sessions.
- Neither SSH nor developer MCP access may be copied into product `.env.local`
  files or treated as production credentials.

Future product GitHub App and Vercel publication variables should be added only
when their typed adapters exist. Prefer short-lived installation credentials
and provider secret stores over personal access tokens.

## Active Supabase project

- Name: `sajtagent`
- Project ref: `ywoltuegeemqznbcgokg`
- Region: `eu-north-1`
- Owner: `sajtagent-site`
- Dashboard: <https://supabase.com/dashboard/project/ywoltuegeemqznbcgokg>

The local project URL and modern publishable key belong only in the ignored
`sajtagent-site/.env.local`. The tracked `.env.example` contains variable names
without values. A database password, direct Postgres URL, secret key, or
service-role key must never be committed.

This project is isolated from `jakebase`, `jakembase_dev`, and `spelsajt`.
Sajtagent must not reuse their database connection strings, migrations, or
server credentials.

## Vercel delivery

- Team: `jakeminator123s-projects`
- Project: `sajtagent-site`
- Project ID: `prj_hMs2VN2gnj9YU42ZDcEv9U8fOpKf`
- Git source: `Jakeminator123/sajtagent-site`, branch `main`
- Framework: Next.js
- Node.js: `24.x`
- Install command: `npm ci`

The Vercel project currently receives only public Supabase configuration in
Production, Preview, and Development:

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`
- `SUPABASE_PROJECT_REF`

All three are Vercel `Config` values, not secrets. No database URL, database
password, Supabase secret/service-role key, OpenAI key, Anthropic key, GitHub
token, Sprite token, or OpenClaw token is configured in the site project.

The local `.vercel/project.json` link and short-lived `VERCEL_OIDC_TOKEN` are
Git-ignored. Prefer OIDC over a static Vercel token. Never target the legacy
Vercel project `builder-v2` from this repository.
