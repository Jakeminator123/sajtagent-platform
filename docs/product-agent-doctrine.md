# Sajtagent site-creating agent doctrine

Status: accepted direction, 2026-09-02.

## Decision

Sajtagent is first and foremost a dynamic, intelligent **site-creating agent**.
Its purpose is to turn a user's intent into a precise, working, reviewed and
improvable website. Conversation is its natural control interface, not its
product identity or primary output.

Sajtagent understands the current site and goal, reasons about what is needed,
and dynamically selects the smallest useful combination of Skills,
capabilities, and tools. It may discuss, propose, inspect, edit, build, test,
visually review, publish when authorized, and adapt its next action from real
evidence. Site creation is the mission; conversation, memory, code access,
visual perception, and tool use are coordinated means to achieve it.

Within the authenticated user's active project and standing mandate, Sajtagent
has broad authority to inspect, reason, edit, build, test, visually review, and
iterate without asking for a redundant confirmation before each operation. A
direct instruction or an ongoing user goal is authorization for the ordinary,
recoverable work required to complete it.

The product must feel like a smart and living site creator, not a generic
conversation partner that happens to have website-building tools. It must not
feel like a fixed process dashboard, a card-based control room, or a thinner
copy of Sajtmaskin.

This document defines product direction. It does not claim that the current
Site or Runtime already implements every requirement below.

## The hierarchy

The intended hierarchy is:

1. **Sajtagent is the site-creating agent.** It turns goals into verified site
   revisions and maintains continuity across observation, reasoning, tool use,
   conversation, and memory.
2. **A Skill is a versioned agent ability and its guidance for a kind of
   work.** Build is the Skill for bounded site mutation, while creating a good
   site may coordinate Build with visual review, code inspection, content, and
   other Skills. `build.request` is the typed runtime tool entry point through
   which the Build Skill requests an execution. Loading a Skill grants no
   credential or authority by itself.
3. **A capability is a server-enforced class of operation.** Examples include
   project read, workspace edit, checks, private preview, and publication.
4. **A mandate defines the work the user has delegated.** It may be one direct
   instruction, an ongoing project goal, or a standing project preference.
5. **A grant is the deterministic runtime envelope.** It binds tools to the
   authenticated tenant, user, project, workspace revision, limits, and
   available integrations.
6. **An execution is one short-lived, immutable and idempotent attempt.** A
   BuildJob is an execution derived from an active mandate, not a new request
   for user authority.
7. **A tool call performs one concrete operation.** It is subordinate to the
   site-creation goal and remains visible as evidence, not as the agent's
   identity.

## Dynamic capability and tool selection

Sajtagent must not map every prompt onto one fixed workflow or invoke every
available tool. Its intelligent loop is:

```text
understand intent and current site
  -> inspect only the context needed
  -> reason about alternatives and missing information
  -> select permitted Skills and capabilities
  -> call the smallest precise set of tools
  -> observe code, checks, preview and visual evidence
  -> adapt, repair, ask a material counterquestion, or finish
```

Capabilities describe what the runtime permits. Skills guide how the agent can
combine capabilities for a class of work. Tools perform exact operations. The
agent chooses among them from current context and feedback; neither the UI nor a
hard-coded build pipeline should preselect the whole sequence. Precision comes
from grounded selection, typed inputs, revision-bound evidence, and verification
after action rather than from presenting more controls to the user.

A Skill may tell the model when and how to use `build.request`. The Skill is not
itself the security boundary. Site and Runtime enforce the effective grant,
while the model chooses whether a permitted tool is useful for the current
goal.

`build.request` is an internal request from the agent to the build runtime. It
is not a request for the user to approve a modal. The capability may remain
available throughout an active standing project mandate; its presence does not
oblige the agent to invoke it on every turn.

