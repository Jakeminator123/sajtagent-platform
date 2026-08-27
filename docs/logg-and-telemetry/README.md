# Logging and telemetry

Status: accepted boundary; storage and vendor are undecided.

This folder documents observability. Runtime logs must not be committed here or
spread into one Git folder per service.

## One event, two views

Keep one structured, access-controlled event stream and derive two views:

- **raw** — short-retention diagnostic payload for restricted operators;
- **readable** — redacted summaries for users, support, and normal debugging.

These are storage/access views, not `RAW/` and `READABLE/` directories copied
through the repositories. The readable view must remain traceable to an event
ID without exposing raw secrets or private model content.

## Minimal event envelope

Every cross-system event should eventually carry a timestamp, event name,
environment, trace ID, project/job IDs where applicable, actor type, component,
outcome, duration, and schema version. Provider request IDs and model usage may
be attached when available.

Never log API keys, authorization headers, raw environment variables, customer
secrets, private chain-of-thought, or unrestricted source archives. Redaction
must happen before durable storage. Product data, audit events, metrics, traces,
and disposable debug logs have different retention and access policies; do not
pretend that one giant log stream gives complete observability.
