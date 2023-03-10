from fairseq.models.bart import BARTModel
import argparse
import random
import os


parser = argparse.ArgumentParser()

parser.add_argument('--path', '-p', default='./greekbart/data-bin/', type=str, help='Path to the input data')
parser.add_argument('--checkpoint', '-check', default='./checkpoints/sentence_prediction/NLI/greekbart/ms32_mu61365_lr5e-05_me5_dws1/3/checkpoint_best.pt', type=str, help='Path to best model')
parser.add_argument('--user_input','-user_in', action='store_true', help='Set this parameter if you want to provide your own sentences. Default value is False')
parser.add_argument('--sentence1', '-sent1', default=None, type=str, help='First sentence that the user provides as an input')
parser.add_argument('--sentence2', '-sent2', default=None, type=str, help='Second sentence that the user provides as an input')
parser.add_argument('--seed', '-s', default=7, type=int)

args = parser.parse_args()

greekbart = BARTModel.from_pretrained(
    '.',
    checkpoint_file=args.checkpoint,
    data_name_or_path=args.path,
    bpe='sentencepiece',
    sentencepiece_vocab='../../pretrain/greekbart.base/sentence.bpe.model',
    task='sentence_prediction'
)

label_fn = lambda label: greekbart.task.label_dictionary.string(
    [label + greekbart.task.label_dictionary.nspecial]
)
greekbart.cuda()
greekbart.eval()

sent1 = ""
sent2 = ""

# give your own input or pick the first sample from test set
if args.user_input:
    sent1 = args.sentence1
    sent2 = args.sentence2
else:    
    c = 0
    with open('./XNLI/test.sent1', 'r') as fr1, open('./XNLI/test.sent2', 'r') as fr2:
        for line1, line2 in zip(fr1, fr2):
            if c > 0:
                break
            sent1 = line1.strip()
            sent2 = line2.strip()
            c+=1

tokens = greekbart.encode(sent1, sent2, add_if_not_exist=False)
prediction = greekbart.predict('sentence_classification_head', tokens).argmax().item()
prediction_label = int(label_fn(prediction))
print(prediction_label)
