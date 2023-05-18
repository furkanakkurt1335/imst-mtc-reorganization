import os, re, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '..', 'UD_Turkish-IMST')
files = [f for f in os.listdir(DATA_DIR) if f.endswith('.conllu')]
annotation_pattern = r'# sent_id = (.*?)\n# text = (.*?)\n(.*?)\n\n'
treebank_d = {}
for f in files:
    with open(os.path.join(DATA_DIR, f), 'r', encoding='utf-8') as infile:
        data_t = infile.read()
    annotations = re.findall(annotation_pattern, data_t, re.DOTALL)
    for annotation in annotations:
        sent_id, text, table = annotation
        treebank_d[sent_id] = {'text': text, 'table': table}

with open(os.path.join(THIS_DIR, 'treebank.json'), 'w', encoding='utf-8') as outfile:
    json.dump(treebank_d, outfile, indent=4, ensure_ascii=False)
