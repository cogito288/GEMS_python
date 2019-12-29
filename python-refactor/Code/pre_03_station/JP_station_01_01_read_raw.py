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
raw_path = os.path.join(data_base_dir, 'Raw') 
station_path = os.path.join(data_base_dir, 'Station') 

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

# p=0; varname = 'SO2'
# p=1; varname = 'NO'
# p=2; varname = 'NO2'
# p=3; varname = 'NOX'
# p=4; varname = 'CO'
# p=5; varname = 'OX'
# p=6; varname = 'NMHC'
# p=7; varname = 'CH4'
# p=8; varname = 'THC'
# p=9; varname = 'SPM'
# p=11; varname = 'PM25'; p=50
# p=20; varname = 'WD'
# p=21; varname = 'WS'
# p=22; varname = 'TEMP'
# p=23; varname = 'HUM'
# p=24; varname = 'SUN'
# p=25; varname = 'RAIN'
# p=26; varname = 'UV'
# p=27; varname = 'PRS'
# p=28; varname = 'NETR'
# p=40; varname = 'CO2'
# p=41; varname = 'O3'
varname = 'PM25'; p=50

header_p = ['doy','year','month','day','scode','ccode','KST', 'stn_{varname}']
# '측정년도/측정국코드/시도코드/측정항목코드/측정단위코드/측정월/측정일'

YEARS = [2016] # range(2009, 2009+1)
for y in YEARS:
    file_list = glob.glob(os.path.join(station_path, 'Station_JP', str(yr), f'*_{p:02d}.txt'))
    data= None
    for fname in file_list:
        data_temp = pd.read_csv(fname)
        if data is None:
            data = data_temp
        else:
            data = pd.concat([data, data_temp])
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
    #vars()[f'stn{varname}_tbl'].to_csv(os.path.join(station_path, 'Station_JP', f'JP_stn{varname}_{yr}.csv'))
    matlab.savemat(os.path.join(station_path, 'Station_JP', f'JP_stn{varname}_{yr}.mat'), vars()[f'stn{varname}_tbl'].to_dict('list'))