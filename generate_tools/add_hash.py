with open('/home/el1sha/Projects/sqlalchemy-rusdoc/generate_tools/sqlalchemy_20_rus/tutorial/data_select.md') as f:
    data_lines = f.readlines()


new_data = []

for i in data_lines:
    if i[0] == "#":
        new_data.append("#" + i)
    else:
        new_data.append(i)
nn_data = []
for i in new_data:
    # t1 = i.replace('#####', '')
    t2 = i.replace('######', '')
    # for j in ['#####', '######']:
    #     t = i.replace(j, '')
    nn_data.append(t2)


with open('/home/el1sha/Projects/sqlalchemy-rusdoc/generate_tools/sqlalchemy_20_rus/tutorial/data_select.md', 'w') as f:
    data_lines = f.writelines(nn_data)