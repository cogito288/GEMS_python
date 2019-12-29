### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
from scipy.interpolate import griddata
import time

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_emis_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'EMIS') 
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km') 
path_ea_goci_emis = os.path.join(path_ea_goci, 'EMIS')

KNU_dir = 'KNU_27_01'
path_read = os.path.join(path_emis_processed, KNU_dir)

#%% 27 km domain
mat = matlab.loadmat(os.path.join(path_grid_raw,'grid_cmaq_27km.mat')) # % lon_cmaq_27km, lat_cmaq_27km
points = np.array([mat['lon_cmaq_27km'].ravel(order='F'), mat['lat_cmaq_27km'].ravel(order='F')]).T
del mat
print (f'points shape : {points.shape}')

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_goci.mat')) # lon_goci, lat_goci
lon_goci = mat['lon_goci']
lat_goci = mat['lat_goci']
del mat
nr_goci, nc_goci = lon_goci.shape

YEARS = [2016]
for yr in YEARS: #:2016
    if yr%4==0: days = 366
    else: days = 365
    for doy in range(1, days+1): #  for doy=294:300 %1:days
        for utc in range(23+1):
            tStart = time.time()
            print (os.path.join(path_read, str(yr), f'emiss_27km_{yr}_{doy:03d}_{utc:02d}.mat'))
            try:
                emiss = matlab.loadmat(os.path.join(path_read, str(yr), f'emiss_27km_{yr}_{doy:03d}_{utc:02d}.mat'))['emiss']
                EA_emis = np.zeros((nr_goci,nc_goci,14))
                EA_emis[:,:,0]=griddata(points, emiss[:,:,0].ravel(order='F'),(lon_goci, lat_goci),method='linear') # ISOPRENE
                EA_emis[:,:,1]=griddata(points,emiss[:,:,1].ravel(order='F'),(lon_goci, lat_goci),method='linear') # TRP1
                EA_emis[:,:,2]=griddata(points,emiss[:,:,4].ravel(order='F'),(lon_goci, lat_goci),method='linear') # CH4
                EA_emis[:,:,3]=griddata(points,emiss[:,:,5].ravel(order='F'),(lon_goci, lat_goci),method='linear') # NO
                EA_emis[:,:,4]=griddata(points,emiss[:,:,6].ravel(order='F'),(lon_goci, lat_goci),method='linear') # NO2
                EA_emis[:,:,6]=griddata(points,emiss[:,:,7].ravel(order='F'),(lon_goci, lat_goci),method='linear') # NH3
                EA_emis[:,:,6]=griddata(points,emiss[:,:,9].ravel(order='F'),(lon_goci, lat_goci),method='linear') # HCOOH
                EA_emis[:,:,7]=griddata(points,emiss[:,:,10].ravel(order='F'),(lon_goci, lat_goci),method='linear') # HCHO
                EA_emis[:,:,8]=griddata(points,emiss[:,:,15].ravel(order='F'),(lon_goci, lat_goci),method='linear') # CO
                EA_emis[:,:,9]=griddata(points,emiss[:,:,36].ravel(order='F'),(lon_goci, lat_goci),method='linear') # SO2
                EA_emis[:,:,10]=griddata(points,emiss[:,:,41].ravel(order='F'),(lon_goci, lat_goci),method='linear') # PMFINE
                EA_emis[:,:,11]=griddata(points,emiss[:,:,42].ravel(order='F'),(lon_goci, lat_goci),method='linear') # PNO3
                EA_emis[:,:,12]=griddata(points,emiss[:,:,43].ravel(order='F'),(lon_goci, lat_goci),method='linear') # POA
                EA_emis[:,:,13]=griddata(points,emiss[:,:,44].ravel(order='F'),(lon_goci, lat_goci),method='linear') # PSO4
            except IOError:
                print ('No data and make nan matrix file')
                EA_emis = np.full((nr_goci,nc_goci, 14), np.nan)
                pass
            matlab.savemat(os.path.join(path_ea_goci_emis, str(yr), f'EA6km_EMIS_{yr}_{doy:03d}_{utc:02d}.mat'), {'EA_emis':EA_emis})
            print (f'EA6km_EMIS_{yr}_{doy:03d}_{utc:02d}') 
            tElapsed = time.time() - tStart
            print (f'{tElapsed} second')