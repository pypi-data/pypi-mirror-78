from __future__ import annotations
import typing
from abc import ABC, abstractmethod

from .action_nodes import RunnerNode


class LoopBreakException(Exception):
    pass


class LoopNode(RunnerNode):
    """
    Node to provide Loop Functionality
    """
    WHILE = 'while'
    FOR = 'for'

    def evaluate_condition(self, payload) -> bool:
        condition_key = self.condition.get('key')
        if condition_key == self.WHILE:
            return self.__evaluate_while(self.condition, payload)
        elif condition_key == self.FOR:
            return self.__evalutate_for(self.condition, payload)

    def __init__(self, node_def: dict):
        RunnerNode.__init__(self, node_def)
        self.loop_targets = node_def.get('loopTargets')
        self.output_targets = node_def.get('outputTargets')
        self.condition = node_def.get('condition')

    def increment(self):
        pass

    def run(
        self,
        payload: dict
    ) -> typing.Tuple[typing.List[str], any]:
        """
        Run a Loop
        """
        if self.evaluate_condition(payload):
            return self.loop_targets, None
        else:
            return self.output_targets, None

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if not exc_type:
            self.increment()
            return True
        else:
            return isinstance(exc_type, LoopBreakException)

    @staticmethod
    def __evaluate_while(condition, payload):
        pass

    @staticmethod
    def __evalutate_for(condition, payload):
        pass


if typing.TYPE_CHECKING:
    from ..valid_flow_path import ValidFlowPath
