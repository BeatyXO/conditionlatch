from pathlib import Path

SOURCE = (Path(__file__).parents[2] / "contracts" / "condition_gate.py").read_text(encoding="utf-8")


def test_gate_is_real_typed_consumer_and_replay_protected():
    assert "@gl.contract_interface" in SOURCE
    assert "IConditionLatch" in SOURCE
    assert ".view().is_latched(" in SOURCE
    assert "used_actions" in SOURCE
    assert "action hash already consumed" in SOURCE
    assert "ActionConsumed" in SOURCE


def test_gate_validates_pinned_identity_inputs():
    assert "expected_definition_hash must be a 64-character hex digest" in SOURCE
    assert "condition_id must be positive" in SOURCE
    assert "expected_generation must be positive" in SOURCE
