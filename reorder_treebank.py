import os, json, difflib

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
    max_size, doc_id_max, idx = 0, None, None
    for doc_id, body in corpus_d.items():
        s = difflib.SequenceMatcher(None, body, text_t)
        size_t = s.find_longest_match().size
        if size_t == len(text_t):
            doc_id_max = doc_id
            idx = s.find_longest_match().a
            break
        elif size_t > max_size:
            max_size = size_t
            doc_id_max = doc_id
            idx = s.find_longest_match().a
    doc_id = doc_id_max
    if doc_id not in sent_corp_d.keys():
        sent_corp_d[doc_id] = {}
    sent_corp_d[doc_id][k] = idx
    counter += 1
    if counter % 100 == 0:
        print('Remaining: {}'.format(tb_len - counter))
        with open('sent_corp.json', 'w', encoding='utf-8') as f:
            json.dump(sent_corp_d, f, indent=4, ensure_ascii=False)

with open('sent_corp.json', 'w', encoding='utf-8') as f:
    json.dump(sent_corp_d, f, indent=4, ensure_ascii=False)
