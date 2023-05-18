import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '..', 'UD_Turkish-IMST')
files = [f for f in os.listdir(DATA_DIR) if f.endswith('.conllu')]
for f in files:
    with open(os.path.join(DATA_DIR, f), 'r') as infile:
        data_t = infile.read()
    print(f, data_t.count('\n\n'))

# tr_imst-ud-dev.conllu 975
# tr_imst-ud-test.conllu 975
# tr_imst-ud-train.conllu 3685