#! /bin/bash
DATA_SET='summarization_title_gr'
MODEL='greekbart'
TASK='translation'
DATA_PATH='./summarization_data_title/data-bin/'
MODEL_PATH='../../pretrain/greekbart.base/model.pt'
MAX_TOKENS=4096
MAX_TOKENS_VALID=10000
MAX_UPDATE=98350
LR=5e-05
MAX_EPOCH=30
DISTRIBUTED_WORLD_SIZE=1
VALID_SUBSET='valid'
SEED=$1
SRC=article
TGT=title

PATH_TENSORBOARD=$TASK/$DATA_SET/$MODEL/ms${MAX_TOKENS}_mu${MAX_UPDATE}_lr${LR}_me${MAX_EPOCH}_dws${DISTRIBUTED_WORLD_SIZE}/$SEED
TENSORBOARD_LOGS=./tensorboard_logs/$PATH_TENSORBOARD
SAVE_DIR=./checkpoints/$PATH_TENSORBOARD

fairseq-train $DATA_PATH \
    --restore-file $MODEL_PATH \
    --max-tokens $MAX_TOKENS \
    --max-tokens-valid $MAX_TOKENS_VALID \
    --task $TASK \
    --source-lang $SRC --target-lang $TGT \
    --update-freq 4 \
    --seed $SEED \
    --arch bart_base \
    --decoder-normalize-before \
    --encoder-normalize-before \
    --reset-optimizer --reset-dataloader --reset-meters \
    --required-batch-size-multiple 1 \
    --criterion label_smoothed_cross_entropy \
    --label-smoothing 0.1 \
    --dropout 0.1 \
    --weight-decay 0.01 --optimizer adam --adam-betas "(0.9, 0.98)" --adam-eps 1e-08 \
    --clip-norm 0.0 \
    --find-unused-parameters \
    --eval-scorer eval-precision-recall \
    --best-checkpoint-metric f-1 \
    --maximize-best-checkpoint-metric \
    --eval-scorer-args '{"beam": 2}' \
    --save-dir $SAVE_DIR \
    --skip-invalid-size-inputs-valid-test \
    --fp16 \
    --lr-scheduler polynomial_decay \
    --lr $LR \
    --max-update $MAX_UPDATE \
    --total-num-update $MAX_UPDATE \
    --no-epoch-checkpoints \
    --no-last-checkpoints \
    --tensorboard-logdir $TENSORBOARD_LOGS \
    --log-interval 5 \
    --warmup-updates $((6*$MAX_UPDATE/100)) \
    --max-epoch $MAX_EPOCH \
    --valid-subset $VALID_SUBSET \
