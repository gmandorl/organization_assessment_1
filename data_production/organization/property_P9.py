import numpy as np
#import matplotlib.pyplot as plt
from objects import *
import copy

label = 'P9'

folder_out = 'P9'
fname_out  = 'P9'

cases = dict()
cases['base']    = 0
cases['plusObj'] = 1


def modify_image ( *args ) :
    image = args[0]
    n     = args[1]


    if n!=0 :
        objects_original  = make_objects(image)   # class containing regions and polynoms
        number_original   = objects_original.number_of_objects

        added = False
        while not added :
            idx1 = np.random.randint(image.shape[0])
            idx2 = np.random.randint(image.shape[1])
            #print('INDICES: ', idx1, idx2, added)
            if np.sum(image[max(idx1-1,0):min(idx1+1,image.shape[0]-1),
                            max(idx2-1,0):min(idx2+1,image.shape[1]-1)])==0 :

                image_tmp = copy.deepcopy(image)
                image_tmp[idx1,idx2]=1
                objects_plus1  = make_objects(image_tmp)
                if number_original < objects_plus1.number_of_objects :
                    image[idx1,idx2]=2
                    added=True


        #plt.imshow(image)
        #plt.show()


    return image
