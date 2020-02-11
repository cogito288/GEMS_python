### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = base_dir
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import rasterio as rio
import time

### Setting path
data_base_dir = os.path.join(base_dir, 'Data')
path_srtm_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'SRTM_DEM')
path_grid = os.path.join(data_base_dir, 'grid')

tStart = time.time()
fname = os.path.join(path_srtm_processed, 'SRTM_DEM_10times_upscaled_masked.tif')
with rio.open(fname) as dem:
    dem_data = dem.read()
    dem_meta = dem.meta.copy()
    dem_trans = dem.transform
    cc, rr = np.meshgrid(np.array(range(np.shape(dem_data)[2])),np.array(range(np.shape(dem_data)[1])))
    lon_dem, lat_dem = dem_trans * (cc,rr) # upper left
    lon_dem = lon_dem + dem_trans[0]/2
    lat_dem = lat_dem + dem_trans[4]/2

matlab.savemat(os.path.join(path_grid, 'grid_SRTM_10up.mat'), {'lon_dem':lon_dem,'lat_dem':lat_dem})
tElapsed = time.time() - tStart
print (f'time taken : {tElapsed}')
