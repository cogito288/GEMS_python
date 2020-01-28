### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import glob
import pandas as pd
import random

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')

path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_kr = os.path.join(path_station, 'Station_KR')

path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km')
path_rtt = os.path.join(data_base_dir, 'Preprocessed_raw', 'RTT') # path_save 

## Station index
mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_korea.mat'))
lat_kor, lon_kor = mat['lat_kor'], mat['lon_kor']
del mat

mat = matlab.loadmat(os.path.join(path_stn_kr, 'stn_1km_location_weight_v201904.mat'))
dup_scode2_1km = mat['dup_scode2_1km']
df = pd.DataFrame(mat['stn_1km_location'], columns=mat['header_stn_1km_location'][0])
stn_1km_location = df.values
del df, mat

## Read data
target = ['PM10','PM25']

i=1 #1:2 # target  ########################################
header = ['NDVI','AOD','AE','FMF','SSA','RSDN','Precip','DEM','LC_ratio', # satellite data(9)
    'Temp','Dew','RH','P_srf','MaxWS','PBLH','Visibility', # numerical data(RDAPS)(16)
    'stack1_np.maxWS','stack3_np.maxWS','stack5_np.maxWS','stack7_np.maxWS', # stacked np.maxWS(20)
    'DOY','PopDens','RoadDens'] #, etc data(23)

nvar = 23
if i==1: header2 = header+['PM10','stn_num','doy_num','time','yr','ovr','k_ind']
else: header2 = header+['PM25','stn_num','doy_num','time','yr','ovr','k_ind']

