# A:======================================================= GENERAL
# The purpose is to import a *.ctgr segmentation scale it and write it into *.ctgr 
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
#               Aortic isthmus hypoplasia           (AIH)
#               
#--------------------------------------------------------

# B:======================================================= START

import os
import sys
import xml.etree.ElementTree as et
import vtk
import math
import numpy as np

# C:======================================================= CLASSES

class ContourGroup(object):
    ''' The ContourGroup class is used to represent a SimVascular contour group.
    '''
    def __init__(self, path_name):
        self.id = path_name
        self.contours = []

class Contour(object):
    ''' The Contour class is used to represent a SimVascular contour.
    '''
    def __init__(self, cid):
        self.id = cid
        self.coordinates = []

# D:======================================================= FUNCTIONS

def sigmoid(scale_factor,number_of_contours,current_contour_number,steepness,x50):
    # L : amplituded must be between indicating diameter reduction (between 0 and one) or expantion ratio (larger than one)
    L                                   = scale_factor
    # k : steepness 
    k                                   = steepness 
    # x : current disrtance from the left end
    x                                   = current_contour_number
    # x0: x at 50% drop used to include longitudinal asymetry of how close to the narrwoing the 50% drop is current assumtion is scaled range of 12 woth 50% happening at 6
    # x50                                 = 0.2             
    x0                                  = number_of_contours * x50
    
    print(x-x0)
    if scale_factor < 1:
        # contraction
        temp                            = 1 - (L / (1 + math.exp(-k*(x-x0))))
    else:
        # explantion
        temp                            = 1 + ((L-1) / (1 + math.exp(-k*(x-x0))))
    return temp 

def scale_factor_insert(scale_factor,scale_factor_local,start_id,stop_id):
    indx_counter = 0
    for sid in range(len(scale_factor)-1):
        if sid > (start_id -1):
            if sid < stop_id-1:
                scale_factor[sid]           = scale_factor_local[indx_counter]
                indx_counter            += 1
            else:
                scale_factor[sid]       = 1
        else:
            scale_factor[sid]           = 1
    # print("number of updated contours: {0:d}".format(indx_counter))
    return scale_factor

def scale_factor_test(number_of_contours,scale_par):
    
    # check
    print("scale_factor_test inputs:")
    print("contour numbers: {}".format(number_of_contours))
    print("scale_par: ")
    print(scale_par)
    
    # function
    length_id = scale_par[0]
    maximum_diameter_change = scale_par[1]
    asymetry_coef = scale_par[2]
    location_id = scale_par[3]
    steepness = scale_par[4]
    x50 = scale_par[5]
    scale_factor                        = []
    for i in range(number_of_contours): scale_factor.append(float(1))
    if (length_id % 2 !=0): 
        length_id -=1
    half_num                        = int(length_id/2)
    center_id                       = location_id
    start_id                        = center_id - half_num
    stop_id                         = start_id + length_id
    center_dislocation              = int(half_num * asymetry_coef)
    center_id                       = center_id + center_dislocation
    number_of_proximal_contours     = center_id - start_id
    number_of_distal_contours       = stop_id - center_id
    print("Start ID: {0:d}".format(start_id))
    print("Center ID: {0:d}".format(center_id))
    print("Stop ID: {0:d}".format(stop_id))
    prox_scale_factors              = []
    dist_scale_factors              = []
    print("Total contour numbers: {0:d}".format(number_of_contours))
    print("Total modified contours: {0:d}".format(length_id))
    print("Proximal contour numbers: {0:d}".format(number_of_proximal_contours))
    print("Distal contour numbers: {0:d}".format(number_of_distal_contours))
    for i in range(number_of_proximal_contours):
        prox_scale_factors.append(sigmoid(maximum_diameter_change,number_of_proximal_contours,i+1,steepness,x50))
    for s in range(number_of_distal_contours):
        dist_scale_factors.append(sigmoid(maximum_diameter_change,number_of_distal_contours,s,steepness,x50))
    # sort the scale lists
    dist_scale_factors                       = np.sort(dist_scale_factors)
    # sort in descending order
    # dist_scale_factors                     = np.sort(dist_scale_factors)[::-1] 
    print("Proximal scale factor list:")
    print(prox_scale_factors)
    print("Distal scale factor list:")
    print(dist_scale_factors)
    scale_factor_local                      = np.concatenate((prox_scale_factors,dist_scale_factors),axis=None)
    indx_counter                            = 0
    scale_factor                = scale_factor_insert(scale_factor,scale_factor_local,start_id,stop_id)
    
    # check
    print("scale_factor_test outputs:")
    print(scale_factor)
    return scale_factor

