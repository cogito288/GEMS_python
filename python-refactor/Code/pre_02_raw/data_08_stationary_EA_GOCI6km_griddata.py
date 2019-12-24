### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import rasterio as rio
from scipy.interploate import griddata

### Setting path
data_base_dir = os.path.join(project_path, 'Data')
path_read = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS', 'MCD12Q1', '03_LC_ratio') 
path_write = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km')

mat = matlab.loadmat(os.path.join(data_base_dir, 'grid', 'grid_goci.mat')) # lon_goci, lat_goci
lon_goci, lat_goci = mat['lon_goci'], mat['lat_goci']
del mat

mat = matlab.loadmat(os.path.join(data_base_dir,'grid','grid_SRTM_1km.mat'))
points = np.array([mat['lon_gcs_1km'].ravel(order='F'), mat['lat_gcs_1km'].ravel(order='F')]).T
del mat

# SRTM DEM
with rio.open(os.path.join(data_base_dir, 'grid', 'SRTM_DEM_1km.tif')) as src:
    dem = src.read(1)
dem = dem.astype('float64')
dem[dem==src.nodata] = np.nan
dem[dem<0] = np.nan
values = dem.ravel(order='F')
dem = griddata(points, values, (lon_goci, lat_goci), methods='linear')
matlab.savemat(os.path.join(path_write, 'stationary', 'EA6km_SRTM_DEM.mat'), {'dem':dem})

# Population density
mat = matlab.loadmat(os.path.join(data_base_dir, 'grid', 'grid_EA_30sec_GPWv4_PopDens.mat')) 
points = np.array([mat['lon_EA_30sec'].ravel(order='F'), mat['lat_EA_30sec'].ravel(order='F')]).T
del mat

popDens_all = np.zeros((3600, 4800, 21))
for yr in range(2000, 2020+1, 5):
    with rio.open(os.path.join(data_base_dir, 'Preprocessed_raw', 
               'PopDens', 'GPW_v4', f'EA_PopDens_v411_30sec_{yr}.tif')) as src:
        popDens = src.read(1)
    popDens = popDens.astype('float64')
    popDens[popDens<0] = np.nan
    popDens[popDens==src.nodata] = np.nan
    popDens_all[:,:,yr-2000] = popDens
    
common_term = (popDens_all[:,:,5]-popDens_all[:,:,0])
popDens_all[:,:,1] = common_term*(1/5) + popDens_all[:,:,0]
popDens_all[:,:,2] = common_term*(2/5) + popDens_all[:,:,0]
popDens_all[:,:,3] = common_term*(3/5) + popDens_all[:,:,0]
popDens_all[:,:,4] = common_term*(4/5) + popDens_all[:,:,0]

common_term = (popDens_all[:,:,10]-popDens_all[:,:,5])
popDens_all[:,:,6] = common_term*(1/5) + popDens_all[:,:,5]
popDens_all[:,:,7] = common_term*(2/5) + popDens_all[:,:,5]
popDens_all[:,:,8] = common_term*(3/5) + popDens_all[:,:,5]
popDens_all[:,:,9] = common_term*(4/5) + popDens_all[:,:,5]

common_term = (popDens_all[:,:,15]-popDens_all[:,:,10])
popDens_all[:,:,11] = common_term*(1/5) + popDens_all[:,:,10]
popDens_all[:,:,12] = common_term*(2/5) + popDens_all[:,:,10]
popDens_all[:,:,13] = common_term*(3/5) + popDens_all[:,:,10]
popDens_all[:,:,14] = common_term*(4/5) + popDens_all[:,:,10]

common_term = (popDens_all[:,:,20]-popDens_all[:,:,15])
popDens_all[:,:,16] = common_term*(1/5) + popDens_all[:,:,15]
popDens_all[:,:,17] = common_term*(2/5) + popDens_all[:,:,15]
popDens_all[:,:,18] = common_term*(3/5) + popDens_all[:,:,15]
popDens_all[:,:,19] = common_term*(4/5) + popDens_all[:,:,15]

for yr in range(2000, 2020+1):
    values = popDens_all[:,:,yr-2000].ravel(order='F')
    popDens = griddata(points,values,(lon_goci,lat_goci),'linear')
    matlab.savemat(os.path.join(path_write, 'PopDens', f'EA6km_popDens_{yr}.mat'), \
                   {'popDens':popDens})
# Road density
mat = matlab.loadmat(os.path.join(data_base_dir, 'grid', 'grid_GRIP4_8km.mat')) 
points = np.array([mat['lon_GRIP4_8km'].ravel(order='F'), mat['lat_GRIP4_8km'].ravel(order='F')]).T
del mat

with rio.open(os.path.join(data_base_dir, 'Preprocessed_raw', 
           'roadDens', 'EA_GRIP4_TOTAL_DENS_m_km2.tif')) as src:
    roadDens = src.read(1)
roadDens = roadDens.astype('float64')
roadDens[roadDens<0] = np.nan
roadDens[roadDens==src.nodata] = np.nan
values = roadDens.ravel(order='F')
roadDens = griddata(points,values,(lon_goci,lat_goci),'linear')
matlab.savemat(os.path.join(path_write, 'stationary', 'EA6km_roadDens.mat'), {'roadDens':roadDens})
