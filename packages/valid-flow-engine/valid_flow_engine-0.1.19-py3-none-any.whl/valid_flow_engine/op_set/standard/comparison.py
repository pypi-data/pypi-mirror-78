from __future__ import annotations
from ..op_set import Op


class ComparisonMixin:

    @staticmethod
    @Op.create(provide_resolver=True, ui_string='Less than')
    def lt(lhs, rhs):
        return lhs < rhs

    @staticmethod
    @Op.create(provide_resolver=True, ui_string='Less than or equal to')
    def lte(lhs, rhs):
        return lhs <= rhs

    @staticmethod
    @Op.create(provide_resolver=True, ui_string='Greater than')
    def gt(lhs, rhs):
        return lhs > rhs

    @staticmethod
    @Op.create(provide_resolver=True, ui_string='Greater than or equal to')
    def gte(lhs, rhs):
        return lhs >= rhs

    @staticmethod
    @Op.create(provide_resolver=True, ui_string='Equal To')
    def eq(lhs, rhs):
        return lhs == rhs
