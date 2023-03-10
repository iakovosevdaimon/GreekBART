from fairseq.models.bart import BARTModel
import argparse
import random
import os


parser = argparse.ArgumentParser()

parser.add_argument('--path', '-p', default='./data-bin/', type=str, help='Path to the input data')
parser.add_argument('--checkpoint', '-check', default='./checkpoints/sentence_prediction/Classification_Summarization/greekbart/ms32_mu15720_lr1e-04_me5_dws1/3/checkpoint_best.pt', type=str, help='Path to best model')
parser.add_argument('--user_input','-user_in', action='store_true', help='Set this parameter if you want to provide your own sentences. Default value is False')
parser.add_argument('--sentence1', '-sent1', default=None, type=str, help='First sentence that the user provides as an input')
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

# give your own input or pick the first sample from the test set
if args.user_input:
    sent1 = args.sentence1
else:
    fr = open('./data/test.sent', 'r')
    for i,line in enumerate(fr):
        if i > 0:
            break
        sent1 = line.strip()
    fr.close()

#sent1 = "YOUR OWN SENTENCE"

tokens = greekbart.encode(sent1, add_if_not_exist=False)
prediction = greekbart.predict('sentence_classification_head', tokens).argmax().item()
prediction_label = int(label_fn(prediction))
print(prediction_label)
