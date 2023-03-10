#! /bin/bash

DATA_DIR=./data

SPLITS="train test valid"
for SPLIT in $SPLITS
do
    spm_encode --model ../../pretrain/greekbart.base/sentence.bpe.model < $DATA_DIR/$SPLIT.sent > $SPLIT.spm.sent
done
