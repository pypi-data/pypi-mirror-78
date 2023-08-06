"""
Module for parsing JSON Dictionary to create valid flow results
"""
from __future__ import annotations
from abc import abstractmethod, ABC
import typing


class __ResolverRegistry:
    """
    Class to manage registry of ParamResolver implementations
    """

    def __init__(self):
        self._resolvers = {}

    def register_resolver(
        self,
        key: str,
        class_: typing.Type[ParamResolver]
    ) -> typing.Type[ParamResolver]:
        """
        Register a rosolver under the provided key
        """
        key = key.lower()
        assert key not in self._resolvers, f'Key: {key} is taken'
        self._resolvers[key] = class_

    def get_resolver(self, type_: str, default):
        if not isinstance(type_, str):
            return default
        return self._resolvers.get(type_.lower(), default)


__register = __ResolverRegistry()


def register_resolver(key):
    def wrapper(class_: typing.Type[ParamResolver]):
        __register.register_resolver(key, class_)
        return class_
    return wrapper


def get_resolver(key, default) -> typing.Type[ParamResolver]:
    return __register.get_resolver(key, default)


class ParamResolver(ABC):
    """
    Abstract class provided resolve method which will convert
    data to desired type (essentially a deserialization method)
    """

    @ classmethod
    @ abstractmethod
    def resolve(cls, data):
        """
        Resolve data to the desired type
        """
        pass
