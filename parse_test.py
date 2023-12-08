import yaml

from generate_tools.parser import source, ParseContentStructure
from generate_tools.generator.generate_mkdocs_yml import MkDocsGenerator
from pathlib import Path

source.root = "/home/el1sha/Projects/sqlalchemy-rusdocs/source"
data = (ParseContentStructure.parse())

dst_path = Path("/home/el1sha/Projects/sqlalchemy-rusdocs/destination/")


def print_data(_data):
    for el in _data:
        if el["children"]:
            print_data(el['children'])
        _dst = dst_path / (el['path'].replace(".html", ".md"))
        _dst.parent.mkdir(parents=True, exist_ok=True)
        _dst.touch(exist_ok=True)
        if not _dst.stat().st_size:
            _dst.write_text(f"title: {el['text']}")


# print("\n")

def flatten_nav(lst):
    _data = []
    for i in lst:
        is_childs_exists = bool(len(i['children']))
        if is_childs_exists:
            _data.append({i["text"]: flatten_nav(i['children'])})
        else:
            _data.append(i["path"])
    return _data


_data = (ParseContentStructure.parse())

# print(MkDocsGenerator.generate(_data))
print_data(_data)