


label='GOESE'

path = '/bdd/MEGHA_TROPIQUES/GOES-E/GRID004.v2.00/'
var_name = 'brightness_temperature'
cut = 21000 #units are 100*K
cut_reversed = True


# shape (375, 376) if 15x15
# shape (125, 126) if 5x5
#lat_min = 5
#lat_max = 0
#lon_min = 145
#lon_max = 150



# shape (240, 240) if 9.6 x 9.6
#lat_min = 9.6
#lat_max = 0
lat_min = 8.4
lat_max = -1.2
lon_min = -39.6
lon_max = -30


import numpy as np

def preprocessing(image) :
    sh = image.shape
    image_to_return = image.reshape(int(sh[0]/2), 2, int(sh[1]/2), 2)
    image_to_return = np.nanmean(image_to_return, axis=(1,3))
    return image_to_return