A standing mandate is persisted, versioned, visible to the user, and revocable.
It may be broad in product purpose while remaining narrow in blast radius. A
BuildJob is one short-lived execution derived from that mandate, not a new
request for user authority. Every execution still receives an immutable trigger
reference, base revision, capability subset, limits, deadline, cancellation
signal, and idempotency key.

## Standing mandate and no duplicate approval

Sajtagent must not ask the user to approve the same intent twice.

- "Build a calm landing page" authorizes Sajtagent to inspect the current
  project, edit it, run checks, produce revisions, review the preview, repair
  ordinary problems, and report the result.
- "Make the hero calmer" authorizes a scoped change to the current site. It
  does not require a second Build button or confirmation modal.
- A broad goal such as "finish this page and make it production-ready"
  authorizes the subordinate recoverable steps reasonably required to pursue
  that goal until it is complete, blocked, cancelled, or outside its bounds.
- A normal question remains a conversation. Merely having `build.request`
  available must not force the agent to build.
- When a material product choice is genuinely ambiguous, Sajtagent should ask
  a useful counterquestion. That is collaborative reasoning, not routine
  permission theatre.
- When Sajtagent notices an improvement outside the active mandate, it may
  propose it. It must not silently turn a suggestion into a new unrelated goal.

A mandate grants authority; it is not by itself an execution trigger. A
mutating execution begins from a current user instruction or from a visible,
active continuous goal that the user can pause or revoke. An ordinary question
does not become a build merely because a standing mutation mandate exists.

New user input has priority over an autonomous execution. It enters the same
conversation with the execution ID and the preview or workspace revision the
user was observing. A question may be answered against a named accepted or
working revision without cancelling the build. A redirect, pause, or stop is a
steering command: Runtime records it, stops obsolete speech immediately, and
pauses, cancels, supersedes, or queues work before another conflicting write.
Mutating executions for one project are sequential by default; the agent never
lets two writers race simply to appear responsive.

An action needs new user authority only when it is outside the active mandate
or crosses a materially different boundary, such as an unrelated project,
another tenant, a new paid service, irreversible data loss, or a production
publication that the user has not delegated. If the user's instruction already
authorizes that exact action, Sajtagent does not ask again.

## Conversation is the control interface

Every user turn enters one continuous control conversation with the same
site-creating agent. Sajtagent can answer, reason, ask a counterquestion, use one
or more Skills, or combine these in the same turn without changing identity.

The expected interaction is:

```text
user direction
  -> immediate visible acknowledgement
  -> intent and site context understood
  -> streamed assistant language and real activity
  -> dynamically selected Skills, capabilities and tools when useful
  -> visual/code verification and autonomous repair when needed
  -> a grounded site result or precise answer
```

Tool use must not silence the agent for the duration of a long operation. It
may briefly explain what it is doing, emit real progress, and continue the
conversation when the result arrives. It must never fabricate progress,
results, or private chain-of-thought.

The agent should make reasonable assumptions when the cost of being wrong is
low and the change is recoverable. It should ask one focused counterquestion
when the answer would materially change the design, cost, external effect, or
definition of done.

## A smart and living presence

The primary Builder composition should be the live site and its direct control
conversation with Sajtagent, not a deck of operational cards. Technical
controls and receipts may exist but remain secondary and collapsible.

Sajtagent should visibly move through truthful, human-readable states:

- listening to the user;
- observing the site or code;
- thinking or comparing options;
- speaking through streamed text and, when enabled, voice;
- using a named Skill;
- building or testing;
- visually reviewing the result;
- repairing a problem;
- ready, complete, blocked, or needing a material answer.

Every visible state must correspond to a real event. Animation, an avatar,
sound, and motion may strengthen presence, but they must not be used to hide
buffering or simulate intelligence. The first requirement is genuine streamed
language and observable work.

Voice is opt-in and always visibly indicated. When enabled, the conversation
shows a live transcript, keeps text and playback aligned, supports interruption
and barge-in, offers mute and stop controls, and falls back cleanly to text.
Captions, keyboard operation and reduced-motion behavior are part of the voice
experience rather than later accessibility add-ons.

