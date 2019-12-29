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

p=11; varname = 'PM25'; # p=51
header_p = ['doy','year','month','day','scode','ccode','KST', f'stn_{varname}']
# '측정년도/측정국코드/시도코드/측정항목코드/측정단위코드/측정월/측정일'

stnPM25 = stnPM25_tbl_old_09.values
stn_unq_09 = np.unique(stnPM25[:,[0,4,6]], axis=0)
yr=2009

# for yr=2015:2015#2016
curr_path = os.path.join(path, str(yr))
file_list = glob.glob(os.path.join(station_path, 'Station_JP', str(yr), f'*_{p:02d}.txt'))
data=None
for fname in file_list:
    data_temp = pd.read_csv(fname)
    if data is None:
        data = data_temp
    else:
        data= np.vstack([data, data_temp])

data_org = copy.deepcopy(data)
# data_unq = np.unique(data_org[:,[1,5,6]], axis=0)

data_p = data[:,3]
idx_PM25 = data_p.isin('PM25')
idx_PMBH = data_p.isin('PMBH')
idx_PMFL = data_p.isin('PMFL')

data = np.delete(data, [2,3,4], axis=1)
data = data.values

# test1
data_PMBH = data[idx_PMBH,:]
data_PMFL = data[idx_PMFL,:]
data_PM25 = data[idx_PM25,:]
data_PMBH_unq = np.unique(data_PMBH[:,[1,3,4]], axis=0)
data_PMFL_unq = np.unique(data_PMFL[:,[1,3,4]], axis=0)
data_PM25_unq = np.unique(data_PM25[:,[1,3,4]], axis=0)

# test2
stn_unq_PMFL = np.unique(data_PMFL[:,1])
stn_unq_PMBH = np.unique(data_PMBH[:,1])
stn_unq_PM25 = np.unique(data_PM25[:,1])
a = matlab.ismember(stn_unq_PMFL,stn_unq_PM25); np.sum(a)
stn_unq_PMFL[a]
a_PM25 = data_PM25[data_PM25[:,1]==27115010,:]
a_PMFL = data_PMFL[data_PMFL[:,1]==27115010,:]

def ismember(subset_df, big_df):
    tuples = [tuple(x) for x in big_df.to_numpy()]
    idx = []
    for row in subset_df.index:
        idx.append(subset_df.roc[row].values in tuples)
    return idx
b = ismember(stn_unq_PMBH, stn_unq_PM25); np.sum(b)
c = ismember(stn_unq_PMFL,stn_unq_PMBH); np.sum(c)
a2 = ismember(stn_unq_PM25,stn_unq_PMFL); np.sum(a2)
b2 = ismember(stn_unq_PM25,stn_unq_PMBH); np.sum(b2)
c2 = ismember(stn_unq_PMBH,stn_unq_PMFL); np.sum(c2)

#% PM25, PMBH 두개다 있는 스테이션값 중에서 PMBH로 측정한거 다 제거
#% idx_rm = idx_PMBH & ismember(data(:,2),27115010); % 2015-2016
idx_rm = idx_PMFL & [val==27115010 for val in data[:, 1].values] # 2011-2014
data = np.delete(data, idx_rm, axis=0)

yrmonday = data[:,0]*10000 + data[:,3]*100 + data[:,4]
data_datenum = matlab.datenum(str(yrmonday))
doy_000 = matlab.datenum(f'{yr}00000')
data_doy = data_datenum-doy_000

data_info = np.hstack([data_doy,data[:,0],data[:,2],data[:,4],data[:,1:3]]) # 'doy','year','month','day','scode','ccode'

data_new = None
for KST in range(1,24+1):
    data_temp = data_info
    data_temp[:,6]=KST
    data_temp = np.hstack([data_temp, data[:,4+KST]])
    if data_new is None:
        data_new = data_temp
    else:
        data_new= np.vstack([data_new, data_temp])

if yr%4==0:
    data_new = np.delete(data_new, data_new[:,2]==2 & data_new[:,3]>29, axis=0)
else:
    data_new = np.delete(data_new, data_new[:,2]==2 & data_new[:,3]>28, axis=0)

data_new = np.delete(data_new, data_new[:,2]==4 & data_new[:,3]==31, axis=0)
data_new = np.delete(data_new, data_new[:,2]==6 & data_new[:,3]==31, axis=0)
data_new = np.delete(data_new, data_new[:,2]==9 & data_new[:,3]==31, axis=0)
data_new = np.delete(data_new, data_new[:,2]==11 & data_new[:,3]==31, axis=0)

stnPM25_tbl = pd.DateFrame(data_new, columns=header_p) 
matlab.savemat(os.path.join(station_path, 'Station_JP', f'JP_stnPM25_{yr}.mat'),stnPM25_tbl.to_dict('list'))