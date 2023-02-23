

class config  :

    def __init__ (self,
                  property_label,
                  fname_original = 'base',
                  fname_modified = '',
                  axis_label_modified = 'with one additional object',
                  var_to_exclude = [],
                  scale_factor=1,
                  ) :

        self.property_label   = property_label
        self.fname_original   = fname_original
        self.fname_modified   = fname_modified
        self.var_to_exclude = var_to_exclude + ['number', 'area_skm', 'area_spg', 'area', 'number_original', 'area_original'] + ['mean_area', 'NN_edge', 'NN_center', 'ROME_norm']

        self.axis_label_modified         = axis_label_modified
        self.scale_factor = scale_factor

    def compute_factors(self, METRICS) :

        factors = {METRIC:1. for METRIC in METRICS}

        for METRIC in METRICS :
            if METRIC in ['area', 'area_skm', 'area_spg', 'ROME', 'ABCOP', 'mean_area'] :
                factors[METRIC] = factors[METRIC] * self.scale_factor**2
            if METRIC in ['NN_center', 'NN_edge', 'SCAI'] : #, 'COP'] :
                factors[METRIC] = factors[METRIC] * self.scale_factor
            if METRIC in ['MCAI'] :
                factors[METRIC] = factors[METRIC] / self.scale_factor  # < ------------------- is this correct for MCAI ?
            if METRIC in ['SCAI'] :
                factors[METRIC] = factors[METRIC] / self.scale_factor**2


        return factors






configs = dict()
configs['P1'] = config('P1', fname_original = 'base', fname_modified = 'plusObj', axis_label_modified = 'with one additional object')
configs['P2'] = config('P2', fname_original = 'base', fname_modified = 'shift20', axis_label_modified = 'ref. object shifted by 20 pixels')
configs['P3'] = config('P3', fname_original = 'base', fname_modified = 'mergedObj', axis_label_modified = 'when two objects are merged')
configs['P4'] = config('P4', fname_original = 'base', fname_modified = 'biggerObj', axis_label_modified = 'when one object has 1 pixel more')
configs['P9'] = config('P9', fname_original = 'base', fname_modified = 'plusObj', axis_label_modified = 'with one additional object')


configs['F1'] = config('F1', fname_original = 'base', fname_modified = 'reso3', axis_label_modified = 'with 3 times reduced resolution', scale_factor=3)
configs['F2'] = config('F2', fname_original = 'base', fname_modified = '30min_later', axis_label_modified = '30 minutes later')
configs['F3'] = config('F3', fname_original = 'base', fname_modified = 'smaller10', axis_label_modified = 'when image reduced by 10 pixel',
                       scale_factor = 120./110 )
configs['F4'] = config('F4', fname_original = 'base', fname_modified = 'shift10', axis_label_modified = 'region shifted by 10 pixels')

configs['E1'] = config('E1', fname_original = 'base', fname_modified = 'shuffled', axis_label_modified = 'random shuffle')


