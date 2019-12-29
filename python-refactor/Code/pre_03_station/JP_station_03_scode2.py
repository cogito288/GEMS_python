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

stn_info = pd.read_csv(os.path.join(station_path, 'Station_JP', 'jp_stn_code_lonlat_period_filtered_yyyymmdd.csv'),header=1)
# scode1, scode2, lon, lat, op_start, op_

## read stn_code_data file
header_ndata = ['doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode','scode2']

yr=2019
ndata = matlab.loadmat(os.path.join(station_path, 'Station_JP','stn_code_data', f'stn_code_data_rm_outlier_{yr}_rm.mat'))
# ndata = np.delete(ndata, [11,12], axis=1);  # O3, NOX
ndata[ndata==-9999]=np.nan

## stn_scode_data for Japan
ndata[:,12]=0 # add column for scode2

ndata_scode = None
# Assign scode2
for j in range(stn_info.shape[0]): 
    ndata_temp = ndata[ndata[:,11]==stn_info[j,0],:]
    for k in range(5): # 1:5 ############
        for dd in range(1,31+1): # 1:31
            ndata_temp2 = ndata_temp[ndata_temp[:,2]==k & ndata_temp[:,3]==dd,:]
            if len(ndata_temp2)!=0:
                yyyymmdd = yr*10000+k*100+dd
                idx = (stn_info[j,4] < yyyymmdd) & (stn_info[j,5] >= yyyymmdd)
                if idx==1:
                    ndata_temp2[:,-1]=stn_info[j,1]
                    if ndata_scode is None:
                        ndata_scode = ndata_temp2
                    else:
                        ndata_scode=np.vstack([ndata_scode,ndata_temp2])
    if (j+1)%100==0:
        matlab.savemat(station_path, 'Station_JP',  f'stn_scode_data_{yr}_{j-98:04d}.mat', {'ndata_scode':ndata_scode})
        ndata_scode = None
    elif (j+1)==stn_info.shape[0]:
        matlab.savemat(station_path, 'Station_JP', f'stn_scode_data_{yr}_2401.mat', {'ndata_scode':ndata_scode})
    print (f'{j} / {stn_info.shape[0]}')
ndata_scode = None
for k in range(1, 2401+1, 100): 
    fname = os.path.join(station_path, 'Station_JP',f'stn_scode_data_{yr}_{k:04d}.mat')
    ndata_scode_temp = matlab.loadmat(fname)['ndata_scode_temp']
    ndata_scode = np.vstack([ndata_scode, ndata_scode_temp])

fname = f'jp_stn_scode_data_rm_outlier_{yr}.mat'
matlab.savemat(os.path.join(station_path, 'Station_JP', fname, 
               {'ndata_scode':ndata_scode,'header_ndata':header_ndata})

for k in range(1, 2401+1, 100): 
    fname = os.path.join(station_path, 'Station_JP', 'stn_scode_data_{yr}_{k:04d}.mat')
    os.remove(fname)
