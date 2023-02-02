import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import datetime
import os



def draw_and_save ( METRIC,
                    H2,
                    axis_label_original,
                    axis_label_modified,
                    folder_out = "figure/2d_comparison/",
                    set_log = False
                    ) :

    fig, ax   = plt.subplots( figsize=(8,6) )

    # transform the histogram into density
    SF         =  100 / np.sum(H2[0]) / (H2[1][1] - H2[1][0])**2
    h2_to_plot =  H2[0]
    h2_to_plot =  h2_to_plot * SF


    # x-y limits
    xedges  = ( H2[1][:-1] + H2[1][1:] ) / 2.
    yedges  = ( H2[2][:-1] + H2[2][1:] ) / 2.

    # z limits
    levels  = np.linspace (SF, h2_to_plot.max(), 11)
    ticks = np.array([levels[0], levels[2], levels[4], levels[6], levels[8], levels[10]])
    ticks_round = np.around(ticks if not set_log else np.exp(ticks), 1)

    # plot the density
    h2_to_plot = np.where(h2_to_plot>levels[0], h2_to_plot, np.nan)
    contourf_  = plt.contourf(xedges, yedges, h2_to_plot, levels=levels, cmap='Blues')

    # plot the diagonal
    range_min = xedges[1]
    range_max = xedges[-2]
    plt.plot( (range_min,range_max),(range_min,range_max), range_max, color='r', linestyle='--', linewidth=2)

    # add colorbar
    fig.subplots_adjust(left=0.15, right=0.82)  # add a new axix to the right
    cbar_ax = fig.add_axes([0.84, 0.2, 0.01, 0.6])
    fig.colorbar(contourf_, cax=cbar_ax)

    # axis label
    ax.set_xlabel(axis_label_original)
    ax.set_ylabel(axis_label_modified)
    plt.text(1.04, 0.97, 'Density', weight='bold', transform = ax.transAxes)

    plt.savefig(f'{folder_out}/{METRIC}.png')






def compare_2d( METRIC,
                df_original,
                df_modified,
                axis_label_original,
                axis_label_modified,
                factors,
                nbins      = 50,
                folder_out = "figure/2d_comparison/"
                ) :

    original = df_original[METRIC]
    modified = df_modified[METRIC] * factors[METRIC]


    # select where there are non NAN values
    non_NAN = np.logical_and( np.isfinite(original),
                              np.isfinite(modified))

    original = original[non_NAN].to_numpy()
    modified = modified[non_NAN].to_numpy()


    # numpy to plot
    up_limit   =  np.quantile(original, q=0.99)
    lo_limit   =  np.quantile(original, q=0.01)
    plot_range =  [[lo_limit, up_limit], [lo_limit, up_limit]]
    H2 = np.histogram2d(modified, original, bins=nbins, range=plot_range)



    if not os.path.isdir(folder_out) : os.makedirs(folder_out)

    # plt font
    font = {'family' : 'serif','size': 18}
    plt.rc('font', **font)


    draw_and_save( METRIC, H2, axis_label_original, axis_label_modified, folder_out, set_log = False)
    # log option still not implemented
    #draw_and_save( METRIC, H2, axis_label_original, axis_label_modified, folder_out, set_log = True )






