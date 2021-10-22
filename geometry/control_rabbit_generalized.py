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
cvsimout                = home + "/github/outofsource/cvsimout/"
# B2: modules
import os
import sys



# other local modules
vmanip_dir                   = cvsim + "modules/"
print("control_point_manipulation:")
print(vmanip_dir)
try:
    sys.path.insert(1, vmanip_dir)
except:
    print("Can't find the modules/graphics package. this package is orginialy from simvascular repository: SimVascular-Tests > new-api-tests > graphics")
import vessel_manipulator as vmanip

# B3: input file directories
# NOTE: all paths are defined relative to the *.py script location. so its important to keep the same foldering format used here

# Terminology:--------------------------------------------------------------------------------------------------------------------
#                       dir refers to folder directory in cvsim (e.g. "documentations/ubuntu/") 
#                       name refers to file name (e.g. "git_installation.txt")
#                       fulldir refers to full directory (e.g. "home/agh/github/cvsim/documentations/ubuntu/git_installation.txt)
#---------------------------------------------------------------------------------------------------------------------------------
input_dir                    = "data/input/"
output_dir                   = cvsimout

# B3a: *.py script fulldir
script_name                 = "control_rabbit_generalized.py"
script_dir                  = "geometry/"
script_fulldir              = cvsim + script_dir + script_name
print("script full directory:")
print(script_fulldir)
# B3b: *.ctgr fulldir

#seg_name                    = "control_rabbit_32181_S01AO_splinepoly2.ctgr"
#seg_name                    = "control_rabbit_32181_S02RS_splinepoly.ctgr"
#seg_name                    = "control_rabbit_32181_S03RC_splinepoly.ctgr"
#seg_name                    = "control_rabbit_32181_S04LC_splinepoly.ctgr"
#seg_name                    = "control_rabbit_32181_S05LS_splinepoly.ctgr"

seg_names                   = ["control_rabbit_32181_S01AO_splinepoly2.ctgr"
                              ,"control_rabbit_32181_S02RS_splinepoly.ctgr"
                              ,"control_rabbit_32181_S03RC_splinepoly.ctgr"
                              ,"control_rabbit_32181_S04LC_splinepoly.ctgr"
                              ,"control_rabbit_32181_S05LS_splinepoly.ctgr"]

branch_name_list            = ["AO","RS","RC","LC","LS"]
# seg_fulldir                 = cvsim + input_dir + seg_name

# B4: manipulation parameters for single aortic narrowing
# number of contours to be manipulated in the region, indicator of the length of the affected region
length_id                   = 3
# diameter reduction at most stenotic segment
perc_diameter_reduction     = 0
scale_id                    = perc_diameter_reduction/100
# longitudinal asymetry (-1 indicating narrowing toward proximal, 0 indicating symmetric narrowing, 1 toward the distal)
long_asym_id                = 0
# narrowing location identified by control point id
control_point_id            = 3
# steepness
steepness                   = 1.5
# x50 between zero and 1 with zero indicating longer CoA and 1 indicating discrete COA
x50                         = 0.7


# mesh parameters
global_max_edge_size        = 0.05
number_of_layers            = 2
edge_size_fraction          = 0.5
layer_decreasing_ratio      = 0.8
angle                       = 60
boundarylayer_meshing       = 0

case_id                     = 1

# control_point_manipulation: morphological scaling, loft, mesh, save .vtp, (performs morphological morphological manipulation only on AO and the branches are just meshed as imported)
for i in range(len(seg_names)):
  if i == 0:                    # modify aorta geometry
    AO_manip_par                = [length_id,scale_id,long_asym_id,control_point_id,steepness,x50]
    mesh_par                    = [global_max_edge_size,number_of_layers,edge_size_fraction,layer_decreasing_ratio,angle,boundarylayer_meshing]
  else:                         # leave the AO branches unchanges 
    AO_manip_par                = [3,1.0,0,3,1.5,0.7]
    mesh_par                    = [global_max_edge_size,number_of_layers,edge_size_fraction,layer_decreasing_ratio,angle,boundarylayer_meshing]
  vessel_id                   = "Case_" + str(case_id) + "_" + branch_name_list[i]
  # call the manipulator
  vmanip.manipulator(vessel_id,cvsim,input_dir,cvsimout,seg_names[i],AO_manip_par,mesh_par)

# union the aorta and branches


