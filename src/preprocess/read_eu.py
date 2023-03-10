import re
import tarfile
import glob
import os
from clean_text import cleaner

def extract(tar_url, extract_path='.'):
    tar = tarfile.open(tar_url, 'r')
    for item in tar:
        tar.extract(item, extract_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            extract(item.name, "./" + item.name[:item.name.rfind('/')])
    tar.close()



def clean_eu(t):
    t = (t.strip()).encode("utf-8", "ignore").decode()
    t = t.replace('\n',"")
    t = re.sub(r"amp;","",t)
    t = t.strip()
    t = re.sub("http\S+|www\S+|WWW\S+",'',t) # remove links in text like https://...
    t = t.strip()
    t = t.replace("γραπτώς. - ","")
    t = t.strip()
    t = t.replace("°. ° °.","")
    t = t.strip()
    t = t.replace("&#x02BC;","\'")
    t = t.strip()
    t = re.sub(r"^[.,;!:]","",t)
    t.strip()
    if re.search(r"\d+\s+°\s*C",t) is None:
        t = t.replace("°","")
        t = t.strip()
    t = re.sub(r"\s*\([^)]*\)","",t) # remove parentheses
    t = t.strip()
    t = re.sub(r"^-","",t)
    t = t.strip()
    if re.search(r"^\"\s*[a-zα-ωίϊΐόάέύϋΰήώ]",t) is not None:
        t=t.replace("\"","")
        t = t.strip()
        t = "Η "+t
    t=t.replace("\"","")
    t=t.strip()
    res = re.search(r".{3,}",t)
    if res is None:
        return None
    res = re.search(r"^(?!.*(.)\1{5,})",t)
    if res is None:
        return None
    res = re.search(r"^(?!.*(..)\1{5,})",t)
    if res is None:
        return None
    res = re.search(r"[A-Za-zΑ-ΩΊΪΪΌΆΈΎΫΫ́ΉΏα-ωίϊΐόάέύϋΰήώ0-9]{25,}",t)
    if res is not None:
        return None
    res = re.search(r"[|\t\[\]\{\}]",t)
    if res is not None:
        return None
    res = re.search(r"([A-Za-zΑ-ΩΊΪΪΌΆΈΎΫΫ́ΉΏα-ωίϊΐόάέύϋΰήώ0-9_]{4,}\d{3,})|(\d{3,}[A-Za-zΑ-ΩΊΪΪΌΆΈΎΫΫ́ΉΏα-ωίϊΐόάέύϋΰήώ0-9_]{4,})",t)
    if res is not None:
        return None
    res = re.search(r"^\s*$",t) #find empty lines
    if res is not None:
        return None
    return t

def check_doc(d):
    res = re.search(r".{100,}",d)
    if res is None:
        return None
    return d



def create_dataset_eu(eu_tgz, eu_path):
    curDir = os.path.dirname(os.path.abspath(__file__))
    eu_tgz = os.path.join(curDir,eu_tgz)
    eu_path = os.path.join(curDir,eu_path)
    if not os.path.exists(os.path.join(eu_path,'txt/el/')):
        extract(eu_tgz, eu_path)
    path = os.path.join(eu_path,'txt/el/*')
    eu_files = glob.glob(path)
    to_path = os.path.join(eu_path,'europarl.el')
    fw=open(to_path,"w")
    #cnt=1
    for i,file in enumerate(eu_files):
        #print(file)
        fr = open(file,'r')
        docum=""
        d = False
        for line in fr:
            if line.strip().startswith("<CHAPTER ID"):
                if docum!="":
                    docum=check_doc(docum)
                    if docum is not None:
                        docum = cleaner(docum)
                        #print(cnt,file)
                        #cnt+=1
                        fw.write('{}\n'.format(docum))
                docum=""
                d = True
            elif line.strip().startswith("<SPEAKER ID"):
                d = False
                if not re.match(".*[.!;:,·]$", docum) and docum!="": #if doesn't end with any punctuaction, then add "."
                    docum+="."
            elif line.strip().startswith("<P"):
                d = False
            else:
                if d:
                    continue
                text = clean_eu(line.strip())
                if text is not None:
                    docum = docum.strip()
                    docum=docum+" "+text

        if docum!="":
            docum=check_doc(docum)
            if docum is not None:
                #print(cnt,file)
                #cnt+=1
                docum = cleaner(docum)
                fw.write('{}\n'.format(docum))
        fr.close()
    fw.close()
