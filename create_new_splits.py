import os, json, random

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

treebank_path = os.path.join(THIS_DIR, 'treebank.json')
with open(treebank_path, 'r', encoding='utf-8') as f:
    treebank_d = json.load(f)

def get_token_count(sent_id):
    return treebank_d[sent_id]['token_count']

avg_token_count = 0
for sent_id in treebank_d.keys():
    table = treebank_d[sent_id]['table']
    table_l = table.split('\n')
    last_row = table_l[-1]
    fields = last_row.split('\t')
    id_t = fields[0]
    token_count = int(id_t)
    # print(token_count)
    avg_token_count += token_count
    treebank_d[sent_id]['token_count'] = token_count
avg_token_count /= len(treebank_d.keys())
print(f'avg_token_count: {avg_token_count}')

sent_corp_path = os.path.join(THIS_DIR, 'sent_corp.json')
with open(sent_corp_path, 'r', encoding='utf-8') as f:
    sent_corp_d = json.load(f)

doc_count_d = {}
for doc_id, sent_d in sent_corp_d.items():
    # order by indices
    sent_l = [i[0] for i in sorted(sent_d.items(), key=lambda x: x[1])]
    sent_count = len(sent_l)
    doc_id = doc_id.replace('.xcs', '')
    token_count = 0
    for i in range(sent_count):
        token_count += get_token_count(sent_l[i])
    doc_count_d[doc_id] = {'sent_count': sent_count, 'token_count': token_count, 'avg_token_count': token_count / sent_count}

# all: 5635, train: 3685, dev: 975, test: 975
new_tb_d = {'train': [], 'dev': [], 'test': []}
sent_count_d = {'train': 0, 'dev': 0, 'test': 0}
token_count_d = {'train': 0, 'dev': 0, 'test': 0}
doc_d = {'train': ["00016112", "00032161", "00038121", "00044121", "00053223", "00058111", "00084111", "00095233", "00105133", "00111211", "00142211", "00166271", "20200000", "20210000", "20270000", "20580000", "20710000", "21040000", "22080000"], 'dev': ["00002213", "22280000"], 'test': ["00048220", "00099161", "20970000"]} # in line with CorefUD ITCC
docs_used = []
for doc_id, sent_d in sent_corp_d.items():
    # order by indices
    sent_l = [i[0] for i in sorted(sent_d.items(), key=lambda x: x[1])]
    doc_id = doc_id.replace('.xcs', '')
    split = None
    if doc_id in doc_d['train']:
        split = 'train'
    elif doc_id in doc_d['dev']:
        split = 'dev'
    elif doc_id in doc_d['test']:
        split = 'test'
    if split is None:
        continue
    sent_count_d[split] += len(sent_l)
    token_count_d[split] += doc_count_d[doc_id]['token_count']
    docs_used.append(doc_id)
    new_tb_d[split].append({'doc_id': doc_id, 'sent_ids': sent_l})

doc_l = [(doc_id, doc_count_d[doc_id]['avg_token_count']) for doc_id in doc_count_d.keys()]
doc_l.sort(key=lambda x: x[1], reverse=True)
random.shuffle(doc_l)

for doc_id, avg_token_count in doc_l:
    # order by indices
    sent_d = sent_corp_d[doc_id + '.xcs']
    sent_l = [i[0] for i in sorted(sent_d.items(), key=lambda x: x[1])]
    sent_count = len(sent_l)
    token_count = doc_count_d[doc_id]['token_count']
    doc_id = doc_id.replace('.xcs', '')
    if doc_id in docs_used:
        continue
    split = None
    if sent_count_d['dev'] + sent_count <= 1100:
        split = 'dev'
    elif sent_count_d['test'] + sent_count <= 1100:
        split = 'test'
    else:
        split = 'train'
    if split is None:
        continue
    sent_count_d[split] += sent_count
    token_count_d[split] += token_count
    new_tb_d[split].append({'doc_id': doc_id, 'sent_ids': sent_l})

for split in ['train', 'dev', 'test']:
    new_tb_d[split].sort(key=lambda x: x['doc_id'])

print(sent_count_d, token_count_d)

with open(os.path.join(THIS_DIR, 'new_treebank.json'), 'w', encoding='utf-8') as f:
    json.dump(new_tb_d, f, indent=2, ensure_ascii=False)
