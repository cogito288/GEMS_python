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

mat = matlab.loadmat(os.path.join(path_data,'grid/grid_goci.mat'))
latlon_data = np.array([mat['lon_goci'].ravel(order='F'),mat['lat_goci'].ravel(order='F')]).T
del mat

## South Korea
stn_info_kr = pd.read_csv(os.path.join(data_base_dir,'Station/Station_KR/stn_code_lonlat_period_2005_201904.csv'),header=1)
# scode1, scode2, lon, lat, op_start, op_

new_station = np.zeros((stn_info_kr.shape[0],4))
for i in range(len(stn_info_kr.shape[0])):
    dist = latlon_data
    dist[:,0] = dist[:,0]-stn_info_kr[i,3]
    dist[:,1] = dist[:,1]-stn_info_kr[i,2]
    dist[:,2] = np.sqrt(np.sum(np.power(dist[:,:2],2),2))
    dist_np.min = np.min(dist[:,2])
    new_station[i,0] = np.where(dist[:,2]==dist_np.min)[0]
    new_station[i,3] = dist_min

new_station[:,1:3]=latlon_data[new_station[:,0],:]

stn = np.hstack([stn_info_kr[:,[0,1,3,4]], new_station]) 
# scode1,scode2, lat_org, lon_org, pxid, lat_px, lon_px, dist_btw_org_px
# new_station = stn
# matlab.savemat(os.path.join(path_data,'Station_Korea/kr_GOCI6km_new_station.mat'],'new_station')

stn_unq = np.unique(stn[:,4])
unq_cnt = np.histogram(stn[:,4],stn_unq)
unqidx = unq_cnt!=1
stn_GOCI6km = stn[np.isin(stn[:,4],stn_unq[unqidx==0]),:]
stn_GOCI6km = np.hstack([stn_GOCI6km, np.zeros([stn_GOCI6km.shape[0], 1])])

idx = stn_unq[unqidx]
dup_scode2_GOCI6km = np.zeros([len(idx),np.max(unq_cnt)+1])
dup_scode2_GOCI6km[:,0]=idx

for i in range(len(idx)):
    aa = stn[stn[:,4]==dup_scode2_GOCI6km[i,0],1]
    dup_scode2_GOCI6km[i,1:np.max(aa.shape[0])+1]=aa

    stn_GOCI6km_temp = stn[stn[:,4]==idx[i],:]
    stn_GOCI6km_temp = np.hstack([stn_GOCI6km_temp, np.ones([stn_GOCI6km_temp.shape[0], 1])])
    stn_GOCI6km = np.vstack([stn_GOCI6km,stn_GOCI6km_temp])

stn_GOCI6km = stn_GOCI6km[stn_GOCI6km[:,1].argsort()]
stn_GOCI6km_location = stn_GOCI6km
header_stn_GOCI6km_location = ['scode1','scode2','lat_org','lon_org','pxid','lat_px','lon_px','avgid','dist']
fname = 'stn_GOCI6km_location_weight_v201904.mat'
matlab.savemat(os.path.join(data_base_dir,'Station/Station_KR', fname,
    {'stn_GOCI6km_location':stn_GOCI6km_location,
    'dup_scode2_GOCI6km':dup_scode2_GOCI6km,
    'header_stn_GOCI6km_location':header_stn_GOCI6km_location})