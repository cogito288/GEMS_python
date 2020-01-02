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
path_in_situ = os.path.join(data_base_dir, 'Raw') 
path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')

# header = {'doy','year','month','day','KST','SO2','CO','O3','NO2','PM10','PM25','scode'}
pcode = [['01','SO2','ppb'],
         ['02','NO','ppb'], 
         ['03','NO2','ppb'],
         ['04','NOX','ppb'],
         ['05','CO','x01ppm'],
         ['06','OX','ppb'],
         ['07','NMHC','x10ppbc'],
         ['08','CH4','x10ppbc'],
         ['09','THC','x10ppbc'],
         ['10','SPM','ug_m3'],
         ['12','PM25','ug_m3'],
         ['21','WD','x16DIRC'],
         ['22','WS','x01m_s'],
         ['23','TEMP','x01degC'],
         ['24','HUM','percent'],
         ['25','SUN','x001MJ'],
         ['26','RAIN','mm'],
         ['27','UV','x001MJ'],
         ['28','PRS','mb'],
         ['29','NETR','x001MJ'],
         ['41','CO2','x01ppm'],
         ['42','O3','ppb']]

# '43','HCL'; '44','HF'; '45','H2S'; '46','SHC'; '47','UHC'

# p=1; varname = 'SO2'
# p=2; varname = 'NO'
# p=3; varname = 'NO2'
# p=4; varname = 'NOX'
# p=5; varname = 'CO'
# p=6; varname = 'OX'
# p=7; varname = 'NMHC'
# p=8; varname = 'CH4'
# p=9; varname = 'THC'
# p=10; varname = 'SPM'
# p=12; varname = 'PM25'; p=51
# p=21; varname = 'WD'
# p=22; varname = 'WS'
# p=23; varname = 'TEMP'
# p=24; varname = 'HUM'
# p=25; varname = 'SUN'
# p=26; varname = 'RAIN'
# p=27; varname = 'UV'
# p=28; varname = 'PRS'
# p=29; varname = 'NETR'
# p=41; varname = 'CO2'
# p=42; varname = 'O3'
varname = 'PM25'; p=12

header_p = ['doy','year','month','day','scode','ccode','KST', f'stn_{varname}']
# '측정년도/측정국코드/시도코드/측정항목코드/측정단위코드/측정월/측정일'

YEARS = [2016] # range(2009, 2009+1)
for yr in YEARS:
    file_list = glob.glob(os.path.join(path_in_situ, 'AirQuality_Japan', str(yr), f'*_{p:02d}.txt'))
    file_list.sort()
    data = None
    for fname in file_list:
        data_temp = pd.read_csv(fname, encoding='latin1')
        if data is None: data = data_temp
        else: data = pd.concat([data, data_temp])
    data = data.values
    if varname == 'PM25': #Need to check
        vv = data[:, 3]
        idx_PM25 = np.isin(vv, ['PM25'])
        idx_PMBH = np.isin(vv, ['PMBH'])
        idx_PMFL = np.isin(vv, ['PMFL'])
        data_PMBH = data[idx_PMBH, :]
        data_PMFL = data[idx_PMFL, :]
        data = data[idx_PM25,:]

    data = np.delete(data, [3,4], axis=1)
    yrmonday = data[:,0]*10000 + data[:,3]*100 + data[:,4]
    data_datenum = [matlab.datenum(str(val)) for val in yrmonday]
    doy_000 = matlab.datenum(f'{yr}00000')
    data_doy = np.array([val-doy_000 for val in data_datenum])

    data_info = np.hstack([data_doy.reshape(-1,1),data[:,0].reshape(-1,1),data[:,3].reshape(-1,1),data[:,4].reshape(-1,1),data[:,1:3]]) # 'doy','year','month','day','scode','ccode'
    data_new = None
    for KST in range(1,24+1):
        data_temp = data_info
        data_temp = np.hstack([data_temp, np.full([data_temp.shape[0], 1], KST)]) #data_temp[:,6]=KST
        data_temp = np.hstack([data_temp, data[:,4+KST].reshape(-1,1)])
        if data_new is None: data_new = data_temp
        else: data_new= np.vstack([data_new, data_temp])
    stn_tbl = pd.DataFrame(data_new, columns=header_p)
    stn_tbl = stn_tbl.apply(pd.to_numeric)
    matlab.savemat(os.path.join(path_stn_jp, f'JP_stn{varname}_{yr}.mat'), 
                   {col: stn_tbl[col].values for col in stn_tbl.columns})