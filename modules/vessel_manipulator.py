# A:======================================================= GENERAL
# The purpose is to create a parametrized model of the concomitant anomalies happening with CoA
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

#--------------------------------------------------------

# B:======================================================= START

# B1: get the home directory
# NOTE: add Path from pathlib, add additional notes heare if needed
from pathlib import Path
# define the local home and repository directories plus out of source directory for outputs not needed to be uploaded to the source repository 
home                    = str(Path.home())
cvsim                   = home + "/github/cvsim/"
# cvsimout                = home + "/github/outofsource/cvsimout/"
# B2: modules
# B2a: import sv module that allows access to simvascular modeling pipeline which is available in gui 
import sv
# B2b: import os, add additional notes heare if needed
import os
# B2c: import sys, add additional notes heare if needed
import sys
# B2d: import vtk, add additional notes heare if needed
import vtk
# B2e: import numpy, add additional notes here if needed
import numpy as np
# B2f: import shutil, add additional notes here if needed
from shutil import copyfile
# B2i: import paraview module
# NOTE: paraview is not a built in module so you need to add its path to the sys.path list where all the module paths are stores 
paraview_dir                =  "/usr/lib/python3/dist-packages/paraview"
print("paraview package directory:")
print(paraview_dir)
try:
    sys.path.insert(1, paraview_dir)
except:
    print("Can't find the modules/paraview package.")

# import paraview as pv
# other local modules
cpmanip_dir                  = cvsim + "modules/"
print("control_point_manipulation:")
print(cpmanip_dir)
try:
    sys.path.insert(1, cpmanip_dir)
except:
    print("Can't find the modules/control_point_manipulatin package")
import control_point_manipulation as cpmanip

# B3: input file directories
# NOTE: all paths are defined relative to the *.py script location. so its important to keep the same foldering format used here

# Terminology:--------------------------------------------------------------------------------------------------------------------
#                       dir refers to folder directory in cvsim (e.g. "documentations/ubuntu/") 
#                       name refers to file name (e.g. "git_installation.txt")
#                       fulldir refers to full directory (e.g. "home/agh/github/cvsim/documentations/ubuntu/git_installation.txt)
#---------------------------------------------------------------------------------------------------------------------------------

# C:======================================================= SEGMENTATION
def set_spline(control_points):
    # .ctgr includes center and distance control points, followed by outer control points
    # this function takes outer control points only
    seg = sv.segmentation.SplinePolygon(control_points=control_points)
    seg.set_subdivision_params(type=sv.segmentation.SubdivisionType.CONSTANT_SPACING)
    return seg
def set_splines(control_points_list):
    segs = [set_spline(control_points) for control_points in control_points_list]
    return segs
def read_contours(cvsim,input_dir,filename):     # reads contours form *.ctgr
    file_name = cvsim + input_dir + filename
    print("Read SV ctgr file: {0:s}".format(file_name))
    contour_group = sv.segmentation.Series(file_name)
    num_conts = contour_group.get_num_segmentations()
    contours = []

    for i in range(num_conts):
        cont = contour_group.get_segmentation(i)
        contours.append(cont)

    print("Number of contours: {0:d}".format(num_conts))
    return contours
 # Manipulation of Contour
def get_center_outer(contour):
    return contour.get_center(),contour.get_control_points()
def manipulate_contour(contour,scale_factor):
    """
    Radially expand or contract given contour
    scale_factor is a np.array of same length as contour. values >1 is expansion, values <1 is contraction
    """
    center,outer = get_center_outer(contour)
    new_outer = manip.vary_points_test(center,outer,scale_factor=scale_factor)
    contour = set_spline(new_outer)
    return contour
def get_center_outer(contour):
    return contour.get_center(),contour.get_control_points()
def manipulate_contour(contour,scale_factor):
    """
    Radially expand or contract given contour
    scale_factor is a np.array of same length as contour. values >1 is expansion, values <1 is contraction
    """
    center,outer = get_center_outer(contour)
    new_outer = cpmanip.vary_points_test(center,outer,scale_factor=scale_factor)
    contour = set_spline(new_outer)
    return contour

# D:======================================================= MODELING
def get_profile_contour(contours, cid, npts):
    cont = contours[cid]
    cont_pd = cont.get_polydata()
    cont_ipd = sv.geometry.interpolate_closed_curve(polydata=cont_pd, number_of_points=npts)
    return cont_ipd
