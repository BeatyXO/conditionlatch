# Reviewer demo

A strong live demonstration should use the repository's immutable public fixture source so all validators can fetch exactly the same bytes.

Recommended scenario: **service outage latch with `CONSECUTIVE_TRUE = 3`.**

1. Deploy ConditionLatch on stable Studionet, chain 61999.
2. Create a condition whose criteria classify the fixture as TRUE only when the text explicitly states that the outage is current and sustained.
3. Add the immutable fixture URL and seal the condition.
4. Record the non-zero 64-hex `definition_hash` and generation `1`.
5. Submit observation #1. Verify verdict TRUE and latch false.
6. Submit observation #2. Verify verdict TRUE and latch false.
7. Submit observation #3. Verify verdict TRUE and latch true solely because the deterministic streak reached 3.
8. Deploy ConditionGate pinned to the ConditionLatch address, condition ID, definition hash, and generation 1.
9. Consume one 64-hex action hash. Verify success.
10. Attempt the same action hash again. Verify replay rejection.
11. For a resettable demonstration, use a separate condition. Latch generation 1, reset it, verify generation 2, and verify a gate pinned to generation 1 no longer sees current latch state.

Do not fake a negative transaction hash if the CLI/runtime does not expose one. Record the command, error/revert text, and any actual transaction identifier that exists.

## Canonical immutable fixture

The live TRUE fixture is pinned to clean repository commit:

`a820417c7b4fd6c74f20d621fcc4801cbeec222b`

Canonical source:

`https://raw.githubusercontent.com/BeatyXO/conditionlatch/a820417c7b4fd6c74f20d621fcc4801cbeec222b/fixtures/outage_true.txt`

Never replace the commit SHA with `main`, `master`, or `HEAD` in final proof.
