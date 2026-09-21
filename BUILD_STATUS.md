# Build and verification status

Canonical repository: `https://github.com/BeatyXO/conditionlatch`

## Verified implementation

- ConditionLatch preserves the frozen source namespace, immutable definition hash, independent validator re-fetch and semantic evaluation, exact source snapshot binding, fail-closed `INDETERMINATE` behavior, deterministic temporal policies, append-only history, generation invalidation, reset rules, and typed IC-to-IC `is_latched` interface.
- ConditionGate uses a typed IC-to-IC call pinned to condition ID, definition hash, and generation, and rejects replayed action hashes.
- No frontend is included.

## Runtime compatibility fixes

- Stable GenLayer events require keyword blob fields in the event constructor before calling `.emit()`; all contract events now follow this API.
- Stable `nondet.web.Response` exposes HTTP status as `.status`; source availability checks now use that field and fail closed on non-2xx responses.
- The Studio schema fallback in the pinned Python client hex-encodes contract source as ASCII. Non-ASCII punctuation in contract module docstrings prevented schema retrieval; those docstrings now use ASCII punctuation.
- ConditionGate deployment requires the constructor address argument to be encoded as `CalldataAddress`. The lifecycle now passes that typed value instead of a plain string.
- Direct Mode time-warp tests now synchronize the transaction message timestamp as well as the test clock. Contract temporal logic remains unchanged.

## Test and live results

- Dependency: `genlayer-test==0.29.2` (already installed).
- Direct Mode: `python -m pytest tests/direct -q` — **33 passed**.
- Python compilation: `python -m compileall -q contracts tests scripts` — **PASS**.
- Standard preflight: `python scripts/preflight.py` — **PASS**.
- Stable Studionet lifecycle: `gltest tests/integration/test_studionet_lifecycle.py -v -s --network studionet` — **1 passed** on Studionet chain 61999.
- Full deployment and rejection evidence is recorded in `DEPLOYMENT.md`.
- Commit containing the verified runtime fixes and lifecycle proof: `f044d97e7f2e576017446e651831e5cc9be6ebb1`.

## Final gate

`python scripts/preflight.py --final` checks the fixture pin and requires deployment evidence to be populated. It does not validate or generate a Git commit SHA; record the resulting GitHub HEAD in the release record after pushing.
