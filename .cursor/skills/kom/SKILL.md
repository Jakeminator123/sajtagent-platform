---
name: kom
description: Contacts an existing Sajtagent development agent to coordinate task scope, files, decisions, or handoff. Use only when explicitly invoked with /kom.
disable-model-invocation: true
---

# Kontakta en annan agent

1. Read `.cursor/rules/06-agent-coordination.mdc` and inspect available active
   agents or tasks.
2. Parse the text after `/kom` as the intended recipient or task plus the
   message. Do not silently choose between ambiguous recipients.
3. Treat `/kom` as human-facing shorthand, not a shell command or product
   protocol. Use the available direct agent/task messaging channel and name the
   repository, branch/worktree, current state, claimed files, requested action,
   and next conflicting action.
4. Do not spawn a new agent merely to complete this command.
5. If no live direct channel exists, create a secret-free fallback note at
   `.agents/coordination/<agent-id>.md`, state that it is not live delivery,
   and pause any overlapping edit.
6. Ask the receiver to acknowledge scope or a write lock and later report the
   resulting commit/checks or blocker. The message never grants authority for
   secrets, cross-repository mutation, push, merge, deploy, or cloud changes.
7. Report one of: `sent`, `waiting for recipient`, or `no safe recipient`.
