#!/bin/bash

dataset=$1

# python main.py  -p P1  --use_anomaly -d $dataset &
# python main.py  -p P2  --use_anomaly -d $dataset -s 1
# python main.py  -p P2  --use_anomaly -d $dataset -s 2 &
# python main.py  -p P3  --use_anomaly -d $dataset
# python main.py  -p P4  --use_anomaly -d $dataset
# python main.py  -p P5  --use_anomaly -d $dataset &
# python main.py  -p P9  --use_anomaly -d $dataset
#
# python main.py  -p F1  --use_anomaly -d $dataset
# python main.py  -p F2  --use_anomaly -d $dataset -s 1 &
# python main.py  -p F2  --use_anomaly -d $dataset -s 2
# python main.py  -p F2  --use_anomaly -d $dataset -s 3
# python main.py  -p F3  --use_anomaly -d $dataset &
# python main.py  -p F4  --use_anomaly -d $dataset -s 1
# python main.py  -p F4  --use_anomaly -d $dataset -s 2 &
#
# python main.py  -p E1  --use_anomaly -d $dataset



python main.py  -p P1  --use_original -d $dataset &
python main.py  -p P2  --use_original -d $dataset -s 1 &
python main.py  -p P2  --use_original -d $dataset -s 2 &
python main.py  -p P2  --use_original -d $dataset -s 3 &
python main.py  -p P3  --use_original -d $dataset
# python main.py  -p P4  --use_original -d $dataset
python main.py  -p P5  --use_original -d $dataset -s 1 &
python main.py  -p P5  --use_original -d $dataset -s 2
python main.py  -p P5  --use_original -d $dataset -s 3 &
python main.py  -p P8  --use_original -d $dataset &
python main.py  -p P9  --use_original -d $dataset

python main.py  -p F1  --use_original -d $dataset
python main.py  -p F2  --use_original -d $dataset -s 1 &
python main.py  -p F2  --use_original -d $dataset -s 2 &
python main.py  -p F2  --use_original -d $dataset -s 3
python main.py  -p F3  --use_original -d $dataset &
python main.py  -p F4  --use_original -d $dataset -s 1 &
python main.py  -p F4  --use_original -d $dataset -s 2 &
python main.py  -p F4  --use_original -d $dataset -s 3

python main.py  -p E1  --use_original -d $dataset



