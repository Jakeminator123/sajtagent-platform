# Future Python backoffice

This is a placeholder for a possible operator-facing client, not a second
backend. The current `control-panel/app.py` remains read-only.

Do not add direct schema, catalog, database, deploy, or secret mutation here.
When the first real backoffice operation is chosen, it must call the same
authenticated API and validator used by the product, expose warnings and
errors consistently, and leave an auditable receipt.
