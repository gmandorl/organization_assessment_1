import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot
import xarray as xr
import pandas as pd
import datetime
import math
import argparse
import os
import scipy.optimize as spo


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset",  default="TOOCAN", help="dataset under study")
parser.add_argument("-p", "--property", default="P1",     help="name of the property")
args = parser.parse_args()

var_to_exclude = ["year", "month", "day", "hour", "minute"]


def fitting_function (xy, A00, A01, A02, A03, A04,
                          A10, A11, A12, A13, A14,
                          A20, A21, A22, A23, A24,
                          A30, A31, A32, A33, A34,
                          A40, A41, A42, A43, A44) :
    """This is the function used to fit. It is a combination of a
    diurnal cycle and annual cycle with 2 harmonic each"""

    year_fraction, day_fraction = xy
    year_fraction = year_fraction * 2. * math.pi
    day_fraction  = day_fraction  * 2. * math.pi

    # annual and semi-annual harmonics in year cycle
    yf_1cos = np.cos(  year_fraction)
    yf_1sin = np.sin(  year_fraction)
    yf_2cos = np.cos(2*year_fraction)
    yf_2sin = np.sin(2*year_fraction)

    # annual and semi-annual harmonics in diurnal cycle
    df_1cos = np.cos(  day_fraction )
    df_1sin = np.sin(  day_fraction )
    df_2cos = np.cos(2*day_fraction )
    df_2sin = np.sin(2*day_fraction )

    out = (A00 + A01*yf_1cos + A02*yf_1sin + A03*yf_2cos + A04*yf_2cos) + \
          (A10 + A11*yf_1cos + A12*yf_1sin + A13*yf_2cos + A14*yf_2cos) * df_1cos + \
          (A20 + A21*yf_1cos + A22*yf_1sin + A23*yf_2cos + A24*yf_2cos) * df_1sin + \
          (A30 + A31*yf_1cos + A32*yf_1sin + A33*yf_2cos + A34*yf_2cos) * df_2cos + \
          (A40 + A41*yf_1cos + A42*yf_1sin + A43*yf_2cos + A44*yf_2cos) * df_2sin
    return out.reshape(-1)#np.ravel(out, order='F')


def compute_day_of_year (year, month, day) :
    """Return the number of day from 1 to 366"""
    return datetime.date(int(year), int(month), int(day)).timetuple().tm_yday



def make_plot(DF, var_on_x, var_to_group, fname) :
    """ Produce and save the plots """

    cmap = matplotlib.cm.get_cmap('twilight')
    fig, ax = plt.subplots(figsize=(8,6))

    for vs in DF.columns :
        if vs in var_to_exclude : continue

        # plotting
        DFg = DF.groupby(by=[var_on_x, var_to_group]).mean().reset_index()
        DFg = DFg.groupby(var_to_group)
        N = len(DFg)
        for label, dfg in DFg:
            #df_selected = dfg.groupby(var_on_x).mean()
            ax.plot(dfg[var_on_x], dfg[vs], color=cmap(1.*int(label)/N), label=label)

        # legend and axes titles
        plt.legend(fontsize=9, loc = (1.01, -0.1))
        ax.set_ylabel(vs)
        ax.set_xlabel(var_on_x)

        # save the plot
        str_to_group = var_to_group + '_'*(9-len(fname))
        fname_out  = f'{fname}_fit___{str_to_group}___{var_on_x}___{vs}'
        folder_out = f'figure/{args.dataset}/{args.property}/{fname}'
        if not os.path.isdir(folder_out) : os.makedirs(folder_out)
        plt.savefig(f'{folder_out}/{fname_out}.png')
        plt.cla()

    plt.close()


def fill_missing_hours_and_days (df) :
    """ dd missing 'day_of_year' and 'half_hour' if needed (P3 needs this) """

    df_to_append = pd.DataFrame(columns=['day_of_year','half_hour'])
    for dd in range(1, 365+1) :
        for hh in range(0, 48) :
            if len(df.query(f'(day_of_year=={dd}) & (half_hour=={hh/2.})')) == 0 :
                df_to_append = df_to_append.append(dict(day_of_year=dd, half_hour=hh/2.), ignore_index=True)

    #print('DEBUG', df)
    #print('df_to_append', df_to_append)
    df = df.append(df_to_append, ignore_index=True)
    return df


if __name__ == '__main__':
    start_time = datetime.datetime.now()


    path       = f'../organization/output/merged/{args.dataset}/{args.property}/'
    file_names = os.listdir(path)
    print(file_names)

    for fname in file_names :
        df = pd.read_csv(f'{path}{fname}')

        # 'day_of_year' and 'half_hour' are the variables used in the fit
        df['half_hour']   = df['hour'] + df['minute']/60.
        df['day_of_year'] = df.apply(lambda x: compute_day_of_year(x['year'], x['month'], x['day']), axis=1)
        df['day_of_year'] = df['day_of_year'] - (df['day_of_year'] > 59)*(df['year']%4==0)  # 29/2 is considered 28/2


        # add missing 'day_of_year' and 'half_hour' if needed (P3 needs this)
        if args.property=='P3' : df = fill_missing_hours_and_days (df)



        # mean and non NAN count
        DFg     = df.groupby(['day_of_year','half_hour'])
        DF      = DFg.mean()
        DFcount = DFg.count()


        year_fraction = np.repeat(np.arange(365), 48)/365.
        day_fraction  = np.tile(np.arange(48), 365)/48.
        xdata = np.vstack((year_fraction, day_fraction))


        for vs in DF.columns :
            if vs in var_to_exclude : continue

            # computing counts, mean and std
            var    = DF[vs].to_numpy()
            counts = DFcount[vs].to_numpy()
            mean   = np.nanmean(var)
            std    = df[vs].std()

            # prepare data for the fit
            uncertainty = std / (counts+0.0001)**0.5 # the bias is to take care of counts=0
            var         = np.where(np.isfinite(var), var, mean)

            #print('SHAPE',  xdata.shape, var.shape)

            # perform the fit
            fit_params, fit_params_errors = spo.curve_fit(fitting_function, xdata, var,
                                                          sigma=uncertainty, maxfev = 10000)


            # save the annual and diurnal cycles on the same dataset
            var_fit = fitting_function (xdata, *fit_params)
            DF[vs]  = var_fit

            # chi2
            Z    = var - var_fit
            dZ   = uncertainty
            ndf  = (365*48 - len(fit_params))
            chi2 = np.sum(Z*Z / (dZ*dZ)) / ndf
            print(vs, '\nChi2: ', chi2, ' \t Chi2 / sigma( Chi2 ) :  ', (chi2-1)*(ndf/2.)**0.5 )


        folder_out_df = f'output/{args.dataset}/{args.property}'
        if not os.path.isdir(folder_out_df) : os.makedirs(folder_out_df)
        DF.to_csv(f'{folder_out_df}/annualCycleFit___{fname}')


        make_plot(DF.reset_index(), 'day_of_year', 'half_hour', fname[:-4])
        make_plot(DF.reset_index(), 'day_of_year', 'hour',      fname[:-4])
        make_plot(DF.reset_index(), 'half_hour',   'month',     fname[:-4])
        make_plot(DF.reset_index(), 'hour',        'month',     fname[:-4])

    print(f'This script needed {(datetime.datetime.now() - start_time).seconds} seconds')


