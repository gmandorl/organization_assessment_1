

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
        self.var_to_exclude = var_to_exclude + ['area_skm', 'area_spg', 'number_original', 'area_original'] + ['mean_area', 'NN_edge', 'NN_center', 'ROME_norm', 'ROME_norm2', 'Iorg_all_events', 'new_index_auto', 'new_index_mutual', 'SCAI2', 'MCAI2', 'D0', 'D2', 'Iorg_recommended', 'Lorg2', 'ROME_delta', 'H', 'Ishape'] # + ['number', 'area']

        self.axis_label_modified         = axis_label_modified
        self.scale_factor = scale_factor








configs = dict()
configs['P1'] = config('P1', fname_original = 'base', fname_modified = 'plusObj',       axis_label_modified = 'with one additional object')
configs['P2'] = config('P2', fname_original = 'base', fname_modified = 'shift20',       axis_label_modified = 'test object shifted by 20 pixels')
configs['P3'] = config('P3', fname_original = 'base', fname_modified = 'mergedObj',     axis_label_modified = 'when two objects are merged')
configs['P4'] = config('P4', fname_original = 'base', fname_modified = 'biggerObj',     axis_label_modified = 'when one object has 1 pixel more')
configs['P5'] = config('P5', fname_original = 'base', fname_modified = 'increased20',   axis_label_modified = 'test object side increased by 20 pixels')
configs['P8'] = config('P8', fname_original = 'base', fname_modified = 'plus2Obj',      axis_label_modified = 'with two additional objects')
configs['P9'] = config('P9', fname_original = 'base', fname_modified = 'plusObj',       axis_label_modified = 'with one additional object')


configs['F1'] = config('F1', fname_original = 'base', fname_modified = 'reso2',         axis_label_modified = 'with 2 times reduced resolution')
#configs['F2'] = config('F2', fname_original = 'base', fname_modified = '30min_later',   axis_label_modified = '30 minutes later')
#configs['F2'] = config('F2', fname_original = 'base', fname_modified = '60min_later',   axis_label_modified = '60 minutes later')
#configs['F2'] = config('F2', fname_original = 'base', fname_modified = '90min_later',   axis_label_modified = '90 minutes later')
#configs['F2'] = config('F2', fname_original = 'base', fname_modified = '720min_later',  axis_label_modified = '12 hours later')
configs['F2'] = config('F2', fname_original = 'base', fname_modified ='131400min_later',axis_label_modified = '6 months later')
configs['F3'] = config('F3', fname_original = 'base', fname_modified = 'smaller10',     axis_label_modified = 'when image reduced by 10 pixel')
configs['F4'] = config('F4', fname_original = 'base', fname_modified = 'shift10',       axis_label_modified = 'region shifted by 10 pixels')

configs['E1'] = config('E1', fname_original = 'base', fname_modified = 'shuffled',      axis_label_modified = 'random shuffle')


