### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import glob
import pandas as pd

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km')

path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')
path_stn_cn = os.path.join(path_station, 'Station_CN')
path_stn_kr = os.path.join(path_station, 'Station_KR')

tg = ['PM10','PM25']

## Load grid
mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_goci.mat'))
lon_goci, lat_goci = mat['lon_goci'], mat['lat_goci']
del mat

YEARS = [ 2016]
for yr in YEARS:
    #mat = matlab.loadmat(os.path.join(path_stn_kr, 'stn_GOCI6km_location_weight_v2018.mat'))
    mat = matlab.loadmat(os.path.join(path_stn_kr, 'stn_GOCI6km_location_weight_v201904.mat'))
    dup_scode2_GOCI6km = mat['dup_scode2_GOCI6km']
    df = pd.DataFrame(mat['stn_GOCI6km_location'], columns=mat['header_stn_GOCI6km_location'])
    stn_GOCI6km_location = df.values
    del df, mat
    
    mat = matlab.loadmat(os.path.join(path_stn_cn, 'cn_stn_GOCI6km_location_weight.mat'))
    cn_dup_scode2_GOCI6km = mat['cn_dup_scode2_GOCI6km']
    header_cn_stn_GOCI6km_location = mat['header_cn_stn_GOCI6km_location']
    df = pd.DataFrame(mat['cn_stn_GOCI6km_location'], columns=header_cn_stn_GOCI6km_location)
    cn_stn_GOCI6km_location = df.values
    del df, mat

    stn_location = np.concatenate((stn_GOCI6km_location,cn_stn_GOCI6km_location), axis=0)
    # scode1,scode2, lat_org, lon_org, pxid, lat_px, lon_px
    
    # nanidx for cases
    fname = f'nanidx_EA6km_{yr}.mat'
    mat = matlab.loadmat(os.path.join(path_ea_goci, fname)) # nanidx
    nanidx = mat['nanidx']
    del mat
    
    # station
    fname = f'Station_GOCI6km_rm_outlier_{yr}_weight.mat'
    mat = matlab.loadmat(os.path.join(path_stn_kr, fname)) # stn_GOCI6km_yr
    stn_GOCI6km_yr = mat['stn_GOCI6km_yr']
    del mat

    fname = f'cn_Station_GOCI6km_rm_outlier_{yr}_weight.mat'
    matlab.loadmat(os.path.join(path_stn_cn,'Station_CN', fname)) # cn_stn_GOCI6km_yr
    cn_stn_GOCI6km_yr = mat['cn_stn_GOCI6km_yr']
    del mat
    
    stn_GOCI6km_yr[:,4]=stn_GOCI6km_yr[:,4]-9
    cn_stn_GOCI6km_yr[:,4]=cn_stn_GOCI6km_yr[:,4]-8
    stn = np.concatenate((stn_GOCI6km_yr, cn_stn_GOCI6km_yr[:,[0,1,2,3,4,10,18,14,12,8,6,20,21]]), axis=0)
    
    del stn_GOCI6km_location, dup_scode2_GOCI6km, header_stn_GOCI6km_location
    del cn_stn_GOCI6km_location, cn_dup_scode2_GOCI6km, header_cn_stn_GOCI6km_location
    del stn_GOCI6km_yr, cn_stn_GOCI6km_yr
    
    stn_nanidx = []
    for doy in range(1, nanidx.shape[1]+1):
        for utc in range(7+1):
            nanidx_temp = nanidx[:,doy-1,utc]
            stn_temp = stn[stn[:,0]==doy & stn[:,4]==utc,:]
            
            for k in range(stn_temp.shape[0]):
                pid = stn_location[stn_location[:,1]==stn_temp[k,12],4]
                stn_temp[k,13]=nanidx_temp[pid]
            stn_nanidx = np.concatenate((stn_nanidx,stn_temp), axis=0)

    stn_fill = stn_nanidx[stn_nanidx[:,13]==0,:13]
    fname = f'stn_rf_day_{yr}.mat'
    matlab.savemat(os.path.join(path_ea_goci, fname), {'stn_fill':stn_fill})
    print (yr)