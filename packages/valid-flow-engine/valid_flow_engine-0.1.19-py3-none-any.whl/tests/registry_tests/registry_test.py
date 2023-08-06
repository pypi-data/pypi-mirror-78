from valid_flow_engine.op_set.base_opsets import *
from valid_flow_engine.op_set.op_set import OpSetRegistry


def test_serialieze():
    output = OpSetRegistry.serialize_registry()
    print(output)
