import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import json
import glob
import rasterio as rio
from rasterio.mask import mask
import fiona
import time 

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_myd_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS', 'MYD13A2')
maskfile = os.path.join(data_base_dir, 'Raw', 'mask', 'v_rec_N50W110S20E150.shp')
with fiona.open(maskfile, "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]
dst_crs = 'EPSG:4326'

YEARS = [2016]
for yr in YEARS:
    print(yr)
    flist = glob.glob(os.path.join(path_myd_processed, '02prj_GCS_WGS84', str(yr), "*.tif"))
    flist.sort()
    for src_dataset in flist:
        tStart = time.time()
        matlab.check_make_dir(os.path.join(path_myd_processed, '03mask', str(yr))) # debugging
        
        dst_dataset = os.path.join(path_myd_processed, '03mask', str(yr), f'm_{os.path.basename(src_dataset)[2:]}') # d
        with rio.open(src_dataset) as dst02:
            out_img, out_transform = mask(dataset=dst02, shapes=shapes, crop=True)
            out_meta = dst02.meta.copy()
            out_meta.update({"height": out_img.shape[1],
                             "width": out_img.shape[2],
                             "transform": out_transform,
                             "crs": dst_crs,
                             "compress":"LZW"}
                           )
            print (out_meta)
            with rio.open(dst_dataset, 'w', **out_meta) as dst03:
                dst03.write(out_img)
        tElapsed = time.time() - tStart
        print (f'time taken : {tElapsed}')
        print (os.path.basename(dst_dataset))
