import fnmatch
import os.path
import shutil
import re
import gzip
import json
from multiprocessing import Pool

oscar_path = "data/OSCAR/"
crawler_path = "data/Crawler/"
eu_path = "data/EU Parliament/"
wiki_path = "data/Wikipedia/"

def fill_whitespace(x):
    pos = [i for i, char in enumerate(x) if char == ' ']
    if len(pos)>0:
        for i,p in enumerate(pos):
            x = x[:p+i]+'\\'+x[p+i:]
    return x

def find_txt(oscar_path, crawler_path, eu_path, wiki_path):
    oscar_files = []
    crawler_files = []
    eu_files = []
    wiki_files = []
    pattern = '*.txt'
    paths = [oscar_path, crawler_path, eu_path, wiki_path]
    switcher = {1: oscar_files, 2: wiki_files, 3: crawler_files, 4: eu_files}
    for path in paths:
        for root, curDir, files in os.walk(path):
            for f in files:
                c = 0
                if 'OSCAR' in root:
                    c = 1
                elif 'Wikipedia' in root:
                    c = 2
                elif 'Crawler' in root:
                    c = 3
                else:
                    pattern = "*.el"
                    c = 4

                if fnmatch.fnmatch(f, pattern):
                    switcher.get(c).append(os.path.join(root, f))
    print('The search of txts is done')
    return oscar_files, crawler_files, eu_files, wiki_files


# mode = 0 -> use the multiple txt files of OSCAR
# mode = 1 -> use the collective txt file of OSCAR with all samples
def create_script(oscar_txts, crawler_txts, eu_txts, wiki_txts, mode):

    curDir = os.getcwd()
    if mode == 0:
        file_name = 'deduplication.sh'
    else:
        file_name = 'deduplication_'+str(mode)+'.sh'
    file = open(file_name, 'w', encoding='utf-8')
    file.write('#! /bin/bash \n')
    file.write('echo \"Deduplication process is running...\"\n')
    curDir += '/data/deduplication/'
    curDir = fill_whitespace(curDir)
    files = []

    # runiq for OSCAR
    command = 'runiq '
    for i in range(len(oscar_txts)):
        item = fill_whitespace(oscar_txts[i])
        if mode == 0:
            if item.find('_all') < 0:
                command += str(item) + ' '
        else:
            if item.find('_all') >= 0:
                command += str(item)

    oscar_ded = str(curDir) + 'oscar_deduplication.txt'
    files.append(oscar_ded)
    if mode == 0:
        command += '> ' + curDir + 'temp_ded.txt\nruniq ' + curDir + 'temp_ded.txt > ' + oscar_ded + '\n'
    else:
        command += '> ' + oscar_ded + '\n'
    file.write(command)
    file.write('echo \"OSCAR is done\"\n')

    # runiq for Wikipedia
    command = 'runiq '
    for i in range(len(wiki_txts)):
        item = fill_whitespace(wiki_txts[i])
        command += str(item) + ' '
    wiki_ded = str(curDir) + 'wiki_deduplication.txt'
    files.append(wiki_ded)
    command += '> ' + wiki_ded + '\n'
    file.write(command)
    file.write('echo \"Wikipidea is done\"\n')

    # runiq for EU parliament
    command = 'runiq '
    for i in range(len(eu_txts)):
        item = fill_whitespace(eu_txts[i])
        command += str(item) + ' '
    eu_ded = str(curDir) + 'eu_parliament_deduplication.txt'
    files.append(eu_ded)
    command += '> ' + eu_ded + '\n'
    file.write(command)
    file.write('echo \"EU Parliament is done\"\n')

    # runiq for crawler
    command = 'runiq '
    for i in range(len(crawler_txts)):
        item = fill_whitespace(crawler_txts[i])
        command += str(item) + ' '
    crawler_ded = str(curDir) + 'crawler_deduplication.txt'
    files.append(crawler_ded)
    command += '> ' + crawler_ded + '\n'
    file.write(command)
    file.write('echo \"Crawler is done\"\n')

    # runiq for deduplication between all the datasets
    command = 'runiq '
    for i in range(len(files)):
        command += str(files[i]) + ' '
    final_ded = str(curDir) + 'corpus.el\n'
    command += '> ' + final_ded
    file.write(command)
    file.write('echo \"Done!\"')
    file.close()


oscar_txts, crawler_txts, eu_txts, wiki_txts = find_txt(oscar_path, crawler_path, eu_path, wiki_path)
folder = 'data/deduplication/'
if os.path.exists(folder):
    shutil.rmtree(folder)
os.mkdir(folder)

# mode = 0 -> use the multiple txt files of OSCAR
# mode = 1 -> use the collective txt file of OSCAR with all samples
# create both scripts
create_script(oscar_txts, crawler_txts, eu_txts, wiki_txts, 0)
create_script(oscar_txts, crawler_txts, eu_txts, wiki_txts, 1)
