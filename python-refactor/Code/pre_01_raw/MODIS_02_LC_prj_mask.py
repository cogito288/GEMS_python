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
mask = os.path.join(data_base_dir, 'Raw', 'mask', 'r_rec_N50W110S20E150.tif')

mask_data = gdal.Open(mask)
minx, xres, xskew, maxy, yskew, yres = mask_data.GetGeoTransform() # minx == upper left x, uly == upper right y 
maxx = minx + xres * mask_data.RasterXSize
miny = maxy + yres * mask_data.RasterYSize
bounds = (minx, miny, maxx, maxy)
#path_modis="\\\\10.72.26.46\\irisnas6\\Data\\MODIS_tile\\02region\\EastAsia\\MCD12Q1\\"

flist = glob.glob(os.path.join(path_mosaic, '01mosaic', "*.tif"))
flist.sort()

for src_dataset in flist:
    last_num = os.path.basename(src_dataset)[-8:] # b 2016.tif
    print (src_dataset)
    
    matlab.check_make_dir(os.path.join(path_mosaic, '02prj_GCS_WGS84')) # debugging
    matlab.check_make_dir(os.path.join(path_mosaic, '03masked_N50W110S20E150')) # debugging
    
    dst_dataset02 = os.path.join(path_mosaic, '02prj_GCS_WGS84', f'GCS_EA_MCD12Q1_{last_num}') # c
    dst_dataset03 = os.path.join(path_mosaic, '03masked_N50W110S20E150', f'm_MODIS_LC_500m_{last_num}') # d
    
    input_raster = gdal.Open(src_dataset)
    gdal.Warp(dst_dataset02, input_raster,
        srcSRS='+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs',
        dstSRS='EPSG:4326', 
        xRes=5.11542231032757E-03, yRes=5.11542231032757E-03,
        resampleAlg='near',
        outputBounds=bounds,
        creationOptions=['COMPRESS=LZW'],
    )
    # gdalwarp -tr 5.11542231032757E-03 5.11542231032757E-03 -r near -s_srs '+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs' -t_srs EPSG:4326 -te xmin ymin xmax ymax -co compress=LZ77 src_dataset dst_dataset02
    print (bounds)
    print (src_dataset)
    print (dst_dataset02)
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
