# Threat model

## Malicious leader

A leader may attempt to return syntactically valid but false JSON. Validators do not validate only shape. They independently fetch and classify the source set and compare the bounded verdict.

A leader may attempt to classify one source snapshot while attaching a different evidence hash. Validators independently compute the aggregate snapshot hash, so this proposal is rejected.

## Dynamic or adversarial web content

A source can change between leader and validator execution. ConditionLatch fails closed because exact snapshot hashes differ. This may reduce liveness but does not silently merge distinct evidence states.

A source can return excessive data. Each response is capped at 5,000 bytes. An oversized, empty, or non-2xx response is represented by a stable unavailable sentinel and forces the round to `INDETERMINATE`; exception text is never hashed because provider/runtime messages can differ across nodes.

A source can disappear or fail. The observation can still finalize fail-closed as `INDETERMINATE` when nodes agree on unavailability; if nodes see different availability/bytes, exact snapshot mismatch rejects consensus.

## Malformed or prompt-injected source text

The classifier prompt explicitly limits authority to the frozen condition and criteria. Source text is evidence, not instructions. Malformed model output canonicalizes to INDETERMINATE. Direct Mode coverage includes adversarial source text that attempts to order an immediate latch/action; even when the semantic round is TRUE, deterministic threshold logic still controls whether the condition can latch.

## Temporal gaming

Rapid repeated calls cannot satisfy `SPACED_TRUE`; transaction timestamps enforce the frozen minimum interval. `CONSECUTIVE_TRUE` breaks on FALSE or INDETERMINATE. `K_OF_N` does not use a partial window.

## Stale-consumer replay

A reset increments generation. A downstream consumer pinned to an earlier generation stops seeing the condition as currently latched. ConditionGate separately blocks duplicate `action_hash` consumption.

## Creator abuse

The creator controls definition construction and reset permission for resettable conditions. The creator cannot alter a sealed definition or erase observations. Integrators should decide whether a resettable or irreversible condition fits their use case before sealing.
