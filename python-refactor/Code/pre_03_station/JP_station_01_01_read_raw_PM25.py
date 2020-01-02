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

p=12; varname = 'PM25'; # p=51
header_p = ['doy','year','month','day','scode','ccode','KST', f'stn_{varname}']
# '측정년도/측정국코드/시도코드/측정항목코드/측정단위코드/측정월/측정일'

#stnPM25 = stnPM25_tbl_old_09.values
#stn_unq_09 = np.unique(stnPM25[:,[0,4,6]], axis=0)
#yr=2009
yr = 2016
# for yr=2015:2015#2016
file_list = glob.glob(os.path.join(path_in_situ, 'AirQuality_Japan', str(yr), f'*_{p:02d}.txt'))
file_list.sort()
data = None
for fname in file_list:
    data_temp = pd.read_csv(fname, encoding='latin1')
    if data is None: data = data_temp
    else: data = pd.concat([data, data_temp])
data = data.values
data_org = copy.deepcopy(data)
# data_unq = np.unique(data_org[:,[1,5,6]], axis=0)

data_p = data[:,3]
idx_PM25 = np.isin(data_p, ['PM25'])
idx_PMBH = np.isin(data_p, ['PMBH'])
idx_PMFL = np.isin(data_p, ['PMFL'])

data = np.delete(data, [3,4], axis=1)

# test1
data_PMBH = data[idx_PMBH,:]
data_PMFL = data[idx_PMFL,:]
data_PM25 = data[idx_PM25,:]
data_PMBH_unq = np.unique(data_PMBH[:,[1,3,4]].astype('float'), axis=0)
try:
    data_PMFL_unq = np.unique(data_PMFL[:,[1,3,4]].astype('float'), axis=0)
except:
    if len(data_PMFL[:,[1,3,4]].astype('float'))==0:
        print ('# of idx_PMFL is zero !!!')
        pass
data_PM25_unq = np.unique(data_PM25[:,[1,3,4]].astype('float'), axis=0)

# test2
stn_unq_PMFL = np.unique(data_PMFL[:,1])
stn_unq_PMBH = np.unique(data_PMBH[:,1])
stn_unq_PM25 = np.unique(data_PM25[:,1])
a = [val in stn_unq_PM25 for val in stn_unq_PMFL]; np.sum(a)
stn_unq_PMFL[a]
a_PM25 = data_PM25[data_PM25[:,1]==27115010,:]
a_PMFL = data_PMFL[data_PMFL[:,1]==27115010,:]

b = [val in stn_unq_PM25 for val in stn_unq_PMBH]; np.sum(b)
c = [val in stn_unq_PMBH for val in stn_unq_PMFL]; np.sum(c)
a2 = [val in stn_unq_PMFL for val in stn_unq_PM25]; np.sum(a2)
b2 = [val in stn_unq_PMBH for val in stn_unq_PM25]; np.sum(b2)
c2 = [val in stn_unq_PMFL for val in stn_unq_PMBH]; np.sum(c2)

#% PM25, PMBH 두개다 있는 스테이션값 중에서 PMBH로 측정한거 다 제거
#% idx_rm = idx_PMBH & ismember(data(:,2),27115010); % 2015-2016
idx_rm = (idx_PMFL & [val==27115010 for val in data[:, 1]]) # 2011-2014
data = data[~idx_rm]

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

if yr%4==0:
    tmp_idx = (data_new[:,2]==2) & (data_new[:,3]>29)
else:
    tmp_idx = (data_new[:,2]==2) & (data_new[:,3]>28)
data_new = data_new[~tmp_idx]

tmp_idx = (data_new[:,2]==4) & (data_new[:,3]==31)
data_new = data_new[~tmp_idx]
tmp_idx = (data_new[:,2]==6) & (data_new[:,3]==31)
data_new = data_new[~tmp_idx]
tmp_idx = (data_new[:,2]==9) & (data_new[:,3]==31)
data_new = data_new[~tmp_idx]
tmp_idx = (data_new[:,2]==11) & (data_new[:,3]==31)
data_new = data_new[~tmp_idx]

stn_tbl = pd.DataFrame(data_new, columns=header_p)
stn_tbl = stn_tbl.apply(pd.to_numeric)
matlab.savemat(os.path.join(path_stn_jp, f'JP_stnPM25_{yr}.mat'), 
               {col: stn_tbl[col].values for col in stn_tbl.columns})