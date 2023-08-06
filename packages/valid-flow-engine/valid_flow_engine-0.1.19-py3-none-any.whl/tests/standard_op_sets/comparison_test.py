import pytest

from valid_flow_engine.op_set.standard.registers_and_resolvers import Number, DateTime
from valid_flow_engine.valid_flow_path.node.action_nodes import _OpRunner
from valid_flow_engine.op_set.op_set import OpSetRegistry
from valid_flow_engine.op_set.op_set import Op


@pytest.fixture
def args():
    return[
        {
            'name': 'lhs',
            'value': 'one',
            'payloadElement': True
        },
        {
            'name': 'rhs',
            'value': 'two',
            'payloadElement': True
        }
    ]


class TestNumberComparison:
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

    def test_lt(self, args, data):
        runner_data = {
            'args': args,
            'block_key': 'lt',
        }
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == True
        assert runner.run_op(data[1]) == False
        assert runner.run_op(data[2]) == False

    def test_lte(self, args, data):
        runner_data = {
            'args': args,
            'block_key': 'lte',
        }
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == True
        assert runner.run_op(data[1]) == False
        assert runner.run_op(data[2]) == True

    def test_gt(self, args, data):
        runner_data = {
            'args': args,
            'block_key': 'gt',
        }
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == False
        assert runner.run_op(data[1]) == True
        assert runner.run_op(data[2]) == False

    def test_gte(self, args, data):
        runner_data = {
            'args': args,
            'block_key': 'gte',
        }
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == False
        assert runner.run_op(data[1]) == True
        assert runner.run_op(data[2]) == True

    def test_eq(self, args, data):
        runner_data = {
            'args': args,
            'block_key': 'eq',
        }
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == False
        assert runner.run_op(data[1]) == False
        assert runner.run_op(data[2]) == True


class TestDateComparison:
    @pytest.fixture
    def data(self):
        return [
            {
                'one': 'Sat Oct 11 17:13:46 UTC 2003',
                'two': 'Sat Oct 11 17:13:46 UTC 2004',
            },
            {
                'one': 'Sat Oct 11 17:13:46 UTC 2003',
                'two': 'Sat Oct 11 17:13:45 UTC 2003',
            },
            {
                'one': 'Sat Oct 11 17:13:46 UTC 2003',
                'two': 'Sat Oct 11 17:13:46 UTC 2003',
            }
        ]

    def test_lt(self, args, data):
        runner_data = {
            'args': args,
            'block_key': 'lt',
        }
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == True
        assert runner.run_op(data[1]) == False
        assert runner.run_op(data[2]) == False

    def test_lte(self, args, data):
        runner_data = {
            'args': args,
            'block_key': 'lte',
        }
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == True
        assert runner.run_op(data[1]) == False
        assert runner.run_op(data[2]) == True

    def test_gt(self, args, data):
        runner_data = {
            'args': args,
            'block_key': 'gt',
        }
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == False
        assert runner.run_op(data[1]) == True
        assert runner.run_op(data[2]) == False

    def test_gte(self, args, data):
        runner_data = {
            'args': args,
            'block_key': 'gte',
        }
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == False
        assert runner.run_op(data[1]) == True
        assert runner.run_op(data[2]) == True

    def test_eq(self, args, data):
        runner_data = {
            'args': args,
            'block_key': 'eq',
        }
        runner = _OpRunner(Number.__name__, block_dict=runner_data)
        assert runner.run_op(data[0]) == False
        assert runner.run_op(data[1]) == False
        assert runner.run_op(data[2]) == True
