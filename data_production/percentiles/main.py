import numpy as np
import datetime
import glob
import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", default="TOOCAN",  help="name of the dataset")
parser.add_argument("-p", "--property",default="P1",      help="property under study")
parser.add_argument("-s", "--split",   default=0,         help="split the input fils in two groups")
parser.add_argument('--use_anomaly',                      action='store_true')
parser.add_argument('--use_original', dest='use_anomaly', action='store_false')
parser.set_defaults(use_anomaly=True)
args = parser.parse_args()


var_to_exclude = ['year', 'month', 'day', 'hour', 'minute', 'day_of_year', 'number_original', 'area_original']


def compute_percentile (x, var_base) :
    """ return the percentile of the distribution of the non NAN base vector"""
    if np.isnan(x) : return np.nan
    return 100 * np.nansum((var_base<=x)) / np.sum(np.isfinite(var_base))


if __name__ == '__main__':
    start_time = datetime.datetime.now()

    print('use_anomaly', args.use_anomaly)

    # path and prefix of the names
    path = f'../organization/output/merged/{args.dataset}/{args.property}/'
    if args.use_anomaly : path = f'../anomaly/output/{args.dataset}/{args.property}/'
    prefix = 'anomaly___' if args.use_anomaly else ''

    # list of the files to read
    fname_base = f'{path}{prefix}{args.property}_base.csv'
    file_names = glob.glob(f'{path}{prefix}{args.property}*.csv')
    file_names.sort()


    # use only half od the files if needed (because they may be too many)
    if args.split=='1' : file_names = file_names[                         :int( len(file_names)/2 ) ]
    if args.split=='2' : file_names = file_names[ int( len(file_names)/2 ):                         ]



    # file base to use for computing percentiles
    df_base = pd.read_csv(fname_base)
    columns = [ x for x in df_base.columns if x not in var_to_exclude]


    # loop over all the files
    for fname_extended in file_names :
        fname   = fname_extended.split('/')[-1]
        print(fname_extended)

        # read file
        df = pd.read_csv(fname_extended)

        ## save number and area
        #df['number_original']   = df['number'].to_numpy()
        #df['area_original']     = df['area'].to_numpy()


        for vs in columns :

            var_base = df_base[vs].to_numpy()
            df[vs]   = df.apply(lambda x: compute_percentile(x[vs], var_base), axis=1)


        folder_out = f'output/{args.dataset}/{args.property}/'
        if not os.path.isdir(folder_out) : os.makedirs(folder_out)
        df.to_csv(f'{folder_out}{fname}', index=False)


    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')


