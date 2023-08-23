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
    domain_length = image.shape[0]
    #print(image.shape)

    properties = dict()
    properties['area']      = objects.area_skm
    #properties['area_spg']  = objects.area_spg
    properties['number']    = objects.number_of_objects

    properties['Iorg']      = metrics.Iorg(pairs_of_objects, image_size=image_size)
    #properties['Iorg_recommended']      = properties['Iorg'] if properties['area'] < 0.1 * image_size else np.nan
    #ncnv, Iorg_Giovanni      = metrics.Iorg_Giovanni(pairs_of_objects, image)
    #properties['Iorg_Giovanni']      = Iorg_Giovanni
    #properties['ncnv']      = ncnv

    #print('\n\n -------------------------------------------------------------------------\n')
    #properties['Iorg2']     = metrics.Iorg2(pairs_of_objects, image_size=image_size)
    #ncnv, Lorg_Giovanni      = metrics.Lorg_Giovanni(pairs_of_objects, image)
    #properties['Lorg_Giovanni']      = Lorg_Giovanni
    #properties['ncnv']      = ncnv
    properties['Lorg']      = metrics.Lorg(pairs_of_objects,  l_max=2.*image.shape[0],  domain_length=domain_length)
    #properties['Lorg2']     = metrics.Lorg(pairs_of_objects,  l_max=   image.shape[0],  domain_length=domain_length)
    #print('\nLorgs : ', properties['Lorg'], properties['Lorg_Giovanni'])
    #print('\nLorgs : ', properties['Lorg'] - properties['Lorg_Giovanni'])


    properties['SCAI']      = - metrics.SCAI(pairs_of_objects, image_size=image_size)
    properties['MCAI']      = - metrics.MCAI(pairs_of_objects, image_size=image_size)

    #properties['SCAI2']      = properties['SCAI']
    #properties['MCAI2']      = properties['MCAI']


    properties['COP']       = metrics.COP(pairs_of_objects)
    properties['ABCOP']     = metrics.ABCOP(pairs_of_objects, image_size=image_size)
    properties['ROME']      = metrics.ROME(pairs_of_objects)
    properties['MICA']      = metrics.MICA(pairs_of_objects, image_size=image_size)
    #properties['Ishape']    = metrics.Ishape(pairs_of_objects)
    #properties['H']         = metrics.H(image, pairs_of_objects)
    #properties['H2']         = metrics.H2(pairs_of_objects, domain_shape = image.shape)

    #properties['NN_center'] = metrics.NN_center(pairs_of_objects)
    properties['OIDRA'] = metrics.OIDRA(pairs_of_objects, image_size=image_size)


    # derived variables
    properties['ROME_norm']  = properties['ROME'] / properties['area'] * properties['number']
    properties['mean_area']  = properties['area'] / properties['number']
    properties['ROME_delta'] = properties['ROME'] - properties['mean_area']

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
        #properties['Ishape']    = np.nan
        properties['OIDRA'] = np.nan






    # store to compare with anomalies and percentiles
    properties['area_original']      = properties['area']
    properties['number_original']    = properties['number']

    return properties


