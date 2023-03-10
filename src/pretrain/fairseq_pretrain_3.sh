#! /bin/bash


VOCAB_DIR='./greekbart.base/sentence.bpe.model'
LR=6e-04
TASK='denoising'
DATA_SET='Pretrain'
MODEL='GreekBart'
DROPOUT=0
data_dir='./greekbart.base/data-bin/input/'
MODEL_PATH=./checkpoints/$TASK/$DATA_SET/$MODEL/LR${LR}/drp0.05/checkpoint_last.pt
# total number of updates over which to decay learning rate
total_updates=80440
# warmup the learning rate linearly for the first N updates
let num_warmup=6*$total_updates/100


TENSORBOARD_LOGS=./tensorboard_logs/$TASK/$DATA_SET/$MODEL/LR${LR}/drp${DROPOUT}
 #path to save checkpoints Default: “checkpoints”
checkpoints_path=./checkpoints/$TASK/$DATA_SET/$MODEL/LR${LR}/drp${DROPOUT}


#if [ -d $TENSORBOARD_LOGS ]
#then
#    rm -rf $TENSORBOARD_LOGS
#fi

#if [ -d $checkpoints_path ]
#then
#    rm -rf $checkpoints_path
#fi


mkdir -p ./tensorboard_logs/$TASK/$DATA_SET/$MODEL/LR${LR}/drp${DROPOUT}/
mkdir -p ./checkpoints/$TASK/$DATA_SET/$MODEL/LR${LR}/drp${DROPOUT}/


fairseq-train $data_dir \
    --restore-file $MODEL_PATH \
    --fp16 \
    --on-cpu-convert-precision \
    --skip-invalid-size-inputs-valid-test \
    --tensorboard-logdir $TENSORBOARD_LOGS \
    --log-interval 100 \
    --find-unused-parameters \
    --ddp-backend 'legacy_ddp' \
    --bpe 'sentencepiece'\
    --sentencepiece-model $VOCAB_DIR \
    --optimizer adam --adam-betas "(0.9, 0.98)" --adam-eps 1e-06 --weight-decay 0.0 \
    --arch bart_base \
    --encoder-normalize-before \
    --decoder-normalize-before \
    --share-all-embeddings \
    --update-freq 128 \
    --lr-scheduler polynomial_decay \
    --lr $LR \
    --power 1.0 \
    --total-num-update $total_updates \
    --warmup-updates $num_warmup \
    --save-dir $checkpoints_path \
    --max-tokens 6000 \
    --dropout 0 --attention-dropout 0 \
    --clip-norm 0.1 \
    --max-epoch 20 \
    --validate-interval 1 \
    --save-interval 1 \
    --save-interval-updates 100000 \
    --seed 7 \
    --best-checkpoint-metric 'loss' \
    --task $TASK \
    --mask 0.3 \
    --poisson-lambda 3.5 \
    --mask-length span-poisson \
    --permute-sentences 1.0 \
    --shuffle-instance \
    --encoder-learned-pos \
    --decoder-learned-pos \
    --mask-random 0.1 \
    --replace-length 1 \
    --criterion cross_entropy
