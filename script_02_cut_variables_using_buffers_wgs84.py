# cutting variables (tree cover from the year 2000 and temporal series of deforestation) for the 
# NEOTROPICAL region using buffers in WGS84

# open Python
python

# import modules
import os, fnmatch, lib
import numpy as np
import grass.script as grass
from grass.pygrass.modules.shortcuts import general as g
from grass.pygrass.modules.shortcuts import vector as v
from grass.pygrass.modules.shortcuts import raster as r

#---------------------------------------
# The code below assumes you have already loaded the treecover and deforestation datasets 
# from Global Forest Change (Hansen, 2000), loaded the tiles in a GRASS GIS location, in the
# mapset PERMANENT, and made a mosaic out of each of them.
#
# The following steps will be made in a mapset called "cut_variables_using_buffers".

#---------------------------------------
# Change to a new mapset

mapset_name = 'cut_variables_using_buffers'
g.mapset(mapset = mapset_name, flags = '-c') #-c to create

#---------------------------------------
# Import vector of points and make buffer
#
# Each point correspond to the sampling location of an ecological community
# We load them and make a 5km buffer around each point

# folder
folder_path = r'E:\World_landscape_metrics_master_Africa\01_data\community_locations_africa'
os.chdir(folder_path) # Change to this folder

# import points
v.in_ogr(input = 'comm_data_neotro_checked_2020_d11_06.shp', 
	output = 'comm_data_neotro_checked_2020_d11_06', overwrite = True)
        grass.run_command('v.import', input = i, output = name, overwrite = True) # Import maps


# make buffer of 5km
# 1km (approx, in reality 900m) = 30 arcsec = 0.008333 degrees
# 5km = 0.045 degrees (approx)
v.buffer(input = 'comm_data_neotro_checked_2020_d11_06', 
	output = 'buffers_5km_comm_data_neotro_checked_2020_d11_06',
	type = 'point', distance = 0.045, flags = 't') 

#---------------------------------------
# cutting variables using buffers
#
# Here we cut the tree cover data from GFW to each buffer.
# Then we set as 0 the tree cover of areas deforested until the correspondent year of the sampling
# at each point, and create binary forest/non-forest maps using the threshold or tree cover
# > 70, 80, and 90.

# years for forest prop

# read all lines, column sampling_y
years = grass.read_command('v.db.select', map = 'buffers_5km_comm_data_neotro_checked_2020_d11_06',
 columns = 'sampling_y')
# transforms into list, removes the first element which is the title of the column
years = years.replace('\r', '').split('\n')[1:-1]
# transforms into numeric with only two digits
years = [int(i[2:]) for i in years]
# consider as 0 all years before 2000
for i in range(len(years)):
  if years[i] > 20:
    years[i] = 0

# community codes
comm_code = grass.read_command('v.db.select', map = 'buffers_5km_comm_data_neotro_checked_2020_d11_06',
 columns = 'comm_code')
comm_code = comm_code.replace('\r', '').split('\n')[1:-1]

# list of buffers
buffer_index = range(len(years))

# region aligned to this map
map_for_define_region = 'Neotropic_Hansen_percenttreecoverd_2000_wgs84@PERMANENT'
# input vector with buffers
vector = 'buffers_5km_comm_data_neotro_checked_2020_d11_06'

# For each buffer
for i in buffer_index:
    
  print i, comm_code[i], years[i]
    
  # select feature
  v.extract(input = vector, output = 'vector_cat', where = 'cat = ' + str(i+1), 
    flags = 't', overwrite = True, quiet = True)
  # define region
  g.region(vector = 'vector_cat', align = map_for_define_region, flags = 'p')
  # use vector as a mask
  r.mask(vector = 'vector_cat', overwrite = True, quiet = True)
        
  # Cut maps
  
  # tree cover with zero where there was deforestation
  expr = comm_code[i] + '_treecover_GFW_2000_deforestation = if(Neotropical_Hansen_treecoverlossperyear_wgs84_2017@PERMANENT > 0 && '+ \
  'Neotropical_Hansen_treecoverlossperyear_wgs84_2017@PERMANENT < ' + str(years[i]) + ', 0, Neotropic_Hansen_percenttreecoverd_2000_wgs84@PERMANENT)'
  r.mapcalc(expr, overwrite = True)
  
  # thresholds for binary values of natural vegetation
  thresholds = [70, 80, 90]
    
  # loop to cut for each one and account for deforestation
  for tr in thresholds:
    
    # Hansen bin
    r.mapcalc(comm_code[i]+'_treecover_GFW_2000_deforestation_threshold'+str(tr)+'_binary = if('+comm_code[i]+'_treecover_GFW_2000_deforestation > '+str(tr)+', 1, 0)', 
      overwrite = True)
         
  # remove mask and vector_cat to avoid problems
  r.mask(flags = 'r')
  g.remove(type = 'vector', name = 'vector_cat', flags = 'f')


#---------------------------------------
# exporting all output

# output folder
pa = r'D:\bernardo\00_academico\01_artigos\ms_Lucas_world_landscape_metrics\maps'
os.chdir(pa)

# list maps
list_maps = grass.list_grouped(type = 'raster', pattern = 'com_*')[mapset_name]

# export
for i in list_maps:
  
  # region
  g.region(raster = i)
  # export
  r.out_gdal(input = i, output = i + '_cgs_wgs84.tif', 
    createopt = 'COMPRESS=DEFLATE,TFW=YES', overwrite = True, flags = 'f')

        
  
# cutting variables for the CENTRAL ÁFRICA region using buffers in WGS84

# open Python
python

