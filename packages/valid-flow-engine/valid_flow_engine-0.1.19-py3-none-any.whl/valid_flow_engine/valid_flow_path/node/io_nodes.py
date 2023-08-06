from __future__ import annotations
import typing

from .node import Node, get_payload_element


class InputNode(Node):
    """
    Node starts of all processes
    Example of Input Node's node_def:
    {
        'type': 'Input',
        'id': 0,
        'outputTargetNodeIDs': [1],
    }
    """

    def __init__(self, node_def: dict):
        Node.__init__(self, node_def)
        self.is_evalutated = True
        self.targets = node_def.get('targets')

    def run(
        self,
        path: ValidFlowPath,
        payload: dict
    ):
        pass


class OutputNode(Node):
    """
    Node for the output of a path, provides functions to run if desired
    Example of Output Node's node_def:
    {
        'type': 'Output',
        'id': 3,
        'output': {
            'outputPairs': [
                {
                'key': 'out1',
                'value': 'Item 2',
                'literal': False  <--Output would the value of Payload Element with key 'Item 2'
                },
                {
                    'key': 'out2',
                    'value': 'OUT 2',
                    'literal': True  <--Output would be the literal value: 'OUT 2'
                }
            ]
        },
    }
    """

    def __init__(self, node_def: dict):
        self._id = node_def.get('id')
        self.output = node_def.get('outputPairs')

    def resolve_data(self, payload: dict) -> dict:
        """Resolve the outputPair is in the Output Node

        Arguments:
            payload {dict} -- Payload to pull data from if output needs data from payload

        Returns:
            dict -- Values that the user defined in this output node
        """
        result = {}
        for pair in self.output:
            key = pair.get('key')
            if pair.get('payloadElement', False):
                assert 'payloadKey' in pair
                result[key] = get_payload_element(payload, pair.get('payloadKey'))
            else:
                assert 'literalDef' in pair
                result[key] = pair.get('literalDef').get('value')
        return result

    def run(
        self,
        path: ValidFlowPath,
        payload: dict
    ):
        pass
