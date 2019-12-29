### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import glob
from osgeo import gdal
import subprocess
import tempfile
import time

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_mcd_raw = os.path.join(data_base_dir, 'Raw', 'MODIS', 'MCD12Q1')  
path_mcd_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS', 'MCD12Q1')
tmpdirname = tempfile.TemporaryDirectory(dir=base_dir)  # will be deleted

flist = glob.glob(os.path.join(path_mcd_raw, "*.hdf"))
flist.sort()
nfile = len(flist)

for k in range(0,nfile,14):
    flist_temp = flist[k:k+14]
    yr = os.path.basename(flist_temp[0])[9:13]
    
    input_files = [] 
    for m in range(0,14):
        fname = flist_temp[m]
        dst_dataset = os.path.join(tmpdirname.name, f"LC_{yr}_{m+1}.tif")
        
        gdal_dataset = gdal.Open(os.path.join(path_mcd_raw, fname))
        src_dataset = gdal_dataset.GetSubDatasets()[0][0]
        subprocess.call(["gdal_translate", src_dataset, dst_dataset])
        input_files.append(dst_dataset)
    
    # Mosaic
    tStart = time.time()
    matlab.check_make_dir(os.path.join(path_mcd_processed, '01mosaic')) # debugging
    dst_fname = os.path.join(path_mcd_processed, '01mosaic', f"EA_MCD12Q1_mosaic_{yr}.tif")
    pixel_type = 'Int16'
    in_nodata_val = "255"
    out_nodata_val = "-9999"
    compression = "COMPRESS=LZW"
    
    cmd = ["gdal_merge.py", "-n", in_nodata_val, "-a_nodata", out_nodata_val, "-ot", pixel_type]
    cmd += ["-co", compression]
    cmd += ["-o", dst_fname]
    cmd += input_files
    subprocess.call(cmd)
    
    tmpdirname.cleanup()
    tElapsed = time.time() - tStart
    print (f'time taken : {tElapsed}')
    print (os.path.basename(dst_fname))
    