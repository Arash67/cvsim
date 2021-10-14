#! /usr/bin/python
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
script_name                 = "oneD_optim.py"
script_dir                  = "oneD/"
script_fulldir              = cvsim + script_dir + script_name
print("script full directory:")
print(script_fulldir)

## Create a ROM simulation.
rom_simulation = sv.simulation.ROM() 

## Create ROM simulation parameters.
params = sv.simulation.ROMParameters()

## Mesh parameters.
mesh_params = params.MeshParameters()


## Model parameters.
model_params = params.ModelParameters()
model_params.name = "demo-oneD"
model_params.inlet_face_names = ['cap_aorta' ] 
model_params.outlet_face_names = ['cap_right_iliac', 'cap_aorta_2' ] 
model_params.centerlines_file_name = cvsim + input_dir + 'demo-oneD-centerlines.vtp' 

## Fluid properties.
fluid_props = params.FluidProperties()

## Set wall properties.
#
print("Set wall properties ...")
material = params.WallProperties.OlufsenMaterial()
print("Material model: {0:s}".format(str(material)))

## Set boundary conditions.
#
bcs = params.BoundaryConditions()
#bcs.add_resistance(face_name='outlet', resistance=1333)
bcs.add_velocities(face_name='inlet', file_name=cvsim + input_dir + 'demo-oneD-inflow.flow')
bcs.add_rcr(face_name='cap_right_iliac', Rp=90.0, C=0.0008, Rd=1200)
bcs.add_rcr(face_name='cap_aorta_2', Rp=100.0, C=0.0004, Rd=1100)

## Set solution parameters. 
#
solution_params = params.Solution()
solution_params.time_step = 0.001
solution_params.num_time_steps = 1000


## Write a 1D solver input file.
#
rom_simulation.write_input_file(model_order=1, model=model_params, mesh=mesh_params, fluid=fluid_props, 
  material=material, boundary_conditions=bcs, solution=solution_params, directory=cvsim + output_dir)

## Run a simulation.
rom_simulation.run(parameters=fluid_params, use_mpi=True, num_processes=4)


