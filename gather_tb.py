import os, re, json
import pylcs

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

treebank_path = os.path.join(THIS_DIR, 'treebank.json')
with open(treebank_path, 'r', encoding='utf-8') as f:
    treebank_d = json.load(f)

corpus_path = os.path.join(THIS_DIR, 'corpus.json')
with open(corpus_path, 'r', encoding='utf-8') as f:
    corpus_d = json.load(f)

sent_corp_path = os.path.join(THIS_DIR, 'sent_corp.json')
with open(sent_corp_path, 'r', encoding='utf-8') as f:
    sent_corp_d = json.load(f)

def get_lcs_idx(l):
    for i, el in enumerate(l):
        if el != -1:
            return i
    return -1

new_d = {}
counter = 0
for doc_id, sent_id_l in sent_corp_d.items():
    if doc_id not in new_d.keys():
        new_d[doc_id] = {}
    doc_s = corpus_d[doc_id]
    for sent_id in sent_id_l:
        sent_s = treebank_d[sent_id]['text']
        idx_l_t = pylcs.lcs_string_idx(doc_s, sent_s)
        idx = get_lcs_idx(idx_l_t)
        new_d[doc_id][sent_id] = idx
        counter += 1
    if counter % 100 == 0:
        print('Remaining: {}'.format(len(sent_corp_d.keys()) - counter))
        with open('sent_corp_idx.json', 'w', encoding='utf-8') as f:
            json.dump(new_d, f, ensure_ascii=False, indent=2)

with open('sent_corp_idx.json', 'w', encoding='utf-8') as f:
    json.dump(new_d, f, ensure_ascii=False, indent=2)