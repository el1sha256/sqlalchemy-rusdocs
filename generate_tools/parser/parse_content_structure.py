from bs4 import BeautifulSoup
from pathlib import Path
from generate_tools.parser import source


class ParseContentStructure:
    contents_file_name = "contents.html"

    @property
    def contents_path(self):
        return source.root / self.contents_file_name

    @staticmethod
    def _parse_ul(element):
        result = []
        for li in element.find_all("li", recursive=False):
            item = {"text": li.find("a").get_text(strip=True), "path": li.find("a").get('href')}
            nested_ul = li.find("ul")
            if nested_ul:
                item["children"] = ParseContentStructure._parse_ul(nested_ul)
            else:
                item["children"] = []
            result.append(item)
        return result

    @classmethod
    def parse(cls):
        if cls().contents_path.exists():
            with open(cls().contents_path) as file:
                data = file.read()
                soup = BeautifulSoup(data, "html.parser")
                data = soup.find("div", class_=["toctree-wrapper", "compound"])
                uls = data.find("ul")
                return cls._parse_ul(uls)


if __name__ == "__main__":
    source.root = "/home/el1sha/Projects/sqlalchemy-rusdocs/source"
    print(ParseContentStructure.parse())
