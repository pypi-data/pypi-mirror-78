import pytest

from valid_flow_engine.op_set.standard.registers_and_resolvers import DateTime
from valid_flow_engine.valid_flow_path.node.action_nodes import _OpRunner
from valid_flow_engine.op_set.op_set import OpSetRegistry
from valid_flow_engine.op_set.op_set import Op


@pytest.fixture
def data():
    return [
        {
            'one': 'Jun 7 1993',
            'two': 'Jan 1 2000',
        },
        {
            'one': 'Dec 27 1992',
            'two': 'Jan 1 2000',
        },
        {
            'one': 'May 21 2019',
            'two': 'Jan 1 2000',
        }
    ]


def test_age(data):
    runner_data = {
        'args': [
            {
                'name': 'dob',
                'value': 'one',
                'payloadElement': True
            }
        ],
        'block_key': 'age'
    }
    runner = _OpRunner(DateTime.__name__, block_dict=runner_data)
    assert runner.run_op(data[0]) == 27
    assert runner.run_op(data[1]) == 27
    assert runner.run_op(data[2]) == 1


def test_age_at(data):
    runner_data = {
        'args': [
            {
                'name': 'dob',
                'value': 'one',
                'payloadElement': True
            },
            {
                'name': 'at_date',
                'value': 'two',
                'payloadElement': True
            }
        ],
        'block_key': 'age_at_date'
    }
    runner = _OpRunner(DateTime.__name__, block_dict=runner_data)
    assert runner.run_op(data[0]) == 6
    assert runner.run_op(data[1]) == 7
    assert runner.run_op(data[2]) == -20


def test_year_dif(data):
    runner_data = {
        'args': [
            {
                'name': 'date',
                'value': 'one',
                'payloadElement': True
            },
            {
                'name': 'other',
                'value': 'two',
                'payloadElement': True
            }
        ],
        'block_key': 'year_dif'
    }
    runner = _OpRunner(DateTime.__name__, block_dict=runner_data)
    assert runner.run_op(data[0]) == -6
    assert runner.run_op(data[1]) == -7
    assert runner.run_op(data[2]) == 19


def test_month_dif(data):
    runner_data = {
        'args': [
            {
                'name': 'date',
                'value': 'one',
                'payloadElement': True
            },
            {
                'name': 'other',
                'value': 'two',
                'payloadElement': True
            }
        ],
        'block_key': 'month_dif'
    }
    runner = _OpRunner(DateTime.__name__, block_dict=runner_data)
    assert runner.run_op(data[0]) == (-6 * 12) - 6
    assert runner.run_op(data[1]) == (-7 * 12)
    assert runner.run_op(data[2]) == (19 * 12) + 4


def test_day_dif():
    runner_data = {
        'args': [
            {
                'name': 'date',
                'value': 'one',
                'payloadElement': True
            },
            {
                'name': 'other',
                'value': 'two',
                'payloadElement': True
            }
        ],
        'block_key': 'day_dif'
    }
    data = [
        {
            'one': 'Jun 7 1993',
            'two': 'Jun 1 1993',
        },
        {
            'one': 'Jun 7 1993',
            'two': 'Jun 8 1993',
        },
        {
            'one': 'Jun 7 1993',
            'two': 'Jun 10 1993',
        }
    ]
    runner = _OpRunner(DateTime.__name__, block_dict=runner_data)
    assert runner.run_op(data[0]) == 6
    assert runner.run_op(data[1]) == -1
    assert runner.run_op(data[2]) == -3
