### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import glob
import numpy as np
import rasterio as rio
from scipy.interpolate import griddata
import time

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_myd_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS', 'MYD13A2') # Read
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km')
path_ea_goci_ndivi = os.path.join(path_ea_goci, 'MODIS_NDVI')

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_goci.mat')) # lon_goci, lat_goci
lon_goci = mat['lon_goci']
lat_goci = mat['lat_goci']
del mat

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_GCS_MODIS_1km_EA.mat'))
points = np.array([mat['lon_gcs_1km'].ravel(order='F'), mat['lat_gcs_1km'].ravel(order='F')]).T
del mat

YEARS = [2016]
for yr in YEARS:
    flist = glob.glob(os.path.join(path_myd_processed, '03mask', str(yr), "*.tif"))
    flist.sort()
    for fname in flist:
        tStart = time.time()
        print (os.path.basename(fname))
        with rio.open(fname) as src:
            ndvi = src.read(1)
        ndvi = np.float64(ndvi)
        ndvi[ndvi<=-32767] = np.nan
        ndvi = np.divide(ndvi, 10000)
        ndvi[np.abs(ndvi)>=0.99] = np.nan
        values = ndvi.ravel(order='F')
        ndivi = griddata(points=points, 
                         values=values, 
                         xi=(lon_goci, lat_goci),
                         method='linear')
        matlab.savemat(os.path.join(path_ea_goci_ndivi, str(yr), f'EA_MODIS_NDVI_{os.path.basename(fname)[10:-4]}.mat'), 
                       {'ndvi':ndivi})
        del ndvi
        print (f'EA_MODIS_NDVI_{os.path.basename(fname)[10:-4]}.mat')
        tElapsed = time.time() - tStart
        print (f'time taken : {tElapsed}')
    print (yr)
