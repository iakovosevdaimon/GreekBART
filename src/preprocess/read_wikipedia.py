import glob
import os
import re
from clean_text import cleaner


#remove[] and |
def remove_anchor(t):
    p1 = t.find('[')
    p2 = t.find(']')
    p3 = t.find('|')
    if p1 >=0 and p2>=0 and p2>p1:
        if p3 >=0:
            if p3>p1 and p3<p2:
                #keep only 2nd text of anchor link
                t = re.sub(r"\[.+\|","",t)
                t = t.replace("]","")
            else:
                t = t.replace('|',"")
        else:
            t = t.replace("]","")
            t = t.replace('[',"")
    return t


def clean_wikipedia(t):
    t = (t.strip()).encode("utf-8", "ignore").decode()
    t = t.replace('\n'," ")
    t = re.sub(r"amp;","",t)
    t = t.strip()
    t = re.sub("http\S+|www\S+|WWW\S+",'',t) # remove links in text like https://...
    t = t.strip()
    t = re.sub(r"formula_.{1}","",t)
    t = t.strip()
    t = re.sub(r"Εξωτερικοί σύνδεσμοι.","",t)
    t = t.strip()
    t = re.sub(r".*επεκτείνοντάς το.*","",t)
    t = t.strip()
    t = re.sub(r".*Παραπομπές.*","",t)
    t = t.strip()
    t = re.sub(r".*Περαιτέρω ανάγνωση.*","",t)
    t = t.strip()
    t = remove_anchor(t)
    t = t.strip()
    t = re.sub(r".*gt.*","",t)
    t = t.strip()
    t = re.sub(r"\s*\([^)]*\)","",t) # remove parentheses
    t = t.strip()
    res = re.search(r".{30,}",t)
    if res is None:
        return None
    res = re.search(r"^(?!.*(.)\1{5,})",t)
    if res is None:
        return None
    res = re.search(r"^(?!.*(..)\1{5,})",t)
    if res is None:
        return None
    res = re.search(r"[A-Za-zΑ-ΩΊΪΪΌΆΈΎΫΫ́ΉΏα-ωίϊΐόάέύϋΰήώ0-9]{20,}",t)
    if res is not None:
        return None
    res = re.search(r"([A-Za-zΑ-ΩΊΪΪΌΆΈΎΫΫ́ΉΏα-ωίϊΐόάέύϋΰήώ0-9_]{4,}\d{3,})|(\d{3,}[A-Za-zΑ-ΩΊΪΪΌΆΈΎΫΫ́ΉΏα-ωίϊΐόάέύϋΰήώ0-9_]{4,})",t)
    if res is not None:
        return None
    res = re.search(r"^\s*$",t) #find empty lines
    if res is not None:
        return None
    return t


def read_dataset_wikipedia():
    curDir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(curDir, 'data/Wikipedia')

    pattern = '*.xml'

    #download and preprocess greek version of wikipedia
    if not os.path.exists(path):
        os.system('mkdir '+str(path))
        os.system('cd '+str(path))
        os.system('wget http://download.wikimedia.org/elwiki/latest/elwiki-latest-pages-articles-multistream.xml.bz2')
        os.system('python -m wikiextractor.WikiExtractor -cb 250K -o extracted elwiki-latest-pages-articles-multistream.xml.bz2')
        os.system('find extracted -name \'*bz2\' -exec bunzip2 -c {} \; > text.xml') # store each bz2 file into a xml file


    rpath = os.path.join(path,'text.xml')
    wpath = os.path.join(path,'text.txt')

    fr = open(rpath,'r')
    fw = open(wpath,'w')
    for line in fr:
        if (line.strip()).startswith("<doc"):
            text = ""
            fr.readline()
            fr.readline()
            l=fr.readline()
            while not (l.strip()).startswith("</doc>"):
                if l.strip().startswith("\n") or len(l.strip())==0:
                    l = fr.readline()
                    continue
                t = clean_wikipedia(l)
                if t is not None:
                    text+=t
                l = fr.readline()
            if text is not None and text!="":
            	text = cleaner(text)
            	fw.write('{}\n'.format(text))

    fr.close()
    fw.close()
