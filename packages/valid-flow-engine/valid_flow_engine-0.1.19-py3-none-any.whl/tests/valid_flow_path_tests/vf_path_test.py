import re

import pytest

from valid_flow_engine.valid_flow_path.valid_flow_path import ValidFlowPath
from valid_flow_engine.op_set.standard import *


@pytest.fixture
def node_json():
    return [
        {
            'type': 'INPUT',
            'id': '0',
            'targets': ['1'],
        },
        {
            "block": {
                "blockSetKey": "blockset_Number",
                "blockKey": "gt",
                "args": [
                    {
                        "name": "lhs",
                        "value": 7
                    },
                    {
                        "name": "rhs",
                        "value": 5
                    }
                ]
            },
            "id": '1',
            "type": "FUNCTION",
            "returnKey": "isGreaterThan",
            "targets": ['3'],
            "parentNodeIDs": ['0']
        },
        {
            "block": {
                "blockSetKey": "blockset_Number",
                "blockKey": "lt",
                "args": [
                    {
                        "name": "lhs",
                        "value": "item1.child1",
                        "payloadElement": True
                    },
                    {
                        "name": "rhs",
                        "value": "item2",
                        "payloadElement": True
                    }
                ]
            },
            "id": '3',
            "type": "BOOLEAN",
            "returnKey": "item1isLessThan2",
            "falseTargets": ['4'],
            "trueTargets": ['5'],
            "parentNodeIDs": ['1']
        },
        {
            "id": '4',
            "type": "OUTPUT",
            "outputPairs": [
                {
                    "key": "simpleOutput",
                    "payloadElement": False,
                    "literalDef": {
                        "type": "string",
                        "value": "Output Value"
                    }
                },
                {
                    "key": "valueFromPayload",
                    "payloadElement": True,
                    "payloadKey": "item3"
                }
            ],
            "parentNodeIDs": ['3']
        },
        {
            "id": '5',
            "type": "OUTPUT",
            "outputPairs": [
                {
                    "key": "simpleOutput",
                    "payloadElemet": False,
                    "literalDef": {
                        "type": "string",
                        "value": "Other Output Value"
                    }
                },
                {
                    "key": "valueFromPayload",
                    "payloadElement": True,
                    "payloadKey": "isGreaterThan"
                }
            ],
            "parentNodeIDs": ['3']
        }
    ]


@pytest.fixture
def payload_one():
    payload = {
        'item1': {
            'child1': 1
        },
        'item2': 2,
        'item3': '3',
        'item4': 4,
    }
    return {
        'payload': payload,
        'expected': {
            'simpleOutput': 'Other Output Value',
            'valueFromPayload': True
        }
    }


@pytest.fixture
def payload_two():
    payload = {
        'item1': {
            'child1': 1
        },
        'item2': 0,
        'item3': '3',
        'item4': 4,
    }
    return {
        'payload': payload,
        'expected': {
            'simpleOutput': 'Output Value',
            'valueFromPayload': payload.get('item3')
        }
    }


@pytest.fixture
def payloads(payload_one, payload_two):
    return [
        payload_one,
        payload_two,
    ]


def test_ctor(node_json):
    path = ValidFlowPath(node_json)
    assert isinstance(path, ValidFlowPath)


def test_run(node_json, payloads):
    path = ValidFlowPath(node_json)
    for payload in payloads:
        res = path.run_path(payload=payload.get('payload'))
        output = {}
        for out in res:
            output.update(out.resolve_data(payload.get('payload')))
        for key, value in output.items():
            assert payload.get('expected').get(key) == value
