import numpy as np


label      = 'P1'
fname_out  = 'P1'

cases = dict()
cases['base']    = 0
cases['plusObj'] = 1


def modify_image ( *args ) :
    image = args[0]
    n     = args[1]


    sh    = image.shape
    to_add = np.zeros((sh[0],2))
    to_add[int((sh[0]+1)/2),1] = n

    image_to_return = np.concatenate((image, to_add), axis=1)
    return image_to_return
