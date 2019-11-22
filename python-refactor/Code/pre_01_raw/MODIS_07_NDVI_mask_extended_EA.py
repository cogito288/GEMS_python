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
mask = "\\\\10.72.26.56\\irisnas5\\Data\\mask\\v_rec_N50W110S20E150.shp"

YEARS = [2019]
for i in YEARS:
    print(i)
    workspace=os.path.join(path, "02prj_GCS_WGS84", str(i))
    flist = glob.glob(os.path.join(workspace, "*.tif"))
    flist.sort()
    nfile = len(flist)
    npath = len(workspace)
    for j in range(4,nfile): # range(0,nfile):
        in_raster = flist[j]
        in_raster_name = os.path.basenam(a) #a[npath+3:]
        out_raster = os.path.join(path, "03mask", str(i), f"m_{b}")

        #tempEnvironment0 = arcpy.env.snapRaster
        arcpy.env.snapRaster = a
        # Process: Extract by Mask
        #arcpy.gp.ExtractByMask_sa(a, mask, c)
        # ExtractByMask_sa <in_raster> <in_mask_data> <out_raster>
        arcpy.env.snapRaster = tempEnvironment0
        cmd = ["gdal_calc.py", "-A", in_raster, "--outfile", out_raster, 
        print(in_raster_name)
