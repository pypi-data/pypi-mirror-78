"""
Module providing the logic for converting from Functions
provided by the front end to Node Dicts and Rule Sets
"""
from __future__ import annotations
import typing
import json

from .node import InputNode, OutputNode, ActionNode, Node


class ParentNotEvaluated(Exception):
    pass


class ValidFlowPath:
    """Define the progromatic flow, consume list of json described nodes
    and create a series of lists for varrious node types
    """

    def __init__(self, node_defs: typing.List[dict]):
        self.output = []
        self.nodes = {}
        self.input_nodes = []
        self.output_nodes = []
        self.forks = []
        self.track_node_evals = False
        self.node_evals = {}
        for node in node_defs:
            type_ = node.get('type')
            n = None
            if type_ == 'INPUT':
                n = InputNode(node)
                self.input_nodes.append(n)
            elif type_ == 'OUTPUT':
                n = OutputNode(node)
                self.output_nodes.append(n)
            else:
                n = ActionNode.factory(node)
                self.forks.append(n)
            self.put_node(n)

    def put_node(self, node: typing.Type[Node]):
        """Add node to this path's nodes, verifying no duplicate keys

        Arguments:
            node {typing.Type[FunctionalNode]} --
            Node to add to this Path's nodes
        """
        id = node.id
        assert id not in self.nodes, f'Duplicate Node ID Found: {id}'
        self.nodes[id] = node

    def run_path(
        self,
        payload: dict,
        get_node_evals: bool = False
    ) -> typing.List[OutputNode]:
        """Kick off runninng the path. Runs starting at each input node
        and extends the returened list to return a list of results

        Arguments:
            payload {dict} --
                Dictionary to use as data source for op parameters
            get_node_evauls {boo} --
                If a dictionary with node id's as key and
                evaluations results should be created

        Returns:
            typing.List[OutputNode] -- List of Output Nodes
        """
        self.track_node_evals = get_node_evals
        self.output = []
        for i in self.input_nodes:
            for target_id in i.targets:
                self.run_node(target_id, payload)
        return self.output

    def run_node(
        self,
        node_id: str,
        payload
    ) -> typing.List[OutputNode]:
        """Get Node with provided id, return if it's an output node, other wise
        run the node and continue down the path

        Arguments:
            node_id {str} -- Key for the Node of interest
            payload {dict} -- Dictioary with the data to put from for nodes

        Returns:
            OutputNode -- Either returns the OutputNode with key 'node_id' or
            calls the node's run method
            (which will intern end up returning a OutputNode)
        """
        node: Node = self.nodes.get(node_id)
        if node in self.output_nodes:
            self.output.append(node)
            return
        next_node_ids, node_eval = node.run(payload)
        if self.track_node_evals:
            self.node_evals.update({node_id: node_eval})
        for next_id in next_node_ids:
            self.run_node(next_id, payload)

    @staticmethod
    def vfm_get_path_json(
        *,
        diagram_json: typing.Union[dict, str]
    ) -> str:
        if isinstance(diagram_json, str):
            diagram_json = json.loads(diagram_json)
        diagram_layers = diagram_json.get('layers', [])
        nodes = [layer for layer in diagram_layers if layer.get(
            'type', None) == 'diagram-nodes']
        assert len(
            nodes) > 0, f'Unable to find nodes in diagram_json: {diagram_json}'
        nodes = nodes[0]
        models = nodes.get('models')
        rules = ValidFlowPath.__get_rules(models=models)
        ios = ValidFlowPath.__get_io_nodes(models=models)
        rules.extend(ios)
        return json.dumps(rules)

    @staticmethod
    def __get_rules(
        *,
        models: typing.Dict[str, any]
    ) -> typing.List[typing.Dict[str, any]]:
        decisons = []
        for _, value in models.items():
            if value.get('type') in ['decision', 'function']:
                decisons.append(value)
        return [decison.get('extras', {}).get('logicNode')
                for decison in decisons]

    @staticmethod
    def __get_io_nodes(
        *,
        models: typing.Dict[str, any]
    ) -> typing.List[typing.Dict[str, any]]:
        io_nodes = []
        for _, value in models.items():
            if value.get('type') == 'io':
                io_nodes.append(value)
        return [io_nodes.get('extras') for io_nodes in io_nodes]


if typing.TYPE_CHECKING:
    NODES = typing.List[dict]
