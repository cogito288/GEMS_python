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
# addpath(genpath('/share/irisnas5/Data/matlab_func/'))

matlab.loadmat(os.path.join(path_data,'grid/grid_goci.mat'))
latlon_data = np.asarray(list(zip(lat_goci.flatten(),lon_goci.flatten())))

## South Korea
stn_info_kr = pd.read_csv(os.path.join(path_data,'Station/Station_Korea/stn_code_lonlat_period_2005_201904.csv'),header=1)
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

stn = np.concatenate((stn_info_kr[:,[0,1,3,4]], new_station), axis=1) # scode1,scode2, lat_org, lon_org, pxid, lat_px, lon_px, dist_btw_org_px
# new_station = stn
# matlab.savemat(os.path.join(path_data,'Station_Korea/kr_GOCI6km_new_station.mat'],'new_station')

stn_unq = np.unique(stn[:,4])
unq_cnt = np.histogram(stn[:,4],stn_unq)
unqidx = unq_cnt!=1
stn_GOCI6km = stn[matlab.ismember(stn[:,4],stn_unq[unqidx==0]),:]
stn_GOCI6km[:,-1]=0

idx = stn_unq[unqidx]
dup_scode2_GOCI6km = np.zeros(len(idx),np.max(unq_cnt)+1)
dup_scode2_GOCI6km[:,0]=idx

for i in range(len(idx)):
    aa = stn[stn[:,4]==dup_scode2_GOCI6km[i,0],1]
    dup_scode2_GOCI6km[i,1:matlab.length(aa)+1]=aa

    stn_GOCI6km_temp = stn[stn[:,4]==idx[i],:]
    stn_GOCI6km_temp[:,-1]=1
    stn_GOCI6km = np.concatenate((stn_GOCI6km,stn_GOCI6km_temp), axis=0)


stn_GOCI6km = matlab.sortrows(stn_GOCI6km,[2])
stn_GOCI6km_location = stn_GOCI6km
header_stn_GOCI6km_location = ['scode1','scode2','lat_org','lon_org','pxid','lat_px','lon_px','avgid','dist']
# stn_1km_location_tbl = array2table(stn_1km_location, 'VariableNames',header)
# csvwrite_with_headers([path_data,'stn_1km.csv'],stn_1km,header)
fname = 'stn_GOCI6km_location_weight_v201904.mat'
matlab.savemat(os.path.join(path_data,'Station/Station_Korea', fname,
    {'stn_GOCI6km_location':stn_GOCI6km_location,
    'dup_scode2_GOCI6km':dup_scode2_GOCI6km,
    'header_stn_GOCI6km_location':header_stn_GOCI6km_location})