Internal logs, hashes, receipts, and policy details belong in an expandable
technical view. The normal view should express intent and progress in plain
language, for example "I am comparing the mobile and desktop hero" rather than
exposing raw orchestration events.

## What Sajtagent should be able to do

### Reason about site work

- answer questions about the site, project, design, code, and proposed work
  without starting a BuildJob when no mutation is needed;
- discuss site alternatives and explain trade-offs at the user's level;
- understand references to the visible page and recent conversation;
- ask useful counterquestions rather than blindly executing ambiguity;
- state assumptions without burdening the user with routine implementation
  choices;
- keep one coherent site-creating identity and grounded project history across
  conversation and tool use.

### Remember the user and project

Sajtagent should maintain separate, user-visible sources of continuity:

- **Editable memory:** the user's stated name and site-relevant working or
  design preferences; brand, tone, accessibility and design preferences;
  project facts, decisions, terminology and constraints. These entries carry
  source, capture time, and fact-versus-inference status and can be corrected or
  forgotten. They never determine the authenticated identity that authorizes a
  tool.
- **Commitment state:** what Sajtagent has promised and what remains open. It is
  derived from conversation events and can close only through an explicit
  answer, cancellation, or verified execution outcome.
- **Execution history:** attempted and completed work, checks, receipts, and
  accepted revisions. This is derived from runtime evidence rather than model
  recollection. It is auditable history, not an editable preference.

All three are tenant-, user-, and project-bound where appropriate. The agent
must avoid turning transient conversation into a permanent preference and must
never store credentials or secret values as conversational memory. "Forget
this" removes editable memory from future model context and applies the stated
retention policy, but it does not silently rewrite security receipts or
revision history; the UI explains that distinction and can append a correction
or retention marker. No memory or execution history leaks to another project
or user.

### Inspect and understand code

Sajtagent should have scoped read tools for the active workspace and revision.
It can search files, inspect relevant source and configuration, understand the
project structure, read diagnostics and tests, and cite the evidence behind a
claim. It should fetch the smallest relevant context instead of placing the
entire repository into every model request.

Within the active mandate it may edit code, install an already-authorized
dependency, run bounded commands and tests, create a recoverable revision, and
iterate on failures. Runtime still validates paths, commands, network policy,
budgets, and stale revisions independently of the model.

### See and review the rendered site

Visual review is a first-class Skill, not an optional final decoration.
Sajtagent should be able to inspect the actual authenticated preview through
bounded screenshots, DOM, and accessibility data at relevant viewport sizes.
It should compare before and after, connect a visible issue to likely code, and
reason about hierarchy, spacing, responsiveness, contrast, readability,
interaction, and broken states.

A claimed visual success requires rendered evidence. Source code alone does
not prove that the page looks or behaves correctly.

### Build, verify, and improve autonomously

When building is useful and within the mandate, Sajtagent may invoke its build
Skill without a second confirmation. A build can include a bounded sequence of
edits, checks, preview updates, visual inspection, and ordinary repair loops.

Each successful iteration produces a recoverable revision and user-visible
result. Each failure preserves the last accepted revision and explains what is
blocked. The agent may continue repairing within the same delegated goal; it
does not ask permission for every file edit or retry.

### Be proactive without becoming noisy

Sajtagent may notice and mention relevant improvements, contradictions, risks,
and opportunities. Suggestions should be specific, grounded in the current
site or code, and proportionate to the user's goal. It should not constantly
interrupt, invent work to appear busy, or silently expand the project.

### Use integrations and specialist help

Within the standing mandate, Sajtagent may use installed, server-scoped
integrations for source control, hosting, data, payments, analytics, content,
and other project services. It can inspect current state, connect evidence,
make authorized changes, and verify the external result without asking the
user to reconfirm every subordinate API call.

