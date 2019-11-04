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
import pandas as pd

### Setting path
data_base_dir = os.path.join('/', 'media', 'sf_GEMS_1', 'Data')
raw_data_path = os.path.join(data_base_dir, 'Raw', 'GOCI_AOD') 
write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_AOD')

try:
    path_data = '//10.72.26.56/irisnas5/Data/'
    os.chdir(path_data)
except:
    path_data = '/share/irisnas5/Data/'
    os.chdir(path_data)
    #addpath(genpath('/share/irisnas5/Data/matlab_func/'))

# tg = {'SO2','NO','NO2','NOX','CO','OX','NMHC','CH4','THC','SPM','PM25','CO2'}
tg = ['HUM','NETR','PRS','RAIN','SUN','TEMP','UV','WD','WS']

## 
# 2012년 CO2 없음.
YEARS = range(2009, 2016+1)
for yr in YEARS:
    for i in range(9):
        fname = f'JP_stn{tg[i]}_{yr}'
        vars()[f'stn{tg[i]_tbl}'] = pd.read_csv(os.path.join(path_data, 'Station/Station_JP/byPollutant/fail/', fname))
        # matlab.loadmat(os.path.join(path_data, 'Station/Station_JP/byPollutant/fail/', fname))
        stn = vars()[f'stn{tg[i]_tbl}']
        stn[stn[:,7]>=9997,7] = np.nan
        
        if yr%4==0:
            stn[stn[:,2]==2 & stn[:,3]>29,:]=[]
        else:
            stn[stn[:,2]==2 & stn[:,3]>28,:]=[]
        
        stn[stn[:,2]==4 & stn[:,3]==31,:]=[]
        stn[stn[:,2]==6 & stn[:,3]==31,:]=[]
        stn[stn[:,2]==9 & stn[:,3]==31,:]=[]
        stn[stn[:,2]==11 & stn[:,3]==31,:]=[]

        vars()['stn{tg[i]}_tbl'] = pd.DataFrame(stn, columns=['VariableNames']+vars()['stn{tg[i]}_tbl'].columns)
        fname = f'JP_stn{tg[i]}_{yr}.csv'
        matlab.savemat(os.path.join(path_data,'Station/Station_JP/byPollutant/', fname, {f'stn{tg[i]_tbl':vars()[f'stn{tg[i]_tbl']})
        #clearvars stn*
        print (f'{yr}_{tg[i]}')
    print (yr)
