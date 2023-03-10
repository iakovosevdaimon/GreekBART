#! /bin/bash

cd ../corpus



echo "Spliting..."
python split.py -p ./corpus_gr.el -tr 0.95 -val 0.05 -ts 0.0 -t ./processed/el/
echo "End of spliting"

cd ..
cd ./pretrain

echo "Beginning of sentence piece training"
DATA=./greekbart.base
mkdir -p ./greekbart.base/

INPUT1=../corpus/processed/el/train.el
INPUT2=../corpus/processed/el/valid.el
VOC_SIZE=50000
SAMPLE_LENGTH=14900000
PREFIX=sentence.bpe
COVERAGE=0.9995
THREADS=64


#Train sentencepiece
spm_train --input=$INPUT1 \
--model_prefix=$DATA/sentence.bpe \
--character_coverage=$COVERAGE \
--vocab_size=$VOC_SIZE \
--model_type=bpe \
--input_sentence_size=$SAMPLE_LENGTH \
--shuffle_input_sentence=true \
--train_extremely_large_corpus=true \
--random_seed=4294967295 \
--unk_id 3 \
--bos_id 0 \
--eos_id 2 \
--pad_id 1 \
--num_threads=$THREADS

echo "End of sentence piece training"
echo "Encode data"

# Encode data
spm_encode --model ./greekbart.base/sentence.bpe.model < $INPUT1 > train.spm.sent
spm_encode --model ./greekbart.base/sentence.bpe.model < $INPUT2 > valid.spm.sent


# Convert sentencepiece vocab to fairseq format
cut -f1 ./greekbart.base/sentence.bpe.vocab | tail -n +5 | sed "s/$/ 100/g" > ./greekbart.base/dict.txt
echo "End of Encoding"
