import pytest

from valid_flow_engine.op_set.standard.registers_and_resolvers import Number
from valid_flow_engine.valid_flow_path.node.action_nodes import _OpRunner


@pytest.fixture
def args():
    return[
        {
            'name': '1',
            'value': 'one',
            'payloadElement': True
        },
        {
            'name': '2',
            'value': 'two',
            'payloadElement': True
        },
        {
            'name': '3',
            'value': 4,
            'payloadElement': False
        }
    ]


class TestMath:

    @pytest.fixture
    def data(self):
        return [
            {
                'one': '1',
                'two': 2,
            },
            {
                'one': 0,
                'two': '-1',
            },
            {
                'one': 0,
                'two': '0',
            }
        ]

    def test_sum(self, args, data):
        runner_data = {
            'args': args,
            'block_key': 'sum',
        }
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == 7
        assert runner.run_op(data[1]) == 3
        assert runner.run_op(data[2]) == 4

    def test_dif(self, args, data):
        runner_data = {
            'args': args,
            'block_key': 'diff'
        }
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == (1 - 2 - 4)
        assert runner.run_op(data[1]) == (0 + 1 - 4)
        assert runner.run_op(data[2]) == (0 - 0 - 4)

    def test_product(self, args, data):
        runner_data = {
            'args': args,
            'block_key': 'product'
        }
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == (1 * 2 * 4)
        assert runner.run_op(data[1]) == 0
        assert runner.run_op(data[2]) == 0

    def test_quotient(self, args, data):
        runner_data = {
            'args': args,
            'block_key': 'quotient'
        }
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == (1 / 2 / 4)
        runner.run_op(data[1]) == 0
        with pytest.raises(ZeroDivisionError):
            runner.run_op(data[2])

    def test_max(self, args, data):
        runner_data = {
            'args': args,
            'block_key': 'max'
        }
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == 4
        assert runner.run_op(data[1]) == 4
        assert runner.run_op(data[2]) == 4

    def test_min(self, args, data):
        runner_data = {
            'args': args,
            'block_key': 'min'
        }
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == 1
        assert runner.run_op(data[1]) == -1
        assert runner.run_op(data[2]) == 0

    def test_pow(self):
        runner_data = {
            'args': [
                {
                    'name': 'base',
                    'value': 'one',
                    'payloadElement': True
                },
                {
                    'name': 'exponent',
                    'value': 2,
                }
            ],
            'block_key': 'pow'
        }
        data = [
            {
                'one': '1'
            },
            {
                'one': 2
            },
            {
                'one': 5
            }
        ]
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == 1 * 1
        assert runner.run_op(data[1]) == 2 * 2
        assert runner.run_op(data[2]) == 5 * 5

    def test_root(self):
        runner_data = {
            'args': [
                {
                    'name': 'base',
                    'value': 'one',
                    'payloadElement': True
                },
                {
                    'name': 'root',
                    'value': 2,
                }
            ],
            'block_key': 'root'
        }
        data = [
            {
                'one': '1'
            },
            {
                'one': 4
            },
            {
                'one': 25
            }
        ]
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == 1
        assert runner.run_op(data[1]) == 2
        assert runner.run_op(data[2]) == 5
