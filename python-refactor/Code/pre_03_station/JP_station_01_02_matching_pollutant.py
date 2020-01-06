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
path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')

data_tbl = pd.read_csv(os.path.join(path_stn_jp, 'stn_code_ing/jp_stn_code_lonlat_period_year.csv'))
data = data_tbl.values
info_tbl = pd.read_csv(os.path.join(path_stn_jp, 'stn_code_ing/measured_pollutant_by_stn.csv'), encoding='latin1')
info_tbl = info_tbl.loc[:, ['Year','scode','SO2','CO','OX','NO2','SPM','PM25','NO','NOX','NMHC','CH4']]
info = info_tbl.values
info[np.isnan(info)]=0  

data = np.hstack([data, np.zeros([data.shape[0], 6])])
for k in range(data.shape[0]):
    data[k,7:]=info[(info[:,0]==data[k,6]) & (info[:,1]==data[k,0]),2:8]
a = np.sum(data[:,7:], axis=1)
aidx = (a==0)
data2 = np.hstack([data[:,:7],aidx.reshape(-1,1)])