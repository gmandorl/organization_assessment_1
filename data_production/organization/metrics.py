import numpy as np
import math
import scipy as sp
import copy


#######################################################################################
######################################### I_org #######################################
#######################################################################################

def Iorg(pairs_of_objects, image_size = 1):
    """Iorg according to [Tompkins et al. 2017]"""

    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan


    #distances = np.array(all_pairs.get_distance_regions())
    dist_min = np.nanmin(pairs_of_objects.distance_centroids, axis=1)


    # the theoretical Weibull-distribution for n particles
    u_dist_min, u_dist_min_counts = np.unique(dist_min, return_counts=True)
    lamda = pairs_of_objects.number_of_objects / image_size
    weib_cdf = 1 - np.exp(- lamda * math.pi * u_dist_min**2)


    # the CDF from the actual data
    data_cdf = np.cumsum(u_dist_min_counts / np.sum(u_dist_min_counts))
    #print("\n\n data_cdf \n", type(data_cdf), data_cdf)

    # compute the integral between Weibull CDF and data CDF
    weib_cdf = np.append(0, weib_cdf   )
    weib_cdf = np.append(   weib_cdf, 1)
    data_cdf = np.append(0, data_cdf   )
    data_cdf = np.append(   data_cdf, 1)
    #print("\n\n da integrare \n", weib_cdf, data_cdf)

    return sp.integrate.trapz(data_cdf, weib_cdf)



#######################################################################################
###############################  Radar Organisation MEtric  ###########################
#######################################################################################


def ROME(pairs_of_objects):
    """ROME according to [Retsch et al. 2020]"""

    if   pairs_of_objects.objects.number_of_objects<1  :  return np.nan
    elif pairs_of_objects.objects.number_of_objects==1 :  return pairs_of_objects.objects.area_skm

    #area_1 = np.tile(pairs_of_objects.objects.areas, (pairs_of_objects.number_of_objects,1) )
    #area_2 = area_1.T
    area_1 = pairs_of_objects.objects.areas
    area_2 = pairs_of_objects.objects.areas[:,None] #transpose the vector

    large_area = np.fmax(area_1, area_2).astype(float)
    small_area = np.fmin(area_1, area_2).astype(float)

    np.fill_diagonal(large_area, np.nan)
    np.fill_diagonal(small_area, np.nan)


    return np.nanmean(large_area + np.fmin(small_area, (small_area / pairs_of_objects.distance_edges)**2))



#######################################################################################
##############################  Distances Nearest Neighbor  ###########################
#######################################################################################

def NN_center(pairs_of_objects) :
    """distance between centers of Nearest Neighbors"""
    if pairs_of_objects.objects.number_of_objects<2 : return np.nan

    dist_min = np.nanmin(pairs_of_objects.distance_centroids, axis=1)
    return np.mean(dist_min)

def NN_edge(pairs_of_objects) :
    """distance between edges of Nearest Neighbors"""
    if pairs_of_objects.objects.number_of_objects<2 : return np.nan

    dist_min = np.nanmin(pairs_of_objects.distance_edges, axis=1)
    return np.mean(dist_min)



#######################################################################################
########################## Convective Organization Potential ##########################
#######################################################################################

def COP(pairs_of_objects):
    """The Convective Organisation Potential according to [White et al. 2018]"""
    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan

    diameter_1 = pairs_of_objects.objects.diameters
    diameter_2 = pairs_of_objects.objects.diameters[:,None] #transpose the vector
    v = np.array(0.5 * (diameter_1 + diameter_2) / pairs_of_objects.distance_centroids)
    return np.nansum(v) / pairs_of_objects.number_of_combinations




#######################################################################################
#################### Area Based Convective Organisation Potential #####################
#######################################################################################

def ABCOP(pairs_of_objects, image_size=1):
    """The Area Based Convective Organisation Potential according to [ ??? 2022]"""
    if pairs_of_objects.objects.number_of_objects<1 :
        return np.nan
    if pairs_of_objects.objects.number_of_objects==1 :
        density = pairs_of_objects.objects.areas[0] / image_size
        return math.pi**0.5 / 2 * density / (2-density**0.5)

    areas_1 = pairs_of_objects.objects.areas
    areas_2 = pairs_of_objects.objects.areas[:,None]

    #distances = copy.deepcopy(pairs_of_objects.distance_edges)   # distances using edges with skimage
    diameter_1 = pairs_of_objects.objects.diameters
    diameter_2 = pairs_of_objects.objects.diameters[:,None] #transpose the vector
    distances = np.maximum(1, pairs_of_objects.distance_centroids - 0.5 * (diameter_1 + diameter_2) )
    np.fill_diagonal(distances, np.nan)

    V_area = 0.5 * (areas_1 + areas_2) / distances
    ABCOP = np.sum(np.nanmax(V_area, axis=0))

    return ABCOP




#######################################################################################
######################  Simple Convective Aggregation Metric  #########################
#######################################################################################

def SCAI(pairs_of_objects, image_size = 1):
    """SCAI according to [Tobin et al. 2013]"""
    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan


    d_0 = np.exp( np.nansum( np.log(pairs_of_objects.distance_centroids)) / pairs_of_objects.number_of_combinations )
    return pairs_of_objects.number_of_objects / (image_size**1.5) * d_0 * 1000



#######################################################################################
#################  Morphological Index of  Convective Aggregation  ####################
#######################################################################################

def MICA(pairs_of_objects, image_size = 1):
    """MICA according to [Kadoya et Masunaga 2018]"""


    if pairs_of_objects.objects.number_of_objects==0 :
        return np.nan

    objects = pairs_of_objects.objects
    regions = objects.regions

    min_row = np.min([r.bbox[0]     for r in regions])
    min_col = np.min([r.bbox[1]     for r in regions])
    max_row = np.max([r.bbox[2]     for r in regions])
    max_col = np.max([r.bbox[3]     for r in regions])

    Acls = (max_row - min_row) * (max_col - min_col)
    MICA = 1.* ( objects.area_skm / Acls ) * ( image_size - Acls ) / image_size

    #print('MICA ', MICA, (max_row - min_row), (max_col - min_col), image_size)
    return MICA



#######################################################################################
#################  Morphological Index of  Convective Aggregation  ####################
#######################################################################################

def MCAI(pairs_of_objects, image_size = 1):
    """MCAI according to [Xu et al. 2018]"""
    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan

    objects = pairs_of_objects.objects
    diameter_1 = pairs_of_objects.objects.diameters
    diameter_2 = pairs_of_objects.objects.diameters[:,None] #transpose the vector
    v = np.array(0.5 * (diameter_1 + diameter_2) / pairs_of_objects.distance_centroids)

    d2 = np.maximum(0, pairs_of_objects.distance_centroids - 0.5 * (diameter_1 + diameter_2) )
    d2 = np.nansum(d2) * 0.5 # 0.5 is needed to avoid double counting
    L = math.sqrt(image_size)

    # correction of characteristic length
    max_edges_x = objects.centroids[:,0] + 0.5*objects.diameters
    min_edges_x = objects.centroids[:,0] - 0.5*objects.diameters
    max_edges_y = objects.centroids[:,1] + 0.5*objects.diameters
    min_edges_y = objects.centroids[:,1] - 0.5*objects.diameters

    L_x = np.max(max_edges_x) - np.min(min_edges_x)
    L_y = np.max(max_edges_y) - np.min(min_edges_y)
    L = np.max([L, L_x, L_y])
    #print('MCAI', L, pairs_of_objects.objects.number_of_objects)


    MCAI = objects.number_of_objects * d2 * 1000 * 2 / L**3
    return MCAI



