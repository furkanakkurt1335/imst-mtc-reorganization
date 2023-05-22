import os, argparse, re

parser = argparse.ArgumentParser()
parser.add_argument('--folder', type=str)
args = parser.parse_args()
tb_dir = args.folder
files = [f for f in os.listdir(tb_dir) if f.endswith('.conllu')]

annotation_pattern = r'# sent_id = (.*?)\n# text = (.*?)\n(.*?)\n\n'
treebank_d = {}
count_d = {'train': {'sent': 0, 'token': 0}, 'dev': {'sent': 0, 'token': 0}, 'test': {'sent': 0, 'token': 0}}
for f in files:
    if 'train' in f:
        split = 'train'
    elif 'dev' in f:
        split = 'dev'
    elif 'test' in f:
        split = 'test'
    with open(f, 'r', encoding='utf-8') as infile:
        data_t = infile.read()
    annotations = re.findall(annotation_pattern, data_t, re.DOTALL)
    count_d[split]['sent'] += len(annotations)
    for annotation in annotations:
        sent_id, text, table = annotation
        rows = table.split('\n')
        last_row = rows[-1]
        fields = last_row.split('\t')
        token_count = int(fields[0])
        count_d[split]['token'] += token_count

print(count_d)