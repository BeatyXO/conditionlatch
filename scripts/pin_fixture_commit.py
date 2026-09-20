"""Pin immutable raw GitHub fixture URLs to a real 40-char commit SHA."""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLACEHOLDER = "FIXTURE_COMMIT_PLACEHOLDER"


def main() -> None:
    if len(sys.argv) != 2 or not re.fullmatch(r"[0-9a-fA-F]{40}", sys.argv[1]):
        raise SystemExit("usage: python scripts/pin_fixture_commit.py <40-char-commit-sha>")
    sha = sys.argv[1].lower()
    targets = [
        ROOT / "tests/integration/test_studionet_lifecycle.py",
        ROOT / "docs/REVIEWER_DEMO.md",
        ROOT / "DEPLOYMENT.md",
    ]
    changed = 0
    for path in targets:
        text = path.read_text(encoding="utf-8")
        if PLACEHOLDER in text:
            path.write_text(text.replace(PLACEHOLDER, sha), encoding="utf-8")
            changed += 1
    if changed == 0:
        raise SystemExit("fixture placeholder not found; repository may already be pinned")
    print(f"Pinned fixture commit {sha} in {changed} files")


if __name__ == "__main__":
    main()
