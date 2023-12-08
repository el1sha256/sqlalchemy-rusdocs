from generate_tools.parser.misc import ParserSingletonMeta


class source(metaclass=ParserSingletonMeta):  # noqa
    ...


from generate_tools.parser.parse_content_structure import ParseContentStructure

__all__ = [
    "ParseContentStructure",
    "source"
]
