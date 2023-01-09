import numpy as np
from objects import *
import copy
import matplotlib.pyplot as plt
from scipy import ndimage


label      = 'P3'
fname_out  = 'P3'

cases = dict()
cases['base']    = 0
cases['mergedObj'] = 1


def modify_image ( *args ) :
    image = args[0]
    n     = args[1]

    if n==0 : return image

    extended_im                = np.zeros((image.shape[0]+2, image.shape[1]+2))
    extended_im[1:-1,1:-1]     = image
    extended_im                = ndimage.binary_fill_holes(extended_im).astype(int)  # fill holes
    objects_original           = make_objects(extended_im)   # class containing regions and polynoms
    pairs_of_objects_original  = make_pairs(objects_original)   # class containing all pairs of objects

    area_skm_original   = objects_original.area_skm
    numb_original       = objects_original.number_of_objects

    distances = copy.deepcopy(pairs_of_objects_original.distance_edges)
    np.fill_diagonal(distances, np.nan)

    #### condition to add a point ####
    if numb_original<2 or np.nanmin(distances)!= 1 :
        return image

    #arg_min_1d = np.nanargmin(distances)
    #i1 = int( arg_min_1d / distances.shape[1]) + 1  # position of the first  of the two close objects
    #i0 = int( arg_min_1d % distances.shape[1]) + 1  # position of the second of the two close objects
    #im_with_2_obj = np.where((labeled==i1) | (labeled==i0), 1, 0)


    labeled = objects_original.labeled



    empty_close_to_two_objects_1 = extended_im[0:-2,1:-1] + extended_im[2:,1:-1] - extended_im[1:-1,1:-1]
    empty_close_to_two_objects_2 = extended_im[1:-1,0:-2] + extended_im[1:-1,2:] - extended_im[1:-1,1:-1]
    empty_weighted_1 = labeled[0:-2,1:-1] - labeled[2:,1:-1]
    empty_weighted_2 = labeled[1:-1,0:-2] - labeled[1:-1,2:]
    candidates = np.where((empty_close_to_two_objects_1 == 2) & (empty_weighted_1!=0), 1, 0) +                 np.where((empty_close_to_two_objects_2 == 2) & (empty_weighted_2!=0), 1, 0)


    # check plot
    #fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(14,8))
    #axs[0,2].imshow(extended_im[1:-1,1:-1] + 2*candidates)
    #axs[1,2].imshow(labeled[1:-1,1:-1] )
    #axs[0,0].imshow(extended_im[1:-1,1:-1])
    #axs[1,0].imshow(candidates)
    #axs[0,1].imshow(empty_close_to_two_objects_1)
    #axs[1,1].imshow(empty_close_to_two_objects_2);plt.show()

    candidate_indices = np.where(candidates>0)
    image_to_return = image
    image_to_return[candidate_indices[0][0],candidate_indices[1][0]] =1

    objects_new           = make_objects(image_to_return)   # class containing regions and polynoms

    area_skm_new   = objects_new.area_skm
    numb_new       = objects_new.number_of_objects

    #print('check\t', area_skm_new-area_skm_original, ' \t', numb_new-numb_original)

    return image_to_return