# import modules
import os, fnmatch, lib
import numpy as np
import grass.script as grass
from grass.pygrass.modules.shortcuts import general as g
from grass.pygrass.modules.shortcuts import vector as v
from grass.pygrass.modules.shortcuts import raster as r

#---------------------------------------
# The code below assumes you have already loaded the treecover and deforestation datasets 
# from Global Forest Watch (Hansen, 2000), loaded the tiles in a GRASS GIS location, in the
# mapset PERMANENT, and made a mosaic out of each of them.
#
# The following steps will be made in a mapset called "cut_variables_using_buffers".

#---------------------------------------
# Change to a new mapset

mapset_name = 'cut_variables_using_buffers_africa'
g.mapset(mapset = mapset_name, flags = 'c') #-c to create

#---------------------------------------
# Import vector of points and make buffer
#
# Each point correspond to the sampling location of an ecological community
# We load them and make a 5km buffer around each point

# folder
folder_path = r'E:\World_landscape_metrics_master_Africa\01_data\community_locations_africa'
os.chdir(folder_path) # Change to this folder

# import points
v.in_ogr(input = 'comm_data_africa_checked_2020_d08_07.shp', 
  output = 'comm_data_africa_checked_2020_d08_07', overwrite = True)
grass.run_command('v.import', input = i, output = name, overwrite = True) # Import maps

folder_path_cover = r'E:\04_new_grassdb_africa_treecover_loss_v4'
os.chdir(folder_path_cover)

#import tree cover raster
r.in_gdal(input = 'Hansen_treecover_2000_30m_mosaic_africa.tif', output = 'Hansen_treecover_2000_30m_mosaic_africa', overwrite = True)

#import forest loss raster
r.in_gdal(input = 'Hansen_forest_loss_00_18_mosaic_africa.tif', output = 'Hansen_forest_loss_00_18_mosaic_africa', overwrite = True)

#r.external(input = 'Hansen_treecover_2000_30m_mosaic_africa.tif', source = r'E:\04_new_grassdb_africa_treecover_loss_v4', output = 'Hansen_treecover_2000_30m_mosaic_africa')



# make buffer of 5km
# 1km (approx, in reality 900m) = 30 arcsec = 0.008333 degrees
# 5km = 0.045 degrees (approx)
v.buffer(input = 'comm_data_africa_checked_2020_d08_07', 
  output = 'buffers_5km_comm_data_africa_checked_2020_d08_07',
  type = 'point', distance = 0.045, flags = 't')

#---------------------------------------
# cutting variables using buffers
#
# Here we cut the tree cover data from GFW to each buffer.
# Then we set as 0 the tree cover of areas deforested until the correspondent year of the sampling
# at each point, and create binary forest/non-forest maps using the threshold or tree cover
# > 70, 80, and 90.

# years for forest prop

# read all lines, column sampling_y
years = grass.read_command('v.db.select', map = 'buffers_5km_comm_data_africa_checked_2020_d08_07',
 columns = 'sampling_y')
# transforms into list, removes the first element which is the title of the column
years = years.replace('\r', '').split('\n')[1:-1]
# transforms into numeric with only two digits
years = [int(i[2:]) for i in years]
# consider as 0 all years before 2000
for i in range(len(years)):
  if years[i] > 20:
    years[i] = 0

# community codes
comm_code = grass.read_command('v.db.select', map = 'buffers_5km_comm_data_africa_checked_2020_d08_07', columns = 'comm_code')
comm_code = comm_code.replace('\r', '').split('\n')[1:-1]

# list of buffers
buffer_index = range(len(years))


# region aligned to this map
map_for_define_region = 'Hansen_treecover_2000_30m_mosaic_africa'
# input vector with buffers
vector = 'buffers_5km_comm_data_africa_checked_2020_d08_07'

# For each buffer
for i in buffer_index:
    
  print(i, comm_code[i], years[i])
    
  # select feature
  v.extract(input = vector, output = 'vector_cat', where = 'cat = ' + str(64+1), flags = 't', overwrite = True, quiet = True)
  # define region
  g.region(vector = 'vector_cat', align = map_for_define_region, flags = 'p')
  # use vector as a mask
  r.mask(vector = 'vector_cat', overwrite = True, quiet = True)
        
  # Cut maps

  # tree cover with zero where there was deforestation
expr = comm_code[64] + '_treecover_GFW_2000_deforestation = if(Hansen_forest_loss_00_18_mosaic_africa > 0 && '+ \
'Hansen_forest_loss_00_18_mosaic_africa < ' + str(years[64]) + ', 0, Hansen_treecover_2000_30m_mosaic_africa)'
r.mapcalc(expr, overwrite = True)
  
  # thresholds for binary values of natural vegetation
  thresholds = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

  # loop to cut for each one and account for deforestation
  for tr in thresholds:
    
    # Hansen bin
    r.mapcalc(comm_code[64]+'_treecover_GFW_2000_deforestation_threshold'+str(tr)+'_binary = if('+comm_code[64]+'_treecover_GFW_2000_deforestation > '+str(tr)+', 1, 0)', 
      overwrite = True)
         
  # remove mask and vector_cat to avoid problems
  r.mask(flags = 'r')
  g.remove(type = 'vector', name = 'vector_cat', flags = 'f')

  #---------------------------------------
# exporting all output

# output folder
pa = r'E:\World_landscape_metrics_master_Africa\01_data\forest_maps_cut_by_buffer'
os.chdir(pa)

# list maps
list_maps = grass.list_grouped(type = 'raster', pattern = 'com_*')[mapset_name]

# export
for i in list_maps:
  
  # region
  g.region(raster = i)
  # export
  r.out_gdal(input = i, output = i + '_cgs_wgs84.tif', createopt = 'COMPRESS=DEFLATE,TFW=YES', overwrite = True, flags = 'f')
