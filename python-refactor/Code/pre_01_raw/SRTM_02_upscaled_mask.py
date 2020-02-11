### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = base_dir
sys.path.insert(0, project_path)
from Code.utils import matlab

import rasterio as rio
from rasterio import features
from rasterio.mask import mask
from rasterio.warp import Resampling
import time
import fiona

### Setting path
data_base_dir = os.path.join(base_dir, 'Data')
path_srtm_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'SRTM_DEM')

tStart = time.time()
# Load mask file
v_maskfile = os.path.join(data_base_dir, 'mask', 'v_rec_N50W110S20E150.shp')
with fiona.open(v_maskfile, "r") as shapefile:
    v_mask = [feature["geometry"] for feature in shapefile]
del v_maskfile, shapefile

# Upscaling
upscale_factor = 0.1 #0.05
fname = os.path.join(path_srtm_processed, 'SRTM_DEM_3Arc_Void_Filled_mosaic.tif')
with rio.open(fname) as dataset:
    data = dataset.read(
        out_shape=(
            dataset.count,
            int(dataset.height * upscale_factor),
            int(dataset.width * upscale_factor)
        ),
        resampling=Resampling.bilinear
    )
    transform = dataset.transform * dataset.transform.scale(
        (dataset.height / data.shape[-2]),
        (dataset.width / data.shape[-1])
    )
    out_meta = dataset.meta.copy()
    out_meta.update({"height": data.shape[1],
                     "width": data.shape[2],
                     "transform": transform,
                     "compress":"LZW"})
    up_fname = os.path.join(path_srtm_processed, f'SRTM_DEM_{int(1/upscale_factor)}times_upscaled.tif')
    with rio.open(up_fname, 'w', **out_meta) as dst:
        dst.write(data)
    
# Masking the upscaled data using mask shapefile    
with rio.open(up_fname) as dem:
    dem_data, dem_transform = mask(dem, v_mask, crop=True)
    out_meta = dem.meta.copy()
    out_meta.update({"height": dem_data.shape[1],
                     "width": dem_data.shape[2],
                     "transform": dem_transform,
                     "compress":"LZW"})
    dst_fname = os.path.join(path_srtm_processed, f'SRTM_DEM_{int(1/upscale_factor)}times_upscaled_masked.tif')
    with rio.open(dst_fname, 'w', **out_meta) as dst:
        dst.write(dem_data)

tElapsed = time.time() - tStart
print (f'time taken : {tElapsed}')
