import pytest

from valid_flow_engine.op_set.standard.string import String
from valid_flow_engine.valid_flow_path.node.action_nodes import _OpRunner
from valid_flow_engine.op_set.op_set import OpSetRegistry
from valid_flow_engine.op_set.op_set import Op


def test_contains():
    container = 'I\'m a test string'
    search_one = 'test'
    search_two = 'not here'
    runner_data = {
        'args': [
            {
                'name': 'search_container',
                'value': 'container',
                'payloadElement': True
            },
            {
                'name': 'search_for',
                'value': 'search',
                'payloadElement': True
            }
        ],
        'block_key': 'contains'
    }
    runner = _OpRunner(String.__name__, block_dict=runner_data)
    payload_one = {
        'container': container,
        'search': search_one
    }
    payload_two = {
        'container': container,
        'search': search_two
    }
    assert runner.run_op(payload_one) is True
    assert runner.run_op(payload_two) is False


def test_split():
    to_split = 'I should split into five'
    split_by_one = ' '
    split_by_two = 's'
    runner_data = {
        'args': [
            {
                'name': 'to_split',
                'value': 'to_split',
                'payloadElement': True
            },
            {
                'name': 'split_by',
                'value': 'split_by',
                'payloadElement': True
            }
        ],
        'block_key': 'split'
    }
    runner = _OpRunner(String.__name__, block_dict=runner_data)
    payload_one = {
        'to_split': to_split,
        'split_by': split_by_one
    }
    payload_two = {
        'to_split': to_split,
        'split_by': split_by_two
    }
    s1 = runner.run_op(payload_one)
    assert len(s1) == 5
    assert s1[0] == 'I'
    assert s1[-1] == 'five'
    s2 = runner.run_op(payload_two)
    assert len(s2) == 3
    assert s2[0] == 'I '
    assert s2[-1] == 'plit into five'