def read_ctgr_file(file_name, scale_par):
    print(scale_par)
    # Remove 'format' tag from xml file.
    f = open(file_name, "r")
    lines = f.readlines()
    new_lines = []
    for line in lines:
      if '<format' not in line:
        new_lines.append(line)

    # Create string from xml file and parse it.
    xml_string = "".join(new_lines)
    tree = et.ElementTree(et.fromstring(xml_string))
    root = tree.getroot()

    ## Create contour groups.
    #
    
    contour_groups = []
    scaled_contour_groups = []
    for contour_group_t in root.iter('contourgroup'):
        path_name = contour_group_t.attrib["path_name"]
        contour_group = ContourGroup(path_name)
        scaled_contour_group = ContourGroup(path_name)
        num_contours = 0
        for i in contour_group_t.iter('contour'):num_contours += 1
        # print("number of contours: {}".format(num_contours))
        scale_factors                       = scale_factor_test(num_contours,scale_par)
        scale_factor_90perc_discrete_CoA = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.9433239795487032, 0.7916723051491159, 0.4830017348695068, 0.2276659584104389, 0.4830017348695068, 0.7916723051491159, 0.9433239795487032, 1, 1, 1, 1, 1, 1.0]
        scale_factor_70perc_discrete_CoA = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.9559186507601024, 0.8379673484493123, 0.5978902382318387, 0.3992957454303414, 0.5978902382318387, 0.8379673484493123, 0.9559186507601024, 1, 1, 1, 1, 1, 1.0]
        scale_factor_AIH                 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.8751300527975588, 0.75, 0.6248699472024412, 0.5498752445598426, 0.6248699472024412, 0.75, 0.8751300527975588, 1, 1, 1, 1, 1, 1, 1, 1.0]
        scale_factor_TAH                 = [1, 1, 1, 1, 1, 1, 1, 0.8170677955054003, 0.6829322044945996, 0.5805544747882927, 0.6829322044945996, 0.8170677955054003, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1.0]
        
        # CoA with TAH
        scale_factors = np.dot(scale_factors,scale_factor_TAH)
        # CoA with AIH
        # scale_factors = np.dot(scale_factors,scale_factor_AIH)
        # print("scale factor")
        # print(scale_factors)
        for contour_t in contour_group_t.iter('contour'):
            cid = contour_t.attrib["id"]
            contour = Contour(cid)
            scaled_contour = Contour(cid)
            # print("cid = {}".format(int(cid)))
            scale = scale_factors[int(cid)]

            ## Iterate over control points. 
            #
            # The first control point is the contour center.
            #
            for control_pts in contour_t.iter('control_points'):
                for i,point in enumerate(control_pts.iter('point')):
                    x = float(point.attrib['x'])
                    y = float(point.attrib['y'])
                    z = float(point.attrib['z'])
                    if i == 0:
                        cx = x
                        cy = y
                        cz = z
                        xs = x 
                        ys = y 
                        zs = z 
                    else:
                        xs = scale * (x - cx) + cx
                        ys = scale * (y - cy) + cy
                        zs = scale * (z - cz) + cz
                    point.attrib['x'] = str(xs)
                    point.attrib['y'] = str(ys)
                    point.attrib['z'] = str(zs)
            
            ## Iterate over contour points. 
            #
            for contour_pts in contour_t.iter('contour_points'):
                for point in contour_pts.iter('point'):
                    x = float(point.attrib['x'])
                    y = float(point.attrib['y'])
                    z = float(point.attrib['z'])
                    xs = scale * (x - cx) + cx
                    ys = scale * (y - cy) + cy
                    zs = scale * (z - cz) + cz
                    point.attrib['x'] = str(xs)
                    point.attrib['y'] = str(ys)
                    point.attrib['z'] = str(zs)
                    contour.coordinates.append([x,y,z])
                    scaled_contour.coordinates.append([xs,ys,zs])
            contour_group.contours.append(contour)
            scaled_contour_group.contours.append(scaled_contour)
            contour_groups.append(contour_group)
        scaled_contour_groups.append(scaled_contour_group)

    # Write the scaled file name.
    scaled_file_name = os.path.splitext(file_name)[0] + "-scaled.ctgr" 
    tree.write(scaled_file_name)

    return contour_groups, scaled_contour_groups

