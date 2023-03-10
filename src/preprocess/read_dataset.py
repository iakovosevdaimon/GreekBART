# runiq source: https://github.com/whitfin/runiq

import fnmatch
import os.path
import shutil
import re
import gzip
import json
from multiprocessing import Pool
from read_eu import create_dataset_eu
from clean_oscar import clean_sent_oscar, clean_doc_oscar
from read_wikipedia import read_dataset_wikipedia
from clean_text import cleaner
from clean_crawler import crawler_cleaner

oscar_path = "data/OSCAR/"
crawler_path = "data/Crawler/"
eu_path = "data/EU Parliament/"
#wiki_path = "data/Wikipedia/"

# read all datasets

'''
# crawler refers to the dataset of Outsios et al.
# take each path and read all folders/files until to find out the appropriate files with the suitable prefix or suffix.
# After that, I read these data(maybe I have to create a create as DatasetLoader.

# in wiki open only the text.xml file-> wiki's dataset wants preprocess because it is in xml format
# in other to open the compressed files(.gz->OSCAR, crawler and parliament)
'''
def find_dataset(oscar_path, crawler_path, eu_path):
    oscar_files = []
    crawler_files = []
    eu_files = []
    paths = [oscar_path, crawler_path, eu_path]
    switcher = {1: oscar_files, 3: crawler_files, 4: eu_files}
    for path in paths:
        for root, curDir, files in os.walk(path):
            for f in files:
                c = 0
                if 'OSCAR' in root:
                    c = 1
                    pattern = '*.gz'
                elif 'Crawler' in root:
                    c = 3
                    pattern = '*.gz'
                else:
                    c = 4
                    pattern = '*.tgz'

                if fnmatch.fnmatch(f, pattern):
                    switcher.get(c).append(os.path.join(root, f))
    print('Loading of paths is done')
    return oscar_files, crawler_files, eu_files


def preprocess_compressed(file, to_file, dataset, mode):
    fw = open(to_file,'w', encoding='utf-8')
    if mode == 1:
        prefix = to_file.find("el_meta_part")
        to_file_all = to_file[:prefix] + "el_meta_all.txt"
        fw_all = open(to_file_all, 'a', encoding='utf-8')
    if dataset == "oscar":
        with gzip.GzipFile(file, 'r') as fin:
            for line in fin:
                l = json.loads(line)['content'].encode("utf-8", "ignore").decode()
                annotate = json.loads(line)["metadata"]['annotation']
                if annotate is not None:
                    if "noisy" in annotate:
                        continue
                sents = l.split('\n')
                txt = ""
                for s in sents:
                    t = clean_sent_oscar(s)
                    if t is not None:
                        txt=txt+' '+t
                if txt!="" and txt!="None" and txt is not None:
                    txt = txt.strip()
                    txt = clean_doc_oscar(txt)
                    if txt is not None:
                        txt = cleaner(txt)
                        txt = txt.strip()
                        if not txt[0].isupper():
                            txt = txt[0].upper()+txt[1:]
                        if not re.match(".*[.!;:,·]$", txt):
                            txt = txt+'.'
                        fw.write("{}\n".format(txt))
                        if mode == 1:
                            fw_all.write("{}\n".format(txt))
    else:
        with gzip.open(file, 'rt') as fin:
            for line in fin:
                text = crawler_cleaner(line)
                if text is not None:
                    text = cleaner(text)
                    text = text.strip()
                    if not text[0].isupper():
                        text = text[0].upper()+text[1:]
                    if not re.match(".*[.!;:,·]$", text):
                        text = text+'.'
                    fw.write("{}\n".format(text))
    if mode == 1:
        fw_all.close()
    fw.close()



# read datasets
oscar_files, crawler_files, eu_files = find_dataset(oscar_path, crawler_path, eu_path)

# preprocess EU Parliament dataset
create_dataset_eu(eu_files[0], eu_path)
print('Preprocess of the EU Parliament dataset is done')


# preprocess wikipedia dataset
read_dataset_wikipedia()
print('Preprocess of the Wikipedia dataset is done')

# preprocess OSCAR and crawled datasets
# crawler
file = crawler_files[0]
prefix = file.find(".gz")
des_file = file[:prefix]
preprocess_compressed(file, des_file, 'crawler', 0)
print('Preprocess of the crawled dataset is done')

# OSCAR
fl = oscar_files[0]
prefix = fl.find("el_meta_part")
par_dir = fl[:prefix]
folder = os.path.join(par_dir, 'texts')
if os.path.exists(folder):
    shutil.rmtree(folder)
os.mkdir(folder)
total = len(oscar_files)
for i,file in enumerate(oscar_files):
    prefix = file.find("el_meta_part")
    suffix = file.find(".json")
    des_file = folder+'/'+file[prefix:suffix]+'.txt'
    preprocess_compressed(file, des_file, 'oscar', 1)
    if (i+1) % 10 == 0:
        print('Processing %d/%d' % (i+1, total))
print('Preprocess of the OSCAR dataset is done')
