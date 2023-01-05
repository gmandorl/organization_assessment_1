import numpy as np
import matplotlib.pyplot as plt
from objects import *
import copy

label = 'P4'

folder_out = 'P4'
fname_out  = 'P4'

cases = dict()
cases['base']    = 0
cases['biggerObj'] = 1


def modify_image ( *args ) :
    image = args[0]
    n     = args[1]


    if n!=0 :
        objects_original  = make_objects(image)   # class containing regions and polynoms
        area_spg_original   = objects_original.area_spg
        numb_original       = objects_original.number_of_objects

        not_added = True

        inner_im = image[1:-1,1:-1] + image[0:-2,1:-1] + image[2:,1:-1] + image[1:-1,0:-2] + image[1:-1,2:]
        idx_edges = np.argwhere((inner_im==1) & (image[1:-1,1:-1]==0))
        N = idx_edges.shape[0]
        #print(N, idx_edges[0], idx_edges[1])
        if idx_edges.shape[0]>0 :
            iterator=0
            while not_added and iterator<N:
                #print('condition', not_added, iterator<N, not_added and iterator<N)
                iterator=iterator+1
                nth_candidate = np.random.randint(N)
                idx1 = idx_edges[nth_candidate][0]+1
                idx2 = idx_edges[nth_candidate][1]+1
                #print('INDICES: ', idx1, idx2, iterator)

                image_tmp = copy.deepcopy(image)
                image_tmp[idx1,idx2]=1
                objects_plus1  = make_objects(image_tmp)

                if area_spg_original < objects_plus1.area_spg and numb_original ==  objects_plus1.number_of_objects:
                    image[idx1,idx2]=2
                    not_added=False




        #plt.imshow(image)
        #plt.show()



    return image
