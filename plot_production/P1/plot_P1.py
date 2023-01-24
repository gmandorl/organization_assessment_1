import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import datetime
import pandas as pd
import sys

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", default="TOOCAN", help="name of the dataset")
args = parser.parse_args()


sys.path.insert(0, '../types')
from compare_2d    import compare_2d
from variation_all import variation_all



if __name__ == '__main__':
    start_time = datetime.datetime.now()

    path = f'../../data_production/anomaly/output/{args.dataset}/P1/'
    df_original = pd.read_csv( f'{path}anomaly___P1_base.csv')
    df_modified = pd.read_csv( f'{path}anomaly___P1_plusObj.csv')

    METRICS = df_original.columns
    METRICS = [m for m in METRICS if m not in ['year', 'month', 'day', 'hour', 'minute', 'day_of_year']]
    print(METRICS)

    #for METRIC in METRICS :
        #print(METRIC)
        #compare_2d( METRIC              = METRIC,
                    #df_original         = df_original,
                    #df_modified         = df_modified,
                    #axis_label_original = METRIC,
                    #axis_label_modified = f'{METRIC} with one additional object',
                    #folder_out          = f'figure/{args.dataset}/2d_comparison'
                    #)

    var_to_exclude = ['number', 'area', 'area_skm', 'area_spg']
    METRICS = [x for x in METRICS if x not in var_to_exclude]

    variation_all( METRICS,
                   df_original,
                   df_modified,
                   folder_out = f'figure/{args.dataset}',
                   extra_text =''
                   )



    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')

