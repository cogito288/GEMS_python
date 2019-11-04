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

## China
# path_data = '//10.72.26.56/irisnas5/Data/'
path_data = '/share/irisnas5/Data/'

fname = f'cn_stn_GOCI6km_location_weight.mat'
mat = matlab.loadmat(os.path.join(path_data,'Station/Station_CN/', fname)) # period_GOCI.csv 사용해서 만든거

dup_scode2 = cn_dup_scode2_GOCI6km[:,1:]
unq_scode2 = cn_stn_GOCI6km_location[cn_stn_GOCI6km_location[:,8]==0, 1]
dup_dist = cn_stn_GOCI6km_location[matlab.ismember(cn_stn_GOCI6km_location[:,1],dup_scode2), [1,7]]

YEARS = [2016] # range(2015, 2019+1)
for yr in YEARS:
    fname = f'cn_stn_scode_data_rm_outlier_{yr}.mat'
    mat = matlab.loadmat(os.path.join(path_data,'Station/Station_CN/stn_scode_data/', fname))

    if yr%4==0: days=366; else: days=365; 
    
    stn_GOCI6km_yr = []
    for doy in range(1, days+1):
        stn_temp = ndata_scode[ndata_scode[:,0]==doy,:]
        for CST in range(8, 15+1): #= 8:15  # 0:23  ###### 1:24
            stn_temp2 = stn_temp[stn_temp[:,4]==CST,:]
            if np.all(stn_temp2==0):
                stn_GOCI6km = stn_temp2[matlab.ismember(stn_temp2[:,21],unq_scode2),:[

                for j in range(dup_scode2.shape[0]):
                    stn_GOCI6km_temp = stn_temp2[matlab.ismember(stn_temp2[:,21],dup_scode2[j,:]),:]

                    if stn_GOCI6km_temp.shape[0]==1:
                        stn_GOCI6km_temp2 = stn_GOCI6km_temp
                        stn_GOCI6km = np.concatenate((stn_GOCI6km, stn_GOCI6km_temp2), axis=1)
                    elif stn_GOCI6km_temp.shape[0]!=0:
                        weight_sum = []
                        for k in range(stn_GOCI6km_temp.shape[0]):
                            stn_GOCI6km_temp[k,22] = dup_dist[dup_dist[:,0]==stn_GOCI6km_temp[k,21],1]
                            nanidx = np.isnan(stn_GOCI6km_temp[k,5:20])==0
                            weight = np.divide(nanidx, stn_GOCI6km_temp[k,22])
                            stn_GOCI6km_temp[k,5:20] = np.multiplye(stn_GOCI6km_temp[k,5:20], weight)
                            weight_sum = np.concatenate((weight_sum, weight), axis=1)
                        

                        min_dist = np.min(stn_GOCI6km_temp[:,22])

                        stn_GOCI6km_temp2 = stn_GOCI6km_temp[stn_GOCI6km_temp[:,22]==min_dist,:]
                        if stn_GOCI6km_temp2.shape[0]!=1:
                            stn_GOCI6km_temp2[2:,:] = []
                        
                        # 픽셀중심에 더 가까운 관측소의 scode2를 사용하기 위함. 관측값은 가중평균한 값으로 다시 할당될거이므로 신경 쓰지말기

                        weight_sum = np.sum(weight_sum,axis=0)
                        stn_GOCI6km_temp2[0,5:20]=np.divide(np.nansum(stn_GOCI6km_temp[:,4:20], axis=0), weight_sum)
                        stn_GOCI6km = np.concatenate((stn_GOCI6km, stn_GOCI6km_temp2[:,:-1]), axis=1)
                    
                temp_idx = np.argsort(stn_GOCI6km[:,21]) # sortrows(stn_GOCI6km,22); # sort by scode2
                stn_GOCI6km = stn_GOCI6km[temp_idx]
                stn_GOCI6km_yr = np.concatenate((stn_GOCI6km_yr, stn_GOCI6km), axis=1)
        print (doy)
    
    cn_stn_GOCI6km_yr=stn_GOCI6km_yr 
    fname = f'cn_Station_GOCI6km_rm_outlier_{yr}_weight.mat'
    matlab.savemat(os.path.join(path_data,'Station/Station_CN/'), fname,{'cn_stn_GOCI6km_yr':cn_stn_GOCI6km_yr})
