### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = base_dir
sys.path.insert(0, project_path)
from Code.utils import matlab

import copy
import numpy as np
import pandas as pd
import glob
import h5py

### Setting path
data_base_dir = os.path.join(base_dir, 'Data')
path_in_situ = os.path.join(data_base_dir, 'Raw', 'In_situ')
path_station = os.path.join(data_base_dir, 'Station') 
path_stn_kr = os.path.join(path_station, 'Station_KR')

stn_info = pd.read_csv(os.path.join(path_in_situ,'AirQuality_SouthKorea', 'stn_code_lonlat_period_2005_201904.csv'))
stn_info = stn_info.values
# scode1, scode2, lon, lat, installation, abolation

## read raw files
header_ndata = np.array(['doy','yr','mon','day','KST','SO2','CO','O3','NO2','PM10','PM25','scode','scode2'], 
                        dtype=h5py.string_dtype(encoding='utf-8'))
## stn_scode_data for South Korea
YEARS = range(2014,2018+1)
for yr in YEARS: 
    if yr==2019:
        ndata=matlab.loadmat(os.path.join(path_stn_kr,'stn_code_data', 'stn_code_data_2019_010100_042300.mat'))['ndata']
    else:
        ndata=matlab.loadmat(os.path.join(path_stn_kr,'stn_code_data', f'stn_code_data_{yr}.mat'))['ndata']
    ndata = np.hstack([ndata, np.zeros([ndata.shape[0], 1])]) # add column for scode2
    ndata[ndata<0] = np.nan

    ndata_scode = None
    # Assign scode2
    for j in range(stn_info.shape[0]): 
        ndata_temp = ndata[ndata[:,11]==stn_info[j,0],:]
        for k in range(1,12+1):
            ndata_temp2 = ndata_temp[ndata_temp[:,2]==k,:]
            if len(ndata_temp2)!=0:
                yrmon = yr*100+k
                idx = (stn_info[j,4]<=yrmon)&(stn_info[j,5]>yrmon)
                if idx==1:
                    ndata_temp2[:,12]=stn_info[j,1]
                    if ndata_scode is None:
                        ndata_scode = ndata_temp2
                    else:
                        ndata_scode=np.vstack([ndata_scode,ndata_temp2])
        print (f'{j+1} / {stn_info.shape[0]}')
    fname = f'stn_scode_data_{yr}.mat'
    matlab.savemat(os.path.join(path_stn_kr, 'stn_scode_data', fname), 
                   {'ndata_scode':ndata_scode,'header_ndata':header_ndata})
