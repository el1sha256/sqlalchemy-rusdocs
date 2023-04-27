from chatgpt_translator import get_paraphed_token_checked_strings, base_path

with open('new_files.txt', 'r') as f:
    files = f.readlines()
    not_processed_files = files[:]
for e, file in enumerate(files):
    print(f'file: {str(file)} {e + 1}/{len(files)}', end='\r')
    md_path = base_path / 'sqlalchemy_20_md' / file[1:-1]
    with open(md_path) as t:
        tmp_data = t.read()
    try:
        # workflow(read_text_from_file(md_path), rus_path)
        get_paraphed_token_checked_strings(tmp_data)
    except AssertionError as e:
        with open('need_human_editing.txt', 'a+') as f:
            f.write(file)
        break
        # print("error", e)
