# A:======================================================= GENERAL
# This python script is developed by Arash Ghorbannia (Oct. 2021)
# The purpose is to create a automated framework for...
# tuning boundary conditions to match target hemodynamic values in cardiovascilar simulations
# 
# NOTE: to start, please create a SimVascular project and run this script in the python console  
# NOTE: this script assumes the cvsim repository is mounted on an ubuntu os in the following directory: (/home/ubuntu_username/github/) please see line 38 as an example
# NOTE: for information regarding how to mount github repository on local computer please read the git_installation.txt file in cvsim/documentations/ubuntu/git_installation.txt

# NOTE: You will need SimVascular installed on Ubuntu (for windows users its most easy through hyper-v manager),
# NOTE: to install ubuntu on hyper-v please see the instructions in hyperv_instructions.txt at cvsim/documentations/mswindows/hyperv_instructions.txt
# NOTE: additional instructions are included within the script


#--------------------------------------------------------
# ABREVIATIONS:
#               Aorta                               (AO)
#               Right subclavian artery             (RS)
#               Right carotic artery                (RC)   
#               Left carotid artery                 (LC)
#               Left subclavian artery              (LS)
#               Proximal Ascending aorta            (AA)
#               Distal descending aorta             (DA)
#               Transverse arch hypoplasia          (TAH)
#               Aortic isthmus hypoplasia           (AIH)
#               coarctation of the aorta            (CoA)
#               Ascending aorta dilation            (AAD)
#               Left aortic arch                    (LAA)
#--------------------------------------------------------

# B:======================================================= START

# B1: get the home directory
# NOTE: add Path from pathlib, add additional notes heare if needed
from pathlib import Path
# define the local home and repository directories 
home = str(Path.home())
cvsim = home + "/github/cvsim/"
# B2: modules
# B2a: import sv module that allows access to simvascular modeling pipeline which is available in gui 
import sv
# B2b: import os, add additional notes heare if needed
import os
# B2c: import sys, add additional notes heare if needed
import sys
# B2d: import vtk, add additional notes heare if needed
import vtk
# B2e: import graphics module which defines functions used to visualize SV objects using VTK; the module is taken from simvascular repository on Github under: SimVascular>simvascular-tests>new-api-testes.graphics
# NOTE: graphics is not a built in module so you need to add its path to the sys.path list where all the module paths are stores 
graphics_dir                = cvsim + "modules/graphics/"
print("graphics module directory:")
print(graphics_dir)
try:
    sys.path.insert(1, graphics_dir)
except:
    print("Can't find the modules/graphics package. this package is orginialy from simvascular repository: SimVascular-Tests > new-api-tests > graphics")
# import graphics module
import graphics as gr
# set the view point parameters and renderer
win_width = 500
win_height = 500
renderer, renderer_window = gr.init_graphics(win_width, win_height)

# B3: input file directories
# NOTE: all paths are defined relative to the *.py script location. so its important to keep the same foldering format used here

# Terminology:--------------------------------------------------------------------------------------------------------------------
#                       dir refers to folder directory in cvsim (e.g. "documentations/ubuntu/") 
#                       name refers to file name (e.g. "git_installation.txt")
#                       fulldir refers to full directory (e.g. "home/agh/github/cvsim/documentations/ubuntu/git_installation.txt)
#---------------------------------------------------------------------------------------------------------------------------------
input_dir                    = "data/input/"
output_dir                   = "data/output/"

# B3a: *.py script fulldir
script_name                 = "oneD_generalized_rabbit.py"
script_dir                  = "oneD/"
script_fulldir              = cvsim + script_dir + script_name
print("script full directory:")
print(script_fulldir)

# B3b: input path file names (*.pth )
path_names = ["control_rabbit_32181_P01AO.pth",
              "control_rabbit_32181_P02RS.pth",
              "control_rabbit_32181_P03RC.pth",
              "control_rabbit_32181_P04LC.pth",
              "control_rabbit_32181_P05LS.pth"]

# B3: input segmentation file names(*.ctgr)
seg_names = ["control_rabbit_32181_S01AO.ctgr",
             "control_rabbit_32181_S02RS.ctgr",
             "control_rabbit_32181_S03RC.ctgr",
             "control_rabbit_32181_S04LC.ctgr",
             "control_rabbit_32181_S05LS.ctgr"]

# C:======================================================= FUNCTIONS
def get_profile_contour(gr, renderer, contours, cid, npts):
    cont = contours[cid]
    #gr.create_contour_geometry(renderer, cont)
    cont_pd = cont.get_polydata()
    cont_ipd = sv.geometry.interpolate_closed_curve(polydata=cont_pd, number_of_points=npts)
    gr.add_geometry(renderer, cont_ipd)
    # gr.display(renderer_window)
    return cont_ipd

