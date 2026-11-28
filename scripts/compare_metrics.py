"""Compare metrics with a baseline and fail when AUC drops too much.

Usage: python scripts/compare_metrics.py BASELINE NEW [--max-drop 0.02] [--markdown FILE]
"""

import argparse
import json
import sys
from pathlib import Path

MARKER = "<!-- ml-metrics -->"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("baseline")
    ap.add_argument("new")
    ap.add_argument("--max-drop", type=float, default=0.02)
    ap.add_argument("--markdown")
    a = ap.parse_args()
    base = json.loads(Path(a.baseline).read_text())
    new = json.loads(Path(a.new).read_text())

    rows = [f"| {k} | {base[k]:.4f} | {new[k]:.4f} | {new[k] - base[k]:+.4f} |"
            for k in ("auc", "accuracy")]
    drop = base["auc"] - new["auc"]
    ok = drop <= a.max_drop
    verdict = ("PASS: no AUC regression" if ok
               else f"FAIL: AUC dropped by {drop:.4f} (allowed {a.max_drop})")
    md = "\n".join([MARKER, "### Model evaluation", "",
                    "| metric | baseline | this commit | change |", "|---|---|---|---|",
                    *rows, "", f"**{verdict}**"])
    print(md)
    if a.markdown:
        Path(a.markdown).write_text(md + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
