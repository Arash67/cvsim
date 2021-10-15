
# This ensures that even when current sizes are not a perfect
# fraction of the requested size, we can generate an image of
# exact size.

from paraview.vtk.util.misc import vtkGetTempDir
from paraview.simple import *
from os.path import join

def layoutprep(viewsize,bgcolor):
  # Create a new 'Render View'
  renderView1 = CreateView('RenderView')
  # renderView1.ViewSize = [300, 259]
  renderView1.ViewSize = viewsize
  # renderView1.Background = [0.32, 0.34, 0.43]
  renderView1.Background = bgcolor
  
  AssignViewToLayout(renderView1)

  layout1 = GetLayout()
  layout1.SeparatorWidth = 2
  layout1.SplitVertical(0, 0.5)
  # RenderAllViews()
  layout = layout1
  return layout

def vtpscreenshot(vtpname,viewsize,bgcolor,resolution,pngname):
  # read the file
  vtpfile           = XMLPolyDataReader(FileName=vtpname)
  # prepare the layout
  layout            = layoutprep(viewsize,bgcolor)
  SaveScreenshot(pngname, layout, SaveAllViews=1, ImageResolution=resolution)
    
filename = ['/home/agh/github/outofsource/cvsimout/mesh-complete.exterior.vtp']
