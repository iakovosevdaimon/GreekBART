#! /bin/bash

DICT=./greekbart.base/dict.txt


fairseq-preprocess \
  --only-source \
  --trainpref train.spm.sent \
  --validpref valid.spm.sent \
  --destdir ./greekbart.base/data-bin/input \
  --srcdict $DICT \
  --workers 16
