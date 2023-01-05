import numpy as np
from objects import *
import copy
import matplotlib.pyplot as plt

label = 'P3'

folder_out = 'P3'
fname_out  = 'P3'

cases = dict()
#cases['base']    = 0
cases['mergedObj'] = 1


def modify_image ( *args ) :
    image = args[0]
    n     = args[1]


    objects_original           = make_objects(image)   # class containing regions and polynoms
    pairs_of_objects_original  = make_pairs(objects_original)   # class containing all pairs of objects

    area_spg_original   = objects_original.area_skm
    numb_original       = objects_original.number_of_objects

    distances = copy.deepcopy(pairs_of_objects_original.distance_edges)
    np.fill_diagonal(distances, np.nan)
    sh    = image.shape

    if np.nanmin(distances)!= 1 :
        new_image = np.zeros((sh[0],sh[1]))
        return new_image
    if n==0 : return image

    labeled = objects_original.labeled

    empty_close_to_two_objects_1 = image[0:-2,1:-1] + image[2:,1:-1] - image[1:-1,1:-1]
    empty_close_to_two_objects_2 = image[1:-1,0:-2] + image[1:-1,2:] - image[1:-1,1:-1]
    empty_weighted_1 = labeled[0:-2,1:-1] - labeled[2:,1:-1]
    empty_weighted_2 = labeled[1:-1,0:-2] - labeled[1:-1,2:]
    candidates = np.where((empty_close_to_two_objects_1 == 2) & (empty_weighted_1!=0), 1, 0) +                 np.where((empty_close_to_two_objects_2 == 2) & (empty_weighted_2!=0), 1, 0)


    # check plot
    #fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(14,8))
    #axs[0,2].imshow(image[1:-1,1:-1] + 2*candidates)
    #axs[1,2].imshow(empty_weighted_1[1:-1,1:-1] )
    #axs[0,0].imshow(image[1:-1,1:-1])
    #axs[1,0].imshow(candidates)
    #axs[0,1].imshow(empty_close_to_two_objects_1)
    #axs[1,1].imshow(empty_close_to_two_objects_2);plt.show()
    candidate_indices = np.where(candidates>0)
    print(candidate_indices[0], candidates[candidate_indices])
    image_to_return = image
    image_to_return[candidate_indices[0][0]+1,candidate_indices[1][0]+1] =1

    objects_new           = make_objects(image)   # class containing regions and polynoms

    area_spg_new   = objects_new.area_skm
    numb_new       = objects_new.number_of_objects

    print('check\t', area_spg_new-area_spg_original, ' \t', numb_new-numb_original)
    #return np.zeros(image.shape)




    to_add = np.zeros((sh[0],2))
    to_add[int((sh[0]+1)/2),1] = n

    image_to_return = np.concatenate((image, to_add), axis=1)
    return image_to_return
