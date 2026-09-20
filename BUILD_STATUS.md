# Build status

Canonical repository: `https://github.com/BeatyXO/conditionlatch`

## Implemented before live deployment

- primary ConditionLatch contract;
- DRAFT → ACTIVE → LATCHED lifecycle;
- frozen source namespace and 64-hex definition hash;
- TRUE / FALSE / INDETERMINATE semantic vocabulary;
- storage-to-memory copying before nondeterministic execution;
- independent leader/validator source re-fetch and semantic re-evaluation;
- exact source snapshot binding;
- 5,000-byte per-source bound with no hidden/unprompted hashed tail;
- fail-closed HTTP, empty/oversized response, and model-error handling;
- prompt-injection boundary that treats source material as untrusted evidence;
- deterministic CONSECUTIVE_TRUE, K_OF_N, and SPACED_TRUE policies;
- append-only observation links preserved across reset generations;
- irreversible and resettable modes with generation overflow guard;
- generation invalidation after reset;
- typed `is_latched` consumer interface;
- ConditionGate typed IC-to-IC consumer with pinned definition/generation, replay protection, and consumption event;
- expanded Direct Mode adversarial tests;
- GitHub Actions Direct Mode workflow;
- full Studionet lifecycle integration test;
- immutable fixture pinning script;
- normal and final repository preflight;
- stable Studionet / chain 61999 network configuration;
- no frontend.

## Remaining live-only proof

The only evidence that must not be fabricated is the actual stable Studionet deployment/lifecycle proof: finalized addresses, transaction evidence, live observation hashes, gate success/rejection evidence, and final post-deployment documentation. `DEPLOYMENT.md` remains explicit about these fields until they are produced.
