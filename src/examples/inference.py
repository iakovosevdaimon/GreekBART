from fairseq.models.bart import BARTModel
import argparse
import random
import os
from fairseq.models.roberta import RobertaModel


"""
EXAMPLE:

CUDA_VISIBLE_DEVICES=0 python inference.py \
    --model bart \
    --path classification/greekbart/data-bin \
    --test_path classification/data/processed/test.sent \
    --output_path classification/test_output_3.txt \
    --checkpoint  classification/checkpoints/sentence_prediction/Classification/greekbart/ms16_mu4750_lr5e-05_me20_dws1/3/checkpoint_best.pt \
    --task classification
"""


parser = argparse.ArgumentParser()

parser.add_argument('--model', '-m', default=None, type=str, help='Name of model: robert or bart')
parser.add_argument('--path', '-p', default='./greekbart/data-bin/', type=str, help='Path to the input data')
parser.add_argument('--checkpoint', '-check', default='./checkpoints/sentence_prediction/Classification/greekbart/ms16_mu4750_lr5e-05_me20_dws1/3/checkpoint_best.pt', type=str, help='Path to best model')
parser.add_argument('--task','-t', default=None, type=str, help='Set this parameter if you want to provide your own sentences. Default value is False')
parser.add_argument('--test_path', '-test', default=None, type=str)
parser.add_argument('--output_path', '-out', default=None, type=str)
parser.add_argument('--seed', '-s', default=7, type=int)


args = parser.parse_args()

if args.model=="bart":
    model = BARTModel.from_pretrained(
        '.',
        checkpoint_file=args.checkpoint,
        data_name_or_path=args.path,
        bpe='sentencepiece',
        sentencepiece_model='../pretrain/greekbart.base/sentence.bpe.model',
        task='sentence_prediction'
    )
else:
    model = RobertaModel.from_pretrained(
        '.',
        checkpoint_file=args.checkpoint,
        data_name_or_path=args.path,
        bpe='sentencepiece',
        sentencepiece_model='../pretrain/xlmr.base/sentencepiece.bpe.model',
        task='sentence_prediction'
    )

label_fn = lambda label: model.task.label_dictionary.string(
    [label + model.task.label_dictionary.nspecial]
)
model.cuda()
model.eval()


count = 1
bsz = 32

fw = open(args.output_path, "w")
if args.task=="NLI":
    sent1 = ""
    sent2 = ""
    with open('./NLI/XNLI/test.sent1', 'r') as fr1, open('./NLI/XNLI/test.sent2', 'r') as fr2:
        for line1, line2 in zip(fr1, fr2):
            sent1 = line1.strip()
            sent2 = line2.strip()
            tokens = model.encode(sent1, sent2)
            prediction = model.predict('sentence_classification_head', tokens).argmax().item()
            prediction_label = int(label_fn(prediction))
            fw.write(str(prediction_label)+"\n")
else:
    fr = open(args.test_path, 'r')
    for line in fr:
        sent1 = line.strip()
        tokens = model.encode(sent1)
        if args.model=="roberta":
            if len(tokens) > 512:
                tokens = tokens[:511]
        else:
            if len(tokens) > 1024:
                tokens = tokens[:1023]
        prediction = model.predict('sentence_classification_head', tokens).argmax().item()
        prediction_label = int(label_fn(prediction))
        fw.write(str(prediction_label)+"\n")
    fr.close()
fw.close()
