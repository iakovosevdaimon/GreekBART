#! /bin/bash

SPLITS="train test valid"
TASKS="title"
DATA_DIR=./summarization_data_title

for TASK in $TASKS
do
    for SPLIT in $SPLITS
    do
        spm_encode --model ../../pretrain/greekbart.base/sentence.bpe.model < $DATA_DIR/$SPLIT-article.txt > $DATA_DIR/$SPLIT.spm.article
        spm_encode --model ../../pretrain/greekbart.base/sentence.bpe.model < $DATA_DIR/$SPLIT-$TASK.txt > $DATA_DIR/$SPLIT.spm.$TASK
    done
done
