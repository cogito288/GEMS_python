### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
from matplotlib.pyplot import imread
from scipy.interploate import griddata

### Setting path
data_base_dir = os.path.join(project_path, 'Data')
path_read = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS', 'MCD12Q1', '03_LC_ratio') 
path_write = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km', 'MODIS_LC_ratio')

mat = matlab.loadmat(os.path.join(data_base_dir, 'grid', 'grid_goci.mat')) # lon_goci, lat_goci
lon_goci = mat['lon_goci']
lat_goci = mat['lat_goci']
del mat

mat = matlab.loadmat(os.path.join(path_data,'grid','grid_GCS_MODIS_500m_EA.mat'))
points = np.array([mat['lon_gcs_500m'].ravel(order='F'), mat['lat_gcs_500m'].ravel(order='F')]).T
del mat

matlab.loadmat(os.path.join(path_data,'grid','grid_GCS_MODIS_500m_EA.mat')

lcclass = ['barren','crop','forest','grass','savannas','shrub','snow','urban','water','wetland']
YEARS = [2017]
for yr in YEARS: # 2015:2016
    for k in range(10):
        LC_ratio = imread(os.path.join(path_data,'pre','MODIS','MCD12Q1','03_LC_ratio',str(yr),f'EA_{cclass[k]}_ratio_r6_500m_{yr}.tif'))
        LC_ratio = np.float64(LC_ratio) 
        LC_ratio[LC_ratio<0] = np.nan #% nodata value -3.40282346639e+038
        LC_ratio = griddata(zip(lon_gcs_500m,lat_gcs_500m),LC_ratio,zip(lon_goci,lat_goci),method='linear')
        
        vars()[f'LC_{lcclass[k]}'] = LC_ratio 
       	matlab.savemat(os.path.join(path, 'MODIS_LC_ratio'),f'EA6km_{lcclass[k]}_ratio_r6_{yr}.mat', vars()[f'LC_{lcclass[k]}')
