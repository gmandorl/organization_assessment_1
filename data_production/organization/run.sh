#!/bin/bash



PROP=$1
dataset=$2

for yy in {2012..2016}
# for yy in {2017..2020}
# for yy in 2017
do
python main.py -y $yy -m 1  -p $PROP -d $dataset  &
python main.py -y $yy -m 2  -p $PROP -d $dataset  &
python main.py -y $yy -m 3  -p $PROP -d $dataset  &
python main.py -y $yy -m 4  -p $PROP -d $dataset  &
python main.py -y $yy -m 5  -p $PROP -d $dataset  &
python main.py -y $yy -m 6  -p $PROP -d $dataset  &
python main.py -y $yy -m 7  -p $PROP -d $dataset  &
python main.py -y $yy -m 8  -p $PROP -d $dataset  &
python main.py -y $yy -m 9  -p $PROP -d $dataset  &
python main.py -y $yy -m 10 -p $PROP -d $dataset  &
python main.py -y $yy -m 11 -p $PROP -d $dataset  &
python main.py -y $yy -m 12 -p $PROP -d $dataset
sleep 40
done