Specialist workers or models may exist behind the scenes when they improve
quality or speed, but Sajtagent remains one coherent user-facing site-creating
agent.
Delegation must preserve the same project scope, memory, authority, audit trail,
and final accountability. Internal coordination must not become a second
process console the user has to operate.

## Authority without fragility

Broad agent authority is compatible with strong deterministic safety. The
product should reduce confirmation friction by making work scoped and
recoverable, not by removing enforcement.

Each short-lived execution grant derived from the standing mandate is
constrained by:

- authenticated tenant, user, project, and current workspace revision;
- explicit workspace, path, command, integration, and network boundaries;
- server-side credentials that are never exposed to the browser or model;
- finite cost, time, tool-call, retry, and changed-byte budgets;
- cancellation, idempotency, stale-write rejection, and concurrency control;
- durable versions, checkpoints where useful, and a clear rollback path;
- auditable tool calls and receipts without private reasoning or secret data;
- deterministic verification for authorization, data access, publication, and
  other externally consequential effects.

The model may select broadly useful Skills from this envelope. It cannot widen
the envelope, select another tenant, reveal credentials, bypass a failed check,
or convert untrusted page content into new authority.

## Speed and continuity requirements

Sajtagent should feel responsive even when the underlying work is long.

- The UI acknowledges the user's message immediately.
- Conversation events stream incrementally; Site must not buffer the complete
  Runtime response and database write before the browser sees the first word.
- A plain conversation does not initialize a project workspace, compute a Git
  tree, or run a build model.
- Model routing matches the task. A fast conversational turn must not use a
  deep build route merely because the build Skill is available.
- Long Skills emit bounded, truthful progress often enough that the user can
  tell the agent is active and cancel it.
- Persistence preserves event order without turning the whole turn into one
  delayed replay burst.

The product records at least these user-perceived timings:

1. message sent to `turn.accepted` received by the browser;
2. accepted to first assistant text delta;
3. accepted to first Skill event;
4. build started to verified preview ready;
5. accepted to terminal result.

Voice sessions additionally record microphone input to partial transcript,
end-of-turn speech to first audible assistant segment, barge-in to playback
stop, and stop command to execution steering receipt.

Latency goals should be set from real measurements and reported by task type.
A fast acknowledgement animation is not a substitute for a slow first real
event.

Initial UX budgets, to be validated and tightened with production evidence,
are:

- local message echo painted at p95 within 100 ms;
- first truthful server activity painted at p95 within 1 second;
- first assistant text delta for a plain conversation at p50 within 2 seconds
  and p95 within 5 seconds;
- browser event receipt to visible paint at p95 within 100 ms;
- no silent gap longer than 5 seconds during an active long-running Skill;
- end-of-turn speech to the first audible assistant segment at p95 within 2
  seconds for a voice-only conversational turn;
- barge-in to obsolete playback stopping at p95 within 250 ms, with a visible
  steering acknowledgement at p95 within 1 second.

## Architectural consequences

- Site must not preclassify every message as a build solely because the agent
  possesses the build Skill.
- A conversation policy always permits genuine assistant responses. A
  project-scoped standing mandate may also permit mutating Skills without a
  second user confirmation.
- Runtime should let the agent choose a permitted Skill from the effective
  grant. It must not force a build tool call on an ordinary conversational
  turn.
- Tool and progress events are interleaved with the same conversation instead
  of replacing assistant language with a separate hidden workflow.
- Site streams Runtime events as they arrive and persists them without waiting
  to replay the entire completed turn.
- Code and visual inspection use server-bound read tools. Browser input cannot
  choose tenant, project, workspace, credentials, or arbitrary URLs.
- Build results remain revision-bound, verified, auditable, and recoverable.
- Memory is a typed product subsystem with user controls, not an ever-growing
  raw prompt transcript.

The effective runtime grant remains:

```text
platform policy
  intersect authenticated identity and project
  intersect active user mandate version
  intersect current trigger and workspace revision
  intersect installed integrations
  intersect runtime health and per-execution hard limits
```

