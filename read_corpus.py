import os, json
from bs4 import BeautifulSoup as bs

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '..', 'corpus-xnt-1.0', 'corpus-xces-ntkn-1.0')
files = sorted(os.listdir(DATA_DIR))

replace_d = {
    'ý': 'ı',
    'þ': 'ş',
    'Þ': 'Ş',
    'ð': 'ğ',
    'Ý': 'İ',
}

corpus_d = {}
for file in files:
    with open(os.path.join(DATA_DIR, file), 'r', encoding='ISO-8859-1') as f:
        data_t = f.read()
    soup = bs(data_t, "lxml")
    body_l = soup.find_all('body')
    text_l = []
    for body in body_l:
        p_l = body.find_all('p')
        if not p_l:
            continue
        text_add = ''
        for p in p_l:
            text = p.get_text()
            for k, v in replace_d.items():
                text = text.replace(k, v)
            text_add += text + ' '
        text_add = text_add.replace('\t', ' ')
        text_add = text_add.replace('', "'")
        while '  ' in text_add:
            text_add = text_add.replace('  ', ' ')
        text_l.append(text_add.strip())
    corpus_d[file] = text_l

with open(os.path.join(THIS_DIR, 'corpus.json'), 'w', encoding='utf-8') as f:
    json.dump(corpus_d, f, ensure_ascii=False, indent=4)