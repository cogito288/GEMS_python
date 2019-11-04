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

# Station index
# path_data = '//10.72.26.56/irisnas5/Data/'
path_data = '/share/irisnas5/Data/'
path_stn_kor = [path_data,'Station/Station_Korea/']
# addpath(genpath('/share/irisnas5/Data/matlab_func/'))

## South Korea
matlab.loadmat(os.path.join(path_stn_kor,'stn_GOCI6km_location_weight_v201904.mat'))

dup_scode2 = dup_scode2_GOCI6km[:,1:]
unq_scode2 = stn_GOCI6km_location[stn_GOCI6km_location[:,8]==0,1]
dup_dist = stn_GOCI6km_location[matlab.ismember(stn_GOCI6km_location[:,1],dup_scode2),[2,8]]

YEARS = [2019] #2005:2019
for yr in YEARS:
    tStart = time.time()
    fname = f'stn_scode_data_{yr}.mat'
    matlab.loadmat(os.path.join(path_stn_kor,'stn_scode_data', fname))
    # ndata_scode: {'DOY','year','month','day','time','SO2','CO','O3','NO2','PM10','PM25','scode1','scode2'}
    
    if yr%4==0: days=366 
    else: days=365 
     
    stn_GOCI6km_yr = []
    for doy in range(1,days+1):
        stn_temp = ndata_scode[ndata_scode[:,0]==doy,:]
        for KST in range(0, 23+1):
            stn_temp2 = stn_temp[stn_temp[:,4)==KST,:]
            if np.all(stn_temp2==0):
                stn_GOCI6km = stn_temp2[matlab.ismember(stn_temp2[:,12],unq_scode2),:]
                
                for j in range(dup_scode2.shape[0]):
                    stn_GOCI6km_temp = stn_temp2[matlab.ismember(stn_temp2[:,12],dup_scode2[j,:]),:]

                    if stn_GOCI6km_temp.shape[0]==1:
                        stn_GOCI6km_temp2 = stn_GOCI6km_temp
                        stn_GOCI6km = np.concatenate((stn_GOCI6km, stn_GOCI6km_temp2), axis=0)
                    elif stn_GOCI6km_temp.shape[0]!=0:
                        weight_sum = []
                        for k in range(stn_GOCI6km_temp.shape[0]):
                            stn_GOCI6km_temp[k,13] = dup_dist[dup_dist[:,1]==stn_GOCI6km_temp[k,12],1]
                            nanidx = np.isnan(stn_GOCI6km_temp[k,5:11])==0
                            weight = np.divide(nanidx, stn_GOCI6km_temp[k, 13])
                            stn_GOCI6km_temp[k,5:11] = np.multiply(stn_GOCI6km_temp[k, 5:11], weight)
                            weight_sum = np.concatenate((weight_sum, weight), axis=0)

                        
                        min_dist = np.min(stn_GOCI6km_temp[:,13])

                        stn_GOCI6km_temp2 = stn_GOCI6km_temp[stn_GOCI6km_temp[:,13]==min_dist,:]
                        if stn_GOCI6km_temp2.shape[0]!=1:
                            stn_GOCI6km_temp2[1:,:]=[]
                        # 픽셀중심에 더 가까운 관측소의 scode2를 사용하기 위함. 관측값은 가중평균한 값으로 다시 할당될거이므로 신경 쓰지말기
                        weight_sum = np.sum(weight_sum, axis=0)
                        stn_GOCI6km_temp2[5:11]=np.divide(np.nansum(stn_GOCI6km_temp[:,5:11],axis=0), weight_sum)
                        stn_GOCI6km = np.concatenate((stn_GOCI6km, stn_GOCI6km_temp2[:,:-1]), axis=0)
                
                stn_GOCI6km = matlab.sortrows(stn_GOCI6km,[13]) # sort by scode2
                stn_GOCI6km_yr = np.concatenate((stn_GOCI6km_yr, stn_GOCI6km), axis=0)

        print (doy)
    fname = f'Station_GOCI6km_{yr}_weight.mat'
    matlab.savemat(os.path.join(path_stn_kor,'Station/Station_JP'), fname, {'stn_GOCI6km_yr':stn_GOCI6km_yr})
    tElapsed = time.time() - tStart