def loft(vessel_id,contours,cvsimout):
    num_contours = len(contours)
    num_profile_points = 50
    use_distance = True
    contour_list = []
    start_cid = 0
    end_cid = num_contours
    for cid in range(start_cid,end_cid):
        cont_ipd = get_profile_contour(contours, cid, num_profile_points)
        if cid == start_cid:
            cont_align = cont_ipd
        else:
            cont_align = sv.geometry.align_profile(last_cont_align, cont_ipd, use_distance)
        contour_list.append(cont_align)
        last_cont_align = cont_align
    options = sv.geometry.LoftNurbsOptions()
    loft_surf = sv.geometry.loft_nurbs(polydata_list=contour_list, loft_options=options)#, num_divisions=12
    loft_capped = sv.vmtk.cap(surface=loft_surf, use_center=False)

    # We dont need to save the ugly_file, it will be remeshed
    ugly_file = cvsimout + vessel_id + "_capped_loft_surface.vtp"
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(ugly_file)
    writer.SetInputData(loft_capped)
    writer.Update()
    writer.Write()
    return loft_capped
def remesh(loft_capped,cvsimout):
    modeler = sv.modeling.Modeler(sv.modeling.Kernel.POLYDATA)
    model = sv.modeling.PolyData()
    model.set_surface(surface=loft_capped)
    model.compute_boundary_faces(angle=60.0)
    remesh_model = sv.mesh_utils.remesh(model.get_polydata(), hmin=0.1, hmax=0.3)
    model.set_surface(surface=remesh_model)
    model.compute_boundary_faces(angle=60.0)
    model.write(cvsimout, format="vtp")
    polydata = model.get_polydata()
    print("Model: ")
    print("  Number of points: " + str(polydata.GetNumberOfPoints()))
    print("  Number of cells: " + str(polydata.GetNumberOfCells()))
    return cvsimout + '.vtp',polydata
  
# D:======================================================= MESHING
# see https://github.com/SimVascular/SimVascular-Tests/blob/master/new-api-tests/meshing/tetgen-options.py
def do_mesh(vessel_id,cvsimout,file_name,mesh_par):
    mesher = sv.meshing.create_mesher(sv.meshing.Kernel.TETGEN)
    options = sv.meshing.TetGenOptions(global_edge_size=mesh_par[0], surface_mesh_flag=True, volume_mesh_flag=True) 
    mesher.load_model(cvsimout + file_name)

    ## Set the face IDs for model walls.
    wall_face_ids = [1]
    mesher.set_walls(wall_face_ids)

    ## Compute model boundary faces.
    mesher.compute_model_boundary_faces(angle=mesh_par[4])
    face_ids = mesher.get_model_face_ids()
    print("Mesh face ids: " + str(face_ids))

    ## Set boundary layer meshing options
    if mesh_par[5] == 1:
        print("Set boundary layer meshing options ... ")
        mesher.set_boundary_layer_options(number_of_layers=mesh_par[1], edge_size_fraction=mesh_par[2], layer_decreasing_ratio=mesh_par[3], constant_thickness=False)
        options.no_bisect = False

    ## Print options.
    #print("Options values: ")
    #[ print("  {0:s}:{1:s}".format(key,str(value))) for (key, value) in sorted(options.get_values().items()) ]

    ## Generate the mesh. 
    mesher.generate_mesh(options)
    
    ## Get the mesh as a vtkUnstructuredGrid. 
    mesh = mesher.get_mesh()
    
    print("Mesh:")
    print("  Number of nodes: {0:d}".format(mesh.GetNumberOfPoints()))
    print("  Number of elements: {0:d}".format(mesh.GetNumberOfCells()))

    ## Write the mesh.
    mesher.write_mesh(file_name = cvsimout + vessel_id + "_mesh_complete_mesh.vtu")

    ## Export the mesh-complete files
    for i in range(4):#complete exterior and 3 faces
        if i==0:
            temp_name = cvsimout + vessel_id + "_mesh_complete_exterior.vtp"
            surf_mesh = mesher.get_surface()
        else:
            temp_name = cvsimout + vessel_id + "_mesh_face_" + str(i) + ".vtp"
            surf_mesh = mesher.get_face_polydata(i)
        writer = vtk.vtkXMLPolyDataWriter()
        writer.SetFileName(temp_name)
        writer.SetInputData(surf_mesh)
        writer.Update()
        writer.Write()
        #Main wall
        if i==1:
            temp_name2 = cvsimout + vessel_id + "_walls_combined.vtp"
            copyfile(temp_name,temp_name2)

