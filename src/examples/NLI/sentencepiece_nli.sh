#! /bin/bash

SPLITS="train test valid"
SENTS="sent1 sent2"
DATA_DIR=./XNLI

for SENT in $SENTS
do
    for SPLIT in $SPLITS
    do
        spm_encode --model ../../pretrain/greekbart.base/sentence.bpe.model < $DATA_DIR/$SPLIT.$SENT > $SPLIT.spm.$SENT
    done
done
