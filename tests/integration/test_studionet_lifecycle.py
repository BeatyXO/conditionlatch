"""Stable Studionet lifecycle proof for ConditionLatch.

This test is intentionally excluded from normal CI. Run explicitly with:
    gltest tests/integration/test_studionet_lifecycle.py -v -s --network studionet

The fixture URL is pinned to an immutable Git commit before final live proof.
"""

from __future__ import annotations

import hashlib

from gltest import get_contract_factory
from gltest.assertions import tx_execution_failed, tx_execution_succeeded
from genlayer_py.types import CalldataAddress
from gltest.utils import extract_contract_address

FIXTURE_COMMIT = "a820417c7b4fd6c74f20d621fcc4801cbeec222b"
FIXTURE_TRUE_URL = (
    "https://raw.githubusercontent.com/BeatyXO/conditionlatch/"
    + FIXTURE_COMMIT
    + "/fixtures/outage_true.txt"
)


def _tx_hashish(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _report_receipt(label: str, receipt) -> None:
    consensus = receipt.get("consensus_data", {})
    leader_receipts = consensus.get("leader_receipt", [])
    leader = leader_receipts[0] if leader_receipts else {}
    genvm = leader.get("genvm_result", {})
    result = leader.get("result", {})
    error = genvm.get("stderr") or result.get("payload", "")
    print(
        f"EVIDENCE {label}: tx={receipt.get('hash')} "
        f"status={receipt.get('status_name')} "
        f"execution={leader.get('execution_result')} "
        f"error={error[:500]}"
    )


def _deploy(factory, args, account, label):
    receipt = factory.deploy_contract_tx(
        args=args,
        account=account,
        consensus_max_rotations=5,
    )
    _report_receipt(label, receipt)
    assert tx_execution_succeeded(receipt)
    address = extract_contract_address(receipt)
    return factory.build_contract(contract_address=address, account=account)


def test_conditionlatch_full_studionet_lifecycle(default_account):
    assert len(FIXTURE_COMMIT) == 40 and "PLACEHOLDER" not in FIXTURE_COMMIT

    latch_factory = get_contract_factory("ConditionLatch")
    latch = _deploy(latch_factory, None, default_account, "ConditionLatch deploy")
    assert latch.address is not None
    print(f"EVIDENCE ConditionLatch address={latch.address}")

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
    _report_receipt("condition create", create_tx)
    assert tx_execution_succeeded(create_tx)

    source_tx = latch.add_source(args=[1, FIXTURE_TRUE_URL]).transact(
        consensus_max_rotations=5,
    )
    _report_receipt("source registration", source_tx)
    assert tx_execution_succeeded(source_tx)

    seal_tx = latch.seal_condition(args=[1]).transact(
        consensus_max_rotations=5,
    )
    _report_receipt("condition seal", seal_tx)
    assert tx_execution_succeeded(seal_tx)

    definition_hash = latch.current_definition_hash(args=[1]).call()
    assert isinstance(definition_hash, str) and len(definition_hash) == 64
    assert latch.current_generation(args=[1]).call() == 1
    assert latch.is_latched(args=[1, definition_hash, 1]).call() is False
    print(f"EVIDENCE definition_hash={definition_hash} generation=1")

    observation_receipts = []
    for index in range(3):
        tx = latch.observe(args=[1]).transact(
            consensus_max_rotations=5,
            wait_interval=1500,
            wait_retries=40,
        )
        assert tx_execution_succeeded(tx)
        observation_receipts.append(tx)
        _report_receipt(f"observation round {index + 1}", tx)
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
            print(
                f"EVIDENCE final snapshot_hash={final_obs['snapshot_hash']} "
                f"round_hash={final_obs['round_hash']}"
            )

    gate_factory = get_contract_factory("ConditionGate")
    gate = _deploy(
        gate_factory,
        [CalldataAddress(latch.address), 1, definition_hash, 1],
        default_account,
        "ConditionGate deploy",
    )
    assert gate.address is not None
    print(f"EVIDENCE ConditionGate address={gate.address}")

    action_hash = _tx_hashish("conditionlatch-live-gate-action-v1")
    allowed = gate.consume(args=[action_hash]).transact(
        consensus_max_rotations=5,
    )
    _report_receipt("ConditionGate allowed action", allowed)
    assert tx_execution_succeeded(allowed)

    replay = gate.consume(args=[action_hash]).transact(
        consensus_max_rotations=5,
    )
    _report_receipt("ConditionGate replay rejection", replay)
    assert tx_execution_failed(replay)

    wrong_definition_gate = _deploy(
        gate_factory,
        [CalldataAddress(latch.address), 1, "f" * 64, 1],
        default_account,
        "wrong-definition ConditionGate deploy",
    )
    wrong_definition = wrong_definition_gate.consume(
        args=[_tx_hashish("wrong-definition-action")]
    ).transact(
        consensus_max_rotations=5,
    )
    _report_receipt("wrong-definition rejection", wrong_definition)
    assert tx_execution_failed(wrong_definition)

    wrong_generation_gate = _deploy(
        gate_factory,
        [CalldataAddress(latch.address), 1, definition_hash, 2],
        default_account,
        "wrong-generation ConditionGate deploy",
    )
    wrong_generation = wrong_generation_gate.consume(
        args=[_tx_hashish("wrong-generation-action")]
    ).transact(
        consensus_max_rotations=5,
    )
    _report_receipt("wrong-generation rejection", wrong_generation)
    assert tx_execution_failed(wrong_generation)
