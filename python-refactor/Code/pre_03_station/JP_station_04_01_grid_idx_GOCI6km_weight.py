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
#path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_grid_raw = os.path.join('//','10.72.26.56','irisnas5','Data','grid')
#path_grid_raw = os.path.join('/', 'share', 'irisnas5', 'Data', 'grid')
path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_goci.mat'))
latlon_data = np.array([mat['lat_goci'].ravel(order='F'),mat['lon_goci'].ravel(order='F')]).T
del mat
                     
## Japan
# scode1, scode2, lat, lon, installation, abolation
stn_info_jp = pd.read_csv(os.path.join(path_stn_jp, 'jp_stn_code_lonlat_period_filtered_yyyymmdd_v2017.csv'))
stn_info_jp = stn_info.values

new_station = np.zeros((stn_info_jp.shape[0],4))
for i in range(stn_info_jp.shape[0]):
    dist = copy.deepcopy(latlon_data)
    dist[:,0] = dist[:,0]-stn_info_jp[i,2]
    dist[:,1] = dist[:,1]-stn_info_jp[i,3]
    dist = np.hstack([dist, np.sqrt(np.sum(dist**2, axis=1)).reshape(-1, 1)])
    dist_min = np.min(dist[:,2])
    new_station[i,0] = np.where(dist[:, 2]==dist_min)[0]
    new_station[i,3] = dist_min
new_station[:,1:3]=latlon_data[new_station[:,0].astype('int'),:]
stn = np.hstack([stn_info_jp[:,[0,1,3,2]], new_station]) 
# scode1, scode2, lat_org, lon_org, pxid, lat_px, lon_px, dist_btw_org_px
# new_station = stn
# matlab.savemat(os.path.join(path_stn_jp,'jp_GOCI6km_new_station.mat'),{'new_station':new_station})

stn_unq = np.unique(stn[:,4])
unq_cnt = matlab.histogram_bin_center(stn[:,4], stn_unq)
unqidx = (unq_cnt!=1)
temp_list = stn_unq[unqidx==0]
stn_GOCI6km = stn[[val in temp_list for val in stn[:, 4]], :]
stn_GOCI6km = np.hstack([stn_GOCI6km, np.zeros([stn_GOCI6km.shape[0], 1])])

idx = stn_unq[unqidx]
dup_scode2_GOCI6km = np.zeros((len(idx),np.max(unq_cnt)+1))
dup_scode2_GOCI6km[:,0]=idx

for i in range(len(idx)):
    aa = stn[stn[:,4]==dup_scode2_GOCI6km[i,0],1]
    dup_scode2_GOCI6km[i,1:len(aa)+1]=aa
    stn_GOCI6km_temp = stn[stn[:,4]==idx[i],:]
    stn_GOCI6km_temp = np.hstack([stn_GOCI6km_temp, np.ones([stn_GOCI6km_temp.shape[0], 1])])
    stn_GOCI6km = np.vstack([stn_GOCI6km, stn_GOCI6km_temp])

stn_GOCI6km = stn_GOCI6km[stn_GOCI6km[:,1].argsort()]
jp_stn_GOCI6km_location = stn_GOCI6km
jp_dup_scode2_GOCI6km = dup_scode2_GOCI6km
header_jp_stn_GOCI6km_location = np.array(['scode1','scode2','lat_org','lon_org','pxid','lat_px','lon_px','dist','avgid'],
                                          dtype=h5py.string_dtype(encoding='utf-8'))
matlab.savemat(os.path.join(path_stn_jp,'jp_stn_GOCI6km_location_weight_v2017.mat'),
    {'jp_stn_GOCI6km_location':jp_stn_GOCI6km_location, 
     'jp_dup_scode2_GOCI6km':jp_dup_scode2_GOCI6km,
     'header_jp_stn_GOCI6km_location':header_jp_stn_GOCI6km_location})
