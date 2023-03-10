#! /bin/bash
DICT=../../pretrain/greekbart.base/dict.txt
SRC=article
TGT=title
TRAIN=./summarization_data_title/train.spm
VALID=./summarization_data_title/valid.spm
TEST=./summarization_data_title/test.spm
fairseq-preprocess \
  --source-lang ${SRC} \
  --target-lang ${TGT} \
  --trainpref ${TRAIN} \
  --validpref ${VALID} \
  --testpref ${TEST} \
  --destdir ./summarization_data_title/data-bin \
  --thresholdtgt 0 \
  --thresholdsrc 0 \
  --srcdict ${DICT} \
  --tgtdict ${DICT} \
  --workers 8
