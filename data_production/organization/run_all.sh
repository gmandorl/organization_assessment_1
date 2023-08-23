#!/bin/bash

dataset=$1


source run.sh P1  $dataset;     sleep 300
source run.sh P2  $dataset;     sleep 300
source run.sh P2_bis  $dataset; sleep 300
source run.sh P3  $dataset;     sleep 300
# source run.sh P4  $dataset;     sleep 300
source run.sh P5  $dataset;     sleep 300
source run.sh P8  $dataset;     sleep 300
source run.sh P9  $dataset;     sleep 300

source run.sh F1  $dataset;     sleep 300
source run.sh F3  $dataset;     sleep 300
source run.sh F4  $dataset;     sleep 300


source run_merge.sh $dataset

python compute_E1.py -d $dataset
python compute_F2.py -d $dataset
