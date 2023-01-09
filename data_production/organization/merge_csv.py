import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
import datetime
import glob
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pFolder", default='P1', help="folder where to merge the files")
parser.add_argument("-d", "--dataset", default='TOOCAN', help="folder where to merge the files")
args = parser.parse_args()


if __name__ == '__main__':
    start_time = datetime.datetime.now()

    #pwd  = os.getcwd()
    path = f'output/tmp/{args.dataset}/{args.pFolder}/'
    labels = os.listdir(path)

    for label in labels :
        print(path, label)
        file_names = glob.glob(f'{path}{label}/*' )
        #print(f'{path}{label}')
        #print(file_names)

        df = pd.concat((pd.read_csv(f) for f in file_names), ignore_index=True)
        df = df.sort_values(by = ['year', 'month', 'day', 'hour', 'minute'], ascending = True)

        folder_out = f'output/merged/{args.dataset}/{args.pFolder}/'
        fname = os.listdir(f'{path}{label}/')[0].split('___')[0]
        if not os.path.isdir(folder_out) : os.makedirs(folder_out)
        df.to_csv(f'{folder_out}{fname}.csv', index=False)




    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')
