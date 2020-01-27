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
import random

### Setting path
### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_stn_kr = os.path.join(path_station, 'Station_Korea')


write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_AOD')

## Station index
mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_korea.mat'))
lat_kor, lon_kor = mat['lat_kor'], mat['lon_kor']
del mat

matlab.loadmat(os.path.join(path_stn_kr, 'stn_1km_location_weight.mat'))

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
    
    fname = f'Station_1km_rm_outlier_{yr}_weight.mat'
    mat = matlab.loadmat(os.path.join(path_stn_kr, fname))
    stn = mat['stn_1km_yr']
    del mat
    
    for doy in range(1, days+1):
        if doy <=30 && yr == 2015:
            for utc in range(7+1):
                fname = f'cases_RTT_{yr}_{doy:03d}_{utc:02d}.mat'
                mat = matlab.loadmat(os.path.join(path_nas4, 'cases/RTT_mat', fname)) # data
                data = mat['data']
                del mat
                data = data[:,[:21,22:24]]
                data[[data[:,-1]==65535],] = -9999
                
                
                # Load station data
                stn_1km = stn[stn[:,0] == doy & stn[:,1] ==yr & stn[:,4]== utc+9 ,:]
                
                stn_idx = matlab.ismember(stn_1km_location[:,1], stn_1km[:,12])
                stn_conc = stn_1km[:,[9,12,0,3,1]] # PM10, stn_num, doy_num,time,yr
                stn_conc[:,5]=0# PM10, stn_num, doy_num,time,yr, ovr
                stn_conc[:,6] =stn_1km_location[stn_idx,4]# PM10, stn_num, doy_num,time,yr, ovr, stn_location
                
                data_1 = stn_conc[stn_conc[:,0]<=30,:]            # (x1)
                data_2 = stn_conc[stn_conc[:,0]>30 & stn_conc[:,0]<=60,:]  # (x0.5)
                data_3 = stn_conc[stn_conc[:,0]>60 & stn_conc[:,0]<=90,:]  # (x1)
                data_4 = stn_conc[stn_conc[:,0]>90 & stn_conc[:,0]<=120,:] # (x3)
                data_5 = stn_conc[stn_conc[:,0]>120 & stn_conc[:,0]<=150,:] # (x9)
                data_6 = stn_conc[stn_conc[:,0]>150 & stn_conc[:,0]<=180,:] # (x30)
                data_7 = stn_conc[stn_conc[:,0]>180,:]            # (x37)
                
                data_2 = rmmissing[data_2,0]
                data_2 = random.sample(data_2, np.round(data_2.shape[0]*0.5))
                #data_2 = datasample(data_2, np.round(data_2.shape[0]*0.5),'Replace',false)
                sampled_data = np.concatenate((data_1,data_2,data_3,data_4,data_5,data_6,data_7), axis=0)
                
                ndata_4 = oversampling_sh[data_4[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],1]
                ndata_5 = oversampling_sh[data_5[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],7]
                ndata_6 = oversampling_sh[data_6[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],28]
                ndata_7 = oversampling_sh[data_7[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],35]
                
                ndata = np.concatenate((sampled_data,ndata_4,ndata_5,ndata_6,ndata_7), axis=0) 
                del sampled_data, data_1, data_2, data_3, data_4, data_5, data_6, data_7, ndata_4, ndata_5, ndata_6, ndata_7  
                
                # remove station pixel among oversampled pixels
                # ndata = [stn_conc, stn_num, doy_num, stn_ind, stn_x, stn_y, over]
                dup_idx = matlab.ismember(ndata[:,7],stn_1km_location[:,5])
                dup_idx = np.multiple(dup_idx, ndata[:,6]) #oversampling col
                ndata = ndata[dup_idx==0,:]
                
                # Extract input variables at station points & oversampling points
                data_tmp = data[ndata[:,7],:]
                #  data_tmp = cases(ndata[:,6],[1:2,4:])
                
                data_tmp[:,nvar:nvar+5] = ndata[:,:6] # data. stn_PM, stn_num, doy_num, time, yr, ovr
                k=((doy-1]*8)+(utc+1)
                data_tmp[:,nvar+6] = k #k_idx
                
                data_tmp[data_tmp==-9999] = np.nan
                data_tmp = rmmissing[data_tmp,0]
                
                data_stn = np.concatenate((data_stn, data_tmp), axis=0)
                print (utc)
            
            print (doy)
            if doy >= 30 & utc == 7:
                fname = f'{target[i]_RTT_{yr}_{doy:03d}_{utc:02d}.csv'
                tmp_df = pd.DataFrame(data_stn, columns=header2)
                tmp_df.to_csv(os.path.join(path_nas4, 'dataset', target[i], 'new', fname), float_format='%7.7f')
                #csvwrite_with_headers2([path_nas4,'dataset/',target{i},'/new/'],data_stn,header2,0,0,'#7.7f')
                print (doy)
            
        else:
            for utc in range(7+1):
                k=240               
                
                # 고농도 남기기
                extra_samples = data_stn[data_stn[:,-1]==1,:]
                if i==1:
                    high_tmp = extra_samples[extra_samples[:,23]>=150,:]
                    low_tmp = extra_samples[extra_samples[:,23]<=60,:]
                else
                    high_tmp = extra_samples[extra_samples[:,23]>=80,:]
                    low_tmp = extra_samples[extra_samples[:,23]<=30,:]
                      
                
                if not np.all(high_tmp==0): # not empty
                    high = high
                else:
                    high = [high high_tmp]  high[:,-1] = high[:,-1]+1
                    high_uniq = np.unique(high[:,:29], axis=1)
                    high_uniq[:,-1]=2
                    high = high_uniq

                if not np.all(low_tmp==0): # not empty
                    low = low
                else:
                    low = np.concatenate((low, low_tmp), axis=0)
                    low[:,-1] = low[:,-1]+1
                    low_uniq = np.unique(low[:,:29])
                    low_uniq[:,-1]=2
                    low = low_uniq
                
                
                #                 matlab.savemat(os.path.join(path_nas4, 'dataset/',target{i},'/variable_test/extra_samples/',target{i},'_high_',
                #                     str(yr),'_',str(doy, '#03i'),'_',str(utc, '#02i'),'.mat'],'high')
                #                 matlab.savemat(os.path.join(path_nas4, 'dataset/',target{i},'/variable_test/extra_samples/',target{i},'_low_',
                #                     str(yr),'_',str(doy, '#03i'),'_',str(utc, '#02i'),'.mat'],'low')                
                
                data_stn = data_stn[data_stn[:,-1]>=2,:]
                high_tmp[:,-1] = high_tmp[:,-1]+1
                low_tmp[:,-1] = low_tmp[:,-1]+1
                data_stn = np.concatenate((low_tmp,high_tmp,data_stn), axis=0)
                data_stn[:,-1] = data_stn[:,-1]-1
                
                fname = f'cases_RTT_{yr}_{doy:03d}_{utc:02d}.mat'
                matlab.loadmat(os.path.join(path_nas4, 'cases/RTT_mat', fname)) # data
                data = data[:,[:21,22:24]]
                data[[data[:,-1]==65535],-1] = -9999
                
                # Load station data
                stn_1km = stn[stn[:,0] == doy & stn[:,0] ==yr & stn[:,4]== utc+9, :]
                
                stn_idx = matlab.ismember(stn_1km_location[:,1], stn_1km[:,12])
                stn_conc = stn_1km[:,[9,12,0,4,1]] # PM10, stn_num, doy_num,time,yr
                stn_conc[:,5] = 0 # PM10, stn_num, doy_num,time,yr, ovr
                stn_conc[:,6] =stn_1km_location[stn_idx,4]# PM10, stn_num, doy_num,time,yr, ovr, stn_location
                
                data_1 = stn_conc[stn_conc[:,0]<=30,:]            # (x1)
                data_2 = stn_conc[stn_conc[:,0]>30 & stn_conc[:,0]<=60,:]  # (x0.5)
                data_3 = stn_conc[stn_conc[:,0]>60 & stn_conc[:,0]<=90,:]  # (x1)
                data_4 = stn_conc[stn_conc[:,0]>90 & stn_conc[:,0]<=120,:] # (x3)
                data_5 = stn_conc[stn_conc[:,0]>120 & stn_conc[:,0]<=150,:] # (x9)
                data_6 = stn_conc[stn_conc[:,0]>150 & stn_conc[:,0]<=180,:] # (x30)
                data_7 = stn_conc[stn_conc[:,0]>180,:]            # (x37)
                
                data_2 = rmmissing[data_2,0]
                if data_2.shape[0]>1:
                    data_2 = random.sample(data_2, np.round(size(data_2,1]*0.5))
                                    
                sampled_data = np.concatenate((data_1,data_2,data_3,data_4,data_5,data_6,data_7), axis=0)
                
                ndata_4 = oversampling_sh(data_4[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],1]
                ndata_5 = oversampling_sh(data_5[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],7]
                ndata_6 = oversampling_sh(data_6[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],28]
                ndata_7 = oversampling_sh(data_7[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],35]
                
                ndata = np.concatenate((sampled_data,ndata_4,ndata_5,ndata_6,ndata_7), axis=0)  
                del sampled_data, data_1, data_2, data_3, data_4, data_5, data_6, data_7, ndata_4, ndata_5, ndata_6, ndata_7  
                
                # remove station pixel among oversampled pixels
                # ndata = [stn_conc, stn_num, doy_num, stn_ind, stn_x, stn_y, over]
                dup_idx = matlab.ismember(ndata[:,6],stn_1km_location[:,4])
                dup_idx = np.multiply(dup_idx, ndata[:,5]) #oversampling col
                ndata = ndata[dup_idx==0,:]
                
                # Extract input variables at station points & oversampling points
                data_tmp = data[ndata[:,6],:]
                
                data_tmp[:,nvar:nvar+5] = ndata[:,:6] # data. stn_PM, stn_num, doy_num, time, yr, ovr
                data_tmp[:,nvar+6] = k #k_idx
                
                data_tmp[data_tmp==-9999] = np.nan
                data_tmp = rmmissing[data_tmp,1]
                data_tmp[data_tmp[:,23]>400,:] =[]
                
                data_stn = np.concatenate((data_stn, data_tmp), axis=0)
                
                high_rate_pre = data_stn[data_stn[:,23]>=150,:].shape[0]/data_stn[:,23].shape[0]*100
                low_rate_pre = data_stn[data_stn[:,23]<=60,:].shape[0]/data_stn[:,23].shape[0]*100
                
                if high_rate_pre<30 and low_rate_pre<30 and data_stn[[:,-1]>1].shape[0]>4000:
                    print ('num of samples = {data_stn.shape[0]:4.0f} \n remove the oversampled samples in the new dataset \n')
                    data_stn[data_stn[:,-1]==1 & data_stn[:,-1]==240 & data_stn[:,23]<150,:] = []
                
                high_rate_pre = data_stn[data_stn[:,23]>=150,:].shape[0]/data_stn[:,23].shape[0]*100
                low_rate_pre = data_stn[data_stn[:,23]<=60,:].shape[0]/data_stn[:,23].shape[0]*100
            # 샘플 조정 part1
                if high_rate_pre>30:
                    print (f'high_rate_pre = {high_rate_pre:3.2f} & remove the oversampled samples in the new dataset \n')
                    data_stn[data_stn[:,-1]==240 & data_stn[:,-1]==1,:]=[]
                if low_rate_pre>30:              
                    print (f'low_rate_pre = {low_rate_pre:3.2f} & remove stacked samples \n')
                    data_stn[data_stn[:,23]<=60 & data_stn[:,-1]==2,:] = []

                high_rate_pre = data_stn[data_stn[:,23]>=150,:].shape[0]/data_stn[:,23].shape[0]*100
                low_rate_pre = data_stn[data_stn[:,23]<=60,:].shape[0]/data_stn[:,23].shape[0]*100                
            # 샘플 조정
                if high_rate<30 and low_rate>30:
                    print (f'high_rate_pre = {high_rate_pre:3.2f}  & stack more \n')
                    print (f'low_rate_pre = {low_rate_pre:3.2f} & remove stacked samples \n')
                # 저농도 지우기
                   if np.all(low==0):
                       idx_low = np.where(data_stn[:,25] <= low[-1,25] & data_stn[:,23]<=60 & data_stn[:,-1]==1)
                       data_stn[idx_low,:] = []
                elif high_rate<30 and low_rate<30:
                    print (f'high_rate_pre = {high_rate_pre:3.2f} & stack more \n')
                    print (f'low_rate_pre = {low_rate_pre:3.2f} & stack more \n')
                elif high_rate>30 and low_rate<30:
                    print (f'high_rate_pre = {high_rate_pre:3.2f} & remove the stacked samples \n')
                    print (f'low_rate_pre = {low_rate_pre:3.2f} & stack more \n')
               # 고농도 지우기
                   if np.all(high==0):
                    idx_high = np.where(data_stn[:,25] <= high[-1,25] & data_stn[:,23]>=150 & data_stn[:,-1]==1)[0]
                    data_stn[idx_high,:] = []             
                   
                elif high_rate>30 and low_rate>30:
                    print (f'high_rate = {high_rate:3.2f \n')
                    print (f'low_rate = {low_rate:3.2f} \n')
                # 고농도 지우기
                    idx_high = np.where(data_stn[:,25] <= high[-1,25] & data_stn[:,23]>=150 & data_stn[:,-1]==1)[0]
                    data_stn[idx_high,:] = []                    
                # 저농도 지우기
                    idx_low = np.where(data_stn[:,25] <= low[-1,25] & data_stn[:,23]<=60 & data_stn[:,-1]==1)
                    data_stn[idx_low,:] = []
                #                     print (('data_stn 파일 갯수 줄이기.\n')
                # sample수 줄이는 코드 추가필요 전체적인 갯수줄이기
                # data_stn[:,-1]==1 인 날에대해서 줄이기         
                print (utc)                
                fname = f'{target[i]}_RTT_{yr}_{doy:03}_{utc:02d}.csv'
                tmp_df = pd.DataFrame(data_stn, columns=header2)
                tmp_df(os.path.joinpath_nas4,'dataset/',target[i],'/new/',fname), float_format='%7.7f')    
            print (doy)    
    print (yr)
