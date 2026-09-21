# Submission

Canonical repository: `https://github.com/BeatyXO/conditionlatch`

## Title
ConditionLatch — Consensus-Backed Temporal Trigger Primitive

## Short description
ConditionLatch converts repeated semantic observations of real-world public evidence into stable, deterministic latch state. GenLayer validators independently fetch a frozen source set and classify each round as TRUE, FALSE, or INDETERMINATE. The contract itself applies one of three deterministic policies—consecutive TRUE, K-of-N, or spaced TRUE—so an LLM never decides whether an action should trigger. Sealed definition hashes prevent semantic substitution, append-only rounds preserve audit history, and resettable conditions increment a generation so old latch state cannot be silently replayed. A minimal ConditionGate contract demonstrates typed IC-to-IC consumption and action replay protection. The primitive can be reused for SLAs, insurance conditions, governance safeguards, milestone monitoring, operational incidents, and other systems that need semantic evidence to persist strongly enough before becoming actionable.

## Submission boundary
Contract-only standalone Intelligent Contract primitive. No frontend.

## Verification evidence

- Direct Mode: `python -m pytest tests/direct -q` — **33 passed**.
- Stable Studionet: `gltest tests/integration/test_studionet_lifecycle.py -v -s --network studionet` — **1 passed**, chain ID `61999`.
- Finalized contract addresses, definition hash, observation hashes, and transaction/revert evidence are recorded in `DEPLOYMENT.md`.
- Final GitHub commit: record the 40-character `main` HEAD after the completed push.
