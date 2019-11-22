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
import subprocess
#import arcpy
#from arcpy import env
#arcpy.CheckOutExtension("spatial")

path="\\\\10.72.26.46\\irisnas6\\Data\\MODIS_tile\\02region\\EastAsia\\MYD13A2\\"
#Extent = "112.99111237331 23.9931929698016 146.998439892367 48.0049852944791"
#mask = "\\\\10.72.26.56\\irisnas5\\Data\\Aerosol\\SRTM\\SRTM_DEM_mask.tif"

YEARS = [2019]
for i in YEARS:
    print(i)
    #env.workspace=""+path+"\\01mosaic\\"+str(i)+""
    workspace = os.path.join(path, "01mosaic", str(i))
    flist = glob.glob(os.path.join(workspace, "*.tif"))
    flist.sort()
    nfile = len(flist)
    npath = len(env.workspace)

    for j in range(4,nfile): # range(0,nfile):
        in_raster = flist[j]
        out_raster = os.path.basename(a)
        c = os.path.join(path, "02prj_GCS_WGS84", str(j), f"p_{b}")
        d = os.path.join(path, "03mask", str(i), f"m_{b}")

        # Process: Project Raster
        #tempEnvironment0 = arcpy.env.snapRaster
        #arcpy.env.snapRaster = mask
        #tempEnvironment1 = arcpy.env.extent
        #arcpy.env.extent = Extent
        out_coor_system = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
        in_coor_system = "PROJCS['Unknown_datum_based_upon_the_custom_spheroid_Sinusoidal',GEOGCS['GCS_Unknown_datum_based_upon_the_custom_spheroid',DATUM['D_Not_specified_based_on_custom_spheroid',SPHEROID['Custom_spheroid',6371007.181,0.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Sinusoidal'],PARAMETER['false_easting',0.0],PARAMETER['false_northing',0.0],PARAMETER['central_meridian',0.0],UNIT['Meter',1.0]]"
        cell_size = "1.02308446206551E-02 1.02308446206551E-02"
        #arcpy.ProjectRaster_management(a, c, out_coor_system, "NEAREST", cell_size, "", "", in_coor_system)
        # ProjectRaster(in_raster, out_raster, out_coor_system, {resampling_type}, {cell_size}, {geographic_transform}, {Registration_Point}, {in_coor_system}, {vertical})

        cmd = ["gdalwarp", "-r", "near",
               "-s_srs", in_coor_system, "-t_src", out_coor_system,
               "-ts", cell_size, in_raster, out_raster]
        subprocess.call(cmd)
        #arcpy.env.snapRaster = tempEnvironment0
        #arcpy.env.extent = tempEnvironment1
        # Process: Extract by Mask
        #arcpy.gp.ExtractByMask_sa(c, mask, d)
        print(b)
