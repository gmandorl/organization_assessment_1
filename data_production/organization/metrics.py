import numpy as np
import math
import scipy as sp
from scipy import special
import copy


#######################################################################################
######################################### I_org #######################################
#######################################################################################

def Iorg(pairs_of_objects, image_size = 1):
    """Iorg according to [Tompkins et al. 2017]"""

    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan

    ## Weger et al. 1992 states that Iorg is not valid for total area > 10% of the image -> not applied here
    #if np.sum(pairs_of_objects.objects.areas) > 0.10 * image_size :
        #return np.nan



    #dist_min = np.nanmin(pairs_of_objects.distance_centroids, axis=1)
    dist_min = pairs_of_objects.dist_min


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


    #return sp.integrate.trapz(data_cdf, weib_cdf)  # DO NO USE trapz ! trapz return always >0.5 for N=2
    integral = np.sum ( data_cdf[:-1] * ( weib_cdf[1:] - weib_cdf[:-1] ) )
    return integral



#######################################################################################
######################################### L_org #######################################
#######################################################################################

def Lorg(pairs_of_objects, image_size = 1):
    """Lorg according to [Biagioli et al. 2023]"""

    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan

    Lorg = 0

    return Lorg


#######################################################################################
######################################## I_org 2 ######################################
#######################################################################################

def Iorg2(pairs_of_objects, image_size = 1):
    """Iorg according to [Tompkins et al. 2017]"""

    if pairs_of_objects.objects.number_of_objects<3 :
        return np.nan

    # Weger et al. 1992 states that Iorg is not valid for total area > 10% of the image
    if np.sum(pairs_of_objects.objects.areas) > 0.10 * image_size :
        return np.nan


    # distances from objects
    distance_centroids = pairs_of_objects.distance_centroids
    dist_NN            = pairs_of_objects.dist_min

    # compute second nearest distance
    dist_minus_NN  = distance_centroids - dist_NN
    dist_SNN       = np.nanmin(np.where(dist_minus_NN==0, np.nan, dist_minus_NN), axis=0)
    dist_SNN       = dist_SNN + dist_NN



    # the theoretical Weibull-distribution for n particles
    u_dist_SNN, u_dist_SNN_counts = np.unique(dist_SNN, return_counts=True)
    lamda = pairs_of_objects.number_of_objects / image_size
    mand_cdf = 1 - np.exp(- lamda * math.pi * u_dist_SNN**2) * ( 1 + lamda * math.pi * u_dist_SNN**2 )

    # the CDF from the actual data
    data_cdf = np.cumsum(u_dist_SNN_counts / np.sum(u_dist_SNN_counts))


    # compute the integral between theoretical CDF and data CDF
    mand_cdf = np.append(0, mand_cdf   )
    mand_cdf = np.append(   mand_cdf, 1)
    data_cdf = np.append(0, data_cdf   )
    data_cdf = np.append(   data_cdf, 1)

    integral = np.sum ( data_cdf[:-1] * ( mand_cdf[1:] - mand_cdf[:-1] ) )
    return integral



#######################################################################################
###############################  Radar Organization MEtric  ###########################
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

    dist_min = pairs_of_objects.dist_min
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
    """The Convective Organization Potential according to [White et al. 2018]"""
    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan

    diameter_1 = pairs_of_objects.objects.diameters
    diameter_2 = pairs_of_objects.objects.diameters[:,None] #transpose the vector
    v = np.array(0.5 * (diameter_1 + diameter_2) / pairs_of_objects.distance_centroids)
    return np.nansum(v) / pairs_of_objects.number_of_combinations




#######################################################################################
#################### Area Based Convective Organization Potential #####################
#######################################################################################

def ABCOP(pairs_of_objects, image_size=1):
    """The Area Based Convective Organization Potential according to [ Jin et al. 2022]"""
    if pairs_of_objects.objects.number_of_objects<1 :
        return np.nan
    if pairs_of_objects.objects.number_of_objects==1 :
        density = pairs_of_objects.objects.areas[0] / image_size
        return math.pi**0.5 / 2 * density / (2-density**0.5)

    areas_1 = pairs_of_objects.objects.areas
    areas_2 = pairs_of_objects.objects.areas[:,None]


    diameter_1 = pairs_of_objects.objects.diameters
    diameter_2 = pairs_of_objects.objects.diameters[:,None] #transpose the vector
    distances = np.maximum(1, pairs_of_objects.distance_centroids - 0.5 * (diameter_1 + diameter_2) )
    np.fill_diagonal(distances, np.nan)

    V_area = 0.5 * (areas_1 + areas_2) / distances / image_size**0.5
    ABCOP = np.sum(np.nanmax(V_area, axis=0))

    return ABCOP




#######################################################################################
######################  Simple Convective Aggregation Metric  #########################
#######################################################################################

def SCAI(pairs_of_objects, image_size = 1):
    """SCAI according to [Tobin et al. 2013]"""
    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan#, np.nan


    d_0  = np.exp( 0.5 * np.nansum( np.log(pairs_of_objects.distance_centroids)) / pairs_of_objects.number_of_combinations )
    SCAI = pairs_of_objects.number_of_objects / (image_size**1.5) * d_0 * 1000 * 2 # *2 comes from Nmax

    return SCAI#, d_0



#######################################################################################
######################  Modified Convective Aggregation Metric  #######################
#######################################################################################

def MCAI(pairs_of_objects, image_size = 1):
    """MCAI according to [Xu et al. 2018]"""
    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan#, np.nan

    diameter_1 = pairs_of_objects.objects.diameters
    diameter_2 = pairs_of_objects.objects.diameters[:,None] #transpose the vector
    #v = np.array(0.5 * (diameter_1 + diameter_2) / pairs_of_objects.distance_centroids)

    d2 = np.maximum(0, pairs_of_objects.distance_centroids - 0.5 * (diameter_1 + diameter_2) )
    d2 = np.nanmean(d2)
    L = math.sqrt(image_size)


    MCAI = pairs_of_objects.objects.number_of_objects * d2 * 1000 * 2 / L**3
    return MCAI#, d2



#######################################################################################
##################  Morphological Index of Convective Aggregation  ####################
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
######################################## I_shape ######################################
#######################################################################################

def Ishape(pairs_of_objects, image_size = 1):
    """Ishape according to [Pscheidt et al. 2019]"""

    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan

    areas       = pairs_of_objects.objects.areas
    perimeters  = pairs_of_objects.objects.perimeters

    Ishape =  np.sum (areas**0.5 / perimeters) /  pairs_of_objects.objects.number_of_objects


    return Ishape


#######################################################################################
######################################### EXTRA #######################################
#######################################################################################


def OIDRA (pairs_of_objects, image_size = 1):
    """Example of organization index that satisfy all properties but P5"""
    if pairs_of_objects.objects.number_of_objects<2 :
        return np.nan

    objects   = pairs_of_objects.objects
    areas     = pairs_of_objects.objects.areas
    distances = pairs_of_objects.distance_edges


    L       = math.sqrt(image_size)
    weights = 1 - np.sqrt( 1.4142135623730951 * distances / L )
    #weights = 2*np.exp( - 1.4142135623730951 * distances / L ) - 1
    areas   = areas / np.sum(areas)


    # compute A_i * A*j * weight_ij
    coefficients = weights
    coefficients = coefficients * areas
    coefficients = (coefficients.T*areas.T).T


    new_index  = np.nansum(coefficients) + np.sum(areas*areas)


    return  new_index


