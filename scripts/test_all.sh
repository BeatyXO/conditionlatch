#!/usr/bin/env bash
set -euo pipefail
python scripts/preflight.py
python -m compileall -q contracts tests scripts
pytest -q
