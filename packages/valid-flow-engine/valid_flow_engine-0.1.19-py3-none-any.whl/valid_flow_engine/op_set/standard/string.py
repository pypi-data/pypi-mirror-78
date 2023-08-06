import typing

from ..resolver import register_resolver, ParamResolver
from ..op_set import OpSetRegistry, Op


@OpSetRegistry.register
@register_resolver('string')
class String(ParamResolver):

    @classmethod
    def resolve(cls, data):
        """
        Resolve data to the desired type
        """
        return str(data)

    @staticmethod
    @Op.create(
        key='contains',
        ui_string='Determine if a string contains another string'
    )
    def contains(search_container: str, search_for: str) -> bool:
        return search_for in search_container

    @staticmethod
    @Op.create(key='split', ui_string='Split a string')
    def split(
        to_split: str,
        split_by: str,
        maxsplit: typing.Optional[int] = None
    ) -> typing.List[str]:
        if maxsplit is not None:
            return to_split.split(split_by, maxsplit)
        return to_split.split(split_by)

    @staticmethod
    @Op.create(key='split_lines', ui_string='Split a string on line breaks')
    def split_lines(to_split: str) -> typing.List[str]:
        return to_split.splitlines()

    @staticmethod
    @Op.create(
        key='title',
        ui_string='Put a string into title format, for exmaple "test string" => "Test String"'
    )
    def title(string: str) -> str:
        return string.title()

    @staticmethod
    @Op.create(key='all_caps', ui_string='Put a string into all caps')
    def capitalize(string: str) -> str:
        return string.capitalize()

    @staticmethod
    @Op.create(key='lower_case', ui_string='Put a string into all lower case')
    def lower(string: str) -> str:
        return string.lower()

    @staticmethod
    @Op.create(key='replace', ui_string='Replace part of a string')
    def replace(replace_container: str, to_repalce: str, replace_with: str):
        return replace_container.replace(to_repalce, replace_with)

    @staticmethod
    @Op.create(
        key='word_count',
        ui_string='Find the number of words in a string'
    )
    def word_count(string: str) -> int:
        words = string.split(' ')
        return len(words)
