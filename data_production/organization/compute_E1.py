import numpy as np
import datetime
import os
import pandas as pd
import argparse
import copy

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset",default="TOOCAN",help="name of the dataset to use")
args = parser.parse_args()



if __name__ == '__main__' :
    start_time = datetime.datetime.now()

    # read the data
    fname = f'output/merged/{args.dataset}/P9/P9_base.csv'
    df = pd.read_csv(fname)
    df = df[df['year'].notna()]  # those NAN are the repeated files

    # create directory for E1
    folder_out = f'output/merged/{args.dataset}/E1'
    if not os.path.isdir(folder_out) : os.makedirs(folder_out)

    # columns to modify
    col_to_not_modify = ['year', 'month', 'day', 'hour', 'minute']
    columns = [ x for x in df.columns if not x in col_to_not_modify ]


    ##########################################################
    ################ produce the new datasets ################
    ##########################################################

    # save the base
    df.to_csv(f'{folder_out}/E1_base.csv', index=False)

    # shuffle the DataFrame rows
    df_shuffled = df.sample(frac = 1)
    df_shuffled.to_csv(f'{folder_out}/E1_shuffled.csv', index=False)


    # define the new dataframes
    df_x1__mean = copy.deepcopy(df)
    df_x10_mean = copy.deepcopy(df)
    df_x1__all  = copy.deepcopy(df)
    df_x10_all  = copy.deepcopy(df)

    for vs in columns :
        mean = df.mean()[vs]

        # increase by 1% and 10% the mean
        df_x1__mean[vs] = df_x1__mean[vs] + 0.01*mean
        df_x10_mean[vs] = df_x10_mean[vs] + 0.10*mean

        # increase by 1% and 10% the all elements
        df_x1__mean[vs] = 1.01 * df_x1__mean[vs]
        df_x10_mean[vs] = 1.10 * df_x10_mean[vs]



    # save the new dataframes
    df_x1__mean.to_csv( f'{folder_out}/E1_mean_x1.csv' , index=False)
    df_x10_mean.to_csv( f'{folder_out}/E1_mean_x10.csv', index=False)
    df_x1__all.to_csv(  f'{folder_out}/E1_all_x1.csv'  , index=False)
    df_x10_all.to_csv(  f'{folder_out}/E1_all_x10.csv' , index=False)



    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')
