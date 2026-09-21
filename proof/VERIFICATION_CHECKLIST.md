# Final verification checklist

- [x] Canonical repository `BeatyXO/conditionlatch` and base commit confirmed.
- [x] Stable Studionet alias/RPC configured; Studio session chain ID and client chain definition verified as 61999 before the successful live run.
- [x] `python scripts/preflight.py` passes.
- [x] Python compilation passes.
- [x] All Direct Mode tests pass: 33 passed.
- [x] Validator dissent rejects a leader proposal.
- [x] Changed source bytes reject the leader snapshot.
- [x] TRUE/FALSE/INDETERMINATE behavior is covered.
- [x] Consecutive, K-of-N, and SPACED_TRUE deterministic timing policies are covered.
- [x] Reset increments generation; irreversible reset and creator-only reset rules are covered.
- [x] ConditionLatch deployed and finalized on Studionet; address and transaction recorded.
- [x] Immutable HTTPS source registered, condition sealed, 64-hex definition hash recorded, generation 1.
- [x] Three consensus-backed TRUE observations; rounds 1 and 2 remain ACTIVE, round 3 latches.
- [x] Final snapshot and round hashes recorded.
- [x] ConditionGate deployed against finalized ConditionLatch address and correctly pinned consumption succeeds.
- [x] Replaying the successful action is rejected by a finalized rollback.
- [x] Wrong definition hash is rejected by a finalized rollback.
- [x] Wrong generation is rejected by a finalized rollback.
- [x] Deployment evidence contains only observed addresses, transaction hashes, and revert messages.
- [x] No `.env`, private key, frontend, or generated artifact is part of the intended repository changes.
- [x] `python scripts/preflight.py --final` passes after evidence docs are updated.
- [x] Changes are committed and pushed to GitHub `main`; implementation and live proof commit: `f044d97e7f2e576017446e651831e5cc9be6ebb1`.
- [x] Final GitHub `main` HEAD is verified after the documentation update.

See `DEPLOYMENT.md` for the complete live transaction evidence.