def read_contours(seg_name):
    file_name = cvsim + input_dir + seg_name 
    print("Read SV ctgr file: {0:s}".format(file_name))
    contour_group = sv.segmentation.Series(file_name)
    num_conts = contour_group.get_num_segmentations()
    contours = []
    for i in range(num_conts):
        cont = contour_group.get_segmentation(i)
        contours.append(cont)

    return contours

def mdl_union_all(modeler,mdls):
    i = len(mdls)
    k = 1
    while i > k:
        mdl1        = mdls[k-1]
        mdl2        = mdls[k]
        if k>1:
            mdl1 = mdl
        mdl         = modeler.union(model1=mdl1,model2=mdl2)
        k += 1
    return mdl

# D:======================================================= MODEL

# D0: define path and segmentation names to be used in SV GUI
svpathnames                 = ["P01AO","P02RS","P03RC","P04LC","P05LS"]
svsegnames                  = ["S01AO","S02RS","S03RC","S04LC","S05LS"]

rng                         = range(len(seg_names))
mdl                         = []
curve_list                  = [] 
start_cid                   = 0
use_distance                = True
num_profile_points          = 25
tolerance                   = 1e-3
# kernel                      = sv.modeling.Kernel.OPENCASCADE
kernel                      = sv.modeling.Kernel.POLYDATA
modeler                     = sv.modeling.Modeler(kernel)
# Aorta
AO_contours                 = read_contours(seg_names[0])
AO_path_series              = sv.pathplanning.Series(cvsim + input_dir + path_names[0])
AO_path                     = AO_path_series.get_path(0)
sv.dmg.add_path(svpathnames[0],AO_path)
sv.dmg.add_segmentation(name=svsegnames[0],path=svpathnames[0],segmentations=AO_contours)
for cid in range(0,len(AO_contours)):
    cont                = AO_contours[cid]
    cont_ipd            = get_profile_contour(gr,renderer,cont,cid,num_profile_points)
    if cid == 0:
        cont_align      = cont_ipd
    else:
        cont_align      = sv.geometry.align_profile(last_cont_align,cont_ipd,use_distance)
    #curve               = modeler.interpolate_curve(cont_align,True)
    curve               = modeler.approximate_curve(cont_align)
    #curve               = cont_align.get_polydata()
    curve_list.append(curve)
    last_cont_align     = cont_align
    
loft_surf               = modeler.loft(curve_list=curve_list)
loft_surf_cap           = modeler.cap_surface(loft_surf)
mdl.append(loft_surf_cap)
sv.dmg.add_model("Aorta",mdl)
'''
for mid in rng:
    curve_list          = []
    seg_name            = seg_names[mid]
    contour             = read_contours(seg_name)
    end_cid             = len(contour)
    path_series         = sv.pathplanning.Series(cvsim + input_dir + path_names[mid])
    vessel_path         = path_series.get_path(0)
    sv.dmg.add_path(svpathnames[mid],vessel_path)
    sv.dmg.add_segmentation(name=svsegnames[mid],path=svpathnames[mid],segmentations=contour)
    
    for cid in range(start_cid,end_cid):
        cont_ipd = get_profile_contour(gr, renderer, contour, cid, num_profile_points)
        if cid == start_cid:
            cont_align = cont_ipd 
        else:
            cont_align = sv.geometry.align_profile(last_cont_align, cont_ipd, use_distance)
        print(cont_align)
        # curve = modeler.approximate_curve(cont_align, tolerance,True)
        curve = modeler.interpolate_curve(cont_align,True)
        curve_list.append(curve) 
        last_cont_align = cont_align
     
    loft_surf           = modeler.loft(curve_list=curve_list)
    loft_surf_cap       = modeler.cap_surface(loft_surf)
    mdl.append(loft_surf_cap)

mdl = mdl_union_all(modeler,mdl)
mdl_pd = mdl.get_polydata()
# mdl.compute_boundary_faces(angle=60.0)
face_ids = mdl.get_face_ids()
print("face_ids:")
print(face_ids)
gr.add_geometry(renderer, mdl_pd, color=[0.0, 1.0, 0.0], wire=True, edges=False)
sv.dmg.add_model("Aorta",mdl)
mdl_name               = cvsim + input_dir + "control_rabbit_32181_aorta"
mdl_format             = "brep"
mdl.write(file_name=mdl_name, format=mdl_format)
'''
