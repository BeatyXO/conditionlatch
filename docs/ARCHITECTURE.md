# Architecture

## Separation of semantic and deterministic authority

ConditionLatch has two layers by design.

**Semantic layer:** one observation round asks validators to classify the frozen condition against the frozen source set as `TRUE`, `FALSE`, or `INDETERMINATE`. The leader fetches all sources and proposes a bounded result. Validators independently re-fetch the same URLs and independently classify them. Agreement requires the same bounded verdict and the same aggregate snapshot hash.

**Deterministic layer:** the contract alone owns temporal policy. No model chooses a threshold, changes the policy, decides whether to latch, resets a condition, or authorizes a downstream action.

## Definition sealing

Conditions begin in `DRAFT`. Sources may be added only during draft. `seal_condition` hashes:

- title;
- semantic condition text;
- evaluation criteria;
- policy code;
- required TRUE count;
- K-of-N window size;
- spacing parameter;
- irreversible/resettable flag;
- ordered source namespace hash.

The resulting `definition_hash` is immutable for that condition. This gives consumers a stable semantic identity rather than trusting only a numeric condition ID.

## Source snapshots

For each observation round, each source body is capped at 5,000 bytes. Every accepted byte is both hashed and included in the semantic prompt, so the contract never commits to unseen source tail data. The ordered URL+availability+digest material is hashed again into one `snapshot_hash`. Before entering the nondeterministic block, sealed storage-backed condition/source data is copied into ordinary memory. Validators independently fetch from that frozen in-memory namespace and verify that their byte snapshot and semantic verdict match the leader's.

HTTP errors, empty bodies, oversized bodies, or model failures produce `INDETERMINATE` rather than optimistic TRUE. This strict binding intentionally prefers safety over liveness on unstable pages.

## Temporal policies

### CONSECUTIVE_TRUE

The contract increments `current_streak` only for TRUE. FALSE and INDETERMINATE both reset the streak to zero. Latching occurs at `current_streak >= required_true`.

### K_OF_N

The contract walks backward through the current generation's append-only observation chain. No latch is possible until a complete N-round window exists. It then counts TRUE rounds in that exact window and latches when the count is at least K.

### SPACED_TRUE

A TRUE round qualifies only when it is the first qualifying TRUE or occurs at least `min_separation_seconds` after the previous qualifying TRUE. Close repeated calls cannot manufacture temporal independence.

## Generations

A resettable condition may be reset only after it has latched and only by its creator. Reset does not rewrite, delete, or unlink any observation. It increments `generation`, returns status to ACTIVE, and resets only current-generation counters. The next round still points to the last round from the previous generation, while window evaluation stops when it reaches a different generation.

Consumers therefore pin `(condition_id, definition_hash, generation)`. A gate pinned to generation 1 fails after reset to generation 2 even though the condition definition itself did not change.

## Consumer proof

`ConditionGate` is deliberately small. It performs a typed IC-to-IC view call to `is_latched(...)` and records one consumption keyed by a 64-hex `action_hash`. Duplicate action hashes are rejected. This demonstrates that ConditionLatch is a reusable primitive rather than a closed demo.
