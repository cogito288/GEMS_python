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
import h5py

### Setting path
"""
if os.path.exists('//10.72.26.56/irisnas5/Data/'):
    data_base_dir = '//10.72.26.56/irisnas5/Data/'
else:
    data_base_dir = '/share/irisnas5/Data/'
"""

data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_in_situ = os.path.join(data_base_dir, 'Raw') 
path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')

#tg = ['SO2','NO','NO2','NOX','CO','OX','NMHC','CH4','THC','SPM','PM25','CO2']
tg = ['HUM','NETR','PRS','RAIN','SUN','TEMP','UV','WD','WS']

## 
# 2012년 CO2 없음.
YEARS = [2016] #range(2009, 2016+1)
for yr in YEARS:
    for col in tg:
        stn_tbl = pd.read_csv(os.path.join(path_stn_jp, 'byPollutant', 'fail', f'JP_stn{col}_{yr}.csv'))
        header = np.array(stn_tbl.columns, dtype=h5py.string_dtype(encoding='utf-8'))
        stn = stn_tbl.values.astype('float')
        del stn_tbl
        
        stn[stn[:,7]>=9997,7] = np.nan
        
        if yr%4==0:
            idx = (stn[:,2]==2) & (stn[:,3]>29)
            stn = stn[~idx]
        else:
            idx = (stn[:,2]==2) & (stn[:,3]>28)
            stn = stn[~idx]
        
        tmp_idx = (stn[:,2]==4) & (stn[:,3]==31)
        stn = stn[~tmp_idx]
        tmp_idx = (stn[:,2]==6) & (stn[:,3]==31)
        stn = stn[~tmp_idx]
        tmp_idx = (stn[:,2]==9) & (stn[:,3]==31)
        stn = stn[~tmp_idx]
        tmp_idx = (stn[:,2]==11) & (stn[:,3]==31)
        stn = stn[~tmp_idx]

        stn_tbl = pd.DataFrame(stn, columns=header)
        stn_tbl = stn_tbl.apply(pd.to_numeric)
        matlab.savemat(os.path.join(path_stn_jp, 'byPollutant', f'JP_stn{col}_{yr}.mat'), 
                       {col: stn_tbl[col].values for col in stn_tbl.columns})
        with h5py.File(os.path.join(path_stn_jp, 'byPollutant', f'JP_stn{col}_{yr}.mat'), 'a') as dst:
            dst['header'] = header
        print (f'{yr}_{col}')
    print (yr)