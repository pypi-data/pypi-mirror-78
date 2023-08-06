from __future__ import annotations
import inspect
import typing


class Op:
    """
    Opperation that has a key, ui_string for display to end user
    and a fn to call to run the actual opperation
    """

    def __init__(
        self,
        *,
        fn: callable,
        key: typing.Optional[str] = None,
        ui_string: typing.Optional[str] = None,
        pre_call: typing.Optional[callable] = None,
        post_call: typing.Optional[callable] = None,
        meta: typing.Optional[dict] = {},
        default_resolver=None,
        provide_resolver=False,
    ):
        '''Create a new Op'''
        if key is None:
            key = fn.__name__
        self.key = key
        self.ui_string = ui_string
        self.fn = fn
        self.class_name = fn.__qualname__.split('.')[0]
        self.return_type = self.get_return_type(fn)
        self._pre_call = pre_call
        self._post_call = post_call
        self._meta = meta
        if not self._meta.get('list_args'):
            self.args = self.get_arg_dict(fn)
        else:
            self.args = []
        self.default_resolver = default_resolver
        self.provide_resolver = provide_resolver

    def __call__(self, *args, **kwargs):
        '''Call the Op's function'''
        kwargs = self.resolve_args(**kwargs)
        if self._pre_call is not None:
            args, kwargs = self._pre_call(*args, **kwargs)
        ret = self.fn(*args, **kwargs)
        if self._post_call is not None:
            ret = self._post_call(ret)
        return ret

    def serialize(self):
        """Serialze the Op for Display on UI"""
        return {
            'key': self.key,
            'display_name': self.ui_string,
            'args': self.args,
            'return_type': self.return_type,
            'meta': self._meta,
        }

    def get_resolver(self, arg_name: str):
        from .resolver import get_resolver
        res_name = None
        for arg in self.args:
            if arg.get('name') == arg_name:
                res_name = arg.get('type')
                break
        return get_resolver(res_name, self.default_resolver)

    def resolve_args(self, **kwargs):
        resolved = {}
        parent_resolver = kwargs.pop('resolver', None)
        for key, value in kwargs.items():
            resolver = self.get_resolver(key)
            if resolver is None and parent_resolver is not None:
                resolver = parent_resolver
            if resolver is not None:
                resolved[key] = resolver.resolve(value)
            else:
                resolved[key] = value
        return resolved

    @staticmethod
    def get_arg_dict(fn: callable):
        args = []
        params = inspect.signature(fn).parameters
        for param in params:
            if 'self' in params:
                continue
            type_ = params.get(param).annotation
            if type_ is inspect._empty:
                type_ = 'any'
            else:
                if not isinstance(type_, str) and hasattr(type_, '__name__'):
                    type_ = type_.__name__
            info = {
                'name': param,
                'type': type_,
            }
            args.append(info)
        return args

    @staticmethod
    def create(
        *,
        key=None,
        ui_string=None,
        resolver=None,
        provide_resolver=False
    ):
        """Decorator to use on function that should be available as ops

        Arguments:
            key {str} -- Key for the function beign decoratored
            ui_string {str} -- Strinng to display on the UI for the function

        Returns:
            Op -- Created Op
        """
        def inner(func):
            return Op(
                key=key, ui_string=ui_string,
                fn=func, default_resolver=resolver,
                provide_resolver=provide_resolver
            )
        return inner

    @staticmethod
    def create_list_args(
        *,
        key=None,
        ui_string=None,
        resolver=None,
        provide_resolver=False
    ):
        def to_list(*args, **kwargs):
            run_args = []
            for a in args:
                run_args.append(a)
            for key, value in kwargs.items():
                run_args.append(value)
            return run_args, {}

        def inner(func):
            return Op(
                key=key,
                ui_string=ui_string,
                fn=func,
                pre_call=to_list,
                meta={'list_args': True},
                default_resolver=resolver,
                provide_resolver=provide_resolver
            )
        return inner

    @staticmethod
    def get_return_type(fn: callable) -> str:
        """
        Parse function and find the return type
        :param fn: Function to Parse
        """
        ret_type = inspect.signature(fn).return_annotation
        if ret_type is inspect._empty:
            return 'None'
        if hasattr(ret_type, '__name__'):
            return ret_type.__name__
        else:
            return 'any'


class OpRegistry:
    """
    Registry to hold Ops
    """

    def __init__(self, name, ops: typing.List[Op] = None):
        '''Create a new OpRegsitry'''
        self.name = name
        self.__reg = {}
        if ops is not None:
            for op in ops:
                self.__reg[op.key] = op

    def add_op(self, op: Op):
        '''Add an Op to the registry'''
        self.__reg[op.key] = op

    def get_op(self, op_key: str):
        '''Get Opfrom the registry'''
        return self.__reg.get(op_key)

    def serialize_registry(self) -> list:
        reg = []
        for op_name, op in self.__reg.items():
            reg.append(op.serialize())
        return reg


class OpSetRegistry:
    """
    Registry to contain a set of Op Sets and all of thier Ops
    """
    __op_types = {}

    @classmethod
    def register(cls, class_):
        """
        Regsiter a class (that inherits from OpSetBase).
        Register all of its Ops.
        Should be used as a decorator on a class
        :param: class_ -> the decorated class
        """
        from .op_set import Op
        op_reg = OpRegistry(class_.__name__)
        ops = [op for op in dir(class_) if isinstance(getattr(class_, op), Op)]
        for op in ops:
            op_reg.add_op(getattr(class_, op))
        cls.__op_types[class_.__name__] = (class_, op_reg)
        return class_

    @classmethod
    def get_op(cls, class_key: str, op_key: str):
        """
        Get and Op from its class_key and op_key
        """
        if class_key not in cls.__op_types:
            return None
        class_reg = cls.__op_types.get(class_key)[1]
        return class_reg.get_op(op_key)

    @classmethod
    def IN(cls, class_name: str):
        '''Check if class_name is in this op types registry'''
        return class_name in cls.__op_types

    @classmethod
    def create_op_class(cls, class_name: str, *args, **kwargs):
        '''Create instance of desired Op Set'''
        if class_name not in cls.__op_types:
            raise ValueError()
        return cls.__op_types.get(class_name)[0](*args, **kwargs)

    @classmethod
    def get_op_class(cls, class_name: str):
        """Get the Class from the registry"""
        if class_name not in cls.__op_types:
            raise ValueError()
        return cls.__op_types.get(class_name)[0]

    @classmethod
    def get_op_registry(cls, class_name: str) -> OpRegistry:
        """Get the Op Registry from the Op Type Registry"""
        if class_name not in cls.__op_types:
            raise ValueError()
        return cls.__op_types.get(class_name)[1]

    @classmethod
    def serialize_registry(cls) -> list:
        """
        Serialize the Registry to provide all the op types and
        their respective ops in a dictonary
        """
        reg = []
        for key, (op_class, op_reg) in cls.__op_types.items():
            item = {
                'key': key,
                'display_name': cls.__get_display_name(op_class),
                'operations': op_reg.serialize_registry()
            }
            reg.append(item)
        return reg

    @staticmethod
    def __get_display_name(op_class):
        if hasattr(op_class, 'DISPLAY_NAME'):
            return op_class.DISPLAY_NAME
        else:
            return op_class.__name__
