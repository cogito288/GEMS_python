### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import scipy.io as sio
import numpy as np
import glob
import time
import h5py 
import pygrib
import re
from osgeo import gdal
import tempfile
#import arcpy
#from arcpy import env


### Setting path
data_base_dir = os.path.join('/','share','irisnas5','GEMS','GEMS_python')
path_mosaic = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS')
mask = os.path.join('/share', 'irisnas5', 'Data', 'mask', 'r_rec_N50W110S20E150.tif')
#tmpdirname = tempfile.TemporaryDirectory(dir=base_dir)  # should call clean up to delete
#path_modis="\\\\10.72.26.46\\irisnas6\\Data\\MODIS_tile\\02region\\EastAsia\\MCD12Q1\\"


flist = glob.glob(os.path.join(path_mosaic, '01mosaic', "*.tif"))
flist = [os.path.basename(f) for f in flist]
flist.sort()
nfile = len(flist)
print (flist)
#npath = len(path_modis+"\\01mosaic\\")

for fname in flist:
    src_dataset = os.path.join(path_mosaic, '01mosaic', fname) # a
    last_num = src_dataset[-8:] # b e.g. 2827.hdf
    print (src_dataset)
    
    matlab.check_make_dir(os.path.join(path_mosaic, '02prj_GCS_WGS84')) # debugging
    matlab.check_make_dir(os.path.join(path_mosaic, '03masked_N50W110S20E150')) # debugging
    
    dst_dataset02 = os.path.join(path_mosaic, '02prj_GCS_WGS84', f'GCS_EA_MCD12Q1_{last_num}') # c
    dst_dataset03 = os.path.join(path_mosaic, '03masked_N50W110S20E150', f'm_MODIS_LC_500m_{last_num}') # d

    #tempEnvironment0 = arcpy.env.snapRaster
    # Snap Raster—Sets a raster that is used to define the cell alignment of an output raster.
    # arcpy.env.snapRaster = mask
    
    # Process: Project Raster
    cell_size= ["5.11542231032757E-03", "5.11542231032757E-03"]
    out_coor_system = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
    cmd = ["gdalwarp", "-r", "near", "-to", out_coor_system]
    cmd += (["-ts"] + cell_size)
    cmd += [src_dataset, dst_dataset02]
    #print (cmd)
    subprocess.call(cmd)
    
    """
    #arcpy.ProjectRaster_management(in_raster=a, 
    #                               out_raster=c,
    #                               out_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]",
    #                               resampling_type="NEAREST",
    #                               cell_size="5.11542231032757E-03 5.11542231032757E-03",
    #                               geographic_transform="",
    #                               Registration_Point="",
                                   in_coor_system="PROJCS['Unknown_datum_based_upon_the_custom_spheroid_Sinusoidal',GEOGCS['GCS_Unknown_datum_based_upon_the_custom_spheroid',DATUM['D_Not_specified_based_on_custom_spheroid',SPHEROID['Custom_spheroid',6371007.181,0.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Sinusoidal'],PARAMETER['false_easting',0.0],PARAMETER['false_northing',0.0],PARAMETER['central_meridian',0.0],UNIT['Meter',1.0]]")
    """
    # Process: Extract by Mask
    cmd = ["gdaltindex", "temp_mask.shp", mask]
    print (cmd)
    subprocess.call(cmd)

    cmd = ["gdalwarp", "-cutline", "temp_mask.shp", 
           dst_dataset02, dst_dataset03]
    subprocess.call(cmd)

    cmd = ["rm", "temp_mask.shp"]
    subprocess.call(cmd)
    #arcpy.gp.ExtractByMask_sa(dst_dataset02, mask, dst_dataset03)
    #arcpy.env.snapRaster = tempEnvironment0
    
    print(last_num)
