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
    
    coef_a                              = 1
    common_ratio                        = float(2/3)
    tmp_len_id                          = length_id
    if (length_id % 2 !=0): 
        tmp_len_id -=1
    half_num                        = int(tmp_len_id/2)
    center_id                       = control_point_id
    start_id                        = center_id - half_num
    stop_id                         = start_id + length_id
    long_asym_dislocation           = int(half_num * long_asym_id)
    center_id                       = center_id + long_asym_dislocation
    '''
    if long_asym_id > 0:
        center_id                   = center_id + long_asym_dislocation
    else:
        center_id                   = center_id - long_asym_dislocation
    '''
    prox_cont_num                   = center_id - start_id
    dist_cont_num                   = stop_id - center_id
    prox_scale_list                 = []
    distal_scale_list               = []
    power                           = prox_cont_num
    
    print("Proximal contour numbers: {0:d}".format(prox_cont_num))
    print("Distal contour numbers: {0:d}".format(dist_cont_num))
    '''
    for i in range(prox_cont_num):
        proximal_scale_list.append(float(coef_a*common_ratio**power))
        power                       -= 1
   
    power                           = distal_cont_num
    for i in range(dist_cont_num):
        distal_scale_list.append(float(coef_a*common_ratio**power))
        power                       -= 1 
    
    print("Proximal scale factors: {0:d}".format(proximal_scale_list))
    print("Distal scale factors: {0:d}".format(distal_scale_list))
    '''
def radial_expansion_test(center,new_outer_points,dists,unit_vectors,scale_factor):
    temp_outer_points                   = new_outer_points.copy()
    new_dists                           = dists * scale_factor
    new_points                          = unit_vectors * new_dists[...,np.newaxis] + center
    return new_points
def get_dists_unit_vectors_test(center,new_outer_points):
    dists = np.linalg.norm(new_outer_points-center,axis=-1)
    unit_vectors = (new_outer_points-center)/ dists[...,np.newaxis]
    return dists,unit_vectors

