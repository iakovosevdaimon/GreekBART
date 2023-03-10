#! /bin/bash
DICT=../../pretrain/greekbart.base/dict.txt
SRC=article
TGT=abstract
TRAIN=./summarization_data_abstract/train.spm
VALID=./summarization_data_abstract/valid.spm
TEST=./summarization_data_abstract/test.spm
fairseq-preprocess \
  --source-lang ${SRC} \
  --target-lang ${TGT} \
  --trainpref ${TRAIN} \
  --validpref ${VALID} \
  --testpref ${TEST} \
  --destdir ./summarization_data_abstract/data-bin \
  --thresholdtgt 0 \
  --thresholdsrc 0 \
  --srcdict ${DICT} \
  --tgtdict ${DICT} \
  --workers 8
