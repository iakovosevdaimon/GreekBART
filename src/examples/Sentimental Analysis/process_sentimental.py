import pandas as pd
import numpy as np
import random
import os
from ..normalize_text import cleaner
import re
import json

path="./data/athinorama.csv"
path_new = "./data/processed"

I2L = {0:"negative",1:"positive"}
with open(os.path.join(path_new,"labels.json"), "w") as outfile:
    json.dump(I2L, outfile)

if os.path.exists(path_new):
    os.system('rm -rf ./data/processed')
os.system('mkdir ./data/processed')

valid_per = 0.15
test_per = 0.15
train_per = 0.7
dev_per = test_per + valid_per
random.seed(7)

def remove_mentions_and_tags(text):
    text = re.sub(r'@\S*', "", text)
    return re.sub(r"#\S*", "", text)

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)


def text_clean(txt):
    txt = re.sub("http\S+|www\S+|WWW\S+",'',txt)
    txt = deEmojify(txt)
    txt = remove_mentions_and_tags(txt)
    txt.strip()
    txt = cleaner(txt)
    return txt


def write_data(filepath, typeofdata, dataset):
    filepath_data = os.path.join(filepath, '{}.review'.format(typeofdata))
    filepath_label = os.path.join(filepath, '{}.label'.format(typeofdata))
    fw_data = open(filepath_data, 'w')
    fw_label = open(filepath_label, 'w')
    for i,el in enumerate(dataset):
        if i!=len(dataset)-1:
            fw_label.write('{}\n'.format(el[1]))
            txt = el[0]
            txt = text_clean(txt)
            fw_data.write('{}\n'.format(txt))
        else:
            fw_label.write('{}'.format(el[1]))
            txt = el[0]
            txt = text_clean(txt)
            fw_data.write(txt)
    fw_data.close()
    fw_label.close()

df = pd.read_csv(path, header=0)

df['sent_label'] = np.where(df['label'] > 3, 1, 0)
df_final=df[['review','sent_label']]
del df


pos_reviews = []
neg_reviews = []
for _, row in df_final.iterrows():
    if row["sent_label"] == 1:
        pos_reviews.append([row['review'],1])
    else:
        neg_reviews.append([row['review'], 0])

del df_final
random.shuffle(pos_reviews)
random.shuffle(neg_reviews)

n_dev_pos = int(dev_per*len(pos_reviews))
n_dev_neg = int(dev_per*len(neg_reviews))

dev_reviews_pos = pos_reviews[:n_dev_pos]
dev_reviews_neg = neg_reviews[:n_dev_neg]
train_reviews = pos_reviews[n_dev_pos:] + neg_reviews[n_dev_neg:]

random.shuffle(dev_reviews_pos)
random.shuffle(dev_reviews_neg)
n_test_pos = int(0.5*len(dev_reviews_pos))
n_test_neg = int(0.5*len(dev_reviews_neg))
test_reviews = dev_reviews_pos[:n_test_pos] + dev_reviews_neg[:n_test_neg]
valid_reviews = dev_reviews_pos[n_test_pos:] + dev_reviews_neg[n_test_neg:]

random.shuffle(pos_reviews)
random.shuffle(neg_reviews)
random.shuffle(train_reviews)
random.shuffle(valid_reviews)
random.shuffle(test_reviews)
write_data(path_new,'valid',valid_reviews)
write_data(path_new,'train',train_reviews)
write_data(path_new,'test',test_reviews)
