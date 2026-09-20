# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

"""ConditionGate — tiny consumer proving typed IC-to-IC reuse of ConditionLatch."""

from genlayer import *
from dataclasses import dataclass


@gl.contract_interface
class IConditionLatch:
    class View:
        def is_latched(self, condition_id: u256, expected_definition_hash: str, expected_generation: u32) -> bool: ...

    class Write:
        pass


def is_hex_hash(value: str) -> bool:
    raw = str(value).strip().lower()
    return len(raw) == 64 and all(ch in "0123456789abcdef" for ch in raw)


class ActionConsumed(gl.Event):
    def __init__(self, consumption_id: u256, condition_id: u256, generation: u32, /, **blob): ...


@allow_storage
@dataclass
class Consumption:
    action_hash: str
    consumed_by: Address
    condition_id: u256
    generation: u32
    definition_hash: str


class ConditionGate(gl.Contract):
    latch_address: Address
    condition_id: u256
    expected_definition_hash: str
    expected_generation: u32
    used_actions: TreeMap[str, bool]
    consumptions: TreeMap[u256, Consumption]
    consumption_count: u256

    def __init__(
        self,
        latch_address: Address,
        condition_id: u256,
        expected_definition_hash: str,
        expected_generation: u32,
    ):
        definition_hash = str(expected_definition_hash).strip().lower()
        if not is_hex_hash(definition_hash):
            raise gl.vm.UserError("expected_definition_hash must be a 64-character hex digest")
        if int(condition_id) <= 0:
            raise gl.vm.UserError("condition_id must be positive")
        if int(expected_generation) <= 0:
            raise gl.vm.UserError("expected_generation must be positive")
        self.latch_address = latch_address
        self.condition_id = condition_id
        self.expected_definition_hash = definition_hash
        self.expected_generation = expected_generation
        self.consumption_count = u256(0)

    @gl.public.write
    def consume(self, action_hash: str) -> u256:
        action = str(action_hash).strip().lower()
        if not is_hex_hash(action):
            raise gl.vm.UserError("action_hash must be a 64-character hex digest")
        if self.used_actions.get(action, False):
            raise gl.vm.UserError("action hash already consumed")

        latch = IConditionLatch(self.latch_address)
        if not latch.view().is_latched(
            self.condition_id,
            self.expected_definition_hash,
            self.expected_generation,
        ):
            raise gl.vm.UserError("ConditionLatch does not establish the pinned latch state")

        consumption_id = u256(int(self.consumption_count) + 1)
        self.used_actions[action] = True
        self.consumptions[consumption_id] = Consumption(
            action_hash=action,
            consumed_by=gl.message.sender_address,
            condition_id=self.condition_id,
            generation=self.expected_generation,
            definition_hash=self.expected_definition_hash,
        )
        self.consumption_count = consumption_id
        ActionConsumed(consumption_id, self.condition_id, self.expected_generation).emit(
            action_hash=action,
            definition_hash=self.expected_definition_hash,
            consumed_by=str(gl.message.sender_address),
        )
        return consumption_id

    @gl.public.view
    def get_consumption(self, consumption_id: u256) -> dict:
        cid = int(consumption_id)
        if cid <= 0 or cid > int(self.consumption_count):
            raise gl.vm.UserError("consumption does not exist")
        item = self.consumptions[u256(cid)]
        return {
            "consumption_id": cid,
            "action_hash": item.action_hash,
            "consumed_by": str(item.consumed_by),
            "condition_id": int(item.condition_id),
            "generation": int(item.generation),
            "definition_hash": item.definition_hash,
        }
