### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import copy
import numpy as np
import pandas as pd
import glob
import scipy.io as sio

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_in_situ = os.path.join(data_base_dir, 'Raw') 
path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')

header = ['doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode']

YEARS = [2016]
for yr in YEARS:
    for mm in range(1, 12+1):
        file_list = glob.glob(os.path.join(path_in_situ, 'AirQuality_Japan', f'{yr}_soramame', f'{yr}{mm:02d}_00', '*.csv'))
        file_list.sort()
        stn_mm = None
        for fname in file_list:
            stn_tbl_temp = pd.read_csv(fname, encoding='latin1')
            stn_tbl_temp = stn_tbl_temp.values
            scode = stn_tbl_temp[:,0]
            
            dstr = [str(int(x)) for x in stn_tbl_temp[:,1]]
            dstr = [f'{d[:4]}{d[5:7]}{d[8:]}' for d in dstr] # yyyy/mm/dd -> yyyymmdd
            dvec = [(int(d[:4]), int(d[4:6]), int(d[6:])) for d in dstr] 
            dvec = np.array(dvec)
            data_datenum = [matlab.datenum(val) for val in dstr]
            doy_000 = matlab.datenum(f'{yr}00000')
            doy = np.array([val-doy_000 for val in data_datenum])
            
            stn_value = stn_tbl_temp[:,2:15]
            
            data = np.hstack([doy.reshape(-1,1), dvec, stn_value[:,[0,1,5,6,3,10,11]], scode.reshape(-1,1)])
            # {'doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode'}
            if stn_mm is None: stn_mm = data
            else: stn_mm = np.vstack([stn_mm, data])
        sio.savemat(os.path.join(path_stn_jp, 'stn_code_data', f'stn_code_data_{yr}_{mm:02d}.mat'),{'stn_mm':stn_mm},
                   do_compression=True)
        print (mm)
    
    print ('Stack monthly data to yearly data')
    stn_yr = None
    for mm in range(1, 12+1):
        stn_mm = matlab.loadmat(os.path.join(path_stn_jp,'stn_code_data', f'stn_code_data_{yr}_{mm:02d}.mat'))['stn_mm']
        if stn_yr is None: stn_yr = stn_mm
        else: stn_yr= np.vstack([stn_yr, stn_mm])
    sio.savemat(os.path.join(path_stn_jp, 'stn_code_data', f'stn_code_data_{yr}_2.mat'),{'stn_yr':stn_yr},
                   do_compression=True)
    print (yr)