from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "control-panel"))

from flow_model import build_dot, load_flow_model, trace_impact  # noqa: E402


class FlowModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_flow_model(ROOT / "system-model" / "platform-flow-v1.json")

    def test_bottom_up_failure_reaches_user_without_skipping_controller(self) -> None:
        impacted = trace_impact(self.model, "evidence-up", "foundation.native-tools")
        self.assertIn("product.controller", impacted)
        self.assertIn("ui.builder-cards", impacted)
        self.assertEqual(impacted[-1], "user.intent")

    def test_browser_contract_never_targets_openclaw_directly(self) -> None:
        browser_edges = [
            edge
            for edge in self.model["edges"]
            if edge["from"] == "ui.builder-cards" and edge["channel"] == "intent"
        ]
        self.assertEqual([edge["to"] for edge in browser_edges], ["product.controller"])

    def test_dot_marks_failed_and_impacted_nodes(self) -> None:
        dot = build_dot(self.model, "evidence-up", "runtime.openclaw")
        self.assertIn("#dc2626", dot)
        self.assertIn("#d97706", dot)
        self.assertIn("WorkerReportV1", dot)


if __name__ == "__main__":
    unittest.main()
