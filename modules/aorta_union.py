
# A:======================================================= GENERAL
# The purpose is to create a boolean union model of the aorta and branches 
# 
# NOTE: this script assumes the cvsim repository is mounted on an ubuntu os in the following directory: (/home/ubuntu_username/github/) please see line 38 as an example
# NOTE: for information regarding how to mount github repository on local computer please read the git_installation.txt file in cvsim/documentations/ubuntu/git_installation.txt

# NOTE: You will need SimVascular installed on Ubuntu (for windows users its most easy through hyper-v manager),
# NOTE: to install ubuntu on hyper-v please see the instructions in hyperv_instructions.txt at cvsim/documentations/mswindows/hyperv_instructions.txt
# NOTE: additional instructions are included within the script


#--------------------------------------------------------
# ABREVIATIONS:
#               Aorta                               (AO)
#               Right subclavian artery             (RS)
#               Right carotid artery                (RC)
#               Left carotid                        (LC)
#               Left subclavian artery              (LS)
#--------------------------------------------------------

# B:======================================================= START

# B1: get the home directory
# NOTE: add Path from pathlib, add additional notes heare if needed
from pathlib import Path
# define the local home and repository directories plus out of source directory for outputs not needed to be uploaded to the source repository 
home                    = str(Path.home())
cvsim                   = home + "/github/cvsim/"
cvsimout                = home + "/github/outofsource/cvsimout/"
# B2: modules
# B2a: import sv module that allows access to simvascular modeling pipeline which is available in gui 
import sv
# B2b: import os, add additional notes heare if needed
import os
# B2c: import sys, add additional notes heare if needed
import sys
# B2d: import vtk, add additional notes heare if needed
import vtk

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
## Create renderer and graphics window.
win_width = 500
win_height = 500
renderer, renderer_window = gr.init_graphics(win_width, win_height)

# C:======================================================= INPUTS
# list of models for aorta and branches (*.vtp) 
vtp_name_list         = ["Case_1_AO_capped_loft_surface.vtp"
                        ,"Case_1_RC_capped_loft_surface.vtp"
                        ,"Case_1_RS_capped_loft_surface.vtp"
                        ,"Case_1_LC_capped_loft_surface.vtp"
                        ,"Case_1_LS_capped_loft_surface.vtp"]

modeler = sv.modeling.Modeler(sv.modeling.Kernel.POLYDATA)
model = sv.modeling.PolyData()

AO_file_name = cvsimout + vtp_name_list[0]
AO_reader = vtk.vtkXMLPolyDataReader()
AO_reader.SetFileName(AO_file_name) 
AO_reader.Update()
AO_read_polydata = AO_reader.GetOutput()
AO_model = model
AO_model.set_surface(surface=AO_read_polydata)

## Add model polydata.
gr.add_geometry(renderer, AO_read_polydata, color=[1.0, 0.0, 0.0], wire=True, edges=False)
# Display window.
# gr.display(renderer_window)


RC_file_name = cvsimout + vtp_name_list[1]
RC_reader = vtk.vtkXMLPolyDataReader()
RC_reader.SetFileName(RC_file_name) 
RC_reader.Update()
RC_read_polydata = RC_reader.GetOutput()
RC_model = model
RC_model.set_surface(surface=RC_read_polydata)

## Add model polydata.
gr.add_geometry(renderer, RC_read_polydata, color=[1.0, 0.0, 0.0], wire=True, edges=False)
# Display window.
# gr.display(renderer_window)

union_model = modeler.intersect(AO_model,RC_model)


'''
union_model_pd = union_model.get_polydata()


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
## Create renderer and graphics window.
win_width = 500
win_height = 500
renderer, renderer_window = gr.init_graphics(win_width, win_height)

## Add model polydata.
#gr.add_geometry(renderer, box_pd, color=[0.0, 1.0, 0.0], wire=True, edges=False)
#gr.add_geometry(renderer, cylinder_pd, color=[0.0, 0.0, 1.0], wire=True, edges=False)
gr.add_geometry(renderer, union_model_pd, color=[1.0, 0.0, 0.0], wire=True, edges=False)

# Display window.
gr.display(renderer_window)

'''
