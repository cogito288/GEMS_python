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
path_data = '//10.72.26.46/irisnas6/Data/Aerosol/'
path = '//10.72.26.46/irisnas6/Work/Aerosol/'
# path_data = '/share/irisnas6/Data/Aerosol/'
# path = '/share/irisnas6/Work/Aerosol/'
# addpath(genpath('/share/irisnas6/Work/Aerosol/matlab_func/'))

tg = ['PM10','PM25']

## Load grid
matlab.loadmat(os.path.join(path_data,'grid/grid_goci.mat'))

YEARS = [2015, 2016]
for yr in YEARS:
    matlab.loadmat(os.path.join(path_data,'Station_Korea/stn_GOCI6km_location_weight.mat'))
    # stn_GOCI6km_location, dup_scode2_GOCI6km,header_stn_GOCI6km_location
    matlab.loadmat(os.path.join(path_data,'Station_CN/cn_stn_GOCI6km_location_weight.mat'))
    # cn_stn_GOCI6km_location, cn_dup_scode2_GOCI6km, header_cn_stn_GOCI6km_location
    
    stn_location = np.concatenatem((stn_GOCI6km_location,cn_stn_GOCI6km_location), axis=0)
    # scode1,scode2, lat_org, lon_org, pxid, lat_px, lon_px
    
    # nanidx for cases
    fname = f'nanidx_EA6km_{yr}.mat'
    matlab.loadmat(os.path.join(path,'EA_GOCI6km', fname)) # nanidx
    
    # station
    fname = f'Station_GOCI6km_rm_outlier_{yr}_weight.mat'
    mat = matlab.loadmat(os.path.join(path_data,'Station_Korea', fname)) # stn_GOCI6km_yr
    stn_GOCI6km_yr = mat['stn_GOCI6km_yr']
    del mat

    fname = f'cn_Station_GOCI6km_rm_outlier_{yr}_weight.mat'
    matlab.loadmat(os.path.join(path_data,'Station_CN', fname)) # cn_stn_GOCI6km_yr
    cn_stn_GOCI6km_yr = mat['cn_stn_GOCI6km_yr']

    stn_GOCI6km_yr[:,4]=stn_GOCI6km_yr[:,4]-9
    cn_stn_GOCI6km_yr[:,4]=cn_stn_GOCI6km_yr[:,4]-8
    stn = np.concatenate((stn_GOCI6km_yr, cn_stn_GOCI6km_yr[:,[:5,10,18,14,12,8,6,20:22]]), axis=0)
    
    del stn_GOCI6km_location, dup_scode2_GOCI6km, header_stn_GOCI6km_location
    del cn_stn_GOCI6km_location, cn_dup_scode2_GOCI6km, header_cn_stn_GOCI6km_location
    del stn_GOCI6km_yr, cn_stn_GOCI6km_yr
    
    stn_nanidx = []
    
    for doy in range(nanidx.shape[1]):
        for utc in range(7):
            nanidx_temp = nanidx[:,doy,utc]
            stn_temp = stn[stn[:,0]==doy & stn[:,3]==utc,:]
            
            for k in range(stn_temp.shape[0]):
                pid = stn_location[stn_location[:,1]==stn_temp[k,12],4]
                stn_temp[k,13]=nanidx_temp[pid]
            stn_nanidx = np.concatenate((stn_nanidx,stn_temp), axis=0)

    stn_fill = stn_nanidx[stn_nanidx[:,13]==0,:13]
    fname = f'stn_rf_day_{yr}.mat'
    matlab.savemat(os.path.join(path,'EA_GOCI6km', fname, {'stn_fill':stn_fill})
    print (yr)