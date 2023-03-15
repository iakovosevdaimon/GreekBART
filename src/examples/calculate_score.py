"""

Evaluate again the fine-tuned model in the Test set and calculate the accuracy, the recall, the precision and the F1-score

Example for NLI task:
# python calculate_score.py -t NLI -p ./NLI -in ./NLI/greekbart/data-bin/ -check ./NLI/checkpoints/sentence_prediction/NLI/greekbart/ms32_mu61365_lr5e-05_me5_dws1/3/checkpoint_best.pt

Supported tasks: NLI, Sentimental Analysis, classification

"""

from fairseq.models.bart import BARTModel
import argparse
import random
import os
from datasets import load_metric

parser = argparse.ArgumentParser()

parser.add_argument('--task', '-t', default=None, type=str, help='Name of the downstream task')
parser.add_argument('--path', '-p', default=None, type=str, help='Path to the folder of the downstream task')
parser.add_argument('--input', '-in', default=None, type=str, help='Path to the input data')
parser.add_argument('--checkpoint', '-check', default=None, type=str, help='Path to the best model')
parser.add_argument('--seed', '-s', default=7, type=int)

args = parser.parse_args()

task_folder = args.path

greekbart = BARTModel.from_pretrained(
    '.',
    checkpoint_file=args.checkpoint,
    data_name_or_path=args.path,
    bpe='sentencepiece',
    sentencepiece_vocab='.././pretrain/greekbart.base/sentence.bpe.model',
    task='sentence_prediction'
)

label_fn = lambda label: greekbart.task.label_dictionary.string(
    [label + greekbart.task.label_dictionary.nspecial]
)
greekbart.cuda()
greekbart.eval()

predictions = []
gold_preds = []

if args.task == "Sentimental Analysis":
    # load test set and predict for each sample
    with open(os.path.join(args.path,'./data/processed/test.review'), 'r') as fr, open(os.path.join(args.path,'./data/processed/test.label'), 'r') as fr_l:
        for line, line_l,  in zip(fr, fr_l):
            if line.strip() and line_l.strip():
                sent1 = line.strip()
                gold = line_l.strip()
                tokens = greekbart.encode(sent1, add_if_not_exist=False)
                prediction = greekbart.predict('sentence_classification_head', tokens).argmax().item()
                prediction_label = int(label_fn(prediction))
                predictions.append([prediction_label])
                gold_preds.append([gold])
elif args.task == "NLI":
    with open(os.path.join(args.path,'XNLI/test.sent1'), 'r') as fr1, open(os.path.join(args.path,'XNLI/test.sent2'), 'r') as fr2, open(os.path.join(args.path,'XNLI/test.label'), 'r') as fr_l:
        for line1, line2, line_l  in zip(fr1, fr2, fr_l):
            if line1.strip() and line2.strip() and line_l.strip():
                sent1 = line1.strip()
                sent2 = line2.strip()
                gold = line_l.strip()
                tokens = greekbart.encode(sent1, sent2, add_if_not_exist=False)
                prediction = greekbart.predict('sentence_classification_head', tokens).argmax().item()
                prediction_label = int(label_fn(prediction))
                predictions.append([prediction_label])
                gold_preds.append([gold])
else:
    if task_folder.contains("Macedonia"):
        with open(os.path.join(args.path,'./data/processed/test.sent'), 'r') as fr, open(os.path.join(args.path,'./data/processed/test.label'), 'r') as fr_l:
            for line, line_l,  in zip(fr, fr_l):
                if line.strip() and line_l.strip():
                    sent1 = line.strip()
                    gold = line_l.strip()
                    tokens = greekbart.encode(sent1, add_if_not_exist=False)
                    prediction = greekbart.predict('sentence_classification_head', tokens).argmax().item()
                    prediction_label = int(label_fn(prediction))
                    predictions.append([prediction_label])
                    gold_preds.append([gold])
    else:
        with open(os.path.join(args.path,'./data/test.sent'), 'r') as fr, open(os.path.join(args.path,'./data/test.label'), 'r') as fr_l:
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
