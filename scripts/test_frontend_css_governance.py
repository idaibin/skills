"""Focused regressions for shared frontend CSS governance."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "protocols/frontend-css-governance-v1.md"

class FrontendCssGovernanceTests(unittest.TestCase):
    def test_protocol_covers_contract_ownership_and_runtime_closure(self) -> None:
        text = PROTOCOL.read_text(encoding="utf-8")
        for marker in (
            "Contract And Correction Gate",
            "page-edge inset and one owner supplies each internal gap",
            "Do not add element-level `opacity`",
            "same-viewport/state runtime",
            "A wrapper MUST",
        ):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