The important change is that a mandate can be standing and broad. It does not
need to be recreated by a confirmation click before every ordinary build step.
The derived execution and its tool grants remain short-lived even when the user
mandate persists across many turns.

## Acceptance examples

### Conversation only

User: "What do you think about the hero section?"

Expected: Sajtagent inspects relevant context when helpful, streams a reasoned
answer, may offer grounded suggestions, and creates no BuildJob merely because
a standing mutation mandate exists. A separate visible continuous goal may
continue independently, but the question itself is not its trigger.

### Direct build instruction

User: "Make the hero calmer and improve it on mobile."

Expected: the instruction itself authorizes the scoped, recoverable change.
Sajtagent acknowledges it, uses code and visual Skills, builds and verifies the
revision, repairs ordinary failures within bounds, and reports the result. No
second approval control is required.

### Material ambiguity

User: "Make the brand completely different."

Expected: Sajtagent inspects the current brand and asks a focused
counterquestion if different reasonable interpretations would produce
materially different results. It does not present a generic permission modal.

### Proactive observation

Sajtagent notices that the mobile call-to-action is obscured.

Expected: if responsive improvement is already part of the active goal, it may
repair and verify it. Otherwise it explains the concrete observation and
offers the change without silently creating an unrelated goal.

## Minimum executable acceptance criteria

The doctrine is not implemented until production-like tests prove all of the
following behaviors.

### Dynamic selection and precise site outcomes

- A scenario matrix varies both the user's instruction and the actual site
  state. It asserts scenario-specific required and forbidden Skills,
  capabilities, and tool classes; a binary answer/build router cannot pass.
- A critique that needs only rendered evidence may use visual read tools and
  answer without mutation. A scoped visual change may combine preview, code
  read, edit, check, and before/after review, while leaving unrelated tools such
  as dependency installation and publication unused.
- Tool selection is recorded with the observed evidence and exact revision.
  Removing or denying one tool produces an appropriate fallback,
  counterquestion, or bounded failure rather than a fabricated result.
- Mutation tests assert the requested observable site outcome at declared
  desktop and mobile viewports, plus relevant code/check evidence. Merely
  creating a BuildJob or receiving a success receipt is insufficient.

### Conversation and streaming

- "Do not build; explain what you see" produces `turn.accepted`, one or more
  `AssistantDelta` events, and `turn.completed(answered)`, with zero BuildJobs
  or mutating Skill events.
- Assistant text already emitted in a turn remains visible if a later Skill
  fails.
- A Skill that fails before the first assistant delta still produces this
  ordered sequence: `turn.accepted`, a truthful Skill start/failure event, one
  or more `AssistantDelta` events explaining the failure in ordinary language,
  and an independent turn completion. It never ends as only a blank canvas or
  failure card.
- Events reach the browser incrementally with stable conversation, turn,
  message and sequence IDs; reconnect resumes without loss or duplicate text.
- The initial latency budgets are measured in the browser and reported by task
  type.

### Living Builder composition

- At the 1440x900 reference viewport, the preview is the largest non-navigation
  content region and the chronological conversation plus active composer are
  visible without opening a panel. Screenshot regression covers this layout.
- DOM/E2E assertions prove that the technical detail region starts collapsed,
  raw BuildJob IDs, hashes and receipts are absent from default rendered text,
  the same conversation root remains mounted through Skill events, and the
  composer remains mounted and accepts steering input while a Skill runs.
- One compact inline Skill status is allowed in the default view.
- Listening, observing, speaking, building and reviewing states are driven by
  real events and remain stable rather than remounting the conversation.

### Code and visual understanding

- Read-only code inspection works without creating a BuildJob and cites the
  exact workspace revision, file and relevant location.
- Every visual review result is bound to an exact preview revision and declared
  viewport. Responsive changes are verified on at least mobile and desktop.
