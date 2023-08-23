import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import datetime
import pandas as pd
import os
import configparser

conf_ = configparser.ConfigParser()
conf_.read('../colors.ini')
colors     = conf_['COLORS']
styles     = conf_['STYLE']
label_leg  = conf_['LEGEND']


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

    nbins = 47 #100
    #if not use_values :
        #x_max = 60 if extra_name else 101
        #y_max = y_max / 100
        #y_min = y_min / 100

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
        color        = colors[METRIC] if METRIC in colors else 'k'
        style        = styles[METRIC] if METRIC in styles else '-'
        METRIC_label = label_leg[METRIC] if METRIC in label_leg else METRIC
        plt.plot(xbins, density_to_plot, color=color, lw=3, label=METRIC_label, linestyle=style)
        #plt.fill_between(xbins, y_min, density_to_plot, interpolate=True, alpha=0.25, label=METRIC_label, color=color)

    # set axis
    ax.spines[['right', 'top', 'left']].set_visible(False)
    ax.set_xlabel('| $ \Delta $ p |' if draw_abs else '$ \Delta $ p')
    if use_values : ax.set_xlabel('|Z|' if draw_abs else 'Z')
    ax.set_ylabel('density')
    plt.yscale('log')
    plt.grid(True, axis='y', linestyle='--')
    plt.tick_params(axis='y', left=False, bottom=False, labelbottom=False,which='both', top=False)
    plt.ylim([y_min, y_max])

    # vertical line at 0
    if not draw_abs : plt.axvline(0, color='k', linewidth=1, linestyle='--')

    # Write the number according to the article ordering
    pert_text = '(X)'
    if 'P9' in folder_out : pert_text = '(1)'
    if 'P3' in folder_out : pert_text = '(2)'
    if 'P2' in folder_out : pert_text = '(3)'
    if 'P5' in folder_out : pert_text = '(4)'
    if 'F1' in folder_out : pert_text = '(5)'
    if 'F2' in folder_out : pert_text = '(6)'
    if 'F4' in folder_out : pert_text = '(7)'
    plt.text(0.04, 0.93, 'Perturbation '+pert_text, weight='bold', transform = ax.transAxes)

    # legend
    #leg = plt.legend(title='Indices', loc = 'upper right', fontsize=13)
    #leg = plt.legend(loc = 'upper right', fontsize=13, ncol=2)
    leg = plt.legend(loc = (0.55, 0.65), fontsize=15, ncol=2)
    plt.setp(leg.get_title(),fontweight='bold')
    leg.get_frame().set_linewidth(0.0)
    leg.get_frame().set_color('white')
    #leg.get_frame().set_alpha(0.)

    plt.savefig(f'{folder_out}/density_Z{extra_name}.png', dpi=300)
    plt.savefig(f'{folder_out}/density_Z{extra_name}.pdf', dpi=300)

    fig.clf()





def variation_all( METRICS,
                   df_original,
                   df_modified,
                   selected_number = 0,
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
    #if not os.path.isdir(folder_out) : os.makedirs(folder_out)
    if not os.path.isdir(f'{folder_out}/output')   : os.makedirs(f'{folder_out}/output')

    # create the output files to store Delta p
    f_txt           = open(f'{folder_out}/Z_mean.txt', 'w')
    variation_dict  = dict()


    for METRIC in METRICS :
        std_touse    =  std[METRIC]     if use_values else 1.

        Z_metric = (df_modified[METRIC].to_numpy() - df_original[METRIC].to_numpy()) / std_touse
        df_difference[METRIC] = Z_metric

        # select where there are non NAN values
        non_NAN = np.logical_and( np.isfinite(df_modified[METRIC]),
                                  np.isfinite(df_original[METRIC]))
        original_values = df_modified[METRIC].to_numpy()[non_NAN]
        modified_values = df_original[METRIC].to_numpy()[non_NAN]


        # write txt file
        abs_delta_Z = round(np.nanmean(np.abs(Z_metric)),                           3)
        corr_coef   = round(np.corrcoef(original_values, modified_values)[0,1],     3)
        neg_freq    = round(np.nansum(Z_metric<0)/np.sum(np.isfinite(Z_metric)),    3)
        nan_count   = round(np.count_nonzero(np.isnan(Z_metric)),                   3)
        f_txt.write(f'{METRIC}{" " * (20 - len(METRIC))}\t  {abs_delta_Z}   \t  {corr_coef}   \t  {neg_freq}    \t  {nan_count}\n')

        # Write the csv file
        variation_dict[METRIC] = [ METRIC,
                                   np.nanmean(np.abs(Z_metric)),
                                   np.corrcoef(original_values, modified_values)[0,1],
                                   np.nansum(Z_metric<0)/np.sum(np.isfinite(Z_metric)),
                                   selected_number
                                  ]


    # Write the dictionary in a csv file
    df = pd.DataFrame.from_dict(variation_dict, orient='index',
                      columns=['METRIC', 'Delta_p', 'correlation',
                               'fraction_of_events_with_decreasing_organization', 'number_of_objects'])
    df.to_csv(f'{folder_out}/output/info_n{selected_number}.csv', index=False)


    df_difference = df_difference[METRICS]
    draw_and_save (METRICS,
                   df_difference,
                   y_min = 0.001 if use_values else 0.00001,
                   y_max = 50    if use_values else 0.99,
                   x_max = 5     if use_values else 60,
                   folder_out = folder_out,
                   extra_text = extra_text,
                   extra_name = '',
                   use_values = use_values,
                   draw_abs = False
                   )

    draw_and_save (METRICS,
                   df_difference,
                   y_min = 0.05  if use_values else 0.0005,
                   y_max = 50    if use_values else 0.99,
                   x_max = 1.3   if use_values else 60,
                   folder_out = folder_out,
                   extra_text = extra_text,
                   extra_name = '_zoom',
                   use_values = use_values,
                   draw_abs = False
                   )


    draw_and_save (METRICS,
                   df_difference,
                   y_min = 0.05  if use_values else 0.0005,
                   y_max = 50    if use_values else 0.999,
                   x_max = 0.8   if use_values else 49,
                   folder_out = folder_out,
                   extra_text = extra_text,
                   extra_name = '_zoom_zoom',
                   use_values = use_values,
                   draw_abs = False
                   )



    draw_and_save (METRICS,
                   df_difference,
                   y_min = 0.011  if use_values else 0.00011,
                   y_max = 99     if use_values else 0.99,
                   x_max = 2      if use_values else 60,
                   folder_out = folder_out,
                   extra_text = extra_text,
                   extra_name = '_abs',
                   use_values = use_values,
                   draw_abs = True
                   )
