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
import time

### Setting path
data_base_dir = os.path.join(base_dir, 'Data')
path_station = os.path.join(data_base_dir, 'Station') 
path_stn_kr = os.path.join(path_station, 'Station_KR')

## South Korea
mat = matlab.loadmat(os.path.join(path_stn_kr,'stn_GOCI6km_location_weight_v201904.mat'))
dup_scode2_GOCI6km, stn_GOCI6km_location = mat['dup_scode2_GOCI6km'], mat['stn_GOCI6km_location']
del mat

dup_scode2 = dup_scode2_GOCI6km[:,1:]
unq_scode2 = stn_GOCI6km_location[stn_GOCI6km_location[:,8]==0,1]
idx = [val in dup_scode2 for val in stn_GOCI6km_location[:,1]]
dup_dist = stn_GOCI6km_location[idx][:, [1,7]]

YEARS = range(2014,2018+1)
for yr in YEARS:
    tStart = time.time()
    ndata_scode = matlab.loadmat(os.path.join(path_stn_kr,'stn_scode_data', f'stn_scode_data_{yr}.mat'))['ndata_scode']
    # ndata_scode: {'DOY','year','month','day','time','SO2','CO','O3','NO2','PM10','PM25','scode1','scode2'}
    
    if yr%4==0: days=366 
    else: days=365 
    
    stn_GOCI6km_yr = None
    for doy in range(1,days+1):
        stn_temp = ndata_scode[ndata_scode[:,0]==doy,:]
        for KST in range(0, 23+1):
            stn_temp2 = stn_temp[stn_temp[:,4]==KST,:]
            if len(stn_temp2)!=0:
                idx = [val in unq_scode2 for val in stn_temp2[:,12]]
                stn_GOCI6km = stn_temp2[idx, :]
                
                for j in range(dup_scode2.shape[0]):
                    idx = [val in dup_scode2[j,:] for val in stn_temp2[:,12]]
                    stn_GOCI6km_temp = stn_temp2[idx,:]

                    if stn_GOCI6km_temp.shape[0]==1:
                        stn_GOCI6km_temp2 = stn_GOCI6km_temp
                        stn_GOCI6km = np.vstack([stn_GOCI6km, stn_GOCI6km_temp2])
                    elif stn_GOCI6km_temp.shape[0]!=0:
                        weight_sum = None
                        if stn_GOCI6km_temp.shape[1]!=14:
                            stn_GOCI6km_temp = np.hstack([stn_GOCI6km_temp, np.zeros([stn_GOCI6km_temp.shape[0], 1])])
                        for k in range(stn_GOCI6km_temp.shape[0]):
                            stn_GOCI6km_temp[k,13] = dup_dist[dup_dist[:,0]==stn_GOCI6km_temp[k,12],1]
                            nanidx = ~np.isnan(stn_GOCI6km_temp[k,5:11])
                            weight = np.divide(nanidx, stn_GOCI6km_temp[k, 13])
                            stn_GOCI6km_temp[k,5:11] = np.multiply(stn_GOCI6km_temp[k, 5:11], weight)
                            if weight_sum is None:
                                weight_sum = weight
                            else:
                                weight_sum = np.vstack([weight_sum, weight])
                        min_dist = np.min(stn_GOCI6km_temp[:,13])
                        
                        stn_GOCI6km_temp2 = stn_GOCI6km_temp[stn_GOCI6km_temp[:,13]==min_dist,:]
                        if stn_GOCI6km_temp2.shape[0]!=1:
                            stn_GOCI6km_temp2 = stn_GOCI6km_temp2[0,:].reshape(1,-1)
                        
                        weight_sum = np.sum(weight_sum, axis=0)
                        stn_GOCI6km_temp2[:,5:11]=np.divide(np.nansum(stn_GOCI6km_temp[:,5:11],axis=0), weight_sum)
                        stn_GOCI6km = np.vstack([stn_GOCI6km, stn_GOCI6km_temp2[:,:-1]])
                stn_GOCI6km = stn_GOCI6km[stn_GOCI6km[:, 12].argsort()] # sort by scode2
                if stn_GOCI6km_yr is None:
                    stn_GOCI6km_yr = stn_GOCI6km
                else:
                    stn_GOCI6km_yr = np.vstack([stn_GOCI6km_yr, stn_GOCI6km])
        print (doy)
    matlab.savemat(os.path.join(path_stn_kr, f'Station_GOCI6km_{yr}_weight.mat'), {'stn_GOCI6km_yr':stn_GOCI6km_yr})
    tElapsed = time.time() - tStart
    print (f'time taken : {tElapsed}')
