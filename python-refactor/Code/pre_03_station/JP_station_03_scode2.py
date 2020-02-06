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
data_base_dir = os.path.join(base_dir,'Data')
path_in_situ = os.path.join(data_base_dir, 'Raw', 'In_situ')
path_station = os.path.join(data_base_dir, 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')

stn_info = pd.read_csv(os.path.join(path_in_situ, 'AirQuality_Japan', 'jp_stn_code_lonlat_period_filtered_yyyymmdd_v2017.csv'))
stn_info = stn_info.values
# scode1, scode2, lat, lon, installation, abolation

## read stn_code_data file
header_ndata = np.array(['doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode','scode2'],
                        dtype=h5py.string_dtype(encoding='utf-8'))

YEARS = range(2015, 2017+1)
for yr in YEARS:
    if os.path.isfile(os.path.join(path_stn_jp,'stn_code_data', f'stn_code_data_{yr}.mat')):
        ndata = matlab.loadmat(os.path.join(path_stn_jp,'stn_code_data', f'stn_code_data_{yr}.mat'))['ndata']
        fname_save = f'jp_stn_scode_data_{yr}.mat'
    else:
        ndata = matlab.loadmat(os.path.join(path_stn_jp,'stn_code_data', f'stn_code_data_rm_outlier_{yr}.mat'))['stn_JP']
        fname_save = f'jp_stn_scode_data_rm_outlier_{yr}.mat'
    ndata[ndata==-9999]=np.nan
    
    ## stn_scode_data for Japan
    ndata = np.hstack([ndata, np.zeros([ndata.shape[0], 1])]) # ndata[:,12]=0  add column for scode2
    
    ndata_scode = None
    # Assign scode2
    for j in range(stn_info.shape[0]): 
        ndata_temp = ndata[ndata[:,-2]==stn_info[j,0],:]
        if yr==2019: mm = 5
        else: mm = 12
        for k in range(1,mm+1): 
            for dd in range(1,31+1):
                ndata_temp2 = ndata_temp[(ndata_temp[:,2]==k) & (ndata_temp[:,3]==dd),:]
                if len(ndata_temp2)!=0:
                    yyyymmdd = yr*10000+k*100+dd
                    idx = (stn_info[j,4] < yyyymmdd) & (stn_info[j,5] >= yyyymmdd)
                    if idx==1:
                        ndata_temp2[:,-1]=stn_info[j,1]
                        if ndata_scode is None:
                            ndata_scode = ndata_temp2
                        else:
                            ndata_scode=np.vstack([ndata_scode,ndata_temp2])
        if (j+1)%50==0:
            fname = f'stn_scode_data_{yr}_{j-48:04d}.mat'
            matlab.savemat(os.path.join(path_stn_jp, fname), {'ndata_scode':ndata_scode})
            ndata_scode = None
        elif (j+1)==stn_info.shape[0]:
            if ndata_scode is not None:
                fname = f'stn_scode_data_{yr}_{np.int((j+1)/50)*50+1:04d}.mat'
                matlab.savemat(os.path.join(path_stn_jp, fname), {'ndata_scode':ndata_scode})
        print (f'{j+1} / {stn_info.shape[0]}')
    
    ndata_scode = None
    file_list = glob.glob(os.path.join(path_stn_jp, f'stn_scode_data_{yr}_*.mat'))
    file_list.sort()
    for fname in file_list:
        print (f'Reading ... {os.path.basename(fname)}')
        ndata_scode_temp = matlab.loadmat(fname)['ndata_scode']
        print (ndata_scode_temp.shape)
        if ndata_scode is None:
            ndata_scode = ndata_scode_temp
        else:
            ndata_scode = np.vstack([ndata_scode, ndata_scode_temp])
    
    matlab.savemat(os.path.join(path_stn_jp, 'stn_scode_data', fname_save), 
                   {'ndata_scode':ndata_scode,'header_ndata':header_ndata})
    
    for fname in file_list: 
        os.remove(fname)
        