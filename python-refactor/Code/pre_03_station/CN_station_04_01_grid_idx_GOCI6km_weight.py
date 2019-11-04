### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import scipy.io as sio
import numpy as np
import glob
import pandas as pd

### Setting path
data_base_dir = os.path.join('/', 'media', 'sf_GEMS_1', 'Data')
raw_data_path = os.path.join(data_base_dir, 'Raw', 'GOCI_AOD') 
write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_AOD')

path_data = '//10.72.26.56/irisnas5/Data/'
# path_data = '/share/irisnas5/Data/'
# path = '/share/irisnas6/Work/Aerosol/'
# addpath(genpath('/share/irisnas2/Data/Aerosol_Work/matlab_func/'))

matlab.loadmat(os.path.join(path_data,'grid/grid_goci.mat'))
latlon_data = np.concatenate((lat_goci.flatten(),lon_goci.flatten()), axis=1)

## China
stn_info_cn = pd.read_csv(os.path.join(path_data,'Station/Station_CN/cn_stn_code_lonlat_period_GOCI.csv'),header=1)
# scode1, scode2, lon, lat, op_start, op_
# idx_coverage = stn_info_cn[:,2]>=113 & stn_info_cn[:,2]<=147 & stn_info_cn[:,4)>=24 & stn_info_cn[:,4)<=48
# stn_info_cn = stn_info_cn(idx_coverage,:)

new_station = np.zeros((stn_info_cn.shape[0],4))
for i in range(stn_info_cn.shape[0]):
    dist = latlon_data
    dist[:,0] = dist[:,0]-stn_info_cn[i,3]
    dist[:,1] = dist[:,1]-stn_info_cn[i,2]
    dist[:,2] = np.sqrt(np.sum(np.power(dist[:,:2], 2),axis=1))
    dist_min = np.min(dist[:,1])
    new_station[i,0] = np.where(dist[:, 2]==dist_min)[0] #find(dist[:,2]==dist_min)
    new_station[i,3] = dist_min

new_station[:,1:3]=latlon_data[new_station[:,0],:]

stn = np.concatenate((stn_info_cn[:,[0,1,3,2]), new_station), axis=1) # scode1,scode2, lat_org, lon_org, pxid, lat_px, lon_px, dist_btw_org_px
# new_station = stn
# matlab.savemat(os.path.join(path_data,'Station_CN/cn_GOCI6km_new_station.mat'],'new_station')

stn_unq = np.unique(stn[:,4])
unq_cnt = hist(stn[:,5),stn_unq)
unqidx = unq_cnt!=1
stn_GOCI6km = stn[stn[:, 4] in stn_unq[unqidx==0], :]
stn_GOCI6km[:,-1]=0

idx = stn_unq[unqidx]
dup_scode2_GOCI6km = np.zeros((matab.length(idx),np.max(unq_cnt)+1))
dup_scode2_GOCI6km[:,0]=idx

for i in range(matlab.length(idx)):
    aa = stn[stn[:,4]==dup_scode2_GOCI6km[i,0],1]
    dup_scode2_GOCI6km[i,1:matlab.length(aa)+1]=aa

    stn_GOCI6km_temp = stn[stn[:,4]==idx[i],:]
    stn_GOCI6km_temp[:,-1]=1
    stn_GOCI6km = np.concatenate((stn_GOCI6km, stn_GOCI6km_temp), axis=1)

#[b,I] = sortrows(a,i) -> I = argsort(a[:,i]), b=a[I,:]
tmp_idx = np.argsort(stn_GOCI6km, axis=1)
stn_GOCI6km = stn_GOCI6km[tpm_idx]
cn_stn_GOCI6km_location = stn_GOCI6km
cn_dup_scode2_GOCI6km = dup_scode2_GOCI6km
header_cn_stn_GOCI6km_location = ['scode1','scode2','lat_org','lon_org','pxid','lat_px','lon_px','avgid','dist']
# stn_1km_location_tbl = array2table(stn_1km_location, 'VariableNames',header)
# csvwrite_with_headers([path_data,'stn_1km.csv'],stn_1km,header)
matlab.savemat(os.path.join(path_data,'Station/Station_CN/cn_stn_GOCI6km_location_weight.mat'],
    {'cn_stn_GOCI6km_location':cn_stn_GOCI6km_location, 
     'cn_dup_scode2_GOCI6km':cn_dup_scode2_GOCI6km,
     'header_cn_stn_GOCI6km_location':header_cn_stn_GOCI6km_location})
