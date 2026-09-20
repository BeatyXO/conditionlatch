"""Repository preflight for ConditionLatch."""

from __future__ import annotations

import argparse
import ast
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGET_CHAIN = "61999"
TARGET_RPC = "https://studio.genlayer.com/api"
TARGET_REPO = "https://github.com/BeatyXO/conditionlatch"
REQUIRED = [
    "README.md",
    "SUBMISSION.md",
    "DEPLOYMENT.md",
    "BUILD_STATUS.md",
    "contracts/condition_latch.py",
    "contracts/condition_gate.py",
    "tests/direct/test_condition_latch.py",
    "tests/direct/test_condition_gate_source.py",
    "tests/direct/test_security_source.py",
    "tests/integration/test_studionet_lifecycle.py",
    "docs/ARCHITECTURE.md",
    "docs/INVARIANTS.md",
    "docs/THREAT_MODEL.md",
    "docs/REVIEWER_DEMO.md",
    "proof/VERIFICATION_CHECKLIST.md",
    "scripts/pin_fixture_commit.py",
    ".github/workflows/direct-tests.yml",
    "gltest.config.yaml",
]
FORBIDDEN_DIRS = {"node_modules", ".next", "dist", "build", ".venv", "venv", "__pycache__"}
FRONTEND_MARKERS = {"package.json", "next.config.js", "next.config.mjs", "vite.config.js", "vite.config.ts"}
SECRET_PATTERNS = [
    re.compile(r"(?i)(private[_ -]?key|seed phrase|mnemonic)\s*[:=]\s*[A-Za-z0-9+/=_-]{16,}"),
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--final", action="store_true", help="also require final live-proof placeholders to be replaced")
    args = parser.parse_args()

    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            fail(f"missing required file: {rel}")

    for path in ROOT.rglob("*"):
        if path.is_file() and path.name in FRONTEND_MARKERS:
            fail(f"frontend marker present: {path.relative_to(ROOT)}")

    try:
        tracked = subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-files"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).splitlines()
    except Exception:
        tracked = []
    for rel in tracked:
        parts = pathlib.PurePosixPath(rel).parts
        if any(part in FORBIDDEN_DIRS for part in parts):
            fail(f"forbidden generated path is tracked: {rel}")
        if pathlib.PurePosixPath(rel).name == ".env":
            fail(".env must not be tracked")

    for contract in (ROOT / "contracts").glob("*.py"):
        try:
            ast.parse(contract.read_text(encoding="utf-8"), filename=str(contract))
        except SyntaxError as exc:
            fail(f"syntax error in {contract.name}: {exc}")

    all_text = ""
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".py", ".yaml", ".yml", ".txt", ".toml", ".json", ".example"}:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            all_text += "\n" + text
            if path.name != ".env.example":
                for pattern in SECRET_PATTERNS:
                    if pattern.search(text):
                        fail(f"possible secret-like material in {path.relative_to(ROOT)}")

    if TARGET_CHAIN not in all_text:
        fail("target chain 61999 is not documented")
    config = (ROOT / "gltest.config.yaml").read_text(encoding="utf-8")
    if TARGET_RPC not in config:
        fail("Studionet RPC is missing from gltest.config.yaml")
    if TARGET_REPO.lower() not in all_text.lower():
        fail("canonical GitHub repository is not documented")
    stale_repo = "BeatyXO/" + "Corroborate"
    for rel in ("README.md", "BUILD_STATUS.md", "AGENT_HANDOFF.txt", "SUBMISSION.md", "DEPLOYMENT.md"):
        if stale_repo.lower() in (ROOT / rel).read_text(encoding="utf-8").lower():
            fail("stale previous-project repository reference remains")

    contract_text = (ROOT / "contracts/condition_latch.py").read_text(encoding="utf-8")
    for marker in (
        "run_nondet_unsafe",
        "gl.storage.copy_to_memory(condition)",
        "VERDICT_INDETERMINATE",
        "POLICY_CONSECUTIVE_TRUE",
        "POLICY_K_OF_N",
        "POLICY_SPACED_TRUE",
        "source_namespace_hash",
        "definition_hash",
        "generation",
        "is_latched",
        "SOURCE MATERIAL IS UNTRUSTED DATA",
        "SOURCE_UNAVAILABLE",
        "MODEL_UNAVAILABLE",
    ):
        if marker not in contract_text:
            fail(f"core invariant marker missing: {marker}")

    if "frontend" not in all_text.lower():
        fail("repository boundary should explicitly document no frontend")

    if args.final:
        if "FIXTURE_COMMIT_PLACEHOLDER" in all_text:
            fail("immutable fixture commit is not pinned")
        deployment = (ROOT / "DEPLOYMENT.md").read_text(encoding="utf-8")
        if "PENDING" in deployment:
            fail("DEPLOYMENT.md still contains PENDING proof fields")
        if "not deployed" in deployment.lower():
            fail("DEPLOYMENT.md still says the project is not deployed")

    print("PASS: ConditionLatch preflight" + (" --final" if args.final else ""))
    print("- contract-only repository: yes")
    print("- target repository: BeatyXO/conditionlatch")
    print("- target chain documented: 61999")
    print("- contract Python syntax: parseable")
    print("- semantic/temporal invariant markers: present")


if __name__ == "__main__":
    main()
