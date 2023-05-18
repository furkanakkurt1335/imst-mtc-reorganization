import os, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
corpus_path = os.path.join(THIS_DIR, 'corpus.json')
with open(corpus_path, 'r', encoding='utf-8') as f:
    corpus_d = json.load(f)

new_corpus_d = {}
for k, v in corpus_d.items():
    if len(v) > 1:
        print(k, len(v))
        exit()
    new_corpus_d[k] = v[0]

with open(os.path.join(THIS_DIR, 'corpus.json'), 'w', encoding='utf-8') as f:
    json.dump(new_corpus_d, f, ensure_ascii=False, indent=4)
