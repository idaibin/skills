#!/usr/bin/env python3
"""Focused synthetic check for the live-Agent fixture."""

from __future__ import annotations

import argparse
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("--expect", choices=("panel", "surface"), required=True)
args = parser.parse_args()
source = Path(__file__).parent / "src/components/neutral-panel.ts"
test = Path(__file__).parent / "src/components/neutral-panel.test.ts"
expected = f"data-neutral-{args.expect}"
other = "data-neutral-surface" if args.expect == "panel" else "data-neutral-panel"
for path in (source, test):
    text = path.read_text(encoding="utf-8")
    if expected not in text or other in text:
        raise SystemExit(f"{path.name} does not match {expected}")
