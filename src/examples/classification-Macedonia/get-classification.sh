#!/usr/bin/env bash

set -e

DATA_DIR=./data
# data paths
DATA_RAW=$DATA_DIR/raw
DATA_PROC=$DATA_DIR/processed

f=greek_classification
URLPATH=http://archive.aueb.gr:8085/files/greek_classification.zip


if [ ! -d $DATA_RAW ]; then
    mkdir -p $DATA_RAW
fi

if [ ! -d $DATA_PROC ]; then
    mkdir -p $DATA_PROC
fi

if [ ! -f $DATA_RAW/${f}.zip ]; then
    # Download data
    wget -c $URLPATH -P $DATA_RAW
    # unzip data
    echo "Unzipping data ..."
    unzip $DATA_RAW/${f}.zip -d $DATA_RAW
else
    echo "Files have been already unzipped."
fi

echo "Finished."
