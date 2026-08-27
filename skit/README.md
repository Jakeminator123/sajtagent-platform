# Disposable scratch space

This folder is for temporary local experiments that do not belong to a product
repository. Everything else in this folder is ignored by Git.

Tool-owned caches such as `.next/`, `node_modules/`, `.ruff_cache/`, and
`__pycache__/` should stay in their conventional locations and be ignored
there. Do not move them here: many tools depend on those standard paths.

Do not store secrets, unique work, customer data, or the only copy of an
artifact here.
