"""
Modified version of
https://github.com/moussaKam/BARThez/blob/main/generate_summary.py

# Original copyright is appended below.
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
"""
"""
    ### EXAMPLE:
    python generate_summary.py \
    --model_path abstract/checkpoints/translation/summarization_abstract_gr/greekbart/ms4096_mu89000_lr5e-05_me30_dws1/3/checkpoint_best.pt \
    --output_path abstract/checkpoints/translation/summarization_abstract_gr/greekbart/ms4096_mu89000_lr5e-05_me30_dws1/3/output.txt \
    --source_text abstract/summarization_data_abstract/test-article.txt \
    --data_path abstract/summarization_data_abstract/data-bin/ \
    --sentence_piece_model ../pretrain/greekbart.base/sentence.bpe.model

# Maybe you should set lenpen = 2 for abstract summarization. In the case of title summarization let lenpen = 1
# We use rouge-score to compute ROUGE score. No stemming is applied before evaluation.
"""

import torch
from fairseq.models.bart import BARTModel
import argparse

parse = argparse.ArgumentParser()
parse.add_argument('--model_path', type=str)
parse.add_argument('--data_path', type=str)
parse.add_argument('--source_text_path', type=str)
parse.add_argument('--output_path', type=str)
parse.add_argument('--beam', type=int, default=4)
parse.add_argument('--lenpen', type=int, default=1)
parse.add_argument('--sentence_piece_model', type=str, default='sentence_piece_multilingual.model')
parse.add_argument('--max_len_b', type=int, default=200)
parse.add_argument('--min_len', type=int, default=3)
parse.add_argument('--no_repeat_ngram_size', type=int, default=3)

args = parse.parse_args()
torch.cuda.set_device(0)

bart = BARTModel.from_pretrained(
    '.',
    checkpoint_file=args.model_path,
    data_name_or_path=args.data_path,
    bpe='sentencepiece',
    sentencepiece_model=args.sentence_piece_model,
    task='translation',
    replace_unk=True,
    print_alignment=True
)


bart.cuda()
bart.eval()
bart.half()
count = 1
bsz = 32
with open(args.source_text_path) as source, open(args.output_path, 'w') as fout:
    sline = source.readline().strip()
    slines = [sline]
    for sline in source:
        if count % bsz == 0:
            with torch.no_grad():
                hypotheses_batch = bart.sample(slines, beam=args.beam, lenpen=args.lenpen, max_len_b=args.max_len_b, min_len=args.min_len, no_repeat_ngram_size=args.no_repeat_ngram_size)
            for hypothesis in hypotheses_batch:
                hypothesis = hypothesis.replace("<unk>","")
                hypothesis = hypothesis.replace("unk","")
                fout.write(hypothesis + '\n')
                fout.flush()
            slines = []

        slines.append(sline.strip())
        count += 1
    if slines != []:
        hypotheses_batch = bart.sample(slines, beam=args.beam, lenpen=args.lenpen, max_len_b=args.max_len_b, min_len=args.min_len, no_repeat_ngram_size=args.no_repeat_ngram_size)
        for hypothesis in hypotheses_batch:
            hypothesis = hypothesis.replace("<unk>","")
            hypothesis = hypothesis.replace("unk","")
            fout.write(hypothesis + '\n')
            fout.flush()
