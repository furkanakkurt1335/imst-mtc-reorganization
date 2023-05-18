import os, re, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

treebank_path = os.path.join(THIS_DIR, 'treebank.json')
with open(treebank_path, 'r', encoding='utf-8') as f:
    treebank_d = json.load(f)

new_treebank_path = os.path.join(THIS_DIR, 'new_treebank.json')
with open(new_treebank_path, 'r', encoding='utf-8') as f:
    new_treebank_d = json.load(f)

split_l = ['train', 'dev', 'test']
for split in split_l:
    tb_l = []
    for doc_d in new_treebank_d[split]:
        doc_id = doc_d['doc_id']
        sent_ids = doc_d['sent_ids']
        for i, sent_id in enumerate(sent_ids):
            sent_id_s = f'# sent_id = {sent_id}'
            md_t = treebank_d[sent_id]
            text, table = md_t['text'], md_t['table']
            text_s = f'# text = {text}'
            if i == 0:
                doc_s = f'# newdoc id = {doc_id}'
                md_l = [doc_s, sent_id_s, text_s, table]
            else:
                md_l = [sent_id_s, text_s, table]
            md_s = '\n'.join(md_l)
            tb_l.append(md_s)
    tb_s = '\n\n'.join(tb_l)
    with open(os.path.join(THIS_DIR, f'{split}.conllu'), 'w', encoding='utf-8') as f:
        f.write(tb_s + '\n\n')
