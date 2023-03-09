import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import datetime
from datetime import timezone
import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", default='TOOCAN', help="folder where to merge the files")
args = parser.parse_args()


def compute_day_of_year (year, month, day, hour, minute) :
    """Return the date in datetime format"""
    return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), tzinfo=timezone.utc)


def time_diff(t1, t2) :
    return t1==t2




if __name__ == '__main__':
    start_time = datetime.datetime.now()


    for n, time_shift in enumerate([30,60,90]) :

        path = f'../organization/output/merged/{args.dataset}/'

        df   = pd.read_csv(f'{path}P9/P9_base.csv')

        df['date'] = df.apply(lambda x: compute_day_of_year(x['year'],
                                                            x['month'],
                                                            x['day'],
                                                            x['hour'],
                                                            x['minute']), axis=1)

        df1  = df
        df2  = df.iloc[n+1:  , :]
        df2  = pd.concat( ( df2, pd.DataFrame(columns=df1.columns, index=list(range(n+1)) ) ) )


        # shift the two dataframe ( "to_numpy" is crucial to perform the shift! )
        df1['date_shifted'] = df2['date'].to_numpy() - datetime.timedelta(minutes=time_shift)
        df1['to_select'] = df1.apply(lambda x: time_diff(x['date'], x['date_shifted']), axis=1)
        df2['to_select'] = df1['to_select'].to_numpy()


        # perform the selection
        #df1 = df1.query('to_select==True')
        #df2 = df2.query('to_select==True')
        df2[df2['to_select']==False] = np.nan


        # remove new used columns
        del df1['date_shifted']
        del df1['to_select']
        del df2['to_select']
        del df1['date']
        del df2['date']

        #print(df1, '\n\n', df2)

        # save the new data
        folder_out = f'{path}/F2/'
        if not os.path.isdir(folder_out) : os.makedirs(folder_out)
        df1.to_csv(f'{folder_out}F2_base.csv',           index=False)
        df2.to_csv(f'{folder_out}F2_{time_shift}min_later.csv',    index=False)


    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')

