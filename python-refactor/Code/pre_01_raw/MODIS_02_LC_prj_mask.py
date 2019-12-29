### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import json
import glob
import rasterio as rio
from rasterio import features
from rasterio.mask import mask
from rasterio.warp import (
    calculate_default_transform, 
    reproject, 
    Resampling
)
import time

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_mcd_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS', 'MCD12Q1')
maskfile = os.path.join(data_base_dir, 'Raw', 'mask', 'r_rec_N50W110S20E150.tif')
with rio.open(maskfile) as masksrc:
    band = masksrc.read(1)
    maskarr = (band!=255)
    shapes = []
    for geometry, raster_value in features.shapes(band, mask=maskarr, transform=masksrc.transform):
        shapes.append(json.loads(json.dumps(geometry)))
    
flist = glob.glob(os.path.join(path_mcd_processed, '01mosaic', "*.tif"))
flist.sort()


for src_dataset in flist:
    tStart = time.time()
    last_num = os.path.basename(src_dataset)[-8:] # b 2016.tif
    print (src_dataset)
    
    matlab.check_make_dir(os.path.join(path_mcd_processed, '02prj_GCS_WGS84')) # debugging
    matlab.check_make_dir(os.path.join(path_mcd_processed, '03masked_N50W110S20E150')) # debugging
    
    dst_dataset02 = os.path.join(path_mcd_processed, '02prj_GCS_WGS84', f'GCS_EA_MCD12Q1_{last_num}') # c
    dst_dataset03 = os.path.join(path_mcd_processed, '03masked_N50W110S20E150', f'm_MODIS_LC_500m_{last_num}') # d

    dst_crs = 'EPSG:4326'
    resolution = 5.11542231032757E-03 # same with maskfile resolution
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
    with rio.open(dst_dataset02) as dst02:
        out_img, out_transform = mask(dataset=dst02, shapes=shapes, crop=True)
        out_meta = dst02.meta.copy()
        out_meta.update({"height": out_img.shape[1],
                         "width": out_img.shape[2],
                         "transform": out_transform,
                         "crs": dst_crs,
                         "compress":"LZW"}
                       )
        print (out_meta)
        with rio.open(dst_dataset03, 'w', **out_meta) as dst03:
            dst03.write(out_img)
    
    tElapsed = time.time() - tStart
    print (f'time taken : {tElapsed}')
    print (os.path.basename(dst_dataset02))
    print (os.path.basename(dst_dataset03))
    
