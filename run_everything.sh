#!/bin/bash

# compute the organization indices and store them in csv files (and compute eamples E1)
cd data_production/organization/
source run_all.sh
sleep 300


# compute the deseasonal and dediurnalized anomaly (and compute property F2)
echo 'running anomalies'
cd ../anomaly/
source run_fit.sh
source run_anomaly.sh
sleep 300
python compute_F2.py


# compute the deseasonal and dediurnalized anomaly (and compute property F2)
echo 'running percentiles'
cd ../percentiles/
source run.sh
sleep 300
cd ../..


# produce the plots
echo 'running plots'
cd plot_production/two_configurations/
source run.sh
cd ../many_configurations/
source run.sh


