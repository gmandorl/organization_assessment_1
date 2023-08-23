#!/bin/bash

dataset=$1

for x in use_original
do
for y in use_values use_percentiles
do

python plot.py -p P2 --$x --$y -d $dataset
python plot.py -p P5 --$x --$y -d $dataset
python plot.py -p F1 --$x --$y -d $dataset
python plot.py -p F2 --$x --$y -d $dataset
python plot.py -p F3 --$x --$y -d $dataset
python plot.py -p F4 --$x --$y -d $dataset
python plot.py -p E1 --$x --$y -d $dataset

done
done


