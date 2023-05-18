import os, re, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

treebank_path = os.path.join(THIS_DIR, 'treebank.json')
with open(treebank_path, 'r', encoding='utf-8') as f:
    treebank_d = json.load(f)

corpus_path = os.path.join(THIS_DIR, 'corpus.json')
with open(corpus_path, 'r', encoding='utf-8') as f:
    corpus_d = json.load(f)

sent_corp_path = os.path.join(THIS_DIR, 'sent_corp_idx.json')
with open(sent_corp_path, 'r', encoding='utf-8') as f:
    sent_corp_d = json.load(f)

sent_count = 0
for i, doc_id in enumerate(sent_corp_d.keys()):
    print(doc_id, len(sent_corp_d[doc_id].keys()))
    sent_count += len(sent_corp_d[doc_id].keys())
print('Total sentences: {}'.format(sent_count))