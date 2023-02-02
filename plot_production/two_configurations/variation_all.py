import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import datetime
import pandas as pd
import os



def draw_and_save (METRICS,
                   df_difference,
                   y_min = 0.09,
                   y_max = 99,
                   x_max = 1.4,
                   folder_out = 'figure',
                   extra_text = '',
                   extra_name = '',
                   draw_abs = False
                   ) :

    fig, ax   = plt.subplots( figsize=(8,6) )

    nbins = 100
    x_min = 0 if draw_abs else -x_max
    bsize = (x_max-x_min)/nbins

    for METRIC in METRICS :
        Z_metric    = df_difference[METRIC].to_numpy()
        sample_size = Z_metric.size
        if draw_abs : Z_metric = np.abs(Z_metric)

        h1 = np.histogram(Z_metric, bins=nbins, range=(x_min,x_max))#, density=True)

        xbins = (h1[1][1:] + h1[1][:-1] ) /2.
        density_to_plot = h1[0] / bsize / sample_size  # this normalization is better than numpy's
        plt.plot(xbins, density_to_plot)#, label=METRIC)
        plt.fill_between(xbins, y_min, density_to_plot, interpolate=True, alpha=0.25, label=METRIC)

    # set axis
    ax.spines[['right', 'top', 'left']].set_visible(False)
    ax.set_xlabel('|Z|' if draw_abs else 'Z')
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
                   extra_text = ''
                   ) :



    # plt font
    font = {'family' : 'serif','size': 18}
    plt.rc('font', **font)

    df_original   = df_original[METRICS]
    df_modified   = df_modified[METRICS]
    df_difference = pd.DataFrame(index=range(len(df_original)),columns=METRICS)


    std = df_original.std(skipna=True)
    #print(df_original, '\n', std, std['ABCOP'])

    for METRIC in METRICS :
        df_difference[METRIC] = (df_modified[METRIC]*factors[METRIC] - df_original[METRIC]) / std[METRIC]
        Z_metric = df_difference[METRIC].to_numpy()
        print(METRIC, '    \t ', np.nanmean(np.abs(Z_metric)))


    if not os.path.isdir(folder_out) : os.makedirs(folder_out)

    draw_and_save (METRICS,
                   df_difference,
                   y_min = 0.001,
                   y_max = 99,
                   x_max = 5,
                   folder_out = folder_out,
                   extra_text = extra_text,
                   extra_name = '',
                   draw_abs = False
                   )

    draw_and_save (METRICS,
                   df_difference,
                   y_min = 0.11,
                   y_max = 99,
                   x_max = 1.3,
                   folder_out = folder_out,
                   extra_text = extra_text,
                   extra_name = '_zoom',
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
                   draw_abs = True
                   )
