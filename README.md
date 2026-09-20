# ConditionLatch

**ConditionLatch is a standalone GenLayer Intelligent Contract primitive for turning noisy semantic observations into stable, generation-pinned temporal facts.**

Many contracts can identify a real-world condition once. Far fewer can answer the safer question: **has that condition been observed often, recently, or far enough apart to become actionable contract state?** ConditionLatch separates those two jobs.

Validators perform one narrow semantic task per round: independently fetch the condition's frozen HTTPS source set and classify the current observation as `TRUE`, `FALSE`, or `INDETERMINATE`. The Intelligent Contract never asks an LLM whether to trigger an action. Instead, deterministic policy code decides whether the observation history satisfies one of three temporal policies:

- `CONSECUTIVE_TRUE`: latch only after K uninterrupted TRUE rounds.
- `K_OF_N`: latch only when at least K of the latest N rounds are TRUE, after a complete N-round window exists.
- `SPACED_TRUE`: latch only after K TRUE rounds separated by at least a frozen minimum interval.

A sealed condition has a frozen `definition_hash` covering its semantic condition, evaluation criteria, temporal policy, and source namespace. Resettable conditions also carry a monotonically increasing `generation`. Consumers must pin **both** values, preventing a latch from one lifecycle from being silently reused after reset.

## Why GenLayer belongs here

A conventional contract can count rounds and timestamps, but it cannot reliably interpret changing public evidence such as an incident page, official announcement, court docket, procurement notice, project status page, or other unstructured source. GenLayer handles only that semantic observation step. Everything about temporal qualification, latching, reset behavior, replay protection, and consumer compatibility remains deterministic.

The leader does not receive a privileged truth oracle. Every validator independently re-fetches the same frozen source URLs, independently re-runs the bounded semantic classifier, and verifies both the resulting verdict and the exact source snapshot hash. Changed source bytes therefore cannot validate a leader proposal from another snapshot.

## Repository boundary

Canonical repository: `https://github.com/BeatyXO/conditionlatch`

This is a contract-only submission. **There is no frontend.**

- `contracts/condition_latch.py` — primary reusable primitive.
- `contracts/condition_gate.py` — minimal typed IC-to-IC consumer proving composability and replay protection.
- `tests/direct/` — invariant-focused Direct Mode tests.
- `docs/` — architecture, invariants, threat model, and reviewer walkthrough.
- `scripts/preflight.py` — repository/network/security hygiene gate.

## Core lifecycle

1. Creator calls `create_condition(...)` with semantic criteria and a temporal policy.
2. Creator adds one to five bounded HTTPS sources while the condition is `DRAFT`.
3. Creator calls `seal_condition(...)`. The source namespace and definition hash become immutable.
4. Anyone may call `observe(...)` while the generation is active.
5. Validators independently fetch and classify the frozen source set.
6. The contract appends an immutable observation round and deterministically evaluates the temporal policy.
7. Once the policy qualifies, the generation becomes `LATCHED`.
8. Another IC can call `is_latched(condition_id, expected_definition_hash, expected_generation)`.
9. If the condition was configured resettable, only the creator may reset a latched generation. History remains intact and the generation increments.

## Safety properties

ConditionLatch deliberately fails closed. Missing sources, malformed model output, conflicting evidence, or inadequate evidence must resolve to `INDETERMINATE` rather than an optimistic TRUE. For the consecutive policy, both FALSE and INDETERMINATE break the streak. For `K_OF_N`, INDETERMINATE occupies a slot but does not count as TRUE. For `SPACED_TRUE`, only sufficiently separated TRUE observations advance qualification.

Exact source snapshot binding is intentionally strict. Each frozen source is capped at 5,000 bytes, and every accepted byte is included in the classifier prompt; the contract never hashes source bytes that the classifier did not receive. Highly dynamic pages may reduce liveness because a validator seeing different bytes will reject the leader's observation. That is preferable to silently certifying an observation against different evidence. Integrators should choose focused stable endpoints or immutable snapshots when possible. HTTP failures, oversized bodies, empty responses, and unusable model output fail closed to `INDETERMINATE`.

## Network target

The submission target is stable Studionet only:

- network alias: `studionet`
- chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`

Do not migrate this repository to another network merely to simplify testing.

## Local checks

Requires Python 3.12+.

```bash
python -m pip install -r requirements-test.txt
python scripts/preflight.py
python -m compileall -q contracts tests scripts
pytest -q
```

`genlayer-test==0.29.2` is pinned because it is the latest stable PyPI release at the time this handoff was prepared. Pre-release testing-suite versions should not be introduced unless a real stable Studionet incompatibility proves they are necessary.

## Verification flow

GitHub Actions runs the pinned Direct Mode suite on every push. The repository also includes a full Studionet lifecycle test, an immutable-fixture pinning script, `preflight.py`, and `preflight.py --final`. Live deployment evidence is intentionally kept out of documentation until a real Studionet run produces it.
