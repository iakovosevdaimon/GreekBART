"""

Take the generated summaries and calculate ROUGE-score and BERTScore for each

Example for Abstract Summarization:
# python calculate_score.py  \
--output_path abstract/metrics.txt \
--predictions_text_path abstract/checkpoints/translation/summarization_abstract_gr/greekbart/ms4096_mu89000_lr5e-05_me30_dws1/3/output.txt \
--target_text_path abstract/summarization_data_abstract/test-abstract.txt

Example for Title Summarization:
# python calculate_score.py  \
--output_path title/metrics.txt \
--predictions_text_path title/checkpoints/translation/summarization_title_gr/greekbart/ms4096_mu98350_lr5e-05_me30_dws1/3/output.txt \
--target_text_path title/summarization_data_title/test-title.txt

"""

import argparse
from evaluate import load

parse = argparse.ArgumentParser()
parse.add_argument('--predictions_text_path', type=str)
parse.add_argument('--target_text_path', type=str)
parse.add_argument('--output_path', type=str)

args = parse.parse_args()

preds = []
true_preds = []

with open(args.predictions_text_path) as fpred, open(args.target_text_path, 'r') as ftarg:
    for line1, line2,  in zip(fpred, ftarg):
        if line1.strip() and line2.strip():
            preds.append(line1.strip())
            true_preds.append(line2.strip())

rouge = load("rouge")
bertscore = load("bertscore")

results_bs1 = bertscore.compute(predictions=preds, references=true_preds, lang="el")
results_bs2 = bertscore.compute(predictions=preds, references=true_preds, model_type="nlpaueb/bert-base-greek-uncased-v1",num_layers=9)
results_rg = rouge.compute(predictions=preds, references=true_preds)

bert_precision = sum(results_bs1['precision'])/len(results_bs1['precision'])
bert_recall = sum(results_bs1['recall'])/len(results_bs1['recall'])
bert_f1 = sum(results_bs1['f1'])/len(results_bs1['f1'])

bert2_precision = sum(results_bs2['precision'])/len(results_bs2['precision'])
bert2_recall = sum(results_bs2['recall'])/len(results_bs2['recall'])
bert2_f1 = sum(results_bs2['f1'])/len(results_bs2['f1'])

fw = open(args.output_path, 'w')
#fw.write(str(results_bs1)+'\n')
#fw.write(results_bs2+'\n')
fw.write(str(results_rg)+'\n')
fw.write("Precision of mBERT Score: "+str(bert_precision)+'\n')
fw.write("Recall of mBERT Score: "+str(bert_recall)+'\n')
fw.write("F1-score of mBERT Score: "+str(bert_f1)+'\n')


fw.write("Precision of GreekBERT Score: "+str(bert2_precision)+'\n')
fw.write("Recall of GreekBERT Score: "+str(bert2_recall)+'\n')
fw.write("F1-score of GreekBERT Score: "+str(bert2_f1))
fw.close()
