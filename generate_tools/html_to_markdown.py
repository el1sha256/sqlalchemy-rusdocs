import bs4
import six
from bs4 import BeautifulSoup
import markdownify

ATX_CLOSED = 'atx_closed'
UNDERLINED = 'underlined'


class CustomConverter(markdownify.MarkdownConverter):
    def convert_hn(self, n, el, text, convert_as_inline):
        if convert_as_inline:
            return text
        text = text.rstrip()
        hashes = '#' * n
        # +# for cheat
        if 'id' in el.attrs.keys():
            return '%s %s {#%s} \n\n' % (hashes + "#", text, el.attrs['id'])
        else:
            return '%s %s \n\n' % (hashes + "#", text)

    def process_text(self, el):
        text = six.text_type(el) or ''

        # dont remove any whitespace when handling pre or code in pre
        if not (el.parent.name == 'pre'
                or (el.parent.name == 'code'
                    and el.parent.parent.name == 'pre')):
            text = markdownify.whitespace_re.sub(' ', text)
        if el.parent.name != 'code' and el.parent.name != 'pre' and el.parent.name != 'marked':
            text = self.escape(text)

        if el.parent.name == 'marked':
            text = f"{text}"
        # remove trailing whitespaces if any of the following condition is true:
        # - current text node is the last node in li
        # - current text node is followed by an embedded list
        if (el.parent.name == 'li'
                and (not el.next_sibling
                     or el.next_sibling.name in ['ul', 'ol'])):
            text = text.rstrip()
        return text


def html_md_converter(data: str):
    converter = CustomConverter()
    converted_text = converter.convert(data)
    return converted_text
