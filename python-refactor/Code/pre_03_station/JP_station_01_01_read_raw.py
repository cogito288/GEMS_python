### Package Import
import sys
import os
#base_dir = os.environ['GEMS_HOME']
base_dir = 'D:\github\GEMS_python'
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import copy
import numpy as np
import pandas as pd
import glob

### Setting path
#data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
#path_in_situ = os.path.join(data_base_dir, 'Raw') 
data_base_dir = os.path.join('//', '10.72.26.56','irisnas5', 'GEMS', 'GEMS_python')
path_in_situ = os.path.join('//','10.72.26.46','irisnas6','Data','In_situ')
#data_base_dir = os.path.join('/', 'share', 'irisnas5', 'GEMS', 'GEMS_python')
#path_in_situ = os.path.join('/','share','irisnas6','Data','In_situ')
path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')

# header = {'doy','year','month','day','KST','SO2','CO','O3','NO2','PM10','PM25','scode'}
pcode = [['01','SO2','ppb'],
         ['03','NO2','ppb'],
         ['05','CO','x01ppm'],
         ['06','OX','ppb'],
         ['10','SPM','ug_m3'],
         ['12','PM25','ug_m3']]

for p,varname,unit in pcode:
    header_p = ['doy','year','month','day','scode','ccode','KST',f'stn_{varname}']
    # 'yr/scode/ccode/pcode/unit/month/day'
   
    YEARS = [2016] # range(2009, 2009+1)
    for yr in YEARS:
        file_list = glob.glob(os.path.join(path_in_situ, 'AirQuality_Japan', str(yr), f'*_{p}.txt'))
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
        #stn_tbl.to_csv(os.path.join(path_stn_jp, f'JP_stn{varname}_{yr}.csv'),sep=',',na_rep='NaN')
        