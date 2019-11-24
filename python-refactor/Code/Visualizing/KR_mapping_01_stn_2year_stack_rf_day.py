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
import time
import pandas as pd

path_data = '//10.72.26.46/irisnas6/Data/Aerosol/'
path = '//10.72.26.46/irisnas6/Work/Aerosol/'
# path_data = '/share/irisnas6/Data/Aerosol/'
# path = '/share/irisnas6/Work/Aerosol/'
# addpath(genpath('/share/irisnas6/Work/Aerosol/matlab_func/'))

tg = ['PM10','PM25']

## Load grid
matlab.loadmat(os.path.join(path_data,'grid/grid_korea.mat'))
matlab.loadmat(os.path.join(path_data,'Station_Korea/stn_1km_location_weight.mat')) # stn_1km_location
# scode1,scode2, lat_org, lon_org, pxid, lat_px, lon_px

##
YEARS = [2015, 2016]
for yr in YEARS:
    # nanidx for cases
    mat = matlab.loadmat(os.path.join(path,'Korea/cases/', f'nanidx_1km_hourly_{yr}')) # nanidx
    nanidx = mat['nanidx']
    del mat
    
    # station
    mat = matlab.loadmat(os.path.join(path_data,'Station_Korea/' ,'Station_1km_rm_outlier_{yr}_weight.mat')) # stn_1km_yr
    stn_1km_yr = mat['stn_1km_yr']
    del mat
    
    stn_1km_yr[:,4] = stn_1km_yr[:,4]-9 # KST to UTC
    stn = stn_1km_yr
    
    stn_nanidx = []
    
    
    for doy in range(nanidx.shape[1]):
        for utc in range(7+1):
            nanidx_temp = nanidx[:,doy,utc]
            stn_temp = stn[stn[:,0]==doy & stn[:,4]==utc,:]
            
            for k in range(stn_temp.shape[0]):
                pid = stn_location[stn_location[:,1]==stn_temp[k,12],4]
                stn_temp[k,13]=nanidx_temp[pid]
            stn_nanidx = np.concatenate((stn_nanidx,stn_temp), axis=0)
    stn_fill = stn_nanidx[stn_nanidx[:,13]==0,:13]
    fname = f'KR_1km_stn_rf_day_{yr}.mat'
    matlab.savemat(os.path.join(path,'Korea', 'cases', fname), {'stn_fill':stn_fill})
    print (yr)

