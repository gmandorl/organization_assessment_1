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
    #print(image.shape)

    properties = dict()
    properties['area']      = objects.area_skm
    #properties['area_spg']  = objects.area_spg
    properties['number']    = objects.number_of_objects

    properties['Iorg']      = metrics.Iorg(pairs_of_objects, image_size=image_size)
    properties['Iorg_recommended']      = properties['Iorg'] if properties['area'] < 0.1 * image_size else np.nan
    #properties['Iorg_Giovanni']      = metrics.Iorg_Giovanni(image)

    #properties['Iorg2']     = metrics.Iorg2(pairs_of_objects, image_size=image_size)
    properties['Lorg']      = metrics.Lorg(pairs_of_objects, image_size=image_size)


    properties['SCAI']      = - metrics.SCAI(pairs_of_objects, image_size=image_size)
    properties['MCAI']      = - metrics.MCAI(pairs_of_objects, image_size=image_size)


    properties['COP']       = metrics.COP(pairs_of_objects)
    properties['ABCOP']     = metrics.ABCOP(pairs_of_objects, image_size=image_size)
    properties['ROME']      = metrics.ROME(pairs_of_objects)
    properties['MICA']      = metrics.MICA(pairs_of_objects, image_size=image_size)
    properties['Ishape']    = metrics.Ishape(pairs_of_objects)

    properties['NN_center'] = metrics.NN_center(pairs_of_objects)
    properties['OIDRA'] = metrics.OIDRA(pairs_of_objects, image_size=image_size)


    # derived variables
    properties['ROME_norm']  = properties['ROME'] / properties['area'] * properties['number']
    properties['mean_area']  = properties['area'] / properties['number']
    #properties['ROME_delta'] = properties['ROME'] - properties['mean_area']

    # set to NAN all the metrics when N=1 (23% of the events, 1.5% of the events for P3)
    if properties['number'] <= 1 :
        properties['Iorg']      = np.nan
        #properties['Iorg_Giovanni']      = np.nan
        properties['Lorg']      = np.nan
        properties['SCAI']      = np.nan
        properties['MCAI']      = np.nan
        properties['COP']       = np.nan
        properties['ABCOP']     = np.nan
        properties['ROME']      = np.nan
        properties['ROME_norm'] = np.nan
        properties['MICA']      = np.nan
        properties['Ishape']    = np.nan
        properties['OIDRA'] = np.nan





    # store to compare with anomalies and percentiles
    properties['area_original']      = properties['area']
    properties['number_original']    = properties['number']

    return properties