- A mutating result presents a concise changed-file or diff summary plus checks
  and rendered evidence, not a raw process log.

### Memory and continuity

- Reloading a conversation preserves editable user and project memory with its
  source, capture time and fact-versus-inference status.
- User, project and tenant isolation have negative tests.
- "Forget this" takes effect immediately for future model context and removes
  or tombstones editable memory according to the declared retention policy; it
  does not rewrite receipts or accepted revisions and the UI states what audit
  history remains.
- Open commitments are reconstructed from conversation events. Claims about
  attempted or completed work come only from matching execution events,
  receipts, and accepted revisions; corrections append provenance rather than
  editing historical evidence.

### Authority, autonomy and questions

- A direct in-scope build instruction starts the build Skill without a second
  modal or approval turn.
- A BuildJob, ToolGrant, or tool call with a missing, mismatched, expired, or
  revoked mandate version, trigger reference, base revision, or grant digest is
  rejected fail-closed before the tool acts. A mismatched ToolReceipt is rejected
  or quarantined when ingested. Both failures are visible in the audit trail and
  cannot be overridden by model output.
- A suggestion outside the mandate creates no BuildJob. A conversational "do
  it" may extend the mandate once and proceeds without another confirmation.
- Material ambiguity produces one focused counterquestion with a recommendation
  and useful options. The turn enters `waiting_for_user`; an affected execution
  enters `paused_needs_user`. Both are resumable states, not dead terminal
  process cards.
- Autonomous work stops or narrows safely on scope expansion, stale revision,
  aggregate budget exhaustion, cancellation, repeated identical failure, or a
  genuinely undelegated external effect. The last accepted revision survives.
- Every mutating execution starts in an isolated candidate hydrated from its
  exact base revision. Failed, cancelled, or stale candidates never advance the
  canonical revision pointer and never become the implicit base for the next
  job; only a verified accepted candidate advances it atomically.
- During an active build, a plain question is answered against an explicitly
  named accepted or working revision without silently retriggering the build.
  A redirect carries the target execution and observed revision, and the old
  execution is visibly paused, cancelled, or superseded before a conflicting
  write begins. A stop command prevents further tool calls; non-conflicting
  requests may queue with their order visible.

### Voice

- Voice cannot start without opt-in and a visible microphone state.
- Transcript deltas, playback, interruption, mute and stop stay synchronized;
  barge-in cancels obsolete speech and the text transcript remains usable.
- Keyboard, captions, reduced motion and text-only fallback cover the complete
  interaction.
- Browser measurements enforce the initial first-audio and barge-in budgets,
  and a voice stop produces the same execution steering receipt as text.

## Current known gap

As observed on 2026-09-02, the deployed Builder does not yet conform to this
doctrine. Site grants the build path to every turn, Runtime consequently forces
a build-only tool response, and Site buffers events before presenting them.
The result proves the build pipeline but does not provide the intended direct,
dynamic site-creation control loop.

The first corrective vertical slice is:

1. preserve broad standing project authority;
2. let a site question or design/code reasoning turn answer and stream without
   a BuildJob;
3. let the agent dynamically choose the smallest permitted Skill and tool set
   from the instruction, site state, and observed evidence;
4. let a clear build instruction invoke the Build Skill without a second
   confirmation;
5. show direct control conversation, Skill progress, preview evidence, and the
   final site result in one continuous thread;
6. lock the paths and precise site outcomes with production-like regressions
   and measured live smoke tests.

## Relationship to Sajtmaskin

Sajtmaskin remains a source of proven implementation ideas, especially around
verification, revisions, and bounded execution. It is not the desired product
personality or primary interaction model for Sajtagent.

Do not reproduce a card deck, dense process map, gate-first language, or a
console-like Builder merely because similar infrastructure already exists.
Sajtagent should expose the site, the conversation, the agent's grounded
understanding, and the result. Infrastructure remains available underneath for
trust and diagnosis.
