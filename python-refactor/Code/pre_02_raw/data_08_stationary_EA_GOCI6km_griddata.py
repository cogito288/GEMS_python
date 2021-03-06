### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import time
import numpy as np
import rasterio as rio
from scipy.ndimage import map_coordinates

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km') 

mat = matlab.loadmat(os.path.join(path_grid_raw,'grid_SRTM_1km.mat'))
lon_SRTM_1km, lat_SRTM_1km = mat['lon_SRTM_1km'], mat['lat_SRTM_1km']
del mat
dx = 0.01023084 # point x 간격 np.diff(mat['lon_gcs_500m'])
dy = 0.01023084 # point y 간격 np.diff(mat['lat_gcs_500m'])
xmin = np.min(lon_SRTM_1km[0])
ymin = np.min(lat_SRTM_1km[:, 0])

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_goci.mat')) # lon_goci, lat_goci
lon_goci, lat_goci = mat['lon_goci'], mat['lat_goci']
del mat
coords = ((lon_goci-xmin)/dx, (lat_goci-ymin)/dy)

# SRTM DEM
with rio.open(os.path.join(path_grid_raw, 'SRTM_DEM_1km.tif')) as src:
    dem = src.read(1)
dem = dem.astype('float64')
dem[dem==src.nodata] = np.nan
dem[dem<0] = np.nan
tStart = time.time()
dem = map_coordinates(dem[::-1].T, coords, order=1)
#dem = griddata(points, values, (lon_goci, lat_goci), method='linear')
tElapsed = time.time() - tStart
print (f'time taken : {tElapsed}')
matlab.savemat(os.path.join(path_ea_goci, 'stationary', 'EA6km_SRTM_DEM.mat'), {'dem':dem})
print ('stationary/EA6km_SRTM_DEM.mat')

# Population density
mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_EA_30sec_GPWv4_PopDens.mat')) 
lon_EA_30sec, lat_EA_30sec = mat['lon_EA_30sec'], mat['lat_EA_30sec']
del mat
dx = 0.00833333 
dy = 0.00833333 
xmin = np.min(lon_EA_30sec[0])
ymin = np.min(lat_EA_30sec[:, 0])
coords = ((lon_goci-xmin)/dx, (lat_goci-ymin)/dy)

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
    tStart = time.time()
    values = popDens_all[:,:,yr-2000]
    popDens = map_coordinates(values[::-1].T, coords, order=1)
    #popDens = griddata(points,values,(lon_goci,lat_goci),'linear')
    matlab.savemat(os.path.join(path_ea_goci, 'PopDens', f'EA6km_popDens_{yr}.mat'), \
                   {'popDens':popDens})
    tElapsed = time.time() - tStart
    print (f'time taken : {tElapsed}')
    print (f'PopDens/EA6km_popDens_{yr}.mat')
    del popDens
    
# Road density
mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_GRIP4_8km.mat')) 
lon_GRIP4_8km, lat_GRIP4_8km = mat['lon_GRIP4_8km'], mat['lat_GRIP4_8km']
del mat
dx = 0.00833333 
dy = 0.00833333 
xmin = np.min(lon_EA_30sec[0])
ymin = np.min(lat_EA_30sec[:, 0])
coords = ((lon_goci-xmin)/dx, (lat_goci-ymin)/dy)

with rio.open(os.path.join(data_base_dir, 'Preprocessed_raw', 
           'roadDens', 'GRIP4_TOTAL_DENS_m_km2.tif')) as src:
    roadDens = src.read(1)
roadDens = roadDens.astype('float64')
roadDens[roadDens<0] = np.nan
roadDens[roadDens==src.nodata] = np.nan
roadDens = map_coordinates(roadDens[::-1].T, coords, order=1)
#roadDens = griddata(points,values,(lon_goci,lat_goci),'linear')
matlab.savemat(os.path.join(path_ea_goci, 'stationary', 'EA6km_roadDens.mat'), {'roadDens':roadDens})
print ('stationary/EA6km_roadDens.mat')