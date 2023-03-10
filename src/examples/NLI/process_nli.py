# Editor: Moussa Kamal Eddine
# Modified from
# https://github.com/moussaKam/BARThez/blob/main/FLUE/prepare_xnli.py
# Original copyright is appended below.
#
# Copyright 2021, Moussa Kamal Eddine
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import json
import os
from ..normalize_text import cleaner

script_dir = os.path.dirname(os.path.realpath(__file__))
#path_bash_script = os.path.join(script_dir, 'get-xnli.sh')

#os.system('bash {}'.format(path_bash_script))

path = os.path.join(script_dir, 'data/processed')
path_new = './XNLI'
os.system('mkdir '+str(path_new))

datasets = [('el.raw.valid', 'valid'), ('el.raw.test', 'test'), ('el.raw.train', 'train')]

def write_data(path, data):
    with open(path, 'w+') as fw:
        for element in data:
            fw.write('{}\n'.format(element))
        fw.close()

labels = ['contradiction', 'entailment', 'neutral']
I2L = {i:k for i, k in enumerate(labels)}
with open(os.path.join(path_new,"NLI_labels.json"), "w") as outfile:
    json.dump(I2L, outfile)
for dataset in datasets:
    with open(os.path.join(path, dataset[0]), 'r') as fr:
        fr.readline() #skip first line
        examples = []
        for line in fr:
            example = line.split('\t')
            example[-1] = example[-1].strip()
            assert example[-1] in labels
            example[-1] = labels.index(example[-1])
            examples.append(example)
        write_data(os.path.join(path_new, '{}.sent1'.format(dataset[1])),
                  [cleaner(example[0]) for example in examples])
        write_data(os.path.join(path_new, '{}.sent2'.format(dataset[1])),
                  [cleaner(example[1]) for example in examples])
        write_data(os.path.join(path_new, '{}.label'.format(dataset[1])),
                   [example[2] for example in examples])
        fr.close()

#os.system('rm -rf ./data/processed')
#os.system('rm -rf ./data/raw')
