# this modules apply morphological manipulations on local vascular geometries and generate vtp mesh
import numpy as np


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

def scale_factor_test(length_id,scale_id,discrt_id,long_asym_id,num_contours,control_point_id):
    scale_factor                        = []
    for i in range(num_contours): scale_factor.append(float(1))
    # print(scale_factor)
    
    
    tmp_len_id                          = length_id
    if (length_id % 2 !=0): 
        tmp_len_id -=1
    half_num                        = int(tmp_len_id/2)
    center_id                       = control_point_id
    start_id                        = center_id - half_num
    stop_id                         = start_id + length_id
    long_asym_dislocation           = int(half_num * long_asym_id)
    center_id                       = center_id + long_asym_dislocation
    prox_cont_num                   = center_id - start_id
    dist_cont_num                   = stop_id - center_id
    prox_scale_list                 = []
    dist_scale_list                 = []
    print("Total contour numbers: {0:d}".format(num_contours))
    print("Proximal contour numbers: {0:d}".format(prox_cont_num))
    print("Distal contour numbers: {0:d}".format(dist_cont_num))
    # discrete_id (values between 0 and 1) defines how fast area drops, however currently method is limited only to 0.5 and other values cause deviation from scale_id 
    discrt_id                           = 0.5                     
    coef_a                              = 1
    common_ratio                        = np.power((0.5*scale_id/discrt_id),(1/(prox_cont_num-1)))
    for i in range(prox_cont_num): prox_scale_list.append(float(coef_a*common_ratio**i))
    common_ratio                        = np.power((0.5*scale_id/discrt_id),(1/(dist_cont_num-1)))
    for i in range(dist_cont_num): dist_scale_list.append(float(coef_a*common_ratio**i))
    dist_scale_list                     = np.sort(dist_scale_list)
    # sort in descending order
    # dist_scale_list                     = np.sort(dist_scale_list)[::-1] 
    print(prox_scale_list)
    print(dist_scale_list)
    scale_factor_local                  = prox_scale_list + dist_scale_list
    for i in range(len(scale_factor_local)-1):
        indx                            = start_id + i
        scale_factor[indx]              = scale_factor_local[i]
    print("Scale factor size: {0:d}".format(len(scale_factor)))
    print("Scale factor:")
    print(scale_factor)
    
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
