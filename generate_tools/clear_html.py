from bs4 import BeautifulSoup

remove_with_class_and_tag_candidates = {'aside': 'topic', 'a': 'headerlink'}


class CleanHtml:
    def __init__(self, tree):
        self.tree = tree
        self.body = self.tree.find_all(id='docs-body')[0]

    def clean_and_fix(self):
        self.__remove_by_tag_and_class()
        self.__remove_all_tags_inside_code_block()
        self.__replace_span_pre_to_marked()
        self.__fix_titles_ids()

    def __remove_by_tag_and_class(self):
        for key in remove_with_class_and_tag_candidates.keys():
            for el in self.body.find_all(key, {'class': remove_with_class_and_tag_candidates[key]}):
                el.decompose()

    def __remove_all_tags_inside_code_block(self):
        code_blocks = self.body.find_all('div', {'class': 'highlight-pycon+sql'})
        for i in code_blocks:
            code = i.get_text()
            i.findNext('div').decompose()
            code_tag = self.tree.new_tag("pre")
            code_tag.string = code
            i.append(code_tag)

    def __replace_span_pre_to_marked(self):
        code_blocks = self.body.find_all('span', {'class': 'pre'})
        for i in code_blocks:
            code = i.get_text()
            i.string = ''
            code_tag = self.tree.new_tag("marked")
            code_tag.string = code
            i.append(code_tag)

    def __fix_titles_ids(self):
        for heading in self.body.find_all(["h1", "h2", "h3", "h4"]):
            heading.attrs['id'] = heading.previous_element.attrs['id']
