from pathlib import Path

from read_html import Parser
from clear_html import CleanHtml
from chatgpt_translator import workflow
from html_to_markdown import html_md_converter
import os


def main(filename):
    # filename = input("Filename: ")
    file = filename.split('.')[-1]
    parser = Parser(filename)

    cleaner = CleanHtml(parser.tree)
    cleaner.clean_and_fix()

    md_text = html_md_converter(str(cleaner.body))
    return md_text
    # with open('output.md', 'r') as f:
    #     data = f.read()
    # workflow(str(data), file)


def run():
    with open('new_files.txt', 'r') as f:
        files = f.readlines()
    for e, file in enumerate(files):
        print(f'file: {str(file)} {e}/{len(files)}', end='\r')
        path = str(file).replace('\n', '')
        path_end = path.split('home/el1sha/Projects/sqlalchemy-rusdoc/generate_tools/sqlalchemy_20')[1]
        fixed_end = path_end.split('.')
        path_end = fixed_end[0] + "." + "md"
        path_start = '/generate_tools/sqlalchemy_20_md'
        Path(path_start+'/'.join(path_end.split('/')[1: -1])).mkdir(parents=True, exist_ok=True)

        with open(path_start+path_end, 'w') as f:
            f.write(main(path))
run()
