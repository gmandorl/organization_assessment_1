import numpy as np



label      = 'F3'
fname_out  = 'F3'

cases = dict()
cases[f'base'] = 0
for n in range(1,11) :
    cases[f'smaller{n}'] = n


def modify_image ( *args ) :
    image = args[0]
    n     = args[1]


    image_to_return = image
    if n!=0 : image_to_return = image_to_return[n:-n, n:-n]
    return image_to_return
