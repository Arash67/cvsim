
# A:======================================================= GENERAL
# The purpose is to create a parametrized model of the CoA and concomitant anomalies...
# often coexisting with it such as:
#       dilated ascending aorta, 
#       hypoplastic aortic arch,
#       aortic isthmus hypoplasia,
#       long-segment CoA
# 
# NOTE: Run this script in the python console in SimVascular GUI  
# NOTE: This script assumes the cvsim repository is mounted on an ubuntu os in the following directory:
#       /home/ubuntu_username/github/
#
# NOTE: To mount github repository on local computer please read the git_installation.txt file in:
#       cvsim/documentations/ubuntu/git_installation.txt
#
# NOTE: You will need SimVascular installed on Ubuntu (for windows users its most easy through hyper-v manager),
# NOTE: To install ubuntu on hyper-v please see the instructions in hyperv_instructions.txt at:
#       cvsim/documentations/mswindows/hyperv_instructions.txt
#
# NOTE: additional instructions are included within the script


# ABREVIATIONS:------------------------------------------
# 
#               Aorta                               (AO)
#               
#--------------------------------------------------------

# B:======================================================= START

from pathlib import Path
# define the local home and repository directories plus out-of-source directory for outputs not needed to be uploaded to the source repository 
home                    = str(Path.home())
cvsim                   = home + "/github/cvsim/"
cvsimout                = home + "/github/outofsource/cvsimout/"
input_dir                    = "data/input/"
output_dir                   = cvsimout

ctgr_file_name  = cvsim + input_dir + "control_rabbit_32181_S01AO.ctgr"
vtp_file_name   = output_dir + "Case_1_AO_mesh_complete_exterior.vtp"

# B4: manipulation parameters for single aortic narrowing
# number of contours to be manipulated in the region, indicator of the length of the affected region
length_id                   = 8
# diameter reduction at most stenotic segment
perc_diameter_reduction     = 70
scale_id                    = perc_diameter_reduction/100
# longitudinal asymetry (-1 indicating narrowing toward proximal, 0 indicating symmetric narrowing, 1 toward the distal)
long_asym_id                = 0.0
# narrowing location identified by control point id
control_point_id            = 16

# steepness
    # AIH
# steepness                   = 1.1
    # CoA
steepness                   = 1.5


# x50 between zero and 1 with zero indicating longer CoA and 1 indicating discrete COA
x50                         = 0.1

AO_manip_par                = [length_id,scale_id,long_asym_id,control_point_id,steepness,x50]

# other local modules
vmanip_dir                   = cvsim + "modules/"
#print("scale_ctgr:")
#print(vmanip_dir)
try:
    sys.path.insert(1, vmanip_dir)
except:
    print("Can't find the modules/graphics package. this package is orginialy from simvascular repository: SimVascular-Tests > new-api-tests > graphics")
import scale_ctgr as sc

sc.main(vtp_file_name,ctgr_file_name,AO_manip_par)
