# this modules apply morphological manipulations on local vascular geometries and generate vtp mesh
import numpy as np
import math


def to_numpy(lists):
	return [np.array(one_list,dtype=np.float32) for one_list in lists]
def to_lists_2d(arr):
	return [[float(c) for c in b] for b in arr]
def vary_points_test(center,outer_points,scale_factor):
	center,outer_points                 = to_numpy([center,outer_points])
	dists,unit_vectors                  = get_dists_unit_vectors_test(center,outer_points)
	new_points                          = radial_expansion_test(center,outer_points,dists,unit_vectors,scale_factor)
	new_points                          = to_lists_2d(new_points)
	return new_points
def sigmoid(scale_factor,number_of_contours,current_contour_number):
	# L : amplituded must be between indicating diameter reduction (between 0 and one) or expantion ratio (larger than one)
	L                                   = scale_factor
	# k : steepness (-1 to zero is smooth, 0 is logistic default function, and 0 to 1 is sharp 
	k                                   = 1 
	# x : current disrtance from the left end
	x                                   = current_contour_number
	# x0: x at 50% drop used to include longitudinal asymetry of how close to the narrwoing the 50% drop is current assumtion is scaled range of 12 woth 50% happening at 6
	x50                                 = 0.3				
	x0                                  = number_of_contours * x50
	
	print(x-x0)
	if scale_factor < 1:
		# contraction
		temp                            = 1 - (L / (1 + math.exp(-k*(x-x0))))
	else:
		# explantion
		temp                            = 1 + ((L-1) / (1 + math.exp(-k*(x-x0))))
	return temp 
def scale_factor_insert(scale_factor,scale_factor_local,start_id,stop_id):
	indx_counter = 0
	for sid in range(len(scale_factor)-1):
		if sid > (start_id -1):
			if sid < stop_id-1:
				scale_factor[sid]           = scale_factor_local[indx_counter]
				indx_counter            += 1
			else:
				scale_factor[sid]		= 1
		else:
			scale_factor[sid]			= 1
	print("number of updated contours: {0:d}".format(indx_counter))
	return scale_factor
def scale_factor_test(number_of_contours,length_id,maximum_diameter_change,asymetry_coef,location_id):
	scale_factor                        = []
	for i in range(number_of_contours): scale_factor.append(float(1))
	if (length_id % 2 !=0): 
		length_id -=1
	half_num                        = int(length_id/2)
	center_id                       = location_id
	start_id                        = center_id - half_num
	stop_id                         = start_id + length_id
	center_dislocation              = int(half_num * asymetry_coef)
	center_id                       = center_id + center_dislocation
	number_of_proximal_contours     = center_id - start_id
	number_of_distal_contours       = stop_id - center_id
	print("Start ID: {0:d}".format(start_id))
	print("Center ID: {0:d}".format(center_id))
	print("Stop ID: {0:d}".format(stop_id))
	prox_scale_factors              = []
	dist_scale_factors              = []
	print("Total contour numbers: {0:d}".format(number_of_contours))
	print("Total modified contours: {0:d}".format(length_id))
	print("Proximal contour numbers: {0:d}".format(number_of_proximal_contours))
	print("Distal contour numbers: {0:d}".format(number_of_distal_contours))
	for i in range(number_of_proximal_contours):
		prox_scale_factors.append(sigmoid(maximum_diameter_change,number_of_proximal_contours,i+1))
	for s in range(number_of_distal_contours):
		dist_scale_factors.append(sigmoid(maximum_diameter_change,number_of_distal_contours,s))
	# sort the scale lists
	dist_scale_factors                       = np.sort(dist_scale_factors)
	# sort in descending order
	# dist_scale_factors                     = np.sort(dist_scale_factors)[::-1] 
	print("Proximal scale factor list:")
	print(prox_scale_factors)
	print("Distal scale factor list:")
	print(dist_scale_factors)
	scale_factor_local                  	= np.concatenate((prox_scale_factors,dist_scale_factors),axis=None)
	indx_counter                        	= 0
	scale_factor				= scale_factor_insert(scale_factor,scale_factor_local,start_id,stop_id)
	return scale_factor
def radial_expansion_test(center,new_outer_points,dists,unit_vectors,scale_factor):
	temp_outer_points                   = new_outer_points.copy()
	new_dists                           = dists * scale_factor
	new_points                          = unit_vectors * new_dists[...,np.newaxis] + center
	return new_points
def get_dists_unit_vectors_test(center,new_outer_points):
	dists = np.linalg.norm(new_outer_points-center,axis=-1)
	unit_vectors = (new_outer_points-center)/ dists[...,np.newaxis]
	return dists,unit_vectors
