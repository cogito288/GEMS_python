### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import scipy.io as sio
import numpy as np
import glob
import time
import h5py 
import pygrib

### Setting path
data_base_dir = os.path.join('/', 'media', 'sf_GEMS', 'Data')
rdaps_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'RDAPS') 
#path = os.path.join(project_data, 'Data', 'Aerosol', 'Aerosol_Work', 'Korea')
#data_path = os.path.join(project_data, 'Data', 'Aerosol')

### Setting period
YEARS = [2016] #, 2018, 2019
for yr in YEARS:
    curr_path = os.path.join(rdaps_path, str(yr))
    if yr%4==0: days = 366
    else: days = 365
    
    for i in range(1, days+1):
        data06 = None
        data18 = None
        
        data00 = matlab.loadmat(os.path.join(curr_path, f'RDAPS_{yr}_{i:03d}_00.mat')) # rdaps
        data00 = data00['rdaps']

        try:
            data06 = matlab.loadmat(os.path.join(curr_path, f'RDAPS_{yr}_{i:03d}_06.mat')) # rdaps
            data06 = data06['rdaps']
        except:
            # 분석장06시 자료가 없을 때, 예측장00-006시 자료 가져오기
            # (2015 232 (Aug20))
            data00_006 = matlab.loadmat(os.path.join(curr_path, f'RDAPS_{yr}_{i:03d}_06_frcst.mat')) # rdaps forecast 06
            data00_006 = data00_006['rdaps']
        data12 = matlab.loadmat(os.path.join(curr_path, f'RDAPS_{yr}_{i:03d}_12.mat')) # rdaps
        data12 = data12['rdaps']
        
        try:
            data18 = matlab.loadmat(os.path.join(curr_path, f'RDAPS_{yr}_{i:03d}_18.mat')) # rdaps
            data18 = data18['rdaps']
        except:
            # 분석장18시 자료가 없을 때, 12-006시 자료 가져오기
            # From 2016 028 to 045 (Jan28 to Feb14) 18 UTC analysis data missing
            data12_006 = matlab.loadmat(os.path.join(curr_path, f'RDAPS_{yr}_{i:03d}_18_frcst.mat')) #rdaps forecast 06
            data12_006 = data12_006['rdaps']
        
        if i == days:
            data24 = matlab.loadmat(os.path.join(curr_path, 'RDAPS', str(yr+1), f'RDAPS_{yr+1}_001_00.mat')) #rdaps
        else:
            data24 = matlab.loadmat(os.path.join(curr_path, f'RDAPS_{yr}_{i+1:03d}_00.mat')) # rdaps
        data24 = data24['rdaps']
                                    
        if (data06 is not None) and (data18 is not None):
            for j in range(1, 5+1):
                rdaps = np.multiply((data06 - data00), (j/6)) + data00 # 01 to 05 UTC
                fname = f'RDAPS_{yr}_{i:03d}_{j:02d}.mat'
                matlab.savemat(rdaps_path, fname, {'rdaps':rdaps})
                
                rdaps = np.multiply((data12 - data06), (j/6)) + data06 # 07 to 11 UTC
                fname = f'RDAPS_{yr}_{i:03d}_{j+6:02d}.mat'
                matlab.savemat(rdaps_path, fname, {'rdaps':rdaps})
                
                rdaps = np.multiply((data18 - data12), (j/6)) + data12 # 13 to 17 UTC
                fname = f'RDAPS_{yr}_{i:03d}_{j+12:02d}.mat'
                matlab.savemat(rdaps_path, fname, {'rdaps':rdaps})
                
                rdaps = np.multiply((data24 - data18), (j/6)) + data18 # 19 to 23 UTC
                fname = f'RDAPS_{yr}_{i:03d}_{j+18:02d}.mat'
                matlab.savemat(rdaps_path, fname, {'rdaps':rdaps})
                
        elif (data06 is None) and (data18 is not None):
            for j in range(1, 5+1):
                rdaps = np.multiply((data00_006 - data00), (j/6)) + data00 # 01 to 05 UTC
                fname = f'RDAPS_{yr}_{i:03d}_{j:02d}_frcst.mat'
                matlab.savemat(rdaps_path, fname, {'rdaps':rdaps})
                
                rdaps = np.multiply((data12 - data00_006), (j/6)) + data00_006 #  07 to 11 UTC
                fname = f'RDAPS_{yr}_{i:03d}_{j+6:02d}_frcst.mat'
                matlab.savemat(rdaps_path, fname, {'rdaps':rdaps})
                
                rdaps = np.multiply((data18 - data12), (j/6)) + data12 #  13 to 17 UTC
                fname = f'RDAPS_{yr}_{i:03d}_{j+12:02d}.mat'
                matlab.savemat(rdaps_path, fname, {'rdaps':rdaps})
                
                rdaps = np.multiply((data24 - data18), (j/6)) + data18 #  19 to 23 UTC
                fname = f'RDAPS_{yr}_{i:03d}_{j+18:02d}.mat'
                matlab.savemat(rdaps_path, fname, {'rdaps':rdaps})
                
        elif (data06 is not None) and (data18 is None):
            for j in range(1, 5+1):
                rdaps = np.multiply((data06 - data00), (j/6)) + data00 # 01 to 05 UTC
                fname = f'RDAPS_{yr}_{i:03d}_{j:02d}.mat'
                matlab.savemat(rdaps_path, fname, {'rdaps':rdaps})
                
                rdaps = np.multiply((data12 - data06), (j/6)) + data06 #  07 to 11 UTC
                fname = f'RDAPS_{yr}_{i:03d}_{j+6:02d}_frcst.mat'
                matlab.savemat(rdaps_path, fname, {'rdaps':rdaps})
                
                rdaps = np.multiply((data12_006 - data12), (j/6)) + data12 #  13 to 17 UTC
                fname = f'RDAPS_{yr}_{i:03d}_{j+12:02d}_frcst.mat'
                matlab.savemat(rdaps_path, fname, {'rdaps':rdaps})
                
                rdaps = np.multiply((data24 - data12_006), (j/6)) + data12_006 #  19 to 23 UTC
                fname = f'RDAPS_{yr}_{i:03d}_{j+18:02d}_frcst.mat'
                matlab.savemat(rdaps_path, fname, {'rdaps':rdaps})
                
        print (i)
