"""
This file is needed because P2 hqs execution time too big.
It contains the same configuration of P2, but it run different cases
"""

import numpy as np
from property_P2 import modify_image as modify_image_P2


label      = 'P2'
fname_out  = 'P2'

cases = dict()
for n in range(20,39) :
    cases[f'shift{n}'] = n


def modify_image ( *args ) :
    return modify_image_P2 ( *args )
