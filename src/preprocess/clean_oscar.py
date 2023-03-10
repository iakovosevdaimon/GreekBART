import glob
import os
import re



#remove emojis
def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def remove_mentions_and_tags(text):
    text = re.sub(r'@\S*', "", text)
    return re.sub(r"#\S*", "", text)


def clean_sent_oscar(t):
    t = (t.strip()).encode("utf-8", "ignore").decode()
    t = re.sub(r"amp;","",t)
    t = t.strip()
    t = re.sub("http\S+|www\S+|WWW\S+",'',t) # remove links in text like https://...
    t = t.strip()
    t = re.sub(r"\s[A-Za-z0-9]*[.]gr{1}\/*.*","",t) # remove links in text like something.gr/... or something.gr
    t = t.strip()
    t = re.sub(r"\s[A-Za-z0-9]*[.]com{1}\/*.*","",t) # remove links in text like something.gr/... or something.gr
    t = t.strip()
    t=deEmojify(t)
    t = t.strip()
    t = remove_mentions_and_tags(t)
    t.strip()
    t=re.sub(r"_{1,}"," ",t) #remove underscores
    t = t.strip()
    re.sub(r'(?<=[α-ωίϊΐόάέύϋΰήώ])(?=[Α-ΩΊΪΪΌΆΈΎΫΫ́ΉΏ])', ' ', t)
    t=re.sub(r"Πηγή.*|Πηγη.*","",t)
    t = t.strip()
    t=t.replace("| ","")
    t=t.strip()
    res = re.search(r"^(?!.*(.)\1{5,})",t)
    if res is None:
        return None
    res = re.search(r"^(?!.*(..)\1{5,})",t)
    if res is None:
        return None
    res = re.search(r"[A-Za-zΑ-ΩΊΪΪΌΆΈΎΫΫ́ΉΏα-ωίϊΐόάέύϋΰήώ0-9]{25,}",t)
    if res is not None:
        return None
    res = re.search(r"\d+ Fax|Τηλ|Τηλ[.] \(",t)
    if res is not None:
        return None
    res = re.search(r"[|\t\[\]\{\}]",t)
    if res is not None:
        return None
    res = re.search(r"\\{2,}",t)
    if res is not None:
        return None
    res = re.search(r"^:",t) # inspect again this
    if res is not None:
        return None
    res = re.search(r"(\/ ){2,}|(\/){2,}",t)
    if res is not None:
        return None
    res = re.search(r"[eE]mail|[fF]ax|[τΤ]ηλέφωνο|[τΤ]ηλ|[cC]ontact|[i|I]nfo *[@:]+",t)
    if res is not None:
        return None
    res = re.search(r"([A-Za-zΑ-ΩΊΪΪΌΆΈΎΫΫ́ΉΏα-ωίϊΐόάέύϋΰήώ0-9_]{4,}\d{3,})|(\d{3,}[A-Za-zΑ-ΩΊΪΪΌΆΈΎΫΫ́ΉΏα-ωίϊΐόάέύϋΰήώ0-9_]{4,})",t)
    if res is not None:
        return None
    res = re.search(r"^\s*$",t) #find empty lines
    if res is not None:
        return None
    res = re.search(r".{5,}",t)
    if res is None:
        return None
    return t

def clean_doc_oscar(t):
    t = re.sub(r"Σχόλια.*|Σχολια.*","",t)
    res = re.search(r".{100,}",t)
    if res is None:
        return None
    return t
