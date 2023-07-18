

label='HIMAWARI_210'


path = '/bdd/MEGHA_TROPIQUES/HIMAWARI/GRID004.v2.00/'
var_name = 'brightness_temperature'
cut = 21000 #units are 100*K
cut_reversed = True

## shape (375, 376) if 15x15
#lat_min = 5
#lat_max = 0
#lon_min = 145
#lon_max = 150

# shape (240, 240) if 9.6 x 9.6
lat_min = 9.6
lat_max = 0
lon_min = 140.4
lon_max = 150


import numpy as np

def preprocessing(image) :  # reduce resolution to 0.008 degree
    sh = image.shape
    image_to_return = image.reshape(int(sh[0]/2), 2, int(sh[1]/2), 2)
    image_to_return = np.nanmean(image_to_return, axis=(1,3))
    return image_to_return

