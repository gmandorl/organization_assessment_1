import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import datetime
import pandas as pd
import argparse
import config

from compare_2d    import compare_2d
from variation_all import variation_all


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset",  default="TOOCAN", help="name of the dataset")
parser.add_argument("-p", "--property", default="P1",     help="property to plot")
args = parser.parse_args()


config=config.configs[args.property]



if __name__ == '__main__':
    start_time = datetime.datetime.now()

    path = f'../../data_production/anomaly/output/{args.dataset}/{args.property}/'
    df_original = pd.read_csv( f'{path}anomaly___{args.property}_{config.fname_original}.csv')
    df_modified = pd.read_csv( f'{path}anomaly___{args.property}_{config.fname_modified}.csv')


    METRICS = df_original.columns
    METRICS = [m for m in METRICS if m not in ['year', 'month', 'day', 'hour', 'minute', 'day_of_year']]

    factors = config.compute_factors(METRICS)

    for METRIC in METRICS :
        #print(METRIC)
        compare_2d( METRIC              = METRIC,
                    df_original         = df_original,
                    df_modified         = df_modified,
                    factors             = factors,
                    axis_label_original = METRIC,
                    axis_label_modified = f'{METRIC} {config.axis_label_modified}',
                    folder_out          = f'figure/{args.dataset}/{args.property}/2d_comparison'
                    )

    METRICS = [x for x in METRICS if x not in config.var_to_exclude]

    variation_all( METRICS,
                   df_original,
                   df_modified,
                   factors    = factors,
                   folder_out = f'figure/{args.dataset}/{args.property}',
                   extra_text =''
                   )



    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')

