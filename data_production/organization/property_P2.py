import numpy as np



label = 'P2'

folder_out = 'P2'
fname_out  = 'P2'

cases = dict()
#cases[f'base'] = 0
#for n in range(1,11) :
    #cases[f'shift{n}'] = n
for n in range(11,21) :
    cases[f'shift{n}'] = n

def modify_image ( *args ) :
    image = args[0]
    n     = args[1]

    sh    = image.shape
    to_add = np.zeros((sh[0],50))
    to_add[int((sh[0]+1)/2)-5:int((sh[0]+1)/2)+5,1:n+11] = 1

    image_to_return = np.concatenate((image, to_add), axis=1)
    return image_to_return
