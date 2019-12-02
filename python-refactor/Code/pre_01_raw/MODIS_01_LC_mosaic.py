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
data_base_dir = os.path.join('/', 'media', 'sf_GEMS', 'Data')
raw_modis_path = os.path.join(data_base_dir, 'Raw', 'MODIS', 'MCD12Q1') 
path_mosaic = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS', '01mosaic') #workspace = os.path.join(work_path, '01_mosaic')
tmpdirname = tempfile.TemporaryDirectory(dir=base_dir)  # should call clean up to delete
#path_data="\\\\10.72.26.46\\irisnas6\\Data\\MODIS_tile\\"
#path_work=path_data+"02region\\EastAsia\\MCD12Q1\\"
#path_raw = path_data+"00raw\\MCD12Q1\\"

flist = glob.glob(os.path.join(raw_modis_path, "*.hdf"))
flist = [os.path.basename(f) for f in flist]
flist.sort()
nfile = len(flist)

for k in range(0,nfile,14):
    flist_temp = flist[k:k+14]
    yr = flist_temp[0][9:13]
    #print (flist_temp[0])
    #print (yr)

    for m in range(0,14):
        # Extract Subdataset
        fname = flist_temp[m]
        dst_dataset = os.path.join(tmpdirname.name, f"LC_{yr}_{m+1}.tif")
        #print (fname, dst_dataset)
        
        gdal_dataset = gdal.Open(os.path.join(raw_modis_path, fname))
        src_dataset = gdal_dataset.GetSubDatasets()[0][0]
        subprocess.call(["gdal_translate", dset, dst_dataset])
        
        if m==0:
            input_files = [dst_dataset]
        else:
            input_files.append(dst_dataset)
    
    # Mosaic
    matlab.check_make_dir(path_mosaic) # debugging
    fname = f"EA_MCD12Q1_mosaic_{yr}.tif"
    out_filename = os.path.join(path_mosaic, fname)
    pixel_type = 'Int16'
    cmd = ["gdal_merge.py", "-init", "255", "-ot", pixel_type, "-o", out_filename]
    cmd = cmd + input_files
    subprocess.call(cmd)
    
    tmpdirname.cleanup()
    print(yr)
