from __future__ import annotations
import typing
from abc import ABC, abstractmethod

from .node import Node, get_payload_element
from ...op_set.op_set import OpSetRegistry


class _OpRunner:
    def __init__(self, block_set_key, op_str=None, block_dict=None):
        assert op_str is not None or block_dict is not None, 'Either a OpString or OpDict must be provided'
        if not OpSetRegistry.IN(block_set_key):
            raise ValueError(
                f'Op Class Name must be registered. Name: {block_set_key}')
        self.block_set_key = block_set_key
        self.op_str = op_str
        self.block_dict = block_dict

    def run_op(self, payload: dict):
        op_key = self.block_dict.get('block_key')
        op_args = self.block_dict.get('args')
        op = OpSetRegistry.get_op(self.block_set_key, op_key)
        args_ = []
        kwargs_ = {}
        if op.provide_resolver:
            kwargs_['resolver'] = OpSetRegistry.get_op_class(self.block_set_key)
        for arg_def in op_args:
            if isinstance(arg_def, dict):
                key = arg_def.get('name')
                arg_val = arg_def.get('value')
                if arg_def.get('payloadElement', False):
                    value = get_payload_element(payload, arg_val)
                else:
                    value = arg_val
                kwargs_[key] = value
            else:
                args_.append(payload.get(arg_def))
        return op(*args_, **kwargs_)


class RunnerNode(Node, ABC):
    @abstractmethod
    def run(
        self,
        payload: dict
    ) -> typing.Tuple[typing.List[str], any]:
        """Abstract method to be called when a node's function should be invoked

        Arguments:
            path {Path} -- The path which contains the other nodes
            payload {dict} -- Dictionary contianing data to use for node parameters
        """
        pass


class ActionNode(RunnerNode, ABC):
    """
    Abstract Class to be used for elements within a Path which run functions
    """

    def __init__(self, node_def: dict):
        RunnerNode.__init__(self, node_def)
        self._return_key = node_def.get('returnKey', None)
        self.node = self.parse_node(node_def.get('block'))

    @staticmethod
    def parse_node(func: dict) -> _OpRunner:
        """Take the JSON description of nodes and create Node instances

        Arguments:
            func {dict} -- JSON parse node

        Returns:
            Node -- Node from which ops can be called
        """
        block_set = func.get('blockSetKey')
        args = func.get('args')
        block_key = func.get('blockKey')
        block_dict = {
            'block_key': block_key,
            'args': args,
        }
        return _OpRunner(block_set, block_dict=block_dict)

    @staticmethod
    def factory(node: dict) -> typing.Type[ActionNode]:
        """Create a Fork based on the type provided in the dictionary

        Arguments:
            node {dict} -- JSON Parsed dictionary

        Returns:
            typing.Type[Fork] -- Fork instance based on the provided data
        """
        node_type = node.get('type')
        assert node_type is not None, 'Node Type must be provided'
        if node_type == 'BOOLEAN':
            return BooleanNode(node)
        elif node_type == 'FUNCTION':
            return FunctionNode(node)
        else:
            raise NotImplementedError(
                f'Node type: {node_type} is not supported')

    @staticmethod
    def run_targets(results_list: list, target_node: int, payload: dict, path: ValidFlowPath):
        ret = path.run_node(target_node, payload)
        if isinstance(ret, (list, tuple)):
            results_list.extend(path.run_node(target_node, payload))
        else:
            results_list.append(ret)


class BooleanNode(ActionNode):
    """
    Boolean Implementation of Fork. Changes programatic path based
    on the result of the Fork's function
    Example Boolean Node's node_def:
    {
        'type': 'Bool',
        'id': 1,
        'function': {
            'opSetKey': 'Number',
            'opKey': 'lt',
            'arguments': [
                {
                'argumentKey': 'lhs',
                'argumentValue': 'Item 1'
                },
                {
                    'argumentKey': 'rhs',
                    'argumentValue': 'Item 2'
                }
            ]
        },
        'falseTargetNodeIDs': [2],
        'trueTargetNodeIDs': [3],
    }
    In this example, if 'Item 1' < 'Item 2', then path would proceed to node with ID of 3,
    otherweise it would proceed to node with ID of 2
    """

    def __init__(self, node_def: dict):
        ActionNode.__init__(self, node_def)
        self.false_targets = node_def.get('falseTargets')
        self.true_targets = node_def.get('trueTargets')

    def run(self, payload: dict):
        """Implementation of move on for Boolean Fork.
        calls path.run_node for either the true or false targets,
        based on the result of the inoked opperation for this Fork's onde

        Arguments:
            path {Path} -- The path to call run_node on
            payload {dict} -- The Payload with avaiable data for nodes

        Returns:
            typing.List[typing.Type[OutputNode]] -- List of out put nodes that are the result
        """
        op_res = self.node.run_op(payload)
        if self._return_key is not None:
            payload[self._return_key] = op_res
        targets = self.true_targets if op_res else self.false_targets
        self.is_evalutated = True
        return targets, op_res


class FunctionNode(ActionNode):
    """
    Fork that invokes a function. It may provide a return value or just do action
    Example of Function Node's node_def:
    {
        'type': 'Function',
        'id': 2,
        'function': {
            'opSetKey': 'Number',
            'opKey': 'gt',
            'arguments': [
                {
                    'argumentKey': 'lhs',
                    'argumentValue': 'Item 3'
                },
                {
                    'argumentKey': 'rhs',
                    'argumentValue': 'Item 4'
                }
            ]
        },
        'outputSourceNodeIDs': [4],
        'returnKey': 'retKey'
    }
    In this example the result of 'Item 3' > 'Item 4' would be saved to payload with key of
    'retKey' and would be avaialbe downstream. Path would proceed to Node of ID 4
    """

    def __init__(self, node_def: dict):
        ActionNode.__init__(self, node_def)
        self.targets = node_def.get('targets')

    def run(self, payload: dict):
        op_res = self.node.run_op(payload=payload)
        if self._return_key is not None:
            payload[self._return_key] = op_res
        self.is_evalutated = True
        return self.targets, op_res


class LoopStartNode(ActionNode):

    def __init__(self, node_def: dict):
        ActionNode.__init__(self, node_def)
        self.targets = node_def.get('targets')

    def run(self, path, payload):
        results = []
        for target in self.targets:
            ActionNode.run_targets(results, target, payload, path)
        return results, {}


class LoopEndNode(ActionNode):

    def __init__(self, node_def: dict):
        ActionNode.__init(self, node_def)
        self.loop_start = node_def.get('loopStartID')
        self.end_loop_targets = node_def.get('endLoopTargets')

    def run(self, path, payload):
        results = []
        for target in self.end_loop_targets:
            ActionNode.run_targets(results, target, payload, path)
        return results, {}


if typing.TYPE_CHECKING:
    from ..valid_flow_path import ValidFlowPath
