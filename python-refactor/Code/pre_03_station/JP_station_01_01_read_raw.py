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
data_base_dir = os.path.join('//', '10.72.26.56','irisnas5', 'GEMS', 'GEMS_python')
#data_base_dir = os.path.join('/', 'share', 'irisnas5', 'GEMS', 'GEMS_python')
path_in_situ = os.path.join('/','share','irisnas6','Data','In_situ')
path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 

# header = {'doy','year','month','day','KST','SO2','CO','O3','NO2','PM10','PM25','scode'}
pcode = [['01','SO2','ppb'],
         ['03','NO2','ppb'],
         ['05','CO','x01ppm'],
         ['06','OX','ppb'],
         ['10','SPM','ug_m3'],
         ['12','PM25','ug_m3']]

# p=0; varname = 'SO2'
# p=2; varname = 'NO2'
# p=4; varname = 'CO'
# p=5; varname = 'OX'
# p=9; varname = 'SPM'
# p=11; varname = 'PM25'; p=50

for p,varname,unit in pcode:
    header_p = ['doy','year','month','day','scode','ccode','KST',f'stn_{varname}']
    # 'yr/scode/ccode/pcode/unit/month/day'

    YEARS = [2016] # range(2009, 2009+1)
    for yr in YEARS:
        file_list = glob.glob(os.path.join(path_in_situ, 'Station_JP', str(yr), f'*_{p:02d}.txt'))
        for fname in file_list:
            data_temp = pd.read_csv(fname)
            if data is None:
                data = data_temp
            else:
                data = pd.concat([data, data_temp])
            print (data)
        if varname == 'PM25': #Need to check
            vv = data[:, data.columns[3]]
            idx_PM25 = vv.isin(['PM25'])
            idx_PMBH = vv.isin(['PMBH'])
            idx_PMFL = vv.isin(['PMFL'])
            data_PMBH = data[idx_PMBH]
            data_PMFL = data[idx_PMFL]
            data = data[idx_PM25,:]
    
        data = np.delete(data, [3,4], axis=1)
        data = data.values
        yrmonday = data[:,0]*10000 + data[:,3]*100 + data[:,4]
        data_datenum = matlab.datenum(str(yrmonday))
        doy_000 = matlab.datenum(f'{yr}00000')
        data_doy = data_datenum-doy_000
    
        data_info = np.hstack([data_doy,data[:,0],data[:,3],data[:,4],data[:,1:3]]) # 'doy','year','month','day','scode','ccode'
        data_new = None
        for KST in range(1,24+1):
            data_temp = data_info
            data_temp[:,6]=KST
            data_temp = np.hstack([data_temp, data[:,4+KST]])
            if data_new is None:
                data_new = data_temp
            else:
                data_new= np.vstack([data_new, data_temp])
        vars()[f'stn{varname}_tbl'] = pd.DateFrame(data_new, columns=header_p) 
        matlab.savemat(os.path.join(path_station, 'Station_JP', f'JP_stn{varname}_{yr}.mat'), 
                       {col: vars()[f'stn{varname}_tbl'][col].values for col in vars()[f'stn{varname}_tbl'].columns})