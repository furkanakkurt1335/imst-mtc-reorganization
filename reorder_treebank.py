import os, re, json
# from thefuzz import fuzz, process
from rapidfuzz import fuzz, process
from time import sleep

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
treebank_path = os.path.join(THIS_DIR, 'treebank.json')
with open(treebank_path, 'r', encoding='utf-8') as f:
    treebank_d = json.load(f)
corpus_path = os.path.join(THIS_DIR, 'corpus.json')
with open(corpus_path, 'r', encoding='utf-8') as f:
    corpus_d = json.load(f)

sent_corp_d = {}

tb_len = len(treebank_d.keys())
counter = 0
for k, v in treebank_d.items():
    text_t = v['text']
    match = process.extractOne(text_t, corpus_d, scorer=fuzz.token_set_ratio)
    doc_id = match[2]
    if doc_id not in sent_corp_d.keys():
        sent_corp_d[doc_id] = []
    sent_corp_d[doc_id].append(k)
    counter += 1
    print('Remaining: {}'.format(tb_len - counter))

with open('sent_corp.json', 'w', encoding='utf-8') as f:
    json.dump(sent_corp_d, f, ensure_ascii=False, indent=2)