data_stn = []
high = []
low = []
YEARS = [2016]
for yr in YEARS:
    if yr%4==0: days = 366
    else: days = 365
    
    #fname = 'Station_1km_2016_weight.mat'
    fname = f'Station_1km_rm_outlier_{yr}_weight.mat'
    mat = matlab.loadmat(os.path.join(path_stn_kr, fname))
    stn = mat['stn_1km_yr']
    del mat
    
    for doy in range(1, days+1):
        if doy <=30:
        #if doy <=30 and yr == 2015:
            for utc in range(7+1):
                fname = f'cases_RTT_{yr}_{doy:03d}_{utc:02d}.mat'
                
                mat = matlab.loadmat(os.path.join(path_rtt, 'cases/RTT_mat', fname)) # data
                data = mat['data']
                del mat
                tmp_axis = list(range(21))+[22,23]
                data = data[:,tmp_axis]
                data[data[:,-1]==65535,-1] = -9999                
                
                # Load station data
                stn_1km = stn[(stn[:,0]==doy) & (stn[:,1]==yr) & (stn[:,4]==utc+9) ,:]           
                
                stn_idx = np.isin(stn_1km_location[:,1], stn_1km[:,12])
                stn_conc = stn_1km[:,[9,12,0,3,1]] # PM10, stn_num, doy_num,time,yr
                stn_conc = np.hstack([stn_conc, np.zeros((stn_conc.shape[0], 2))])
                #stn_conc[:,5]=0# PM10, stn_num, doy_num,time,yr, ovr
                stn_conc[:,6] =stn_1km_location[stn_idx,4]# PM10, stn_num, doy_num,time,yr, ovr, stn_location
                
                data_1 = stn_conc[stn_conc[:,0]<=30,:]            # (x1)
                data_2 = stn_conc[(stn_conc[:,0]>30) & (stn_conc[:,0]<=60),:]  # (x0.5)
                data_3 = stn_conc[(stn_conc[:,0]>60) & (stn_conc[:,0]<=90),:]  # (x1)
                data_4 = stn_conc[(stn_conc[:,0]>90) & (stn_conc[:,0]<=120),:] # (x3)
                data_5 = stn_conc[(stn_conc[:,0]>120) & (stn_conc[:,0]<=150),:] # (x9)
                data_6 = stn_conc[(stn_conc[:,0]>150) & (stn_conc[:,0]<=180),:] # (x30)
                data_7 = stn_conc[(stn_conc[:,0]>180),:]            # (x37)
                
                data_2 = data_2[~np.isnan(data_2).any(axis=1)]
                mask = np.random.choice(data_2.shape[0], np.round(data_2.shape[0]*0.5).astype(int), replace=False)
                data_2 = data_2[mask, :]
                sampled_data = np.concatenate((data_1,data_2,data_3,data_4,data_5,data_6,data_7), axis=0)

                ndata_4 = matlab.oversampling_sh(data_4[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],1,
                                                patch_path=os.path.join(path_grid_raw, 'ovr_patch_order.mat'))
                ndata_5 = matlab.oversampling_sh(data_5[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],7,
                                                 patch_path=os.path.join(path_grid_raw, 'ovr_patch_order.mat'))
                ndata_6 = matlab.oversampling_sh(data_6[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],28,
                                                 patch_path=os.path.join(path_grid_raw, 'ovr_patch_order.mat'))
                ndata_7 = matlab.oversampling_sh(data_7[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],35,
                                                 patch_path=os.path.join(path_grid_raw, 'ovr_patch_order.mat'))
                
                ndata = np.concatenate((sampled_data,ndata_4,ndata_5,ndata_6,ndata_7), axis=0) 
                del sampled_data, data_1, data_2, data_3, data_4, data_5, data_6, data_7, ndata_4, ndata_5, ndata_6, ndata_7  
                
                # remove station pixel among oversampled pixels
                # ndata = [stn_conc, stn_num, doy_num, stn_ind, stn_x, stn_y, over]
                dup_idx = np.isin(ndata[:,6],stn_1km_location[:,4])
                dup_idx = np.multiply(dup_idx, ndata[:,5]) #oversampling col
                ndata = ndata[dup_idx==0,:]
                
                # Extract input variables at station points & oversampling points
                data_tmp = data[ndata[:,6],:]
                
                data_tmp[:,nvar:nvar+6] = ndata[:,:6] # data. stn_PM, stn_num, doy_num, time, yr, ovr
                k=((doy-1)*8)+(utc+1)
                data_tmp[:,nvar+6] = k #k_idx
                data_tmp[data_tmp==-9999] = np.nan
                data_tmp = data_tmp[~np.isnan(data_tmp).any(axis=1)]
                data_stn = np.concatenate((data_stn, data_tmp), axis=0)
                print (utc)
            
            print (doy)
            if doy >= 30 & utc == 7:
                fname = f'{target[i]}_RTT_{yr}_{doy:03d}_{utc:02d}.csv'
                tmp_df = pd.DataFrame(data_stn, columns=header2)
                tmp_df.to_csv(os.path.join(path_rtt, 'dataset', target[i], 'new', fname), float_format='%7.7f')
                print (doy)
            
        else:
            for utc in range(7+1):
                k=240               
                
                # 고농도 남기기
                extra_samples = data_stn[data_stn[:,-1]==1,:]
                if i==1:
                    high_tmp = extra_samples[extra_samples[:,23]>=150,:]
                    low_tmp = extra_samples[extra_samples[:,23]<=60,:]
                else:
                    high_tmp = extra_samples[extra_samples[:,23]>=80,:]
                    low_tmp = extra_samples[extra_samples[:,23]<=30,:]
                      
                
                if len(high_tmp)==0: # empty
                    None
                else:
                    high = np.concatenate((high, high_tmp), axis=0)
                    high[:,-1] = high[:,-1]+1
                    high_uniq = np.unique(high[:,:29], axis=1)
                    high_uniq = np.hstack([high_uniq, np.ones(high_uniq.shape[0])*2])
                    high = high_uniq
                           
                if len(low_tmp)==0: # empty
                    None
                else:
                    low = np.concatenate((low, low_tmp), axis=0)
                    low[:,-1] = low[:,-1]+1                    
                    low_uniq = np.unique(low[:,:29], axis=1)
                    low_uniq = np.hstack([low_uniq, np.ones(low_uniq.shape[0])*2])
                    low = low_uniq
                
                data_stn = data_stn[data_stn[:,-1]>=2,:]
                high_tmp[:,-1] = high_tmp[:,-1]+1
                low_tmp[:,-1] = low_tmp[:,-1]+1
                data_stn = np.concatenate((low_tmp, high_tmp, data_stn), axis=0)
                data_stn[:,-1] = data_stn[:,-1]-1
                           
                fname = f'cases_RTT_{yr}_{doy:03d}_{utc:02d}.mat'
                matlab.loadmat(os.path.join(path_rtt, 'cases/RTT_mat', fname)) # data
                tmp_axis = list(range(21))+[22,23]
                data = data[:,tmp_axis]
                data[data[:,-1]==65535,-1] = -9999
                
                # Load station data
                stn_1km = stn[(stn[:,0]==doy) & (stn[:,1]==yr) & (stn[:,4]==utc+9) ,:]           
                
                stn_idx = np.isin(stn_1km_location[:,1], stn_1km[:,12])
                stn_conc = stn_1km[:,[9,12,0,4,1]] # PM10, stn_num, doy_num,time,yr
                stn_conc = np.hstack([stn_conc, np.zeros((stn_conc.shape[0], 2))])
                #stn_conc[:,5] = 0 # PM10, stn_num, doy_num,time,yr, ovr
                stn_conc[:,6] = stn_1km_location[stn_idx,4]# PM10, stn_num, doy_num,time,yr, ovr, stn_location
                
                data_1 = stn_conc[stn_conc[:,0]<=30,:]            # (x1)
                data_2 = stn_conc[(stn_conc[:,0]>30) & (stn_conc[:,0]<=60),:]  # (x0.5)
                data_3 = stn_conc[(stn_conc[:,0]>60) & (stn_conc[:,0]<=90),:]  # (x1)
                data_4 = stn_conc[(stn_conc[:,0]>90) & (stn_conc[:,0]<=120),:] # (x3)
                data_5 = stn_conc[(stn_conc[:,0]>120) & (stn_conc[:,0]<=150),:] # (x9)
                data_6 = stn_conc[(stn_conc[:,0]>150) & (stn_conc[:,0]<=180),:] # (x30)
                data_7 = stn_conc[(stn_conc[:,0]>180),:]            # (x37)
                
                data_2 = data_2[~np.isnan(data_2).any(axis=1)]
                if data_2.shape[0]>1:
                    mask = np.random.choice(data_2.shape[0], np.round(data_2.shape[0]*0.5).astype(int), replace=False)
                    data_2 = data2[mask, :]
                sampled_data = np.concatenate((data_1,data_2,data_3,data_4,data_5,data_6,data_7), axis=0)
                
                ndata_4 = matlab.oversampling_sh(data_4[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],1,
                                                 patch_path=os.path.join(path_grid_raw, 'ovr_patch_order.mat'))
                ndata_5 = matlab.oversampling_sh(data_5[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],7,
                                                 patch_path=os.path.join(path_grid_raw, 'ovr_patch_order.mat'))
                ndata_6 = matlab.oversampling_sh(data_6[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],28,
                                                 patch_path=os.path.join(path_grid_raw, 'ovr_patch_order.mat'))
                ndata_7 = matlab.oversampling_sh(data_7[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],35,
                                                 patch_path=os.path.join(path_grid_raw, 'ovr_patch_order.mat'))
                
                ndata = np.concatenate((sampled_data,ndata_4,ndata_5,ndata_6,ndata_7), axis=0)  
                del sampled_data, data_1, data_2, data_3, data_4, data_5, data_6, data_7, ndata_4, ndata_5, ndata_6, ndata_7  
                
                # remove station pixel among oversampled pixels
                # ndata = [stn_conc, stn_num, doy_num, stn_ind, stn_x, stn_y, over]
                dup_idx = np.isin(ndata[:,6],stn_1km_location[:,4])
                dup_idx = np.multiply(dup_idx, ndata[:,5]) #oversampling col
                ndata = ndata[dup_idx==0,:]
                
                # Extract input variables at station points & oversampling points
                data_tmp = data[ndata[:,6],:]
                
                data_tmp[:,nvar:nvar+6] = ndata[:,:6] # data. stn_PM, stn_num, doy_num, time, yr, ovr
                data_tmp[:,nvar+6] = k #k_idx
                
                data_tmp[data_tmp==-9999] = np.nan
                data_tmp = data_tmp[~np.isnan(data_tmp).any(axis=1)]
                idx = data_tmp[:, 23]>400
                data_tmp = data_tmp[~idx]
                           
                data_stn = np.concatenate((data_stn, data_tmp), axis=0)
                
                high_rate_pre = data_stn[data_stn[:,23]>=150,:].shape[0]/data_stn[:,23].shape[0]*100
                low_rate_pre = data_stn[data_stn[:,23]<=60,:].shape[0]/data_stn[:,23].shape[0]*100
                
                if high_rate_pre<30 and low_rate_pre<30 and (data_stn[:,-1]>1).shape[0]>4000:
                    print (f'num of samples = {data_stn.shape[0]:4.0f} \n remove the oversampled samples in the new dataset \n')
                    idx = data_stn[:,-2]==1 & data_stn[:,-1]==240 & data_stn[:,23]<150
                    data_stn = data_stn[~idx,:]
                    
                high_rate_pre = data_stn[data_stn[:,23]>=150,:].shape[0]/data_stn[:,23].shape[0]*100
                low_rate_pre = data_stn[data_stn[:,23]<=60,:].shape[0]/data_stn[:,23].shape[0]*100
            # 샘플 조정 part1
                if high_rate_pre>30:
                    print (f'high_rate_pre = {high_rate_pre:3.2f} & remove the oversampled samples in the new dataset \n')
                    idx = data_stn[:,-1]==240 & data_stn[:,-2]==1
                    data_stn = data_stn[~idx,:]
                    
                if low_rate_pre>30:              
                    print (f'low_rate_pre = {low_rate_pre:3.2f} & remove stacked samples \n')
                    idx = data_stn[:,23]<=60 & data_stn[:,-1]==2
                    data_stn = data_stn[~idx,:]

                high_rate_pre = data_stn[data_stn[:,23]>=150,:].shape[0]/data_stn[:,23].shape[0]*100
                low_rate_pre = data_stn[data_stn[:,23]<=60,:].shape[0]/data_stn[:,23].shape[0]*100                
            # 샘플 조정
                if high_rate<30 and low_rate>30:
                    print (f'high_rate_pre = {high_rate_pre:3.2f}  & stack more \n')
                    print (f'low_rate_pre = {low_rate_pre:3.2f} & remove stacked samples \n')
                    # 저농도 지우기
                    if len(low)!=0:
                        idx_low = np.where(data_stn[:,25] <= low[-1,25] & data_stn[:,23]<=60 & data_stn[:,-1]==1)
                        data_stn = data_stn[~idx_low,:]
                        
                elif high_rate<30 and low_rate<30:
                    print (f'high_rate_pre = {high_rate_pre:3.2f} & stack more \n')
                    print (f'low_rate_pre = {low_rate_pre:3.2f} & stack more \n')
                    
                elif high_rate>30 and low_rate<30:
                    print (f'high_rate_pre = {high_rate_pre:3.2f} & remove the stacked samples \n')
                    print (f'low_rate_pre = {low_rate_pre:3.2f} & stack more \n')
                    # 고농도 지우기
                    if len(high)!=0:
                        idx_high = np.where(data_stn[:,25] <= high[-1,25] & data_stn[:,23]>=150 & data_stn[:,-1]==1)[0]
                        data_stn = data_stn[~idx_high,:]       
                   
                elif high_rate>30 and low_rate>30:
                    print (f'high_rate = {high_rate:3.2f} \n')
                    print (f'low_rate = {low_rate:3.2f} \n')
                    # 고농도 지우기
                    idx_high = np.where(data_stn[:,25] <= high[-1,25] & data_stn[:,23]>=150 & data_stn[:,-1]==1)[0]
                    ddata_stn = data_stn[~idx_high,:]                   
                    # 저농도 지우기
                    idx_low = np.where(data_stn[:,25] <= low[-1,25] & data_stn[:,23]<=60 & data_stn[:,-1]==1)
                    data_stn = data_stn[~idx_low,:]
                #                     print (('data_stn 파일 갯수 줄이기.\n')
                # sample수 줄이는 코드 추가필요 전체적인 갯수줄이기
                # data_stn[:,-1]==1 인 날에대해서 줄이기         
                print (utc)                
                fname = f'{target[i]}_RTT_{yr}_{doy:03}_{utc:02d}.csv'
                tmp_df = pd.DataFrame(data_stn, columns=header2)
                matlab.savemat(os.path.join(path_rtt,'dataset/',target[i],'/new/',fname), float_format='%7.7f')    
            print (doy)    
    print (yr)