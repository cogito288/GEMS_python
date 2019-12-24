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

### Setting path
data_base_dir = os.path.join(project_path, 'Data')
path_read = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS', 'MYD13A2', '03mask') 
path_write = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km', 'MODIS_NDVI')

mat = matlab.loadmat(os.path.join(data_base_dir, 'grid', 'grid_goci.mat')) # lon_goci, lat_goci
lon_goci = mat['lon_goci']
lat_goci = mat['lat_goci']
del mat

mat = matlab.loadmat(os.path.join(data_base_dir, 'grid', 'grid_GCS_MODIS_1km_EA.mat'))
points = np.array([mat['lon_gcs_1km'].ravel(order='F'), mat['lat_gcs_1km'].ravel(order='F')]).T
del mat

YEARS = [2016]
for yr in YEARS:
    flist = glob.glob(os.path.join(path_read, str(yr), "*.tif"))
    flist.sort()
    for fname in flist:
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
        matlab.savemat(os.path.join(path_write, str(yr), f'EA_MODIS_NDVI_{os.path.basename(fname)[10:-4]}.mat'), 
                       {'ndvi':ndivi})
        del ndvi
        print (f'EA_MODIS_NDVI_{os.path.basename(fname)[10:-4]}.mat')
    print (yr)
