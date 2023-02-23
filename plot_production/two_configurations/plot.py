import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import datetime
import pandas as pd
import argparse
import config
import os

from compare_2d    import compare_2d
from variation_all import variation_all


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset",  default="TOOCAN", help="name of the dataset")
parser.add_argument("-p", "--property", default="P1",     help="property to plot")
parser.add_argument('--use_anomaly',                      action='store_true')
parser.add_argument('--use_original', dest='use_anomaly', action='store_false')
parser.add_argument('--use_values',                         action='store_true')
parser.add_argument('--use_percentiles', dest='use_values', action='store_false')
parser.set_defaults(use_anomaly=True)
parser.set_defaults(use_values=True)
args = parser.parse_args()


config=config.configs[args.property]



if __name__ == '__main__':
    start_time = datetime.datetime.now()

    print('property:', args.property, ' \t use_values:', args.use_values, '\t use_anomaly:', args.use_anomaly)

    # path and prefix of the name of the files to read
    fname = 'anomaly___' if args.use_anomaly else ''
    path  = f'../../data_production/organization/output/merged/{args.dataset}/{args.property}/'
    if args.use_anomaly :       path = f'../../data_production/anomaly/output/{args.dataset}/{args.property}/'
    if not args.use_values :    path = f'../../data_production/percentiles/output/{args.dataset}/{args.property}/'

    df_original = pd.read_csv( f'{path}{fname}{args.property}_{config.fname_original}.csv')
    df_modified = pd.read_csv( f'{path}{fname}{args.property}_{config.fname_modified}.csv')


    METRICS = df_original.columns
    METRICS = [m for m in METRICS if m not in ['year', 'month', 'day', 'hour', 'minute', 'day_of_year']]

    factors = config.compute_factors(df_original.columns)

    # directory where to save the plots
    folder_out = 'anomaly' if args.use_anomaly else 'original'
    folder_out = f'{"percentiles" if not args.use_values else "values"}/{folder_out}'
    folder_out = f'figure/{args.dataset}/{folder_out}/{args.property}'
    if not os.path.isdir(f'{folder_out}/2d_comparison') : os.makedirs(f'{folder_out}/2d_comparison')


    ######### possible selection ################
    #idx_to_select = df_original['Iorg'] < 50
    #df_original   = df_original[idx_to_select]
    #df_modified   = df_modified[idx_to_select]
    #############################################

    # loop over all variables to produce the 2d distribution to compare the two cases
    for METRIC in METRICS :
        #print(METRIC)
        compare_2d( METRIC              = METRIC,
                    df_original         = df_original,
                    df_modified         = df_modified,
                    factors             = factors,
                    axis_label_original = METRIC,
                    axis_label_modified = f'{METRIC} {config.axis_label_modified}',
                    folder_out          = f'{folder_out}/2d_comparison',
                    use_values          = args.use_values
                    )



    METRICS = [x for x in METRICS if x not in config.var_to_exclude]

    # compare all indices on the same plot
    variation_all( METRICS,
                   df_original,
                   df_modified,
                   factors    = factors,
                   folder_out = folder_out,
                   use_values = args.use_values,
                   extra_text =''
                   )



    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')

