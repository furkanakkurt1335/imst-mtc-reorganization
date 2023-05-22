import os, json, stanza, difflib

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

treebank_path = os.path.join(THIS_DIR, 'treebank.json')
with open(treebank_path, 'r', encoding='utf-8') as f:
    treebank_d = json.load(f)

new_treebank_path = os.path.join(THIS_DIR, 'new_treebank.json')
with open(new_treebank_path, 'r', encoding='utf-8') as f:
    new_treebank_d = json.load(f)

corpus_path = os.path.join(THIS_DIR, 'corpus.json')
with open(corpus_path, 'r', encoding='utf-8') as f:
    corpus_d = json.load(f)

sent_corp_path = os.path.join(THIS_DIR, 'sent_corp.json')
with open(sent_corp_path, 'r', encoding='utf-8') as f:
    sent_corp_d = json.load(f)

nlp = stanza.Pipeline(lang='tr', processors='tokenize')

used_sent_ids = {}
for split in ['train', 'dev', 'test']:
    tb_l = []
    for doc_d in new_treebank_d[split]:
        doc_id = doc_d['doc_id']
        sent_d = sent_corp_d[doc_id + '.xcs']
        sent_ids = [(k, v) for k, v in sent_d.items()]
        sent_ids = sorted(sent_ids, key=lambda x: x[1])
        sent_ids = [i[0] for i in sent_ids]
        for i, sent_id in enumerate(sent_ids):
            old_sent_id_s = f'# old_sent_id = {sent_id}'
            md_t = treebank_d[sent_id]
            text, table = md_t['text'], md_t['table']
            text_s = f'# text = {text}'
            max_size, order_max = 0, 0
            doc = nlp(corpus_d[doc_id + '.xcs'])
            for i, sentence in enumerate(doc.sentences):
                s = difflib.SequenceMatcher(None, sentence.text, text)
                size_t = s.find_longest_match().size
                if size_t > max_size:
                    max_size = size_t
                    order_max = i
            new_sent_id = f'{doc_id}_{order_max}'
            if new_sent_id in used_sent_ids.keys():
                print(new_sent_id, 'already used')
                print('old sent id:', used_sent_ids[new_sent_id])
                print('new sent id:', sent_id)
            else:
                used_sent_ids[new_sent_id] = sent_id
            sent_id_s = f'# sent_id = {new_sent_id}'
            if i == 0:
                doc_s = f'# newdoc id = {doc_id}'
                md_l = [doc_s, old_sent_id_s, sent_id_s, text_s, table]
            else:
                md_l = [old_sent_id_s, sent_id_s, text_s, table]
            md_s = '\n'.join(md_l)
            tb_l.append(md_s)
        print(doc_id, 'done')
    tb_s = '\n\n'.join(tb_l)
    with open(os.path.join(THIS_DIR, f'{split}.conllu'), 'w', encoding='utf-8') as f:
        f.write(tb_s + '\n\n')
        print(split, 'done')
