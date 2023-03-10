#!/bin/bash

dataset=$1


python make_seasonal_fit.py -p P1 -d $dataset
python make_seasonal_fit.py -p P2 -d $dataset
python make_seasonal_fit.py -p P3 -d $dataset
python make_seasonal_fit.py -p P4 -d $dataset
python make_seasonal_fit.py -p P5 -d $dataset
python make_seasonal_fit.py -p P9 -d $dataset


python make_seasonal_fit.py -p F1 -d $dataset
python make_seasonal_fit.py -p F2 -d $dataset
python make_seasonal_fit.py -p F3 -d $dataset
python make_seasonal_fit.py -p F4 -d $dataset


python make_seasonal_fit.py -p E1 -d $dataset

