from pathlib import Path

import yaml


class MkDocsGenerator:

    @staticmethod
    def __generate_nav_struct(lst):
        _data = []
        for i in lst:
            is_childs_exists = bool(len(i['children']))
            if is_childs_exists:
                _data.append({i["text"]: MkDocsGenerator.__generate_nav_struct(i['children'])})
            else:
                _data.append(i["path"])
        return _data

    @classmethod
    def generate(cls, structure: list[dict]):
        """
        @param structure: this value should be result of execute generate_tools.parser.ParseContentStructure.parse
        """
        structure = structure.copy()
        structure.pop(0)
        first = "index.md"
        structure = cls.__generate_nav_struct(structure)
        structure.insert(0, first)
        yaml_data = yaml.dump({'nav': structure}, default_flow_style=False, allow_unicode=True)

        with open(Path(__file__).parent.resolve() / "data" / "mkdocs_yaml_template.txt", "r") as f:
            return f"{f.read()}\n\n{yaml_data}"
