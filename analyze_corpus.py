import os, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
corpus_path = os.path.join(THIS_DIR, 'corpus.json')
with open(corpus_path, 'r', encoding='utf-8') as f:
    corpus_d = json.load(f)

for k, v in corpus_d.items():
    if len(v) != 1:
        print(k, len(v))