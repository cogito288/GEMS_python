# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# LC_to_bin_by_class.py
# Author: Minso Shin
# Description: Make binary classification data by class from reclassified data
# ---------------------------------------------------------------------------
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

path_modis="\\\\10.72.26.46\\irisnas6\\Data\\MODIS_tile\\02region\\EastAsia\\MCD12Q1\\03masked_N50W110S20E150\\"
path_data="\\\\10.72.26.56\\irisnas5\\Data\\"
path_work=path_data+"pre\\MODIS\\MCD12Q1\\"
class_name = ["forest","shrub","savannas","grass","wetland","crop","urban","snow","barren","water"]


YEARS = range(2001, 2018)
for yr in YEARS:
    #env.workspace=""+path_work+""
    src_dataset = os.path.join(path_modis, f'm_MODIS_LC_500m_{yr}.tif)
    dst_dataset = os.path.join(path_work, '01_reclassified', f'reclass_MODIS_LC_500m_EA_{yr}.tif')

    # Process: Reclassify
    # Reclassify_sa (in_raster, reclass_field, remap, out_raster, missing_values)
    # in_raster : The input raster to be reclassified.
    # reclass_field: Field denoting the values that will be reclassified.
    # remap:  RemapRange and RemapValue
    #       The remap list is composed of three components: From, To, and New values. Each row in the remap list is separated by a semicolon, and the three components are separated by spaces. For example, "0 5 1;5.01 7.5 2;7.5 10 3".
    # out_raster: The raster to be created.
    # Change missing values to NoData (Optional): DATA — A keyword signifying that if any cell location on the input raster contains a value that is not present or reclassed in a remap table, the value should remain intact and be written for that location to the output raster.
    # arcpy.gp.Reclassify_sa(a, "Value", "1 1;2 1;3 1;4 1;5 1;6 2;7 2;8 3;9 3;10 4;11 5;12 6;13 7;14 6;15 8;16 9;17 10;NODATA 10", b, "DATA")
    expr = "1*(A==1)+1*(A==2)+1*(A==3)+1*(A==4)+1*(A==5)"
    expr += "+2*(A==6)+2*(A==7)"
    expr += "+3*(A==8)+3*(A==9)"
    expr += "+4*(A==10)+5*(A==11)+5*(A==12)+6*(A==13)"
    cmd = ["gdal_calc.py", "-A", src_dataset, f"--outfile={dst_dataset}", "--cal", expr]
    print (cmd)
    subprocess.call(cmd)
    expr = None

    for ii in range(0,10):
        dst_dataset02 = os.path.join(path_work, "02_LC_binary", str(yr), f"MODIS_LC_500m_EA_{class_name[ii]}_{yr}.tif")
        expr = f"1*(A=={ii+1})"
        cmd = ["gdal_calc.py", "-A", dst_dataset, f"--outfile={dst_dataset02}", "--cal", expr]
        #arcpy.gp.RasterCalculator_sa("Con(\""+b+"\"=="+str(ii+1)+",1,0)", c)
        print (cmd)
        subprocess.call(cmd)
        

