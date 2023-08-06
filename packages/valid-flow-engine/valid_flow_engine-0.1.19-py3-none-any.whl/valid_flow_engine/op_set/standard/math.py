from ..op_set import Op


class MathMixin:
    @staticmethod
    @Op.create_list_args(provide_resolver=True, ui_string='Sum Of')
    def sum(*args):
        return sum(args)

    @staticmethod
    @Op.create_list_args(provide_resolver=True, ui_string='Difference Of')
    def diff(*args):
        base = args[0]
        for arg in args[1:]:
            base -= arg
        return base

    @staticmethod
    @Op.create_list_args(provide_resolver=True, ui_string='Product Of')
    def product(*args):
        base = args[0]
        for arg in args[1:]:
            base *= arg
        return base

    @staticmethod
    @Op.create_list_args(provide_resolver=True, ui_string='Quotient Of')
    def quotient(*args):
        base = args[0]
        for arg in args[1:]:
            base /= arg
        return base

    @staticmethod
    @Op.create_list_args(provide_resolver=True, ui_string='Max Of')
    def max(*args):
        return max(args)

    @staticmethod
    @Op.create_list_args(provide_resolver=True, ui_string='Min Of')
    def min(*args):
        return min(args)

    @staticmethod
    @Op.create(provide_resolver=True, ui_string='Power Of')
    def pow(base, exponent):
        return base**exponent

    @staticmethod
    @Op.create(provide_resolver=True, ui_string='Root Of')
    def root(base, root):
        return base**(1/root)
