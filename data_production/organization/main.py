import numpy as np
import xarray as xr
import datetime
import pandas as pd
import importlib
import argparse
import os
import warnings
import glob
from run_metrics import *

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config_data",default="config_TOOCAN",help="name of the input config file")
parser.add_argument("-p", "--property", default='P1', help="property under study")
parser.add_argument("-m", "--month", default=1,    type=int, help="month")
parser.add_argument("-y", "--year",  default=2013, type=int, help="year")
args = parser.parse_args()

config=importlib.import_module( args.config_data )
studied_property=importlib.import_module( f'property_{args.property}' )
to_exclude=importlib.import_module( f'to_exclude_{config.label}' )




if __name__ == '__main__':
    start_time = datetime.datetime.now()

    print(f'{args.config_data} \t\t{args.year} \t{args.month}')



    file_names = glob.glob(f'{config.path}{args.year}/{args.year}_{"{0:0=2d}".format(args.month)}_*/*.nc')
    #print(f'{config.path}{args.year}/{args.year}_{"{0:0=2d}".format(args.month)}_*/*.nc')
    file_names.sort()
    print('number of files: ', len(file_names))


    # loop over all the modification of the file "studied_property"
    cases = studied_property.cases
    for k in cases.keys() :


        df = pd.DataFrame()
        df = df.assign( year    =[],
                        month   =[],
                        day     =[],
                        hour    =[],
                        minute  =[] )

        with warnings.catch_warnings():
          warnings.simplefilter("ignore", category=RuntimeWarning)
          for fn in file_names :
            #print(fn)

            ds  = xr.open_dataset(fn)

            # read day and time
            image_time = ds.attrs['image_time']  # in the format 2018-06-06-T10-30-00 UTC
            yy = image_time[ :4]
            mm = image_time[5:7]
            dd = image_time[8:10]
            hh = image_time[12:14]
            mi = image_time[15:17]

            df_time_tmp = { 'year'  :  yy,
                            'month' :  mm,
                            'day'   :  dd,
                            'hour'  :  hh,
                            'minute':  mi
                            }
            df_time_tmp = pd.DataFrame(df_time_tmp, index=[1])
            date = (int(yy), int(mm), int(dd), int(hh), int(mi))
            if date in to_exclude.repeated_images :
                df      = pd.concat([df, df_time_tmp])
                continue


            # select the region and run the organization algorithms
            ds  = ds.sel(latitude  = slice(config.lat_min, config.lat_max),
                        longitude = slice(config.lon_min, config.lon_max) )
            reverse = -1 if config.cut_reversed else 1
            image = np.where( reverse*ds.variables[config.var_name].data[0] > reverse*config.cut, 1, 0 )
            image = studied_property.modify_image(image, cases[k])
            image = np.where(image>0, 1, 0)


            #print(yy,mm,dd,hh,mi)

            dict_org   = run_metrics( image )
            df_org_tmp = pd.DataFrame(dict_org, index=[1])
            df_org_tmp = df_org_tmp.reindex(sorted(df_org_tmp.columns), axis=1)

            df_tmp  = df_time_tmp.join(df_org_tmp)
            df      = pd.concat([df, df_tmp])


        if len(df)==0 : print('empty dataset')
        else :
            folder_out = f'output/tmp/{config.label}/{studied_property.label}/{k}/'
            if not os.path.isdir(folder_out) : os.makedirs(folder_out)
            df.to_csv(f'{folder_out}{studied_property.fname_out}_{k}___{args.year}_{args.month}.csv', index=False)


    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')



