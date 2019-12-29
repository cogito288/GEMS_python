### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import glob
import pygrib
import time

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_rdaps_raw = os.path.join(data_base_dir, 'Raw', 'RDAPS') 
path_rdaps_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'RDAPS') 

### Setting period
YEARS = [2016] #, 2018, 2019

for yr in YEARS:
    file_list = glob.glob(os.path.join(path_rdaps_raw, str(yr), '*000.*.gb2'))
    file_list.sort()
    doy_000 = matlab.datenum(f'{yr}0101')-1
    rdaps = np.full((419,491,18), np.nan) 
    
    for i, fname in enumerate(file_list):
        tStart = time.time()
        print (fname)
        rdaps_data = pygrib.open(fname)
        
        data = rdaps_data.select(name='Temperature', typeOfLevel='heightAboveGround')[0].values
        rdaps[:,:,0] = np.squeeze(data)
        data = rdaps_data.select(name='Dew point temperature', typeOfLevel='heightAboveGround')[0].values
        rdaps[:,:,1] = np.squeeze(data)
        data = rdaps_data.select(name='Relative humidity', typeOfLevel='heightAboveGround')[0].values
        rdaps[:,:,2] = np.squeeze(data)
        data = rdaps_data.select(name='10 metre U wind component', typeOfLevel='heightAboveGround')[0].values
        rdaps[:,:,3] = np.squeeze(data)
        data = rdaps_data.select(name='10 metre V wind component', typeOfLevel='heightAboveGround')[0].values
        rdaps[:,:,4] = np.squeeze(data)
        data = rdaps_data.select(name='Maximum wind speed', typeOfLevel='heightAboveGround')[0].values
        rdaps[:,:,5] = np.squeeze(data)
        data = rdaps_data.select(name='Surface pressure')[0].values
        rdaps[:,:,6] = np.squeeze(data)
        data = rdaps_data.select(name='Planetary boundary layer height')[0].values
        rdaps[:,:,7] = np.squeeze(data)
        data = rdaps_data.select(name='Visibility', typeOfLevel='heightAboveGround')[0].values
        rdaps[:,:,8] = np.squeeze(data)
        data = rdaps_data.select(name='Temperature', typeOfLevel='surface')[0].values
        rdaps[:,:,9] = np.squeeze(data)
        data = rdaps_data.select(name='Maximum temperature', typeOfLevel='heightAboveGround')[0].values
        rdaps[:,:,10] = np.squeeze(data)
        data = rdaps_data.select(name='Minimum temperature', typeOfLevel='heightAboveGround')[0].values
        rdaps[:,:,11] = np.squeeze(data)
        data = rdaps_data.select(parameterName='Total precipitation')[0].values
        rdaps[:,:,12] = np.squeeze(data)
        data = rdaps_data.select(name='Frictional velocity', typeOfLevel='heightAboveGround')[0].values
        rdaps[:,:,13] = np.squeeze(data)
        data = rdaps_data.select(name='Convective available potential energy')[0].values
        rdaps[:,:,14] = np.squeeze(data)
        data = rdaps_data.select(name='Surface roughness', typeOfLevel='surface')[0].values
        rdaps[:,:,15] = np.squeeze(data)
        data = rdaps_data.select(name='Latent heat net flux', typeOfLevel='surface')[0].values
        rdaps[:,:,16] = np.squeeze(data)
        data = rdaps_data.select(name='Specific humidity', typeOfLevel='heightAboveGround')[0].values
        rdaps[:,:,17] = np.squeeze(data)
        
        
        doy = matlab.datenum(os.path.basename(fname)[21:29])-doy_000
        utc = int(os.path.basename(fname)[29:31])
        #fname = f'RDAPS_{yr}_{doy:03d}_{utc:02d}_006.mat'
        fname = f'RDAPS_{yr}_{doy:03d}_{utc:02d}.mat'
        matlab.savemat(os.path.join(path_rdaps_processed, str(yr), fname), {'rdaps':rdaps})
        print (fname)
        tElapsed = time.time() - tStart
        print (f'{tElapsed} second')
    print (yr)
