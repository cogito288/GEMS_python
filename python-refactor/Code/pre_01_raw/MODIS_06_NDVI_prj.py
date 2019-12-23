import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import json
import glob
import time 
import tempfile
import rasterio as rio
from rasterio import features
from rasterio.mask import mask
from rasterio.warp import (
    calculate_default_transform, 
    aligned_target,
    reproject, 
    Resampling
)

### Setting path
data_base_dir = os.path.join(project_path, 'Data')
path_modis = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS', 'MYD13A2')

YEARS = [2016]
for yr in YEARS:
    path_read = os.path.join(path_modis, '01mosaic', str(yr))
    flist = glob.glob(os.path.join(path_read, "*.tif"))
    flist.sort()
    
    for src_dataset in flist:
        matlab.check_make_dir(os.path.join(path_modis, '02prj_GCS_WGS84', str(yr))) # debugging
        
        dst_dataset02 = os.path.join(path_modis, '02prj_GCS_WGS84', str(yr), f'p_{os.path.basename(src_dataset)}') # c        
        dst_crs = 'EPSG:4326'
        resolution = 1.02308446206551E-02 # same with maskfile resolution
        with rio.open(src_dataset) as src:
            transform, width, height = calculate_default_transform(
                    src.crs, dst_crs, 
                    src.width, src.height, *src.bounds, 
                    resolution=resolution)

            kwargs = src.meta.copy()
            kwargs.update({
                    'crs': dst_crs,
                    'transform': transform,
                    'width': width,
                    'height': height,
                    'nodata':-9999,
                    'compress':'LZW',
            })
            with rio.open(dst_dataset02, 'w', **kwargs) as dst02:
                for i in range(1, src.count+1):
                    reproject(
                        source=rio.band(src, i),
                        destination=rio.band(dst02, i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        src_nodata=-9999,
                        dst_transform=transform,
                        dst_crs=dst_crs,
                        dst_nodata=-9999,
                        dst_resolution=resolution,
                        resampling=Resampling.nearest,
                    )
        print (os.path.basename(dst_dataset02))
