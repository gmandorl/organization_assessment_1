#!/bin/bash

dataset=$1


# compute the organization indices and store them in csv files (and compute eamples E1)
cd data_production/organization/
source run_all.sh $dataset
sleep 300


# compute the deseasonal and dediurnalized anomaly (and compute property F2)
echo 'running percentiles'
cd ../percentiles/
source run.sh $dataset
sleep 300
cd ../..




# produce the plots
echo 'running plots'
cd plot_production/two_configurations/
source run.sh $dataset
cd ../many_configurations/
source run.sh $dataset
cd ../..


