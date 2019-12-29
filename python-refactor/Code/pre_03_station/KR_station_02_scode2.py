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
path_insiu = os.path.join(data_base_dir, 'Raw', 'AirQuality_SouthKorea')
path_stn_kor = os.path.join(data_base_dir, 'Station', 'Station_KR')

stn_info = pd.read_csv(os.path.join(path_stn_kor, 'stn_code_lonlat_period_2005_201904.csv'),header=1)
# scode1, scode2, lon, lat, op_start, op_

## read raw files
header_ndata = ['doy','yr','mon','day','KST','SO2','CO','O3','NO2','PM10','PM25','scode','scode2']

## stn_scode_data for South Korea
YEARS = [2008, 2009]
for yr in YEARS: #=2008:2009 #2005:2019
    if yr==2019:
        ndata=matlab.loadmat([path_stn_kor,'stn_code_data/stn_code_data_2019_010100_042300.mat'])['ndata']
    else:
        ndata=matlab.loadmat([path_stn_kor,'stn_code_data', f'stn_code_data_{yr}.mat'])['ndata']
    ndata[:,12]=0 # add column for scode2
    ndata_scode = None
    ndata[ndata<0] = np.nan
# Assign scode2
for j in range(stn_info.shape[0]): 
    ndata_temp = ndata[ndata[:,11]==stn_info[j,0],:]
    for k in range(1,12+1):
        ndata_temp2 = ndata_temp[ndata_temp[:,3]==k,:]
        if len(ndata_temp2)!=0:
            yrmon = yr*100+k
            idx = (stn_info[j,4]<=yrmon)&(stn_info[j,5]>yrmon)
            if idx==1:
                ndata_temp2[:,12]=stn_info[j,1]
                ndata_scode=np.vstack([ndata_scode,ndata_temp2])
    print (f'{j} / {stn_info.shape[0]}')
fname = f'stn_code_data_{yr}.mat'
matlab.savemat(os.path.join(path_stn_kor, fname), {'ndata_scode':ndata_scode, 'header_ndata':header_ndata})