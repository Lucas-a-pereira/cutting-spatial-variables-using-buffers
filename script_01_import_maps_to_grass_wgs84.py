# Importing tiles of tree cover from the year 2000 from the Global Forest Change
# and combining them in a mosaic

python

# Load modules
import os
import subprocess
import grass.script as grass
from grass.pygrass.modules.shortcuts import general as g
from grass.pygrass.modules.shortcuts import vector as v
from grass.pygrass.modules.shortcuts import raster as r


# Import map
folder_path = r'C:\Grassdata\Hansen_treecover2000_30m_neotropics'
os.chdir(folder_path) # Change to this folder
files = os.listdir(folder_path) # List files in the folder
for i in files:
    if i[-3:] == 'tif': # Select tif files
        print i
        name = i.replace('.tif', '_rast')  
        grass.run_command('r.import', input = i, output = name, overwrite = True) # Import maps

# Mosaic of tree cover maps

# List of maps
maps_cover = grass.list_grouped('rast')['PERMANENT']

# Region of study
grass.run_command('g.region', raster = map_cover, flags = 'ap')

# Combine maps
treecover_map_mosaic = 'Hansen_treecover_2000_30m_tif_exp'
grass.run_command('r.patch', input = maps_cover, output = treecover_map_mosaic, overwrite = True)

# Delete input maps
grass.run_command('g.remove', type = 'raster', flags = 'f')