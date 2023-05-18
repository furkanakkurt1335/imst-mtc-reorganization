import os, re, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

treebank_path = os.path.join(THIS_DIR, 'treebank.json')
with open(treebank_path, 'r', encoding='utf-8') as f:
    treebank_d = json.load(f)

sent_corp_path = os.path.join(THIS_DIR, 'sent_corp_idx.json')
with open(sent_corp_path, 'r', encoding='utf-8') as f:
    sent_corp_d = json.load(f)

# all: 5635, train: 3685, dev: 975, test: 975
new_tb_d = {'train': [], 'dev': [], 'test': []}
train_counter, dev_counter, test_counter = 0, 0, 0
for doc_id, sent_d in sent_corp_d.items():
    # order by indices
    sent_l = [i[0] for i in sorted(sent_d.items(), key=lambda x: x[1])]
    if train_counter + len(sent_d.keys()) <= 3685:
        train_counter += len(sent_d.keys())
        new_tb_d['train'].append({'doc_id': doc_id, 'sent_ids': sent_l})
    else:
        if dev_counter + len(sent_d.keys()) <= 975:
            dev_counter += len(sent_d.keys())
            new_tb_d['dev'].append({'doc_id': doc_id, 'sent_ids': sent_l})
        else:
            test_counter += len(sent_d.keys())
            new_tb_d['test'].append({'doc_id': doc_id, 'sent_ids': sent_l})

with open(os.path.join(THIS_DIR, 'new_treebank.json'), 'w', encoding='utf-8') as f:
    json.dump(new_tb_d, f, indent=2, ensure_ascii=False)