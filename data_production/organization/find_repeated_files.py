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


path = f'output/merged/{args.dataset}/'
time_shift = 30


def compute_day_of_year (year, month, day, hour, minute) :
    """Return the date in datetime format"""
    return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), tzinfo=timezone.utc)


def time_diff(t1, t2) :
    return t1==t2




if __name__ == '__main__':
    start_time = datetime.datetime.now()



    df   = pd.read_csv(f'{path}P9/P9_base.csv')

    df['date'] = df.apply(lambda x: compute_day_of_year(x['year'],
                                                        x['month'],
                                                        x['day'],
                                                        x['hour'],
                                                        x['minute']), axis=1)

    df1  = df.iloc[:-1 , :]
    df2  = df.iloc[1:  , :]

    area_1 = df1['area'].to_numpy()
    area_2 = df2['area'].to_numpy()
    number_1 = df1['number'].to_numpy()
    number_2 = df2['number'].to_numpy()
    COP_1 = df1['COP'].to_numpy()
    COP_2 = df2['COP'].to_numpy()
    Iorg_1 = df1['Iorg'].to_numpy()
    Iorg_2 = df2['Iorg'].to_numpy()

    is_the_same = (area_1==area_2) * (number_1==number_2) * (COP_1==COP_2) * (Iorg_1==Iorg_2)

    #df1['date_shifted'] = df2['date'].to_numpy() - datetime.timedelta(minutes=time_shift)
    #df1['to_select'] = df1.apply(lambda x: time_diff(x['date'], x['date_shifted']), axis=1)
    df2['to_select'] = is_the_same


    df2 = df2.query('to_select==True')
    #df2 = df2.query('month==1')
    #df2 = df2.query('year==2013')
    #print(df2['date'].to_list())

    years   = df2['year'].to_list()
    months  = df2['month'].to_list()
    days    = df2['day'].to_list()
    hours   = df2['hour'].to_list()
    miuntes = df2['minute'].to_list()

    f_txt = open(f'to_exclude_{args.dataset}_tmp.py', 'w')
    f_txt.write(f'repeated_images = [ ')
    for n in range(0,len(df2)) :
        f_txt.write(f' ({years[n]}, {months[n]}, {days[n]}, {hours[n]}, {miuntes[n]})')

        if n == len(df2) : continue
        if n%3==0 : f_txt.write(f', ')
        else      : f_txt.write(f', \n                    ')

    f_txt.write(f']\n')





    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')

