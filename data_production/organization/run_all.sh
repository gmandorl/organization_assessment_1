#!/bin/bash

source run.sh P1;     sleep 300
source run.sh P2;     sleep 300
source run.sh P2_bis; sleep 300
source run.sh P3;     sleep 300
source run.sh P4;     sleep 300
source run.sh P9;     sleep 300

source run.sh F1;     sleep 300
source run.sh F3;     sleep 300
source run.sh F4;     sleep 300

python python compute_E1.py

source run_merge.sh
