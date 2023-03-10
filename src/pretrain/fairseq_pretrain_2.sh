#! /bin/bash


VOCAB_DIR='./greekbart.base/sentence.bpe.model'
LR=6e-04
TASK='denoising'
DATA_SET='Pretrain'
MODEL='GreekBart'
DROPOUT=0.05
data_dir='./greekbart.base/data-bin/input/'
MODEL_PATH=./checkpoints/$TASK/$DATA_SET/$MODEL/LR${LR}/drp0.1/checkpoint_last.pt
# total number of updates over which to decay learning rate
total_updates=80440
# warmup the learning rate linearly for the first N updates
let num_warmup=6*$total_updates/100

#log_path=./logs/$TASK/$DATA_SET/$MODEL/LR${LR}/drp${DROPOUT}/logs.json
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

#mkdir -p ./logs/$TASK/$DATA_SET/$MODEL/LR${LR}/drp${DROPOUT}/
mkdir -p ./tensorboard_logs/$TASK/$DATA_SET/$MODEL/LR${LR}/drp${DROPOUT}/
mkdir -p ./checkpoints/$TASK/$DATA_SET/$MODEL/LR${LR}/drp${DROPOUT}/


#--log-format json \
#--log-file $log_path \

#--cpu \

#--fp16 \
#    --memory-efficient-fp16 \
#    --on-cpu-convert-precision \
# --tokens-per-sample 512 \
# --shorten-method 'truncate' \
# --tokens-per-sample 1024 \
#--sample-break-mode None \
#--max-positions: The maximum number of positions to pass into the model. Will skip sequences longer than this.

# TO CHANGE-> --empty-cache-freq 1 --data-buffer-size 1 --seed 7

#CUDA_VISIBLE_DEVICES=0

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
    --dropout 0.05 --attention-dropout 0.05 \
    --clip-norm 0.1 \
    --max-epoch 16 \
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
