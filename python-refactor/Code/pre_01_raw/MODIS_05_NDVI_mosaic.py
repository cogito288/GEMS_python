import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import glob
import tempfile
import subprocess
from osgeo import gdal
import time

data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_myd_raw = os.path.join(data_base_dir, 'Raw', 'MODIS', 'MYD13A2')
path_myd_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS', 'MYD13A2')
tmpdirname = tempfile.TemporaryDirectory(dir=base_dir)  # will be deleted

YEARS = [2016]
for yr in YEARS: 
    print(yr)
    flist = glob.glob(os.path.join(path_myd_raw, str(yr), '*.hdf'))
    flist.sort()
    nfile = len(flist)
    for k in range(0,nfile,14): 
        flist_temp = flist[k:k+14]
        doy = os.path.basename(flist_temp[0])[13:16]
        input_files = []
        for m in range(0,14):
            dst_dataset = os.path.join(tmpdirname.name, f"NDVI_{doy}_{m+1}.tif")
            
            src_dataset = flist_temp[m]
            print (os.path.join(path_myd_raw, src_dataset))
            gdal_dataset = gdal.Open(os.path.join(path_myd_raw, src_dataset))
            src_dataset = gdal_dataset.GetSubDatasets()[0][0]
            cmd = ["gdal_translate", src_dataset, dst_dataset]
            subprocess.call(cmd)
            input_files.append(dst_dataset)
        tStart = time.time()
        dst_fname = os.path.join(path_myd_processed, '01mosaic', str(yr), f"MYD13A2_{yr}_{doy}.tif")
        matlab.check_make_dir(os.path.dirname(dst_fname)) # debugging
        pixel_type = 'Int16'
        in_nodata_val = "-3000"
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
        print(doy)