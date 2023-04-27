import os
from time import sleep
from datetime import datetime
from pathlib import Path

import openai
import tiktoken
from bs4 import BeautifulSoup
import logging

from secret import apikey

# Load your API key from an environment variable or secret management service
openai.api_key = apikey
requests_per_minute = 2.9
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger()
base_path = Path(__file__).parent


def send_request_to_api_gpt(string: str, max_tokens: int):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant",
             "content": "translate from english to russian for technical documentation, dont touch markdown markup"},
            {"role": "system",
             "content": "Translate from english to russian for technical documentation, dont touch markdown markup"},
            {"role": "user",
             "content": string},
        ],
        temperature=0.7,
        max_tokens=max_tokens,
        top_p=0.5
    )
    result = response['choices'][0]['message']['content']
    return result


def num_tokens_from_string(string: str, encoding_name: str = "gpt-3.5-turbo") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)

    num_tokens = len(encoding.encode(string))
    return num_tokens


def read_text_from_file(filename: str or Path) -> str:
    logger.info("Чтение и парсинг...")

    # Read the XML file
    with open(filename, 'r') as f:
        xml_data = f.read()

    return xml_data


def write_to_file(filename: str, data: str, mode: str = "a+"):
    with open(filename, mode) as f:
        f.write(data)


def get_paraphed_token_checked_strings(cleaned_text):
    paraphed = cleaned_text.split("\n\n")
    paraphed = [x for x in paraphed if len(x) != 0]
    paraphed = [x + "\n\n" for x in paraphed]
    paraphed = paraphed[1: -1]
    # max_token_len = 820
    res_list = []
    tmp_str = ''
    tmp_mtl = 820
    for i in range(len(paraphed)):
        ntfs = num_tokens_from_string(paraphed[i])
        tmp_mtl -= ntfs
        if tmp_mtl > 0:
            tmp_str += paraphed[i]
        elif ntfs > 820:
            print(f"overflowed paragraph {paraphed[i]}")
            raise AssertionError("To many tokens in paragraph")
        else:
            res_list.append(tmp_str)
            tmp_str = ''
            tmp_str += paraphed[i]
            tmp_mtl = 820 - ntfs
    else:
        res_list.append(tmp_str)
    return res_list


def workflow(cleaned_text: str, output_file: str or Path):
    res = get_paraphed_token_checked_strings(cleaned_text)
    with open(output_file, 'w') as output:
        for ei, i in enumerate(res):
            # write_to_file('hi.txt', i)
            logger.info(f"Перевод секции {ei + 1}/{len(res)}")
            start_translate = datetime.timestamp(datetime.now())
            translated_text = send_request_to_api_gpt(i, 820)
            end_translate = datetime.timestamp(datetime.now())
            logger.info(f"Перевод завершен")
            logger.info("Запись в файл...")
            # write_to_file(output_file, translated_text)
            output.write(translated_text)
            if (21 - (end_translate - start_translate)) > 0:
                # print((21 - (end_translate - start_translate)))
                sleep((21 - (end_translate - start_translate)))
    # write_to_file(output_file, result_translated, 'w')


if __name__ == "__main__":
    # try:
    #     file = "sqlalchemy_20_md/index.md"
    #     text = read_text_from_file(file)
    #     # write_to_file(f"raw_{file}.txt", text, 'w')
    #     workflow(text, "index.md")
    #
    # except KeyboardInterrupt:
    #     logger.info("Bye")
    with open('new_files.txt', 'r') as f:
        files = f.readlines()
        not_processed_files = files[:]
    with open('need_human_editing.txt') as y:
        exclude_files = y.readlines()
    for e, file in enumerate(files):
        if file in exclude_files:
            continue
        print(f'file: {str(file)} {e + 1}/{len(files)}', end='\r')
        md_path = base_path / 'sqlalchemy_20_md' / file[1:-1]
        rus_path = base_path / 'sqlalchemy_20_rus' / file[1: -1]
        try:
            workflow(read_text_from_file(md_path), rus_path)
            not_processed_files.remove(file)
            with open('new_files.txt', 'w') as f:
                f.writelines(not_processed_files)
        except Exception as e:
            with open('new_files.txt', 'w') as f:
                f.writelines(not_processed_files)
            print("error", e)
