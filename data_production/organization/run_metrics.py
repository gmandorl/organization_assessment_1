import numpy as np

from objects import *
import metrics
import matplotlib.pyplot as plt





def run_metrics (image) :

    objects          = make_objects(image)   # class containing regions and polynoms
    pairs_of_objects = make_pairs(objects)   # class containing all pairs of objects


    #plt.imshow(image)
    #plt.imshow(objects.labeled)
    #plt.show()

    image_size = image.size

    properties = dict()
    properties['area']      = objects.area_skm
    properties['area_spg']  = objects.area_spg
    properties['number']    = objects.number_of_objects

    properties['Iorg']      = metrics.Iorg(pairs_of_objects, image_size=image_size)
    properties['SCAI']      = metrics.SCAI(pairs_of_objects, image_size=image_size)
    properties['MCAI']      = metrics.MCAI(pairs_of_objects, image_size=image_size)
    properties['COP']       = metrics.COP(pairs_of_objects)
    properties['ABCOP']     = metrics.ABCOP(pairs_of_objects, image_size=image_size)
    properties['ROME']      = metrics.ROME(pairs_of_objects)
    properties['MICA']      = metrics.MICA(pairs_of_objects, image_size=image_size)
    properties['NN_center'] = metrics.NN_center(pairs_of_objects)
    properties['NN_edge']   = metrics.NN_edge(pairs_of_objects)



    properties['ROME_norm'] = properties['ROME'] / properties['area'] * properties['number']
    properties['mean_area'] = properties['area'] / properties['number']

    return properties


