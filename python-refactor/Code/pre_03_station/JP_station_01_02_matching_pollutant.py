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
data_base_dir = os.path.join(base_dir, 'Data')
path_in_situ = os.path.join(data_base_dir, 'Raw', 'In_situ')
path_station = os.path.join(data_base_dir, 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')

data_tbl = pd.read_csv(os.path.join(path_in_situ, 'AirQuality_Japan', 'jp_stn_code_lonlat_period_year_v2017.csv'))
data = data_tbl.values
info_tbl = pd.read_csv(os.path.join(path_in_situ, 'AirQuality_Japan', 'measured_pollutant_by_stn_v2017.csv'), encoding='latin1')
info_tbl = info_tbl.loc[:, ['Year','scode','SO2','CO','OX','NO2','SPM','PM25']]
info = info_tbl.values
info[np.isnan(info)]=0  

data = np.hstack([data, np.zeros([data.shape[0], 6])])
for k in range(data.shape[0]):
    try:
        data[k,7:]=info[(info[:,0]==data[k,6]) & (info[:,1]==data[k,0]),2:8]
    except:
        pass
a = np.sum(data[:,7:], axis=1)
aidx = (a==0)
data2 = data[~aidx,:6]

header = np.array(['scode','scode2','lat','lon','installation','abolation'],
                  dtype=h5py.string_dtype(encoding='utf-8'))
data2_tbl = pd.DataFrame(data2, columns=header)
data2_tbl.to_csv(os.path.join(path_in_situ, 'AirQuality_Japan','jp_stn_code_lonlat_period_filtered_yyyymmdd_v2017.csv'),
                 sep=',',na_rep='NaN',index=False)
