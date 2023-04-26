from pathlib import Path

from bs4 import BeautifulSoup


class Parser:
    def __init__(self, filename: str | Path):
        self.raw_text = self.__read(filename)
        self.tree = self.__parse()

    def __get_doc_body(self):
        elements = self.tree.find_all(id='docs-body')

        end_result = ""
        # Print the contents of each element
        for element in elements:
            end_result += element.get_text()

        return end_result

    def __parse(self):
        return BeautifulSoup(self.raw_text, 'html.parser')

    @staticmethod
    def __read(filename):
        with open(filename) as f:
            return f.read()
