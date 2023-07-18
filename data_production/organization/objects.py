import numpy as np
import skimage.measure as skm
import shapely.geometry as spg
from scipy import ndimage





#######################################################################################
################### class containing all the regions and polynoms #####################
#######################################################################################

class make_objects :

    def __init__(self, image):
        "Create the regions and polynoms, they have the same order"

        image    = ndimage.binary_fill_holes(image).astype(int)  # fill holes
        labeled  = skm.label(image, background=0 , connectivity=2) #connect also in diagonal (default is 1)
        regions  = skm.regionprops(labeled)


        polynoms = []
        for r in regions:
            bounds = r.bbox
            y_length = bounds[2] - bounds[0]
            x_length = bounds[3] - bounds[1]
            # prepare bed to put layout in
            bed = np.zeros(shape=(y_length + 2, x_length + 2))
            bed[1:-1, 1:-1] = r.image.astype(int)
            # get the contour needed for shapely
            contour = skm.find_contours(bed, level=0.5, fully_connected='high')
            # increase coordinates to get placement inside of original input array right
            contour[0][:, 0] += bounds[0]  # increase y-values
            contour[0][:, 1] += bounds[1]  # increase x-values

            m_poly = spg.Polygon(contour[0])
            polynoms.append(m_poly)




        ##I need these nested loop to remove holes in objects and to eventual other objects inside
        #for n in range(len(polynoms)-1, -1, -1) :
            #for m in range(len(polynoms)-1, n, -1) :
                #if polynoms[n].distance(polynoms[m]) == 0 :
                    #if polynoms[n].area > polynoms[m].area :
                        #del polynoms[m]
                        #del regions[m]
                    #else :
                        #del polynoms[n]
                        #del regions[n]


        self.labeled  = labeled # saved to be drawn in run_metrics
        self.regions  = regions
        self.polynoms = polynoms

        self.area_skm  =   np.sum([r.area     for r in self.regions ])
        self.area_spg  =   np.sum([p.area+0.5 for p in self.polynoms]) # +0.5 is needed because of the shape of spg.Polygon
        self.areas     = np.array([r.area     for r in self.regions])  # I will use these in the metrics
        self.centroids = np.array([r.centroid for r in self.regions])
        self.diameters = np.array([r.equivalent_diameter     for r in self.regions])
        self.perimeters= np.array([p.length for p in self.polynoms]) # +0.5 is needed because of the shape of spg.Polygon

        self.number_of_objects = len(self.polynoms)









#######################################################################################
############### class containing the list of all the pairs of objects #################
#######################################################################################

class make_pairs:

    def __init__(self, objects):
        self.objects = objects
        self.number_of_objects      = objects.number_of_objects
        self.number_of_combinations = objects.number_of_objects * (objects.number_of_objects-1) / 2


        self.compute_distance_centroids ()
        self.compute_distance_edges ()




    def compute_distance_centroids (self) :
        centroids = self.objects.centroids
        xs  = np.array([c[1] for c in centroids])
        ys  = np.array([c[0] for c in centroids])

        # compute the distances
        dist_x = xs - xs[:,None]
        dist_y = ys - ys[:,None]
        distances =  np.sqrt(dist_x**2 + dist_y**2)
        np.fill_diagonal(distances, np.nan)  # it is inplace
        self.distance_centroids = distances

        # compute the nearest neighbour distance
        self.dist_min = np.nanmin(distances, axis=0) if self.number_of_objects > 1 else np.nan


    def compute_distance_edges (self) :
        distance_edges = np.empty((self.number_of_objects, self.number_of_objects))
        for n in range(self.number_of_objects) :
            for m in range(n) :
                distance_edges[m,n] = self.objects.polynoms[n].distance(self.objects.polynoms[m])
                distance_edges[n,m] = distance_edges[m,n]
                #if distance_edges[n,m]==0 : print('WARNING: distance between edges is zero')
        np.fill_diagonal(distance_edges, np.nan)
        self.distance_edges =  distance_edges









