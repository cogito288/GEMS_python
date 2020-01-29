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
import h5py
import time
from numba import njit, prange

### Setting path
#data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
#path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
#path_stn_jp = os.path.join(path_station, 'Station_JP')

#stn_info = pd.read_csv(os.path.join(path_stn_jp, 'jp_stn_code_lonlat_period_filtered_yyyymmdd.csv'))
#stn_info = stn_info.values
# scode1, scode2, lon, lat, op_start, op_
#scode_unq = np.unique(stn_info[:,0])
#del stn_info 

#data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
#data_base_dir = os.path.join('//', '10.72.26.56','irisnas5', 'GEMS', 'GEMS_python')
data_base_dir = os.path.join('/', 'share', 'irisnas5', 'GEMS', 'GEMS_python')
path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')

stn_info = pd.read_csv(os.path.join(path_stn_jp, 'jp_stn_code_lonlat_period_filtered_yyyymmdd_v2017.csv'))
stn_info = stn_info.values
# scode1, scode2, lat, lon, installation, abolation
scode_unq = np.unique(stn_info[:,0])
del stn_info 

header_ndata = np.array(['doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode'],
                        dtype=h5py.string_dtype(encoding='utf-8'))
def read_table_mat(fname):
    # should contain header column
    mat = matlab.loadmat(fname)
    tmp_cols = ['KST', 'scode', 'doy', list(mat.keys())[-2]]
    df = pd.DataFrame(columns=tmp_cols)
    for col in tmp_cols:
        df[col] = np.squeeze(mat[col])
    data = df.set_index(['KST', 'scode', 'doy'])
    del df
    print (os.path.basename(fname))
    return data

YEARS = [2016]
for yr in YEARS:
    t1 = time.time()
    if yr%4==0: days = 366
    else: days = 365
        
    idx = pd.MultiIndex.from_product([range(1, 24+1), scode_unq, range(1, days+1)],
                                 names=['KST', 'scode', 'doy'])
    cols = header_ndata[5:11]
    df = pd.DataFrame(np.nan, idx, cols)
    
    tmp_df = read_table_mat(os.path.join(path_stn_jp, 'byPollutant/',f'JP_stnSO2_{yr}.mat'))
    df['SO2'] = tmp_df['stnSO2']
    del tmp_df
    

    tmp_df = read_table_mat(os.path.join(path_stn_jp, 'byPollutant/',f'JP_stnCO_{yr}.mat'))
    df['CO'] = tmp_df['stnCO']
    del tmp_df
      
    tmp_df = read_table_mat(os.path.join(path_stn_jp, 'byPollutant/',f'JP_stnOX_{yr}.mat'))
    df['OX'] = tmp_df['stnOX']
    del tmp_df
    

    tmp_df = read_table_mat(os.path.join(path_stn_jp, 'byPollutant/',f'JP_stnNO2_{yr}.mat'))
    df['NO2'] = tmp_df['stnNO2']
    del tmp_df
        
    tmp_df = read_table_mat(os.path.join(path_stn_jp, 'byPollutant/',f'JP_stnSPM_{yr}.mat'))
    df['PM10'] = tmp_df['stnSPM']
    del tmp_df
    
    tmp_df = read_table_mat(os.path.join(path_stn_jp, 'byPollutant/',f'JP_stnPM25_{yr}.mat'))
    df['PM25'] = tmp_df['stnPM25']
    del tmp_df
    
    
    print ('Reading done !')   
    
    aa = np.array(list(df.index)) # KST, scode, doy
    df['KST'] = aa[:, 0]
    df['scode'] = aa[:, 1]
    df['doy'] = aa[:, 2]

    doy000 = matlab.datenum(f'{yr}00000')
    date_list = dict()
    for x in range(1, days+1):
        date_list[x] = matlab.datestr(doy000+x)

    dates = df['doy'].apply(lambda x: date_list[x])
    dates = pd.DatetimeIndex(dates)
    df['yr'] = dates.year
    df['mon'] = dates.month
    df['day'] = dates.day

    df.reset_index(drop=True, inplace=True)
    for col in cols:
        df.loc[df[col]>=9997, col] = np.nan
        df.loc[df[col]==-9999, col] = np.nan
    df.dropna(axis=0, subset=cols, how='all', inplace=True) # axis=0: row, subset: 기준 
    ndata = df[header_ndata].values
    ind = np.lexsort((ndata[:,4],ndata[:,0],ndata[:,11]))    # sort 11->0->4. 0 is primary
    ndata = ndata[ind]    
    matlab.savemat(os.path.join(path_stn_jp,'stn_code_data', f'stn_code_data_{yr}.mat'),
                       {'ndata':ndata, 'header_ndata':header_ndata})
    t2 = time.time() - t1
    print (f'time taken : {t2:.3f}')