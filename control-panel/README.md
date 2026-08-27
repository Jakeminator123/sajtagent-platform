# Sajtagent Platform control panel

This is a local, read-only Streamlit view of the platform's repository and
architecture boundaries. It does not own production state, privileged model
access, deployment, or customer project execution.

From the platform root on Windows:

```powershell
py -m venv control-panel\.venv
.\control-panel\.venv\Scripts\python.exe -m pip install -r control-panel\requirements.txt
.\control-panel\.venv\Scripts\python.exe control-panel\app.py
```

The script relaunches itself through Streamlit when run directly.

The future `python-backoffice/` area is intentionally not implemented yet. A
writable backoffice must use the same authenticated validation and domain APIs
as the product; it must not make direct production or catalog file edits.
