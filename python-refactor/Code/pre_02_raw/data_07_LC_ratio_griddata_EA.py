### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import rasterio as rio
from scipy.ndimage import map_coordinates
import time

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_mcd_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS', 'MCD12Q1')
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km') 
path_ea_goci_modis = os.path.join(path_ea_goci, 'MODIS_LC_ratio')

mat = matlab.loadmat(os.path.join(path_grid_raw,'grid_GCS_MODIS_500m_EA.mat'))
lon_gcs_500m, lat_gcs_500m = mat['lon_gcs_500m'], mat['lat_gcs_500m']
del mat
dx = 0.00511542 # point x 간격 np.diff(mat['lon_gcs_500m'])
dy = 0.00511542 # point y 간격 np.diff(mat['lat_gcs_500m'])
xmin = np.min(lon_gcs_500m[0])
ymin = np.min(lat_gcs_500m[:, 0])

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_goci.mat')) # lon_goci, lat_goci
lon_goci = mat['lon_goci']
lat_goci = mat['lat_goci']
del mat
coords = ((lon_goci-xmin)/dx, (lat_goci-ymin)/dy)

# points를 아래와 같이 배치 
# (x=0,y=0), (x=0,y=1), ..., (x=0, y=n)
# (x=1,y=0), (x=1,y=1), ...
# (x=2,y=0), (x=2,y=1), ... 

class_name = ['barren','crop','forest','grass','savannas','shrub','snow','urban','water','wetland']
YEARS = [2016]
for yr in YEARS: 
    for col in class_name:
        tStart = time.time()
        with rio.open(os.path.join(path_mcd_processed, '03_LC_ratio', str(yr), f'EA_{col}_ratio_r6_500m_{yr}.tif')) as src:
            LC_ratio = src.read(1)
        LC_ratio = np.float64(LC_ratio) 
        LC_ratio[LC_ratio==src.nodata] = np.nan
        LC_ratio[LC_ratio<0] = np.nan #% nodata value -3.40282346639e+038
        LC_ratio = LC_ratio[::-1].T
        
        arr = map_coordinates(LC_ratio[::-1].T, coords, order=1)
        matlab.savemat(os.path.join(path_ea_goci_modis, f'EA6km_{col}_ratio_r6_{yr}.mat'), {f'LC_{col}':arr})
        print (f'EA6km_{col}_ratio_r6_{yr}')
        del LC_ratio, arr
        tElapsed = time.time() - tStart
        print (f'time taken : {tElapsed}')