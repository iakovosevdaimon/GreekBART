#! /bin/bash
DICT=../../pretrain/greekbart.base/dict.txt
DATA_DIR=./XNLI

fairseq-preprocess \
  --only-source \
  --trainpref train.spm.sent1 \
  --validpref valid.spm.sent1 \
  --testpref test.spm.sent1 \
  --srcdict ${DICT} \
  --destdir greekbart/data-bin/input0 \
  --workers 8

fairseq-preprocess \
  --only-source \
  --trainpref train.spm.sent2 \
  --validpref valid.spm.sent2 \
  --testpref test.spm.sent2 \
  --srcdict ${DICT} \
  --destdir greekbart/data-bin/input1 \
  --workers 8

fairseq-preprocess \
  --only-source \
  --trainpref $DATA_DIR/train.label \
  --validpref $DATA_DIR/valid.label \
  --testpref $DATA_DIR/test.label \
  --destdir greekbart/data-bin/label \
  --workers 8
