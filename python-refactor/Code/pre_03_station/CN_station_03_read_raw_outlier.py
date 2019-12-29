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

# scode1, scode2, lon, lat, op_start, op_
stn_info_cn = pd.read_csv(os.path.join(station_path,'Station_CN', 'cn_stn_code_lonlat_period.csv'),header=1)

## stn_scode_data for China
header_ndata = ['doy','yr','mon','day','CST','AQI','PM25','PM25_24h',
    'PM10','PM10_24h','SO2','SO2_24h','NO2','NO2_24h','O3','O3_24h',
    'O3_8h','O3_8h_24h','CO','CO_24h','scode','scode2']

YEARS = [2016] # range(2015, 2019+1)
for yr in YEARS:
    fname = f'stn_code_data_rm_outlier_{yr}.mat'
    mat = matlab.loadmat(os.path.join(station_path,'Station_CN', 'stn_code_data', fname))
    assert len(mat.keys())==1
    ndata=mat[mat.keys()[0]]
    ndata = np.concatenate([ndata, np.zeros((ndata.shape[0], 1))], axis=1)
    ndata_scode = None
    # Assign scode2
    for j in range(stn_info_cn.shape[0]):
        ndata_temp = ndata[ndata[:,-2]==stn_info_cn[j,0],:]
        for k in range(1,5+1): 
            ndata_temp2 = ndata_temp[ndata_temp[:,2]==k,:]
            if len(ndata_temp2)!=0:
                yrmon = yr*100+k
                idx = (stn_info_cn[j,4]<=yrmon)&(stn_info_cn[j,5]>=yrmon)
                if idx==1:
                    ndata_temp2[:,-1]=stn_info_cn[j,1]
                    if ndata_scode is None:
                        ndata_scode = ndata_temp2
                    else:
                        ndata_scode= np.concatenate((ndata_scode,ndata_temp2), axis=1)
        if ((j+1)%100)==0:
            fname = f'stn_scode_data_{yr}_{j-99:04d}.mat'
            matlab.savemat(station_path,'Station_CN', fname, {'ndata_scode':ndata_scode})
            ndata_scode = None
        elif (j+1)==stn_info_cn.shape[0]:
            fname = f'stn_scode_data_{yr}_1501.mat'
            matlab.savemat(station_path,'Station_CN', fname, {'ndata_scode':ndata_scode})
    
        print (f'{j} / {stn_info_cn.shape[0]}')


    ndata_scode = None
    for k in range(1, 1501+1, 100):
        fname = f'stn_scode_data_{yr}_{k:04d}.mat'
        mat = matlab.loadmat(os.path.join(station_path,'Station_CN', fname))
        assert len(mat.keys())==1
        ndata_scode_temp = mat[mat.keys()[0]]
        if ndata_scode is None:
            ndata_scode = ndata_scode_temp
        else:
            ndata_scode = np.concatenate((ndata_scode, ndata_scode_temp), axis=1)
    fname = f'cn_stn_scode_data_rm_outlier_{yr}.mat'
    matlab.savemat(os.path.join(station_path,'Station_CN','stn_scode_data', fname), {'ndata_scode':ndata_scode,'header_ndata':header_ndata})
    print (yr)