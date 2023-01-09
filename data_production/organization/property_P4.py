import numpy as np
import matplotlib.pyplot as plt
from objects import *
import copy
from scipy import ndimage


label      = 'P4'
fname_out  = 'P4'

cases = dict()
cases['base']    = 0
cases['biggerObj'] = 1


def modify_image ( *args ) :
    image = args[0]
    n     = args[1]


    if n!=0 :
        filled_im           = ndimage.binary_fill_holes(image).astype(int)  # fill holes
        #objects_original    = make_objects(filled_im)   # class containing regions and polynoms


        borders_in_row        = np.empty((image.shape[0]-2, image.shape[1]-2, 9))
        borders_in_row[:,:,0] = filled_im [0:-2, 0:-2]
        borders_in_row[:,:,1] = filled_im [0:-2, 1:-1]
        borders_in_row[:,:,2] = filled_im [0:-2, 2:  ]
        borders_in_row[:,:,3] = filled_im [1:-1, 2:  ]
        borders_in_row[:,:,4] = filled_im [2:  , 2:  ]
        borders_in_row[:,:,5] = filled_im [2:  , 1:-1]
        borders_in_row[:,:,6] = filled_im [2:  , 0:-2]
        borders_in_row[:,:,7] = filled_im [1:-1, 0:-2]
        borders_in_row[:,:,8] = filled_im [0:-2, 0:-2]

        borders_changes = np.sum((np.diff(borders_in_row)!=0), axis=2)
        borders_total   = np.sum(borders_in_row, axis=2)



        idx_edges = np.argwhere((borders_changes==2) & (borders_total<7) & (filled_im[1:-1,1:-1]==0))
        N = idx_edges.shape[0]



        if idx_edges.shape[0]==0 :  return image
        else :
            nth_candidate = np.random.randint(N)
            idx1 = idx_edges[nth_candidate][0]+1
            idx2 = idx_edges[nth_candidate][1]+1
            #print('INDICES: ', idx1, idx2, iterator, N)

            image_to_return = copy.deepcopy(image)
            image_to_return[idx1,idx2]=1
            objects_plus1  = make_objects(image_to_return)

            ####check plot
            #fig, axs = plt.subplots(ncols=3, figsize=(14,5))
            #axs[0].imshow(filled_im[1:-1,1:-1])
            #axs[1].imshow(image)
            #axs[2].imshow(2*image_to_return - image)
            #plt.show()

            return image_to_return


    return image
