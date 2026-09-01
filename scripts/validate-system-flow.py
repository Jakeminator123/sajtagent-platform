"""Validate the canonical Sajtagent platform flow model."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "control-panel"))

from flow_model import load_flow_model  # noqa: E402


def main() -> None:
    model = load_flow_model(ROOT / "system-model" / "platform-flow-v1.json")
    print(
        "OK: "
        f"{len(model['nodes'])} nodes, {len(model['edges'])} edges, "
        f"{len(model['views'])} acyclic views"
    )


if __name__ == "__main__":
    main()
