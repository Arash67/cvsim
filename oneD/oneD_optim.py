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
