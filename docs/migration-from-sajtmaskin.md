# Migration from Sajtmaskin

Status: accepted direction, 2026-08-27.

The external reports under `_reference/gpt-om-migrering/` are useful research,
not a blueprint to copy. Sajtagent starts with the three repository boundaries
already chosen for this workspace. We will not refactor the Sajtmaskin monolith
as a prerequisite and will not recreate it as a package monorepo under a new
name.

## Adopt now

- Preserve behavior with golden examples before moving an implementation.
- Keep privileged execution separate from both the browser and production.
- Bind every conversation to server-owned identity and project context. Bind
  tool or mutating executions additionally to a job, base revision, budget,
  and cancellation signal.
- Let deterministic code authorize tools and verify results.
- Use a small typed `ConversationTurn`/`AgentEvent` stream as the primary
  boundary between Site and Sprite Runtime. Carry `BuildJob` and `BuildResult`
  only for optional build executions inside that conversation.
- Retrieve only the files and reference cards needed for the current task.
- Require real build and preview evidence before reporting success.
- Keep a replacement and its old path from becoming two permanent systems.

Useful Sajtmaskin assets can later include selected templates, provenance,
scaffold ideas, validators, preview checks, and regression fixtures. Each asset
must be inventoried and adapted to a new contract; its old route names, tables,
prompt stack, and ownership do not come with it automatically.

## Prove with a small experiment first

- Whether OpenClaw should be central, per project, or split into a durable
  controller and disposable workers.
- Whether one persistent Sprite per project is worth its lifecycle and storage
  cost compared with hydrating a workspace from an authoritative revision.
- Whether project source should become a separate Git repository immediately
  or start behind a replaceable source-store interface.
- How private preview authentication, cold wake, services, tasks, and outbound
  network policy work in the selected Sprite setup.
- Which template and scaffold concepts reduce tokens and improve output in
  measured evaluations.

An experiment must state the question, smallest setup, success threshold,
cost, and what decision follows each outcome. Do not turn a provider assumption
into a permanent domain model before the experiment.

## Deliberately deferred

- A second build Sprite in addition to the first working project workspace.
- Automatic release, production maintenance, and self-triggered repair.
- A large package graph, provider abstraction for every possible service, or a
  complete future database schema.
- A capability broker, secret broker, release controller, artifact provenance,
  and append-only audit platform implemented before the first build path needs
  them.
- Migration of all Sajtmaskin projects or all legacy templates.
- Multi-agent planner, reviewer, and repair chains.

These may become good designs later. Deferring them is not rejecting their
principles; it prevents speculative structure from becoming legacy before the
core workflow exists.

"Self-triggered repair" here means background maintenance without a visible,
active user goal. Autonomous inspection, repair and verification inside a
currently delegated goal or BuildJob are part of the normal Sajtagent loop and
are not deferred.

## First vertical slice

```text
one continuous conversation
  -> SiteAgent validates and streams one ConversationTurn
  -> answer-only response or permitted Skill selection
  -> optional BuildJob derived from the active project mandate
  -> Sajtagent Sprites runs one bounded agent loop
  -> project-scoped read/edit/check/preview tools
  -> deterministic verification
  -> assistant explanation plus typed BuildResult with evidence
```

Start with one supported site kind and one known-good starter. Release remains
manual. The slice is complete only when the browser can show the real preview
and a failed check cannot be presented as success.

## LLM input and catalog direction

Free text, analyzed documents, templates, and audits are four input forms, not
four independent agent pipelines. SiteAgent should normalize them into one
small request contract. The privileged model loop and tool execution belong in
`sajtagent-sprites`.

When template work begins, test the external report's five-part vocabulary:

1. baseline rules shared by every project;
2. a foundation that owns runtime, files, and package-manager policy;
3. a scaffold that expresses structural requirements and freedom;
4. a design recipe that combines useful variant and addendum concepts;
5. lazy page recipes that guide common pages without becoming an allowlist.

Compile only the selected material into a resolved contract. Do not send the
whole catalog, template archive, or Sajtmaskin prompt stack to every model call.
