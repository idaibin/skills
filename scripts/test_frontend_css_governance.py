"""Focused regressions for shared frontend CSS governance."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "protocols/frontend-css-governance-v1.md"
COPIES = (
    ROOT / "skills/dev-frontend/references/frontend-css-governance.md",
    ROOT / "skills/audit-frontend/references/frontend-css-governance.md",
    ROOT / "skills/repo-review/references/frontend-css-governance.md",
)


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

    def test_generated_copies_match_protocol(self) -> None:
        expected = PROTOCOL.read_bytes()
        for copy in COPIES:
            with self.subTest(copy=copy):
                self.assertEqual(expected, copy.read_bytes())


if __name__ == "__main__":
    unittest.main()
