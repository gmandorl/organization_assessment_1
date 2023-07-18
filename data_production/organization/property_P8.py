import numpy as np
#import matplotlib.pyplot as plt
from objects import *
import copy
from scipy import ndimage
from property_P9 import modify_image as modify_image_P9


label      = 'P8'
fname_out  = 'P8'

cases = dict()
cases['base']     = 0
cases['plus2Obj'] = 1


def modify_image ( *args ) :
    image = args[0]
    n     = args[1]

    if n!=0 :
        image = modify_image_P9(image, n)
        image = modify_image_P9(image, n)


    return image
