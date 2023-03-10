#! /bin/bash
DICT=../../pretrain/greekbart.base/dict.txt
DATA_DIR=./data

fairseq-preprocess \
  --only-source \
  --trainpref train.spm.sent \
  --validpref valid.spm.sent \
  --testpref test.spm.sent \
  --srcdict ${DICT} \
  --destdir greekbart/data-bin/input0 \
  --workers 8


fairseq-preprocess \
  --only-source \
  --trainpref $DATA_DIR/train.label \
  --validpref $DATA_DIR/valid.label \
  --testpref $DATA_DIR/test.label \
  --destdir greekbart/data-bin/label \
  --workers 8
