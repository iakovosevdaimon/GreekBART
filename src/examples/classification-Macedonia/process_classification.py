
import os
from normalize_text import cleaner
import pandas as pd
import random
import re
import json

script_dir = os.path.dirname(os.path.realpath(__file__))
path_bash_script = os.path.join(script_dir, 'get-classification.sh')

os.system('bash {}'.format(path_bash_script))

path = os.path.join(script_dir, 'data/raw')
path_new = os.path.join(script_dir, 'data/processed')
raw_file = os.path.join(path, 'greek_classification_dataset.csv')

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
    txt = txt.replace("\n",".")
    txt = cleaner(txt)
    return txt


def write_data(filepath, typeofdata, dataset):
    filepath_data = os.path.join(filepath, '{}.sent'.format(typeofdata))
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


df = pd.read_csv(raw_file, header=0)

labels = list(df['Label'].unique())
L2I = {lab:i for i,lab in enumerate(labels)}
I2L = {i:lab for i,lab in enumerate(labels)}

with open("./data/classification_labels.json", "w") as outfile:
    json.dump(I2L, outfile)
# we have unbalanced labels
#labels(as key) and the number of instances in the dataset that belong to each label(as value)
#L2C = {i:row for i, row in df['Label'].value_counts().iteritems()}

I2List = {}
for _, row in df.iterrows():
    ind = L2I.get(row["Label"])
    if ind not in I2List:
        I2List[ind] = [[row['Text'], ind]]
    else:
        v = [row['Text'], ind]
        temp = I2List.get(ind)
        temp.append(v)
        I2List[ind] = temp

del df
#split dataset to train, valid, test
train_set = []
valid_set = []
test_set = []
train_dict = {}
for k in I2List.keys():
    temp = I2List.get(k)
    random.shuffle(temp)
    #I2List[k] = temp
    n_dev = int(dev_per*len(temp))
    dev_samples = temp[:n_dev]
    train_dict[k] = temp[n_dev:]
    train_set += temp[n_dev:]
    random.shuffle(dev_samples)
    n_test = int(0.5*len(dev_samples))
    test_set += dev_samples[:n_test]
    valid_set += dev_samples[n_test:]


random.shuffle(valid_set)
random.shuffle(test_set)

write_data(path_new,'valid',valid_set)
write_data(path_new,'test',test_set)

# boolean argument 
# change the below argument from False to True in order to apply to apply oversampling
oversample = False
if oversample:
    #apply Oversampling
    I2C = {}
    for k in train_dict.keys():
        I2C[k] = len(train_dict[k])

    all_values = I2C.values()
    max_label = max(all_values)

    for k in I2C.keys():
        cur_count = I2C.get(k)
        n = max_label - cur_count
        if n > 0:
            if n > cur_count:
                times = int(n/cur_count)
                md = n%cur_count
                for _ in range(times):
                    train_set+=train_dict.get(k)
                train_set+=random.sample(train_dict.get(k), md)
            else:
                train_set+=random.sample(train_dict.get(k), n)

random.shuffle(train_set)
write_data(path_new,'train',train_set)
os.system('rm -rf ./data/raw')
