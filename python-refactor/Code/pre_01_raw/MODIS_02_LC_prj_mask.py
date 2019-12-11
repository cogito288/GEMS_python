### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import glob
import time 
from osgeo import gdal
import tempfile
import subprocess

### Setting path
data_base_dir = os.path.join(project_path, 'Data')
path_mosaic = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS')
mask = os.path.join(data_base_dir, 'raw', 'mask', 'r_rec_N50W110S20E150.tif')
#path_modis="\\\\10.72.26.46\\irisnas6\\Data\\MODIS_tile\\02region\\EastAsia\\MCD12Q1\\"

flist = glob.glob(os.path.join(path_mosaic, '01mosaic', "*.tif"))
flist.sort()
print (flist)

for src_dataset in flist:
    last_num = os.path.basename(src_dataset)[-8:] # b 2016.tif
    print (src_dataset)
    
    matlab.check_make_dir(os.path.join(path_mosaic, '02prj_GCS_WGS84')) # debugging
    matlab.check_make_dir(os.path.join(path_mosaic, '03masked_N50W110S20E150')) # debugging
    
    dst_dataset02 = os.path.join(path_mosaic, '02prj_GCS_WGS84', f'GCS_EA_MCD12Q1_{last_num}') # c
    dst_dataset03 = os.path.join(path_mosaic, '03masked_N50W110S20E150', f'm_MODIS_LC_500m_{last_num}') # d
    """
    gdalsrsinfo -o proj4 GCS_EA_MCD12Q1_2016.tif       
    '+proj=longlat +datum=WGS84 +no_defs '  
    gdalsrsinfo -o proj4 ../../Data/Preprocessed_raw/MODIS/01mosaic/EA_MCD12Q1_mosaic_2016.tif
    '+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs '    
    """

    cell_size = ["5.11542231032757E-03", "5.11542231032757E-03"]
    src_proj = ["+proj=sinu", "+lon_0=0", "+x_0=0", "+y_0=0", "+a=6371007.181", "+b=6371007.181", "+units=m", "+no_defs"]
    dst_proj = ["+proj=longlat", "+datum=WGS84", "+no_defs"]
    #gdalwarp -overwrite -r near -s_srs '+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs' -t_srs EPSG:4326 -tr  0.005 0.005 /home/cogito/GEMS_python/python-refactor/Data/Preprocessed_raw/MODIS/01mosaic/EA_MCD12Q1_mosaic_2016.tif /home/cogito/GEMS_python/python-refactor/Data/Preprocessed_raw/MODIS/02prj_GCS_WGS84/GCS_EA_MCD12Q1_2016.tif
    cmd = ["gdalwarp", "-overwrite", "-r", "near"]
    cmd += (["-s_srs"] + src_proj)
    cmd += (["-t_srs"] + dst_proj)
    cmd += (["-tr"] + cell_size)
    cmd += [src_dataset, dst_dataset02]

    print (cmd)
    subprocess.call(cmd)
    
    # Process: Extract by Mask
    #cmd = ["gdaltindex", "temp_mask.shp", mask]
    #print (cmd)
    #subprocess.call(cmd)

    #cmd = ["gdalwarp", "-cutline", "temp_mask.shp", 
    #       dst_dataset02, dst_dataset03]
    #subprocess.call(cmd)

    #cmd = ["rm", "temp_mask.shp"]
    #subprocess.call(cmd)
    #arcpy.gp.ExtractByMask_sa(dst_dataset02, mask, dst_dataset03)
    #arcpy.env.snapRaster = tempEnvironment0
    
    print(os.path.basename(src_dataset))
