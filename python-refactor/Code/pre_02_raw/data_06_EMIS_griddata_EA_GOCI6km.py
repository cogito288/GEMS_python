### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
#from matplotlib.pyplot import imread
from scipy.interploate import griddata

### Setting path
data_base_dir = os.path.join(project_path, 'Data')
path_read = os.path.join(data_base_dir, 'Preprocessed_raw', 'EMIS', 'KNU_27_01') 
path_write = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km', 'EMIS')

path_data = os.path.join('/', 'share', 'irisnas5', 'Data')
path = os.path.join('/', 'share', 'irisnas5', 'Data', 'EA_GOCI6km')

#%% 27 km domain
mat = matlab.loadmat(os.path.join(path_data,'grid','grid_cmaq_27km.mat')) # % lon_cmaq_27km, lat_cmaq_27km
lon_cmaq_27km = mat['lon_cmaq_27km']
lat_cmap_27km = mat['lat_cmaq_27km']
del mat

mat = matlab.loadmat(os.path.join(data_base_dir, 'grid', 'grid_goci.mat')) # lon_goci, lat_goci
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
            try:
                emiss = matlab.loadmat(os.path.join(path_read, f'emiss_27km_{yr}_{doy:03d}_{utc:02d}.mat'))['emiss']
                EA_emis = np.zeros((nr_goci,nc_goci,14))
                EA_emis[:,:,1]=griddata(zip(lon_cmaq_27km,lat_cmaq_27km),emiss[:,:,1],zip(lon_goci, lat_goci),method='linear') # ISOPRENE
                EA_emis[:,:,2]=griddata(zip(lon_cmaq_27km,lat_cmaq_27km),emiss[:,:,2],zip(lon_goci, lat_goci),method='linear') # TRP1
                EA_emis[:,:,3]=griddata(zip(lon_cmaq_27km,lat_cmaq_27km),emiss[:,:,5],zip(lon_goci, lat_goci),method='linear') # CH4
                EA_emis[:,:,4]=griddata(zip(lon_cmaq_27km,lat_cmaq_27km),emiss[:,:,6],zip(lon_goci, lat_goci),method='linear') # NO
                EA_emis[:,:,5]=griddata(zip(lon_cmaq_27km,lat_cmaq_27km),emiss[:,:,7],zip(lon_goci, lat_goci),method='linear') # NO2
                EA_emis[:,:,6]=griddata(zip(lon_cmaq_27km,lat_cmaq_27km),emiss[:,:,8],zip(lon_goci, lat_goci),method='linear') # NH3
                EA_emis[:,:,7]=griddata(zip(lon_cmaq_27km,lat_cmaq_27km),emiss[:,:,10],zip(lon_goci, lat_goci),method='linear') # HCOOH
                EA_emis[:,:,8]=griddata(zip(lon_cmaq_27km,lat_cmaq_27km),emiss[:,:,11],zip(lon_goci, lat_goci),method='linear') # HCHO
                EA_emis[:,:,9]=griddata(zip(lon_cmaq_27km,lat_cmaq_27km),emiss[:,:,16],zip(lon_goci, lat_goci),method='linear') # CO
                EA_emis[:,:,10]=griddata(zip(lon_cmaq_27km,lat_cmaq_27km),emiss[:,:,37],zip(lon_goci, lat_goci),method='linear') # SO2
                EA_emis[:,:,11]=griddata(zip(lon_cmaq_27km,lat_cmaq_27km),emiss[:,:,42],zip(lon_goci, lat_goci),method='linear') # PMFINE
                EA_emis[:,:,12]=griddata(zip(lon_cmaq_27km,lat_cmaq_27km),emiss[:,:,43],zip(lon_goci, lat_goci),method='linear') # PNO3
                EA_emis[:,:,13]=griddata(zip(lon_cmaq_27km,lat_cmaq_27km),emiss[:,:,44],zip(lon_goci, lat_goci),method='linear') # POA
                EA_emis[:,:,14]=griddata(zip(lon_cmaq_27km,lat_cmaq_27km),emiss[:,:,45],zip(lon_goci, lat_goci),method='linear') # PSO4
            except IOError:
                print ('No data and make nan matrix file')
                EA_emis = np.full((nr_goci,nc_goci, 14), np.nan)
                pass
            matlab.savemat(os.path.join(path_write, str(yr), f'EA6km_EMIS_{yr}_{doy:03d}_{utc:02d}.mat'), {'EA_emis':EA_emis})
            print (f'EA6km_EMIS_{yr}_{doy:03d}_{utc:02d}') 
