#!/bin/bash

dataset=$1


Rscript anomaly.R P1 $dataset &
Rscript anomaly.R P2 $dataset 1 &
Rscript anomaly.R P2 $dataset 2 &
Rscript anomaly.R P2 $dataset 3
Rscript anomaly.R P2 $dataset 4 &
Rscript anomaly.R P3 $dataset
Rscript anomaly.R P4 $dataset
Rscript anomaly.R P5 $dataset 1
Rscript anomaly.R P5 $dataset 2
Rscript anomaly.R P5 $dataset 3 &
Rscript anomaly.R P5 $dataset 4
Rscript anomaly.R P9 $dataset


Rscript anomaly.R F1 $dataset &
Rscript anomaly.R F2 $dataset 1
Rscript anomaly.R F2 $dataset 2 &
Rscript anomaly.R F2 $dataset 3
Rscript anomaly.R F2 $dataset 4 &
Rscript anomaly.R F3 $dataset
Rscript anomaly.R F4 $dataset 1
Rscript anomaly.R F4 $dataset 2 &
Rscript anomaly.R F4 $dataset 3
Rscript anomaly.R F4 $dataset 4

Rscript anomaly.R E1 $dataset
