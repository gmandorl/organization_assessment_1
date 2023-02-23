import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import datetime
import pandas as pd
import os
import configparser

conf_ = configparser.ConfigParser()
conf_.read('../colors.ini')
colors = conf_['COLORS']


#import tomllib
#datac = tomllib.loads('example.ini')


def draw_and_save (METRICS,
                   df_difference,
                   y_min = 0.09,
                   y_max = 99,
                   x_max = 1.4,
                   folder_out = 'figure',
                   extra_text = '',
                   extra_name = '',
                   use_values = True,
                   draw_abs = False
                   ) :

    fig, ax   = plt.subplots( figsize=(8,6) )

    nbins = 100
    if not use_values :
        x_max = 101
        y_max = y_max / 100
        y_min = y_min / 100

    x_min = 0 if draw_abs else -x_max
    bsize = (x_max-x_min)/nbins

    for METRIC in METRICS :
        Z_metric    = df_difference[METRIC].to_numpy()
        sample_size = np.count_nonzero(~np.isnan(Z_metric)) # count non NAN
        if draw_abs : Z_metric = np.abs(Z_metric)

        h1 = np.histogram(Z_metric, bins=nbins, range=(x_min,x_max))#, density=True)

        # numpy arrays to plot
        xbins = (h1[1][1:] + h1[1][:-1] ) /2.
        density_to_plot = h1[0] / bsize / sample_size  # this normalization is better than numpy's

        #print('density ', METRIC, np.sum(density_to_plot)*bsize) # should be 1

        # color and plot
        color = colors[METRIC] if METRIC in colors else 'k'
        plt.plot(xbins, density_to_plot, color=color)#, label=METRIC)
        plt.fill_between(xbins, y_min, density_to_plot, interpolate=True, alpha=0.25, label=METRIC, color=color)

    # set axis
    ax.spines[['right', 'top', 'left']].set_visible(False)
    ax.set_xlabel('percentile difference in absolute value' if draw_abs else 'percentile difference')
    if use_values : ax.set_xlabel('|Z|' if draw_abs else 'Z')
    ax.set_ylabel('density')
    plt.yscale('log')
    plt.grid(True, axis='y', linestyle='--')
    plt.tick_params(axis='y', left=False, bottom=False, labelbottom=False,which='both', top=False)
    plt.ylim([y_min, y_max])

    # vertical line at 0
    if not draw_abs : plt.axvline(0, color='k', linewidth=1, linestyle='--')

    # legend
    leg = plt.legend(title='Indices', loc = 'upper right', fontsize=13)
    plt.setp(leg.get_title(),fontweight='bold')
    leg.get_frame().set_linewidth(0.0)
    leg.get_frame().set_color('white')
    #leg.get_frame().set_alpha(1.)

    plt.savefig(f'{folder_out}/density_Z{extra_name}.png')

    fig.clf()





def variation_all( METRICS,
                   df_original,
                   df_modified,
                   factors,
                   folder_out = 'figure',
                   use_values = True,
                   extra_text = ''
                   ) :



    # plt font
    font = {'family' : 'serif','size': 18}
    plt.rc('font', **font)

    # dataframe and variables to use
    columns = [x for x in df_original.columns if x not in ['year', 'month', 'day', 'hour', 'minute', 'day_of_year']]
    df_difference = pd.DataFrame(index=range(len(df_original)),columns=columns)

    std = df_original.std(skipna=True)

    # create the output folder
    if not os.path.isdir(folder_out) : os.makedirs(folder_out)
    f_txt = open(f'{folder_out}/Z_mean.txt', 'w')


    for METRIC in columns :
        std_touse    =  std[METRIC]     if use_values else 1.
        factor_touse =  factors[METRIC] if use_values else 1.
        df_difference[METRIC] = (df_modified[METRIC]*factor_touse - df_original[METRIC]) / std_touse
        Z_metric = df_difference[METRIC].to_numpy()
        f_txt.write(f'{METRIC}    \t  {np.nanmean(np.abs(Z_metric))}    \t  {np.count_nonzero(np.isnan(Z_metric))}\n')
        #print(METRIC, '    \t ', len(df_difference.query(f'{METRIC}<0.1')) / len(df_difference))


    df_difference = df_difference[METRICS]
    draw_and_save (METRICS,
                   df_difference,
                   y_min = 0.001,
                   y_max = 50,
                   x_max = 5,
                   folder_out = folder_out,
                   extra_text = extra_text,
                   extra_name = '',
                   use_values = use_values,
                   draw_abs = False
                   )

    draw_and_save (METRICS,
                   df_difference,
                   y_min = 0.05,
                   y_max = 50,
                   x_max = 1.3,
                   folder_out = folder_out,
                   extra_text = extra_text,
                   extra_name = '_zoom',
                   use_values = use_values,
                   draw_abs = False
                   )

    draw_and_save (METRICS,
                   df_difference,
                   y_min = 0.011,
                   y_max = 99,
                   x_max = 2,
                   folder_out = folder_out,
                   extra_text = extra_text,
                   extra_name = '_abs',
                   use_values = use_values,
                   draw_abs = True
                   )
