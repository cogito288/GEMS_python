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

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
raw_path = os.path.join(data_base_dir, 'Raw') 
station_path = os.path.join(data_base_dir, 'Station') 

header = ['doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode']

YEARS = [2016]
for yr in YEARS:
    for mm in range(1, 12+1):
        list_stn = glob.glob(os.path.join(data_base_dir, 'Raw', 'AirQuality_Japan', f'{yr}_soramame', f'{yr}{mm:02d}_00', '*.csv'))
        stn_mm=None
        for fname in list_stn:
            stn_tbl_temp = pd.read_csv(fname)
            scode = stn_tbl_temp[:,0].values
            dstr = stn_tbl_temp[:,1].values
            date_list = [f'{d[:5]}{d[6:8]}{d[9:]}' for d in dstr] #yyyy/mm/dd -> yyyymmdd
            dnum = matlab.datenum(date_list) 
            doy_000 = matlab.datenum(f'{yr}00000')
            doy = dnum - doy_000
            stn_value = stn_tbl_temp[:,2:15].values
            
            data = np.hstack([doy, date_list, stn_value[:,[0,1,5,6,3,10,11]], scode])
            # {'doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode'}
            if stn_mm is None:
                stn_mm = data
            else:
                stn_mm = np.vstack([stn_mm, data])
        matlab.savemat(os.path.join(station_path, 'Station_JP', 'stn_code_data', f'stn_code_data_{yr}_{mm:02d}.mat'),{'stn_mm':stn_mm})
        print (mm)
    
    print ('Stack monthly data to yearly data')
    stn_yr = None
    for mm in range(1, 12+1):
        stn_mm = matlab.loadmat(os.path.join(station_path, 'Station_JP','stn_code_data', f'stn_code_data_{yr}_{mm:02d}.mat'))['stn_mm']
        if stn_yr is None:
            stn_yr = stn_mm
        else:
            stn_yr= np.vstack([stn_yr, stn_mm])
    matlab.savemat(os.path.join(path, 'stn_code_data', f'stn_code_data_{yr}_2.mat'),{'stn_yr':stn_yr})
    print (yr)