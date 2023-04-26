from read_html import Parser
from clear_html import CleanHtml
from chatgpt_translator import workflow
from html_to_markdown import html_md_converter


def main():
    filename = input("Filename: ")
    file = filename.split('.')[-1]
    parser = Parser(filename)

    cleaner = CleanHtml(parser.tree)
    cleaner.clean_and_fix()

    md_text = html_md_converter(str(cleaner.body))
    with open('output.md', 'w') as f:
        f.write(str(md_text))
    # workflow(str(md_text), file)


main()
