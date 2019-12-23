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

data_base_dir = os.path.join(project_path, 'Data')
path_read = os.path.join(data_base_dir, 'Raw', 'MODIS', 'MYD13A2')
path_write = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS', 'MYD13A2', '01mosaic')
tmpdirname = tempfile.TemporaryDirectory(dir=base_dir)  # will be deleted

YEARS = [2016]
for yr in YEARS: 
    print(yr)
    flist = glob.glob(os.path.join(path_read, str(yr), '*.hdf'))
    flist.sort()
    nfile = len(flist)
    for k in range(0,nfile,14): 
        flist_temp = flist[k:k+14]
        doy = os.path.basename(flist_temp[0])[13:16]
        input_files = []
        for m in range(0,14):
            src_dataset = flist_temp[m]
            gdal_dataset = gdal.Open(os.path.join(path_read, src_dataset))
            src_dataset = gdal_dataset.GetSubDatasets()[0][0]
            dst_dataset = os.path.join(tmpdirname.name, f"NDVI_{doy}_{m+1}.tif")
            cmd = ["gdal_translate", src_dataset, dst_dataset]
            subprocess.call(cmd)
            
            dst_dataset = os.path.join(f"NDVI_{doy}_{m+1}.tif")
            cmd = ["gdal_translate", src_dataset, dst_dataset]
            subprocess.call(cmd)
            
            input_files.append(dst_dataset)
        
        dst_fname = os.path.join(path_write, str(yr), f"MYD13A2_{yr}_{doy}.tif")
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
        #tmpdirname.cleanup()
        print (os.path.basename(dst_fname))
        print(doy)