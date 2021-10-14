# A:======================================================= GENERAL
# This python script is developed by Arash Ghorbannia (Oct. 2021)
# The purpose is to create a automated framework for...
# tuning boundary conditions to match target hemodynamic values in cardiovascilar simulations
# 
# NOTE: to start, please create a SimVascular project and run this script in the python console  
# NOTE: this script assumes the cvsim repository is mounted on an ubuntu os in the following directory: /home/ubuntu_username/github/
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
home = str(Path.home())

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
graphics_dir                = home + "/Desktop/SimVasSim/inputfiles/modules/graphics/"
try:
    sys.path.insert(1, graphics_dir)
except:
    print("Can't find the new-api-tests/graphics package. See the notes within the code. Check the simvascular repository (Github) for the graphics package!")
# import graphics module
import graphics as gr
# set the view point parameters and renderer
win_width = 500
win_height = 500
renderer, renderer_window = gr.init_graphics(win_width, win_height)

# B3: input file directories
# NOTE: all paths are defined relative to the *.py script location. so its important to keep the same foldering format used here

# Terminology:----------------------------------------------------------
#                       dir refers to folder (e.g. home/agh) 
#                       fulldir refers to file (e.g. home/agh/aorta.pth)
#-----------------------------------------------------------------------

# B3a: *.py script fulldir
script_fulldir              = home + "/Desktop/SimVasSim/GenModel/R32181/inputfiles/scripts/R32181.py"
script_dir                  = script_fulldir.parent
parent_dir                  = script_dir.parent
data_dir                    = parent_dir /
# B3b: input path files (*.pth ) directories

AO_path_fullname            = home + "/Desktop/SimVasSim/inputfiles/R32181/paths/P01AA.pth"  
RS_path_fullname            = home + "/Desktop/SimVasSim/inputfiles/R32181/paths/P02RS.pth"
RC_path_fullname            = home + "/Desktop/SimVasSim/inputfiles/R32181/paths/P03RC.pth"
LC_path_fullname            = home + "/Desktop/SimVasSim/inputfiles/R32181/paths/P04LC.pth"
LS_path_fullname            = home + "/Desktop/SimVasSim/inputfiles/R32181/paths/P05LS.pth"
script_path                 = Path(os.path.realpath(AO_path_fullname)).parent
parent_path                 = Path(os.path.realpath(AO_path_fullname)).parent.parent
data_path                   = parent_path / 'data'

print(AO_path_fullname)
print(script_path)
print(parent_path)
print(data_path)
# B3: input segmentation files(*.ctgr) full directories
AO_seg_fullname             = home + "/Desktop/SimVasSim/inputfiles/R32181/segmentations/S01AO.ctgr"
RS_seg_fullname             = home + "/Desktop/SimVasSim/inputfiles/R32181/segmentations/S02RS.ctgr"
RC_seg_fullname             = home + "/Desktop/SimVasSim/inputfiles/R32181/segmentations/S03RC.ctgr"
LC_seg_fullname             = home + "/Desktop/SimVasSim/inputfiles/R32181/segmentations/S04LC.ctgr"
LS_seg_fullname             = home + "/Desktop/SimVasSim/inputfiles/R32181/segmentations/S05LS.ctgr"

# C:======================================================= PATHS

# C1: create path series from *.pth files identified @ START
AO_path_series              = sv.pathplanning.Series(AO_path_fullname)
RS_path_series              = sv.pathplanning.Series(RS_path_fullname)
RC_path_series              = sv.pathplanning.Series(RC_path_fullname)
LC_path_series              = sv.pathplanning.Series(LC_path_fullname)
LS_path_series              = sv.pathplanning.Series(LS_path_fullname)

# C2: get the path @ time 0
AO_path                     = AO_path_series.get_path(0)
RS_path                     = RS_path_series.get_path(0)
RC_path                     = RC_path_series.get_path(0)
LC_path                     = LC_path_series.get_path(0)
LS_path                     = LS_path_series.get_path(0)

# C3: get control points from paths (NOTE: not needed at this point)
AO_control_points           = AO_path.get_control_points()
RS_control_points           = RS_path.get_control_points()
RC_control_points           = RC_path.get_control_points()
LC_control_points           = LC_path.get_control_points()
LS_control_points           = LS_path.get_control_points()

