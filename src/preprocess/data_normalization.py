# Source: https://github.com/nlpaueb/greek-bert/blob/master/normalize_data.property
# Due to summarization task we do not want to transform all the data to lower case

import unicodedata


ded_path = "data/deduplication/final_deduplication.el"




"""
  # Code of is_punctuation() method is taken by:
  # Project: UDPipe-Future (https://github.com/CoNLL-UD-2018/UDPipe-Future)
  # Author: CoNLL-UD-2018
  # File: bert_wrapper.py
  # License: Mozilla Public License 2.0
"""
def is_punctuation(char):
  """Checks whether `chars` is a punctuation character."""
   cp = ord(char)
   # We treat all non-letter/number ASCII as punctuation.
   # Characters such as "^", "$", and "`" are not in the Unicode
   # Punctuation class but we treat them as punctuation anyways, for
   # consistency.
   if ((cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or
           (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126)):
       return True
   cat = unicodedata.category(char)
   if cat.startswith("P"):
       return True
   return False



# https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
def strips_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def _run_split_on_punc(text):
    """Splits punctuation on a piece of text."""
    start_new_word = True
    new_sentence = []
    for char in text:
        if is_punctuation(char):
            new_sentence.append([char])
            start_new_word = True
        else:
            if start_new_word:
                new_sentence.append([])
            start_new_word = False
            new_sentence[-1].append(char)

    return ["".join(w) for w in new_sentence]


def normalize(ded_path):
    fr = open(ded_path, 'r', encoding='utf-8')
    fw = open(ded_path.replace('final_deduplication', 'corpus_gr'), 'w', encoding='utf-8')
    for line in fr:
        tokens = line.split()
        splited_tokens = []
        for token in tokens:
            splited_tokens.extend(_run_split_on_punc(token))
        line = ' '.join(splited_tokens)
        line = strips_accents(line)
        if line.endswith('\n'):
            fw.write(line)
        else:
            fw.write(line+'\n')
    fr.close()
    fw.close()


normalize(ded_path)
