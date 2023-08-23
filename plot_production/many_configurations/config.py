

class config  :

    def __init__ (self,
                  property_label,
                  cases,
                  xlabel = 'base',
                  fname_original = 'base',
                  var_to_exclude = ['number', 'area_skm', 'area_spg', 'area_original', 'number_original']  + ['mean_area', 'Iorg_recommended', 'NN_edge', 'NN_center', 'ROME_norm', 'new_index_auto', 'new_index_mutual', 'D0', 'D2'],
                  ) :

        self.cases   = cases
        self.labels  = [cases[x]['label']  for x in cases]
        #self.factors = [cases[x]['factor'] if 'factor' in cases[x] else 1 for x in cases]
        #self.factors = {x:cases[x]['factor'] if 'factor' in cases[x] else 1 for x in cases}

        self.fname_original = fname_original
        self.var_to_exclude = var_to_exclude
        self.xlabel         = xlabel






cases_P2 = {f'shift{n}':        {'label': f'+{n}'}          for n in range(1,39,2) }
cases_P5 = {f'increased{n}':    {'label': f'+{n}'}          for n in range(1,20,1) }
cases_F1 = {f'reso{n}':         {'label': f'x{n}'}          for n in range(2,7)    }
cases_F3 = {f'smaller{n}':      {'label': f'-{n}'}          for n in range(1,11)   }


cases_F4 = {f'shift{n}':{'label': f'+{n}'} for n in range(1,20,1)}
#cases_F2 = {f'{n}min_later':{'label': f'+{n} min'} for n in [30, 60, 90]}
#cases_F2 = {f'{30*n}min_later':{'label': f'+{n/2} h'} for n in range(1,25)}
cases_F2 = {f'{30*n}min_later':{'label': f'+{int(n/2)} h'} for n in range(1,25)}
#cases_F2 = {f'{30*n}min_later':{'label': f'+{n/2} h'} for n in range(1,5)}
cases_F22= {f'{n}min_later':{'label': f'+{n/60} h'} for n in  [870, 1440, 2880, 4320]}
#cases_F2 = {**cases_F2, **cases_F22}




cases_E1 = {
    'all_x1'    : {'label' : 'a1'},
    'all_x10'   : {'label' : 'a10'},
    'mean_x1'   : {'label' : 'm1'},
    'mean_x10'  : {'label' : 'm10'},
    'shuffled'  : {'label' : 'sh'},
    }


configs = dict()
configs['P2'] = config('P2', cases = cases_P2, xlabel='shift of the test object')
configs['P5'] = config('P5', cases = cases_P5, xlabel='increase of the test object')
configs['F1'] = config('F1', cases = cases_F1, xlabel='scale factor of the grid boxes')
configs['F3'] = config('F3', cases = cases_F3, xlabel='pixels removed from the edge of the image')
configs['F4'] = config('F4', cases = cases_F4, xlabel='shift of region considered')
configs['F2'] = config('F2', cases = cases_F2, xlabel='time delay')
configs['E1'] = config('E1', cases = cases_E1, xlabel='examples')