# C4: with python path objects created above, create new node under SV Data Manager "Path" node 
sv.dmg.add_path("P01AO",AO_path)
sv.dmg.add_path("P02RS",RS_path)
sv.dmg.add_path("P03RC",RC_path)
sv.dmg.add_path("P04LC",LC_path)
sv.dmg.add_path("P05LS",LS_path)

# D:======================================================= SEGMENTATION

# D1: create segmentation series from *.ctgr files identified @ START
AO_seg_series               = sv.segmentation.Series(AO_seg_fullname)
RS_seg_series               = sv.segmentation.Series(RS_seg_fullname)
RC_seg_series               = sv.segmentation.Series(RC_seg_fullname)
LC_seg_series               = sv.segmentation.Series(LC_seg_fullname)
LS_seg_series               = sv.segmentation.Series(LS_seg_fullname) 

# D2: get number of segments in each seg_series
time                        = 0
AO_seg_num                  = AO_seg_series.get_num_segmentations(time)
RS_seg_num                  = RS_seg_series.get_num_segmentations(time)
RC_seg_num                  = RC_seg_series.get_num_segmentations(time)
LC_seg_num                  = LC_seg_series.get_num_segmentations(time)
LS_seg_num                  = LS_seg_series.get_num_segmentations(time)

# D3: scale segmentations
# D3a: global scaling 
gscale                      = 1.0

# D3b: local radial scaling: here each segment is scaled by multiplying its radius by a scale factor between 0 and 1
normal_scale                         = [1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00]
AAD_scale                            = [1.00,1.00,1.05,1.11,1.21,1.23,1.20,1.13,1.08,1.04,1.00,0.96,0.91,0.85,0.62,0.49,0.58,0.76,0.88,0.99,1.00,1.00,1.00,1.00,1.00]
LAA_scale                            = [1.00,1.00,1.03,1.10,1.19,1.22,1.17,1.14,1.09,1.07,1.00,0.95,0.90,0.83,0.59,0.49,0.58,0.76,0.88,0.99,1.00,1.00,1.00,1.00,1.00]
TAH_scale                            = [1.00,1.00,1.00,1.00,1.00,1.00,1.00,0.93,0.75,0.70,0.88,0.91,0.92,0.85,0.62,0.49,0.58,0.76,0.88,0.99,1.00,1.00,1.00,1.00,1.00]
AIH_scale                            = [1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,0.99,0.96,0.87,0.82,0.73,0.69,0.62,0.49,0.58,0.76,0.88,0.99,1.00,1.00,1.00,1.00,1.00]
CoA_scale                            = [1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,1.00,0.96,0.91,0.85,0.62,0.49,0.58,0.76,0.88,0.99,1.00,1.00,1.00,1.00,1.00]
shrink_scale                         = 1.00

# D3c: applying changes to segmentations
segs                = []
curr_time           = time

global_scale        = gscale
local_scale         = normal_scale 

for sid in list(range(AO_seg_num)):
    # get the current segmentation series to work with
    curr_seg_series     = AO_seg_series
    # get the current segment in the selected segmentation series 
    curr_seg            = curr_seg_series.get_segmentation(sid,time=curr_time)
    curr_center         = curr_seg.get_center()
    curr_radius         = curr_seg.get_radius()
    # scale factors for radius and center coordinates of each segment
    curr_radius_scale   = global_scale
    curr_radius_scale   = curr_radius_scale*local_scale[sid]*shrink_scale
    
    curr_center_scale   = global_scale
    # update center and radius values and implement them to the current segment 
    curr_radius         = curr_radius*curr_radius_scale
    curr_seg.set_radius(curr_radius)
    curr_center         = [element * curr_center_scale for element in curr_center]      
    curr_seg.set_center(curr_center)

    #print(curr_center)
    segs.append(curr_seg)

# D4: with python segmentation object list created above, create new node under SV Data Manager "Segmentation" node 
sv.dmg.add_segmentation(name="S01AO",path="P01AO",segmentations=segs)

# E:======================================================= Model

# E1: create a parasolid modeler
modeler = sv.modeling.Modeler(sv.modeling.Kernel.OPENCASCADE)

# E2: read in segmentations to loft
num_segs                = len(segs)
crv_list                = []
start_cid               = 0
end_cid                 = num_segs
use_distance            = True
num_profile_points      = 25
tolrnc                  = 1e-3

