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

#--------------------------------------------------------

# B:======================================================= START

import os
import sys
import xml.etree.ElementTree as et
import vtk

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

def read_ctgr_file(file_name, contour_scale, contour_ids):
    
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

        for contour_t in contour_group_t.iter('contour'):
            cid = contour_t.attrib["id"]
            contour = Contour(cid)
            scaled_contour = Contour(cid)
            if (len(contour_ids) != 0) and (cid not in contour_ids):
                scale = 1.0 
            else:
                scale = contour_scale 
            scale = contour_scale 

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

def main(vtp_file_name,ctgr_file_name,contour_scale, contour_ids):

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
    contour_groups, scaled_contour_groups = read_ctgr_file(file_name, contour_scale, contour_ids)

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
