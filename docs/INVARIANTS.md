# Protocol invariants

1. **No semantic mutation after seal.** Condition text, criteria, policy parameters, and source namespace are frozen once ACTIVE.
2. **At least one frozen HTTPS source.** A condition cannot seal without a source; non-HTTPS, whitespace-bearing, and duplicate source URLs are rejected.
3. **Independent validator observation.** Validators re-fetch and re-classify; leader JSON shape alone is insufficient.
4. **Snapshot binding.** A semantic verdict cannot validate against different fetched bytes or a different availability pattern.
5. **Three-valued semantics.** Unclear, unavailable, malformed, or inadequate evidence maps to `INDETERMINATE`, never optimistic TRUE.
6. **Every hashed accepted source byte is visible to the classifier.** Accepted responses are capped at 5,000 bytes each; there is no hidden hashed tail omitted from the prompt.
7. **Storage is not captured into nondeterministic execution.** Sealed condition/source values are copied to memory before leader/validator closures run.
8. **Temporal logic is deterministic.** No LLM decides streaks, K-of-N windows, spacing, latch state, reset state, or downstream action execution.
9. **Observation history is append-only and continuously linked.** Reset does not rewrite historical rounds or erase the previous-round pointer; the next generation links back to the prior generation while temporal windows refuse to count across the generation boundary.
10. **Definition pinning.** Consumers can reject the wrong condition definition even when a numeric ID is correct.
11. **Generation pinning.** A reset invalidates old current-state claims without changing history.
12. **Irreversible means irreversible.** An irreversible latched condition cannot be reset by its creator or any other caller.
13. **Reset is creator-only.** Public observation does not imply public mutation of lifecycle authority.
14. **No post-latch observation within a generation.** Once latched, the current generation is frozen until reset when reset is allowed.
15. **K_OF_N needs a full window.** Early partial windows cannot latch.
16. **SPACED_TRUE resists rapid-call amplification.** TRUE rounds closer than the frozen minimum spacing do not advance qualification.
17. **Consumer replay protection.** ConditionGate rejects an already-consumed action hash.
18. **Consumer identity is explicit.** ConditionGate pins contract address, condition ID, definition hash, and generation before consumption.