#========================================================================================= GRAPHICS  
def draw_solid(cvsim,polydata):
    # import graphics module which defines functions used to visualize SV objects using VTK; the module is taken from simvascular repository on Github under: SimVascular>simvascular-tests>new-api-testes.graphics
    # NOTE: graphics is not a built in module so you need to add its path to the sys.path list where all the module paths are stores 
    graphics_dir                = cvsim + "modules/graphics/"
    print("graphics module directory:")
    print(graphics_dir)
    try:
        sys.path.insert(1, graphics_dir)
    except:
        print("Can't find the modules/graphics package. this package is orginialy from simvascular repository: SimVascular-Tests > new-api-tests > graphics")
    # B2h: import graphics module
    import graphics as gr
    win_width = 500
    win_height = 500
    renderer, renderer_window = gr.init_graphics(win_width, win_height)
    gr.add_geometry(renderer, polydata, color=[0.0, 1.0, 0.0], wire=False, edges=True)
    gr.display(renderer_window)

def draw_segmentations(cvsim,contours):
    # import graphics module which defines functions used to visualize SV objects using VTK; the module is taken from simvascular repository on Github under: SimVascular>simvascular-tests>new-api-testes.graphics
    # NOTE: graphics is not a built in module so you need to add its path to the sys.path list where all the module paths are stores 
    graphics_dir                = cvsim + "modules/graphics/"
    print("graphics module directory:")
    print(graphics_dir)
    try:
        sys.path.insert(1, graphics_dir)
    except:
        print("Can't find the modules/graphics package. this package is orginialy from simvascular repository: SimVascular-Tests > new-api-tests > graphics")
    # B2h: import graphics module
    import graphics as gr
    num_segs = len(contours)

    ## Create renderer and graphics window.
    win_width = 500
    win_height = 500
    renderer, renderer_window = gr.init_graphics(win_width, win_height)
    ## Show contours.
    for sid in range(num_segs):
        seg = contours[sid]
        control_points = seg.get_control_points()
        gr.create_segmentation_geometry(renderer, seg)

    # Display window.
    gr.display(renderer_window)

# Z:======================================================= MAIN
def manipulator(vessel_id,cvsim,input_dir,cvsimout,seg_name,vessel_par,mesh_par):
    length_id                           = vessel_par[0]
    scale_id                            = vessel_par[1]
    long_asym_id                        = vessel_par[2]
    control_point_id                    = vessel_par[3]
    steepness                           = vessel_par[4]
    x50                                 = vessel_par[5]
    
    
    # read and return contours
    contours                            = read_contours(cvsim,input_dir,seg_name)
    num_contours                        = len(contours)
    if 0.5*length_id + control_point_id > num_contours:
        print("ERROR: changes propagate beyond the last distal segment")
    if control_point_id - 0.5*length_id < 0:
        print("ERROR: changes propagate beyond the first segment of the vessel")
        
    # compute scale factors
    scale_factors                       = cpmanip.scale_factor_test(num_contours,length_id,scale_id,long_asym_id,control_point_id,steepness,x50)
    print("Scale factors:")
    print(scale_factors)
    # Contour manipulation
    contours_manip                      = []
    for i in range(len(contours)-1):
        conti                           = contours[i]
        conti                           = manipulate_contour(conti,scale_factors[i])
        contours_manip.append(conti)
    #print("Manipulated contour:")
    print(contours_manip)
    print(contours_manip[0])
    # save manipulated segmentations as *ctgr
    seg = sv.segmentation.SplinePolygon(contours_manip)
    # seg.set_contour_points(contours_manip[0])
    seg.write(cvsimout + vessel_id + "_segmentation.ctgr")
    # loft, remesh, and save the model as vtp files
    loft_capped                         = loft(vessel_id,contours_manip,cvsimout)
    remesh(loft_capped,cvsimout)
    # mesh
    do_mesh(vessel_id,cvsimout,vessel_id + "_capped_loft_surface.vtp",mesh_par)
    
    # Draw segmentation
    # draw_segmentations(cvsim,contours_manip)
    
    # Take a paraview screenshot
    # cvsimout = /home/agh/github/outofsource/cvsimout/
    # filename = [cvsimout + 'mesh-complete.exterior.vtp']
    # vtpscreenshot(vtpname,[300,200],[0.32, 0.34, 0.43],[300,300],cvsimout + "screen.png")
