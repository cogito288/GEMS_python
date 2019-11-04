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
# path_data = '//10.72.26.56/irisnas5/Data/'
path_data = '/share/irisnas5/Data/'
path_stn_kor = [path_data,'Station/Station_Korea/']
#addpath(genpath('/share/irisnas5/Data/matlab_func/'))

stn_info = pd.read_csv(os.path.join(path_data,'Station/Station_Korea/stn_code_lonlat_period_2005_201904.csv'),header=1)
# scode1, scode2, lon, lat, op_start, op_

## read raw files
header_ndata = ['doy','yr','mon','day','KST','SO2','CO','O3','NO2','PM10','PM25','scode','scode2']

## stn_scode_data for South Korea
YEARS = [2008, 2009]
for yr in YEARS: #=2008:2009 #2005:2019
    if yr==2019:
        ndata=matlab.loadmat([path_stn_kor,'stn_code_data/stn_code_data_2019_010100_042300.mat'])
    else:
        ndata=matlab.loadmat([path_stn_kor,'stn_code_data/', f'stn_code_data_{yr}.mat'])
    
        
    ndata[:,12]=0 # add column for scode2
    ndata_scode = []
    ndata[ndata<0]np.nan
    
# Assign scode2
for j in range(stn_info.shape[0]): 
    ndata_temp = ndata[ndata[:,11]==stn_info[j,0],:]
    for k in range(1,12+1):
        ndata_temp2 = ndata_temp[ndata_temp[:,3]==(k-1),:]
        if np.all(ndata_temp2)==0:
            yrmon = yr*100+k
            idx = (stn_info[j,4]<=yrmon)&(stn_info[j,5]>yrmon)
            if idx==1:
                ndata_temp2[:,12]=stn_info[j,1]
                ndata_scode=np.concatenate((ndata_scode,ndata_temp2), axis=0)

    print (f'{j} / {stn_info.shape[0]}')

fname = f'stn_code_data_{yr}.mat'
matlab.savemat(path_stn_kor, fname, 'stn_code_data'), fname, {'ndata_scode':ndata_scode, 'header_ndata':header_ndata})
