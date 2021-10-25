# NOTE: add Path from pathlib, add additional notes heare if needed
from pathlib import Path
# define the local home and repository directories plus out of source directory for outputs not needed to be uploaded to the source repository 
home                    = str(Path.home())
cvsim                   = home + "/github/cvsim/"
cvsimout                = home + "/github/outofsource/cvsimout/"
input_dir                    = "data/input/"
output_dir                   = cvsimout

ctgr_file_name  = input_dir + "control_rabbit_32181_S01AO.ctgr"
vtp_file_name   = output_dir + "Case_1_AO_mesh_complete_exterior.vtp"

scale_factor = 0.7
contour_ids    = [5,6]
# other local modules
vmanip_dir                   = cvsim + "modules/"
print("control_point_manipulation:")
print(vmanip_dir)
try:
    sys.path.insert(1, vmanip_dir)
except:
    print("Can't find the modules/graphics package. this package is orginialy from simvascular repository: SimVascular-Tests > new-api-tests > graphics")
import scale_ctgr as sc

sc.main(vtp_file_name,ctgr_filename,scale_factor,contour_ids)
