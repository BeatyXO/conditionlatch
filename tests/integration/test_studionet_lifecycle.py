"""Stable Studionet lifecycle proof for ConditionLatch.

This test is intentionally excluded from normal CI. Run explicitly with:
    gltest tests/integration/test_studionet_lifecycle.py -v -s --network studionet

The fixture URL is pinned to an immutable Git commit before final live proof.
"""

from __future__ import annotations

import hashlib

from gltest import get_contract_factory
from gltest.assertions import tx_execution_failed, tx_execution_succeeded

FIXTURE_COMMIT = "a820417c7b4fd6c74f20d621fcc4801cbeec222b"
FIXTURE_TRUE_URL = (
    "https://raw.githubusercontent.com/BeatyXO/conditionlatch/"
    + FIXTURE_COMMIT
    + "/fixtures/outage_true.txt"
)


def _tx_hashish(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def test_conditionlatch_full_studionet_lifecycle(default_account):
    assert len(FIXTURE_COMMIT) == 40 and "PLACEHOLDER" not in FIXTURE_COMMIT

    latch_factory = get_contract_factory("ConditionLatch")
    latch = latch_factory.deploy(account=default_account, consensus_max_rotations=5)
    assert latch.address is not None

    # Fresh deployment -> first created condition is ID 1.
    create_tx = latch.create_condition(
        args=[
            "Sustained outage proof",
            "The supplied immutable status evidence states that the monitored service is presently experiencing a sustained outage.",
            "TRUE only when the supplied source explicitly says the outage is current and sustained. FALSE only when it explicitly says service is restored or normal. Otherwise INDETERMINATE.",
            1,  # CONSECUTIVE_TRUE
            3,
            0,
            0,
            True,
        ]
    ).transact(consensus_max_rotations=5)
    assert tx_execution_succeeded(create_tx)

    source_tx = latch.add_source(args=[1, FIXTURE_TRUE_URL]).transact(
        consensus_max_rotations=5,
    )
    assert tx_execution_succeeded(source_tx)

    seal_tx = latch.seal_condition(args=[1]).transact(
        consensus_max_rotations=5,
    )
    assert tx_execution_succeeded(seal_tx)

    definition_hash = latch.current_definition_hash(args=[1]).call()
    assert isinstance(definition_hash, str) and len(definition_hash) == 64
    assert latch.current_generation(args=[1]).call() == 1
    assert latch.is_latched(args=[1, definition_hash, 1]).call() is False

    observation_receipts = []
    for index in range(3):
        tx = latch.observe(args=[1]).transact(
            consensus_max_rotations=5,
            wait_interval=1500,
            wait_retries=40,
        )
        assert tx_execution_succeeded(tx)
        observation_receipts.append(tx)
        state = latch.get_condition(args=[1]).call()
        if index < 2:
            assert state["status_name"] == "ACTIVE"
            assert latch.is_latched(args=[1, definition_hash, 1]).call() is False
        else:
            assert state["status_name"] == "LATCHED"
            assert latch.is_latched(args=[1, definition_hash, 1]).call() is True
            final_obs = latch.get_observation(args=[state["last_round_id"]]).call()
            assert len(final_obs["snapshot_hash"]) == 64
            assert len(final_obs["round_hash"]) == 64

    gate_factory = get_contract_factory("ConditionGate")
    gate = gate_factory.deploy(
        args=[str(latch.address), 1, definition_hash, 1],
        account=default_account,
        consensus_max_rotations=5,
    )
    assert gate.address is not None

    action_hash = _tx_hashish("conditionlatch-live-gate-action-v1")
    allowed = gate.consume(args=[action_hash]).transact(
        consensus_max_rotations=5,
    )
    assert tx_execution_succeeded(allowed)

    replay = gate.consume(args=[action_hash]).transact(
        consensus_max_rotations=5,
    )
    assert tx_execution_failed(replay)

    # Direct pinned-state negatives are deterministic views on the deployed latch.
    assert latch.is_latched(args=[1, "f" * 64, 1]).call() is False
    assert latch.is_latched(args=[1, definition_hash, 2]).call() is False
