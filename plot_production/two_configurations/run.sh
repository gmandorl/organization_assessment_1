#!/bin/bash

dataset=$1

# for n in {35..0..-5} #use_anomaly
for n in $(seq 3 1 40;seq 0 1 0)
do
for x in use_original #use_anomaly
do
for y in use_values use_percentiles
do


# python plot.py -p P1 --$x --$y -d $dataset -n $n &
python plot.py -p P2 --$x --$y -d $dataset -n $n &
python plot.py -p P3 --$x --$y -d $dataset -n $n &
# python plot.py -p P4 --$x --$y -d $dataset -n $n
python plot.py -p P5 --$x --$y -d $dataset -n $n &
# python plot.py -p P8 --$x --$y -d $dataset -n $n &
python plot.py -p P9 --$x --$y -d $dataset -n $n

python plot.py -p F1 --$x --$y -d $dataset -n $n &
python plot.py -p F2 --$x --$y -d $dataset -n $n &
# python plot.py -p F3 --$x --$y -d $dataset -n $n &
python plot.py -p F4 --$x --$y -d $dataset -n $n

python plot.py -p E1 --$x --$y -d $dataset -n $n

done
done
done


