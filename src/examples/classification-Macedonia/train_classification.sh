#! /bin/bash

DATA_SET='Classification'
TASK='sentence_prediction'
MODEL='greekbart'
DATA_PATH='./greekbart/data-bin/'
MODEL_PATH='../../pretrain/greekbart.base/model.pt'
MAX_SENTENCES=16
MAX_UPDATE=4750
LR=5e-05
MAX_EPOCH=20
DISTRIBUTED_WORLD_SIZE=1
SENTENCE_PIECE_MODEL='../../pretrain/greekbart.base/sentence.bpe.model'
VALID_SUBSET='valid,test'
NUM_CLASSES=18
SEED=$1

TENSORBOARD_LOGS=./tensorboard_logs/$TASK/$DATA_SET/$MODEL/ms${MAX_SENTENCES}_mu${MAX_UPDATE}_lr${LR}_me${MAX_EPOCH}_dws${DISTRIBUTED_WORLD_SIZE}/$SEED
SAVE_DIR=./checkpoints/$TASK/$DATA_SET/$MODEL/ms${MAX_SENTENCES}_mu${MAX_UPDATE}_lr${LR}_me${MAX_EPOCH}_dws${DISTRIBUTED_WORLD_SIZE}/$SEED

if [ -d $TENSORBOARD_LOGS ]
then
    rm -rf $TENSORBOARD_LOGS
fi

if [ -d $SAVE_DIR ]
then
    rm -rf $SAVE_DIR
fi


mkdir -p $TENSORBOARD_LOGS
mkdir -p $SAVE_DIR

CUDA_VISIBLE_DEVICES=0

fairseq-train $DATA_PATH \
    --restore-file $MODEL_PATH \
    --batch-size $MAX_SENTENCES \
    --task $TASK \
    --update-freq 1 \
    --seed $SEED \
    --skip-invalid-size-inputs-valid-test \
    --add-prev-output-tokens \
    --reset-optimizer --reset-dataloader --reset-meters \
    --init-token 0 \
    --separator-token 2 \
    --arch bart_base \
    --decoder-normalize-before \
    --encoder-normalize-before \
    --criterion $TASK \
    --num-classes $NUM_CLASSES \
    --dropout 0.1 --attention-dropout 0.1 \
    --weight-decay 0.01 --optimizer adam --adam-betas "(0.9, 0.98)" --adam-eps 1e-08 \
    --clip-norm 0.0 \
    --find-unused-parameters \
    --bpe 'sentencepiece' \
    --sentencepiece-model $SENTENCE_PIECE_MODEL \
    --maximize-best-checkpoint-metric \
    --best-checkpoint-metric 'accuracy' \
    --save-dir $SAVE_DIR \
    --fp16 \
    --lr-scheduler polynomial_decay \
    --lr $LR \
    --max-update $MAX_UPDATE \
    --total-num-update $MAX_UPDATE \
    --no-epoch-checkpoints \
    --no-last-checkpoints \
    --tensorboard-logdir $TENSORBOARD_LOGS \
    --log-interval 10 \
    --warmup-updates $((6*$MAX_UPDATE/100)) \
    --max-epoch $MAX_EPOCH \
    --keep-best-checkpoints 1 \
    --valid-subset $VALID_SUBSET
