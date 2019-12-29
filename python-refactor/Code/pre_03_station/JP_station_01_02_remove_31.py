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

"""
if os.path.exists('//10.72.26.56/irisnas5/Data/'):
    path_data = '//10.72.26.56/irisnas5/Data/'
else:
    path_data = '/share/irisnas5/Data/'
"""

# tg = {'SO2','NO','NO2','NOX','CO','OX','NMHC','CH4','THC','SPM','PM25','CO2'}
tg = ['HUM','NETR','PRS','RAIN','SUN','TEMP','UV','WD','WS']

## 
# 2012년 CO2 없음.
YEARS = range(2009, 2016+1)
for yr in YEARS:
    for i in range(9):
        vars()[f'stn{tg[i]}_tbl'] = pd.read_csv(os.path.join(station_path, 'Station_JP/byPollutant/fail/', f'JP_stn{tg[i]}_{yr}.csv'))
        stn = vars()[f'stn{tg[i]}_tbl'].values
        stn[stn[:,7]>=9997,7] = np.nan
        
        if yr%4==0:
            stn = np.delete(stn, stn[:,2]==2 & stn[:,3]>29, axis=0)
        else:
            stn = np.delete(stn, stn[:,2]==2 & stn[:,3]>28, axis=0)
        stn = np.delete(stn, stn[:,2]==4 & stn[:,3]==31, axis=0)
        stn = np.delete(stn, stn[:,2]==6 & stn[:,3]==31, axis=0)
        stn = np.delete(stn, stn[:,2]==9 & stn[:,3]==31, axis=0)
        stn = np.delete(stn, stn[:,2]==11 & stn[:,3]==31, axis=0)

        vars()[f'stn{tg[i]}_tbl'] = pd.DataFrame(stn, columns=vars()[f'stn{tg[i]}_tbl'].columns)
        matlab.savemat(os.path.join(station_path,'Station_JP/byPollutant/', f'JP_stn{tg[i]}_{yr}.csv'),
                       vars()[f'stn{tg[i]}_tbl'].to_dict('list'))
        print (f'{yr}_{tg[i]}')
    print (yr)