# E3: loft through the curves created from segmentations
for cid in range(start_cid,end_cid):
    curr_seg            = segs[cid] 
    curr_pd             = curr_seg.get_polydata()
    curr_ipd            = sv.geometry.interpolate_closed_curve(polydata=curr_pd,number_of_points=num_profile_points)

    if cid == start_cid:
        cont_align      = curr_ipd 
    else:
        cont_align      = sv.geometry.align_profile(last_cont_align, curr_ipd, use_distance)

    curve               = modeler.interpolate_curve(cont_align)
    curve_pd            = curve.get_polydata()
    gr.add_geometry(renderer, curve_pd, color=[1.0, 0.0, 0.0])
    crv_list.append(curve) 
    last_cont_align     = cont_align

loft_surf               = modeler.loft(curve_list=crv_list)

# E4: cap the lofted surface
capped_loft_surf        = modeler.cap_surface(loft_surf)

# E5: write the model (STILL NOT WORKING)
AO_mdl_folder           = home + "/Desktop/SimVasSim/inputfiles/R32181"
model_name              = "AO-capped-loft-opencascade-test"
#capped_loft_surf.write(file_name=str(AO_mdl_folder / model_name), format="brep")
capped_loft_surf.write(file_name=os.path.join(AO_mdl_folder,model_name), format="brep")

# E5: with python model object created above, create new node under SV Data Manager "Models" node
mdl_tree_name           = "Aorta"
sv.dmg.add_model(mdl_tree_name,capped_loft_surf)

# E6: visualized model (CURRENTLY CAUSE SIMVASCULAR TO CRASH BUT STILL GIVES THE VISUALIZATION)
'''
gr.add_geometry(renderer, capped_loft_surf.get_polydata(), color=[0.8, 0.8, 0.8], wire=False)
camera                  = renderer.GetActiveCamera();
camera.Zoom(0.5)
#camera.SetPosition(center[0], center[1], center[2])
cont1                   = segs[start_cid]
center                  = cont1.get_center()
camera.SetFocalPoint(center[0], center[1], center[2])
gr.display(renderer_window)
'''

# E7: probably remesh and modify the surfaces 


# F:======================================================= Mesh

# F1: create mesher
mesher                  = sv.meshing.create_mesher(sv.meshing.Kernel.TETGEN)

# F2: compute centerlines
centerlines             = mesher.radius_meshing_compute_centerlines()

# F3: set general meshing options
options                             = sv.meshing.TetGenOptions(global_edge_size =0.4,surface_mesh_flag=True,volume_mesh_flag=True)
options.optimization                        = 3
options.quality_ratio                       = 1.4 
options.no_bisect                           = True

# F4: set radius-based meshing options
options.radius_meshing_centerlines          = centerlines
options.radius_meshing_scale                = 0.4
options.radius_meshing_compute_centerlines  = True
options.radius_meshing_on                   = True

# F5: set wall face IDs
face_ids                                    = mesher.get_model_face_ids()
wall_face_ids                               = face_ids
mesher.set_walls(wall_face_ids)

# F6: generate the mesh
mesh = mesher.generate_mesh(options)

# F7: write the mesh 
'''
see help(sv.meshing): 

     |  write_mesh(...)
     |      write_mesh(file_name)  
     |      
     |      Write the generated volume mesh to a file. 
     |      
     |      The format of the file depends on the meshing kernel used to generate the  
     |      mesh                                                                       
     |         1) TetGen - A vtkUnstructuredGrid .vtu file.                            
     |         2) MeshSim - A MeshSim .sms file.                                       
     |      
     |      Args: 
     |        file_name (str): The name of the file to write the mesh to.
    

'''
AO_msh_folder           = home + "/Desktop/SimVasSim/inputfiles/R32181"
mesh_name               = "msh01" 
mesher.write_mesh(os.sys.join(AO_msh_folder,mesh_name))

# F8: add mesh to the tree
sv.dmg.add_mesh(name="msh01",mesh=mesh,model=mdl_tree_name)

# F9: show the mesh

'''
show_mesh = True
if show_mesh:
    mesh_surf = mesher.get_surface()
    gr.add_geometry(renderer,mesh_surface,color=[1.0,1.0,1.0],wire=True,edges=Ture)
    gr.display(renderer_window)
'''











