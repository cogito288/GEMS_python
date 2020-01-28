### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import glob
import time
import pandas as pd

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km')

path_korea_cases = os.path.join(data_base_dir, 'Preprocessed_raw', 'Korea', 'cases')
matlab.check_make_dir(path_korea_cases)

path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')
path_stn_cn = os.path.join(path_station, 'Station_CN')
path_stn_kr = os.path.join(path_station, 'Station_KR')

tg = ['PM10','PM25']

## Load grid
mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_korea.mat'))
lat_kor, lon_kor = mat['lat_kor'], mat['lon_kor']
del mat

mat = matlab.loadmat(os.path.join(path_stn_kr, 'stn_1km_location_weight_v201904.mat')) # stn_1km_location
stn_1km_location = mat['stn_1km_location']
del mat
# scode1,scode2, lat_org, lon_org, pxid, lat_px, lon_px

##
YEARS = [2016]
for yr in YEARS:
    # nanidx for cases
    mat = matlab.loadmat(os.path.join(path_korea_cases, f'nanidx_1km_hourly_{yr}')) # nanidx
    nanidx = mat['nanidx']
    del mat
    
    # station
    mat = matlab.loadmat(os.path.join(path_stn_kr,f'Station_1km_rm_outlier_{yr}_weight.mat')) # stn_1km_yr
    stn_1km_yr = mat['stn_1km_yr']
    del mat
    
    stn_1km_yr[:,4] = stn_1km_yr[:,4]-9 # KST to UTC
    stn = stn_1km_yr
    
    stn_nanidx = []
    for doy in range(1, nanidx.shape[1]):
        for utc in range(7+1):
            nanidx_temp = nanidx[:,doy-1,utc]
            stn_temp = stn[stn[:,0]==doy & stn[:,4]==utc,:]
            
            for k in range(stn_temp.shape[0]):
                pid = stn_location[stn_location[:,1]==stn_temp[k,12],4]
                stn_temp[k,13]=nanidx_temp[pid]
            stn_nanidx = np.concatenate((stn_nanidx,stn_temp), axis=0)
    stn_fill = stn_nanidx[stn_nanidx[:,13]==0,:13]
    fname = f'KR_1km_stn_rf_day_{yr}.mat'
    matlab.savemat(os.path.join(path_korea_cases, fname), {'stn_fill':stn_fill})
    print (yr)
