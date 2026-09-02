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
environment, trace ID, conversation/turn/message IDs where applicable,
project/Skill/execution/job IDs where applicable, a monotonic event sequence,
actor type, component, outcome, duration, and schema version. Provider request
IDs and model usage may be attached when available.

Every mutating `BuildJob`, `ToolGrant`, tool call, and corresponding
`ToolReceipt` must additionally carry the authorization proof used for that
operation: mandate ID and version, trigger reference, exact base revision, and
grant ID plus digest. Runtime rejects a missing field, mismatch, expiry, or
revoked mandate on the job, grant, or tool call before the tool acts. It
validates the receipt when ingested and rejects or quarantines a mismatch.
Receipts preserve the validated values so an audit can prove why the operation
was allowed without logging credentials.

User-perceived latency also needs browser-received and browser-painted times.
Voice adds audio-start, transcript-delta, playback-start, interruption, and
playback-complete times. Client clocks are not authoritative server time, but
they are required to explain what the interaction actually felt like.

Never log API keys, authorization headers, raw environment variables, customer
secrets, private chain-of-thought, or unrestricted source archives. Redaction
must happen before durable storage. Product data, audit events, metrics, traces,
and disposable debug logs have different retention and access policies; do not
pretend that one giant log stream gives complete observability.
