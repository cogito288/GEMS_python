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

## Japan
matlab.loadmat(os.path.join(path_data,'Station/Station_JP/jp_stn_GOCI6km_location_weight.mat'))
jp_stn_GOCI6km_location = jp_stn_GOCI6km_location.sort(axis=1)

dup_scode2 = jp_dup_scode2_GOCI6km[:,1:]
unq_scode2 = jp_stn_GOCI6km_location[jp_stn_GOCI6km_location[:,8]==0,1]
dup_dist = jp_stn_GOCI6km_location[np.isin(jp_stn_GOCI6km_location[:,1], dup_scode2),[2,8]] # scode2랑 픽셀 중심과의 거리

YEARS = [2017, 2019+1]
for yr in YEARS:
    tStart = time.time()
    #     matlab.loadmat(os.path.join(path_data,'Station/Station_JP/jp_stn_scode_data_',str(yr),'.mat'])
    matlab.loadmat(os.path.join(data_base_dir,'Station/Station_JP', f'jp_stn_scode_data_rm_outlier_{yr}.mat'))
    ind = np.lexsort((ndata_scode[:, 12], ndata_scode[:,0], ndata_scode[:,4]))
    ndata_scode = ndata_scode[ind]

    if yr%4==0: days=366
    else: days=365
   
    stn_GOCI6km_yr = None
    for doy in range(1,days+1):
        stn_temp = ndata_scode[ndata_scode[:,0]==doy,:]
        for KST in range(9, 16+1): # 9:16 #1:24  #####
                stn_temp2 = stn_temp[stn_temp[:,4]==KST,:]
            if len(stn_temp2)!=0:
                stn_GOCI6km = stn_temp2[np.isin(stn_temp2[:,12],unq_scode2),:]
                for j in range(dup_scode2.shape[0]):
                    stn_GOCI6km_temp = stn_temp2[np.isin(stn_temp2[:,12],dup_scode2[j,:]),:]
                    if stn_GOCI6km_temp.shape[0]==1:
                        stn_GOCI6km_temp2 = stn_GOCI6km_temp
                        stn_GOCI6km = np.vstack([stn_GOCI6km, stn_GOCI6km_temp2])
                    else:
                        weight_sum = None
                        for k in range(stn_GOCI6km_temp.shape[0]):
                            stn_GOCI6km_temp[k,13] = dup_dist[dup_dist[:,1]==stn_GOCI6km_temp[k,12],1]
                            nanidx = np.isnan(stn_GOCI6km_temp[k,5:11])==0
                            weight = np.divide(nanidx, stn_GOCI6km_temp[k, 13])
                            stn_GOCI6km_temp[k,5:11] = np.multiply(stn_GOCI6km_temp[k, 5:11], weight)
                            if weight_sum is None:
                                weight_sum = weight
                            else:
                                weight_sum = np.vstack([weight_sum, weight])
                        min_dist = np.min(stn_GOCI6km_temp[:,13])
                        stn_GOCI6km_temp2 = stn_GOCI6km_temp[stn_GOCI6km_temp[:,13]==min_dist,:]
                        if stn_GOCI6km_temp2.shape[0]!=1:
                            stn_GOCI6km_temp2 = stn_GOCI6km_temp2[0,:]
                        # 픽셀중심에 더 가까운 관측소의 scode2를 사용하기 위함. 관측값은 가중평균한 값으로 다시 할당될거이므로 신경 쓰지말기
                        weight_sum = np.sum(weight_sum, axis=0)
                        stn_GOCI6km_temp2[5:11]=np.divide(np.nansum(stn_GOCI6km_temp[:,5:11],axis=0), weight_sum)
                        stn_GOCI6km = np.vstack([stn_GOCI6km, stn_GOCI6km_temp2[:,:-1]])
                stn_GOCI6km = stn_GOCI6km[stn_GOCI6km[:,12].argsort()] # sort by scode2
                stn_GOCI6km_yr = np.vstack([stn_GOCI6km_yr, stn_GOCI6km])
        print (doy)
    #     matlab.savemat(os.path.join(path_data,'Station/Station_JP/jp_Station_GOCI6km_',str(yr),'_weight'],'jp_stn_GOCI6km_yr','-v7.3')
    fname = f'jp_Station_GOCI6km_rm_outlier_{yr}_weight.mat'
    matlab.savemat(os.path.join(data_base_dir,'Station/Station_JP', fname),
                   {'jp_stn_GOCI6km_yr':jp_stn_GOCI6km_yr})
    tElapsed = time.time() - tStart
    
