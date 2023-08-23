#!/bin/bash

dataset=$1

python merge_csv.py -p P1 -d $dataset
python merge_csv.py -p P2 -d $dataset
python merge_csv.py -p P3 -d $dataset
# python merge_csv.py -p P4 -d $dataset
python merge_csv.py -p P5 -d $dataset
python merge_csv.py -p P8 -d $dataset
python merge_csv.py -p P9 -d $dataset
python merge_csv.py -p F1 -d $dataset
python merge_csv.py -p F3 -d $dataset
python merge_csv.py -p F4 -d $dataset
