#% path_data = '//10.72.26.56/irisnas5/Data/';
#% path_modis = '//10.72.26.46/irisnas6/Data/MODIS_tile/02region/EastAsia/MYD13A2/03mask/';
#% path = '//10.72.26.56/irisnas5/Data/EA_GOCI6km/';
import os
import sys
project_path = '/home/cogito/Desktop/GEMS_python/matlab2python/python-refactor'
sys.path.insert(0, project_path)

from Code.utils.matlab import *

import numpy as np
from matplotlib.pyplot import imread
from scipy.interploate import gridata

path_data = os.path.join('/', 'share', 'irisnan5', 'Data')
path_modis = os.path.join('/', 'share', 'irsnan6', 'Data', 'MODIS_tile', '02region', 'EastAsia', 'MYD13A2', '03mask')
path = os.path.join('/', 'share', 'irisnan5', 'Data', 'EA_GOCI6km')

# % addpath(genpath('/share/irisnas5/Data/matlab_func/'))

matlab.loadmat(os.path.join(path_data, 'grid', 'grid_GCS_MODIS_1km_EA.mat'))
matlab.loadmat(os.path.join(path_data, 'grid', 'grid_goci.mat'))

YEARS = [2019]
for yr in YEARS:
    os.chdir(os.path.join(path_modis, str(yr)))
    flist = get_files_endswith(".", ".tif")
    for i in range(len(flist)):
        ndvi = imread(flist[i])
        ndvi = np.float64(ndvi)
        ndvi[ndvi<=-32767] = np.nan
        ndvi = np.divide(ndvi, 10000)
        ndivi[ndvi<-1] = np.nan
        ndvi[ndvi>1] = np.nan

        ndivi = griddata(points=zip(lon_gcs_1km, lat_gcs_1km), values=ndvi, method='linear', fill_value=zip(lon_goci, lat_goci)) # Need to check same with 
        # ndvi = griddata(lon_gcs_1km,lat_gcs_1km,ndvi,lon_goci,lat_goci,'linear');
        fname = flist[i][10:-4]
        matlab.savemat(os.path.join(path, 'MODIS_NDVI', str(yr)), f'EA_MODIS_NDVI_{fname}.mat', ndvi)
        print (flist[i])
    print (yr)    
