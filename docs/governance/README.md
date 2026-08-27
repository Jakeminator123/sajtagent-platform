# Governance contracts

Status: proposal boundary; add concrete files only with the first consumer.

This area will hold shared machine-readable constraints, not product runtime
code and not a second copy of each child repository's types.

## Intended folders

- `schemas/` — versioned JSON Schemas and valid/invalid fixtures for exchanged
  artifacts such as `BuildJob` and `BuildResult`.
- `policies/` — reviewable platform policy declarations. Server code remains
  responsible for enforcing them; prompt text is never the enforcement layer.
- `manifest/` — a small versioned index of published contract or catalog
  artifacts. Generated projections must name their generator and owner.

Do not add a schema merely to fill the folder. The first schema should be
created alongside a real producer, a real consumer, compatibility tests, and a
clear versioning rule.

## Validation path

The same validator must run at every entry point: local backoffice, CI, API
ingestion, and catalog publication. A UI warning is helpful but cannot replace
server-side rejection.

Use three outcomes:

- error — unsafe or structurally invalid; block publication;
- warning — valid but risky or incomplete; require visible acknowledgement;
- information — useful context with no gate effect.

A future writable backoffice must call the same domain/API validation path as
the product. It must not patch registries, unions, or generated files directly.