def read_vtp_file(file_name):
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(file_name)
    reader.Update()
    poly_data = reader.GetOutput()
    points = poly_data.GetPoints()
    num_points = points.GetNumberOfPoints()
    polygons = poly_data.GetPolys()
    num_polys = polygons.GetNumberOfCells()
    return poly_data

def create_contour_geometry(renderer, contour_group, color):
    for contour in contour_group.contours:
        coords = contour.coordinates
        num_pts = len(coords)
        # Create contour geometry points and line connectivity.
        points = vtk.vtkPoints()
        points.SetNumberOfPoints(num_pts)
        lines = vtk.vtkCellArray()
        lines.InsertNextCell(num_pts+1)
        n = 0
        for pt in coords:
            points.SetPoint(n, pt[0], pt[1], pt[2])
            lines.InsertCellPoint(n)
            n += 1
        #_for pt in coords
        lines.InsertCellPoint(0)
        geom = vtk.vtkPolyData()
        geom.SetPoints(points)
        geom.SetLines(lines)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(geom)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetLineWidth(4.0)
        actor.GetProperty().SetColor(color[0], color[1], color[2])
        renderer.AddActor(actor)

def create_graphics_geometry(geom):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(geom)
    mapper.SetScalarVisibility(False)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor

def main(vtp_file_name,ctgr_file_name,contour_scale):

    # Create renderer and graphics window.
    renderer = vtk.vtkRenderer()
    renderer_win = vtk.vtkRenderWindow()
    renderer_win.AddRenderer(renderer)
    renderer.SetBackground(0.5, 0.8, 0.8)
    renderer_win.SetSize(1000, 1000)
    renderer_win.Render()
    renderer_win.SetWindowName("Scale Contours")

    # Read surface .vtp file and create render geometry.
    surface = read_vtp_file(vtp_file_name)
    surface_geom = create_graphics_geometry(surface)
    surface_geom.GetProperty().SetOpacity(0.5)
    surface_geom.GetProperty().SetColor(0.8, 0.8, 0.8)
    renderer.AddActor(surface_geom)

    # Read the contours .ctgr file.
    contour_groups, scaled_contour_groups = read_ctgr_file(ctgr_file_name, contour_scale)

    # Create contour geometry.
    for contour_group in contour_groups:
        create_contour_geometry(renderer, contour_group, color=[0.0, 1.0, 0.0])
    for contour_group in scaled_contour_groups:
        create_contour_geometry(renderer, contour_group, color=[1.0, 0.0, 0.0])

    # Create a trackball interacter to transoform the geometry using the mouse.
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    interactor.SetRenderWindow(renderer_win)
    interactor.Start()

# main(vtp_file_name,ctgr_file_name,contour_scale, contour_ids)
