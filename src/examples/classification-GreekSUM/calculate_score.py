"""

Evaluate again the fine-tuned model in the Test set and calculate the accuracy, the recall, the precision and the F1-score

Example:
# python calculate_score.py -in ./data-bin/ -check ./checkpoints/sentence_prediction/Classification_Summarization/greekbart/ms32_mu15720_lr1e-04_me5_dws1/3/checkpoint_best.pt

"""


from fairseq.models.bart import BARTModel
import argparse
import random
import os
from datasets import load_metric


parser = argparse.ArgumentParser()

parser.add_argument('--input', '-in', default='./data-bin/', type=str, help='Path to the input data')
parser.add_argument('--checkpoint', '-check', default='./checkpoints/sentence_prediction/Classification_Summarization/greekbart/ms32_mu15720_lr1e-04_me5_dws1/3/checkpoint_best.pt', type=str, help='Path to best model')
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

predictions = []
gold_preds = []

with open('./data/test.sent', 'r') as fr, open('./data/test.label', 'r') as fr_l:
    for line, line_l,  in zip(fr, fr_l):
        if line.strip() and line_l.strip():
            sent1 = line.strip()
            gold = line_l.strip()
            tokens = greekbart.encode(sent1, add_if_not_exist=False)
            prediction = greekbart.predict('sentence_classification_head', tokens).argmax().item()
            prediction_label = int(label_fn(prediction))
            predictions.append([prediction_label])
            gold_preds.append([gold])

metric = load_metric("seqeval")
result = metric.compute(predictions=predictions, references=gold_preds)
result = {key: value.mid.fmeasure * 100 for key, value in result.items()}
res={k: round(v, 4) for k, v in result.items()}
print(res)
sd = args.checkpoint.split("/")[-2]
to_path = os.path.join(args.path,"greekbart_score_sd"+str(sd)+".txt")
fw = open(to_path,'w')
fw.write(str(res))
fw.close()
