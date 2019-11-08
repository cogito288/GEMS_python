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
# path_data = '//10.72.26.56/irisnas5/Data/'
# path_save = '//10.72.26.56/irisnas5/GEMS/PM/00_EA6km/RTT/'
# addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'))
path_data = '/share/irisnas5/Data/'
path_save = '/share/irisnas5/GEMS/PM/00_EA6km/RTT/'
addpath(genpath('/share/irisnas5/Data/matlab_func/'))
# path_data = '/Volumes/irisnas5/Data/'
# path_save = '/Volumes/irisnas5/GEMS/PM/00_EA6km/RTT/'
# addpath(genpath('/Volumes/irisnas5/Data/matlab_func/'))

## Station index
matlab.loadmat(os.path.join(path_data,'grid/grid_goci.mat'))
matlab.loadmat(os.path.join(path_data,'Station/Station_CN/cn_stn_GOCI6km_location_weight.mat'))
matlab.loadmat(os.path.join(path_data,'Station/Station_Korea/stn_GOCI6km_location_weight_v2018.mat'))
matlab.loadmat(os.path.join(path_data,'Station/Station_JP/jp_stn_GOCI6km_location_weight.mat'))
stn_6km_location = np.concatenate((stn_GOCI6km_location, jp_stn_GOCI6km_location, cn_stn_GOCI6km_location), axis=0)
cn_dup_scode2_GOCI6km[:,end+1:jp_dup_scode2_GOCI6km.shape[1]]=0
dup_scode2_GOCI6km[:,end+1:jp_dup_scode2_GOCI6km.shape[1]]=0
dup_scode2_6km =np.concatenate((dup_scode2_GOCI6km, cn_dup_scode2_GOCI6km, jp_dup_scode2_GOCI6km), axis=0)

clear stn_GOCI6km_location cn_stn_GOCI6km_location jp_stn_GOCI6km_location cn_dup_scode2_GOCI6km dup_scode2_GOCI6km jp_dup_scode2_GOCI6km header_cn_stn_GOCI6km_location header_jp_stn_GOCI6km_location

## Read data
header = ['AOD','AE','FMF','SSA','NDVI','RSDN','Precip','DEM','LCurban', # satellite data(9)
    'Temp','Dew','RH','P_srf','MaxWS','PBLH','Visibility', # numerical data(RDAPS)(16)
    'stack1_np.maxWS','stack3_np.maxWS','stack5_np.maxWS','stack7_np.maxWS', # stacked np.maxWS(20)
    'DOY','PopDens','RoadDens'] #, etc data(23)

header2 = header+['PM25','stn_num','doy_num','time','yr','ovr','k_ind']
nvar = 23


data_stn=[]
high=[]
low=[]
YEARS = [2015,2016,2017]
for yr in YEARS:
    if yr%4==0: days = 366
    else: days = 365

    fname = f'Station_GOCI6km_{yr}_weight.mat'
    matlab.loadmat(os.path.join(path_data,'Station/Station_Korea', fname))
    fname = f'cn_Station_GOCI6km_rm_outlier_{yr}_weight.mat'
    matlab.loadmat(os.path.join(path_data,'Station/Station_CN', fname))
    if yr < 2017:
        fname = f'jp_Station_GOCI6km_{yr}_weight.mat'
        matlab.loadmat(os.path.join(path_data,'Station/Station_JP', fname))
    else:
        fname = f'jp_Station_GOCI6km_rm_outlier_{yr}_weight.mat'
        matlab.loadmat(os.path.join(path_data,'Station/Station_JP', fname))

    jp_stn_GOCI6km_yr = jp_stn_GOCI6km_yr[jp_stn_GOCI6km_yr[:,4]>=9 & jp_stn_GOCI6km_yr[:,4]<=16,0:13]
    stn_GOCI6km_yr = stn_GOCI6km_yr[stn_GOCI6km_yr[:,4]>=9 & stn_GOCI6km_yr[:,4]<=16,:]
    stn_GOCI6km_yr[:,4]=stn_GOCI6km_yr[:,4]-9
    jp_stn_GOCI6km_yr[:,4]=jp_stn_GOCI6km_yr[:,4]-9
    cn_stn_GOCI6km_yr[:,4]=cn_stn_GOCI6km_yr[:,4]-8
    stn = np.concatenate((stn_GOCI6km_yr, jp_stn_GOCI6km_yr, cn_stn_GOCI6km_yr[:,[:5,10,18,14,12,8,6,20:22]), axis=0)
    
    del stn_GOCI6km_yr, jp_stn_GOCI6km_yr, cn_stn_GOCI6km_yr

    for doy in range(21,days+1):
        if not np.all(data_stn==0): # Not empty
            None # Do nothing
        elif data_stn[data_stn[:,28]==1,:].shape[0]>1:
            rmovr = random.sample(data_stn[data_stn[:,-1]==1,:], np.round(data_stn[data_stn[:,-1]==1,:].shape[0]*0.9))
            data_stn[data_stn[:,-1]==1,:]=[]
            data_stn=np.concatenate((data_stn, rmovr), axis=0)
        else
            data_stn[data_stn[:,-1]==1,:]=[]

        if doy <=30 && yr == 2015:
            for utc in range(7):
                if not np.all(data_stn==0): # Not etmpty
                    None # Do nothing
                elif data_stn[data_stn[:,28]==1,:].shape[0]>1:
                    rmovr = random.sample(data_stn[data_stn[:,-1]==1,:], np.round(data_stn[data_stn[:,-1]==1,:].shape[0]*0.99))
                    data_stn[data_stn[:,-1]==1,:]=[]
                    data_stn=np.concatenate((data_stn, rmovr), axis=0)
                else                    
                    data_stn[data_stn[:,-1]==1,:]=[]

                fname = f'cases_EA6km_{yr}_{doy:03d}_{utc:02d}.mat'
                mat = matlab.loadmat(os.path.join(path_data, 'EA_GOCI6km/cases_mat/',str(yr), fname)) # data_tbl
                data_tbl = mat['data_tbl']
                data = data_tbl[:,header]
                data = data.values
                del data_tbl

                # Load station data
                stn_6km = stn[stn[:,0] == doy & stn[:,1] ==yr & stn[:,4]== utc,:]
                
                if np.all(stn_6km==0): # no observation data in some utc
                    stn_idx = matlab.ismember(stn_6km_location[:,1], stn_6km[:,12])
                    stn_conc = stn_6km[:,[9,12,0,4,1]] # PM10, stn_num, doy_num,time,yr
                    stn_conc[:,5]=0# PM10, stn_num, doy_num,time,yr, ovr
                    stn_conc[:,6] =stn_6km_location[stn_idx,4]# PM10, stn_num, doy_num,time,yr, ovr, stn_location
                    data_1 = stn_conc[stn_conc[:,0]<=20,:]            # (x0.1)
                    data_2 = stn_conc[stn_conc[:,0]>20 & stn_conc[:,0]<=40,:] # (x0.3)
                    data_3 = stn_conc[stn_conc[:,0]>40 & stn_conc[:,0]<=60,:] # (x0.5)
                    data_4 = stn_conc[stn_conc[:,0]>120 & stn_conc[:,0]<=120,:]  # (x3)
                    data_5 = stn_conc[stn_conc[:,0]>240 & stn_conc[:,0]<=240,:]  # (x13)
                    data_6 = stn_conc[stn_conc[:,0]>360 & stn_conc[:,0]<=360,:]  # (x30)
                    data_7 = stn_conc[stn_conc[:,0]>480 & stn_conc[:,0]<=480,:]  # (x37)
                    data_8 = stn_conc[stn_conc[:,0]>480,:]  # (x37)

                    data_1 = rmmissing[data_1,0]
                    data_2 = rmmissing[data_2,0]
                    data_3 = rmmissing[data_3,0]
                    if data_1.shape[0]>1:
                        data_1 = random.sample(data_1, np.round(data_1.shape[0]*0.1))
                    if data_2.shape[0]>1:
                        data_2 = random.sample(data_2, np.round(data_2.shape[0]*0.3))
                    if data_3.shape[0]>1:
                        data_3 = random.sample(data_3, np.round(data_3.shape[0]*0.5))

                    nndata = np.concatenate((data_1,data_2,data_3,data_4,data_5,data_6,data_7,data_8), axis=0)
                    
                    ndata_5 = oversampling_sh(data_5[:,:6],stn_6km_location,lon_goci.shape[0],lon_goci.shape[1],2)
                    ndata_6 = oversampling_sh(data_6[:,:6],stn_6km_location,lon_goci.shape[0],lon_goci.shape[1],12)
                    ndata_7 = oversampling_sh(data_7[:,:6],stn_6km_location,lon_goci.shape[0],lon_goci.shape[1],29)
                    ndata_8 = oversampling_sh(data_8[:,:6],stn_6km_location,lon_goci.shape[0],lon_goci.shape[1],36)

                    ndata = np.concatenate((nndata, ndata_5,ndata_6,ndata_7,ndata_8), axis=0)
                    del nndata, data_1, data_2, data_3, data_4, data_5, data_6, data_7, data_8, ndata_5, ndata_6, ndata_7, ndata_8
                    # remove station pixel among oversampled pixels
                    # ndata = [stn_conc, stn_num, doy_num, stn_ind, stn_x, stn_y, over]
                    dup_idx = matlab.ismember(ndata[:,6],stn_6km_location[:,4])
                    dup_idx = np.multiply(dup_idx, ndata[:,5]) #oversampling col
                    ndata = ndata[dup_idx==0,:]
                    
                    # Extract input variables at station points & oversampling points
                    data_tmp = data[ndata[:,6],:]
                    #  data_tmp = cases(ndata[:,6],[1:2,4:-1])
                    data_tmp[:,nvar:nvar+5] = ndata[:,:6] # data. stn_PM, stn_num, doy_num, time, yr, ovr
                    k=((doy-1)*8)+(utc+1)
                    data_tmp[:,nvar+6] = k #k_idx
                    data_tmp[data_tmp==-9999] = np.nan
                    data_tmp = rmmissing[data_tmp, 0]
                    data_stn = np.concatenate((data_stn, data_tmp), axis=0)
                    data_stn = matlab.sortrows(data_stn,30)
                    print (utc)
            print (doy)
            if doy >= 30 & utc == 7:
                csvwrite_with_headers2([path_save,'time_conc/dataset/PM25/PM25_RTT_EA6km_',
                    str(yr),'_',str(doy,'#03i'),'_',str(utc,'#02i'),'.csv'],data_stn,header2,0,0,'#7.7f')
                print (doy)
            -1
        else       
            for utc=0:7
                k=240               
                
                # leave the high concentration samples
                extra_samples = data_stn(data_stn[:,-1)==1,:)
                
                high_tmp = extra_samples(extra_samples[:,24)>=240,:)
                low_tmp = extra_samples(extra_samples[:,24)<=60,:)
                
                if np.all(high_tmp)==1
                    high = high
                else                    
                    high = [high high_tmp]  high[:,-1) = high[:,-1)+1
                    high_uniq = np.unique(high[:,1:29),'rows','stable') high_uniq[:,-1+1)=2
                    high = high_uniq
                -1
                
                if np.all(low_tmp)==1
                    low = low
                else
                    low = [low low_tmp]  low[:,-1) = low[:,-1)+1                    
                    low_uniq = np.unique(low[:,1:29),'rows','stable') low_uniq[:,-1+1)=2
                    low = low_uniq
                -1           
                
                data_stn = data_stn(data_stn[:,-1)>=2,:)
                high_tmp[:,-1) = high_tmp[:,-1)+1
                low_tmp[:,-1) = low_tmp[:,-1)+1
                data_stn = [low_tmp high_tmp data_stn]
                data_stn[:,-1) = data_stn[:,-1)-1                
                
                if np.all(data_stn)==1
                elif size(data_stn(data_stn[:,29)==1,:),1)>1
                    rmovr = datasample(data_stn(data_stn[:,-1-1)==1,:), round(size(data_stn(data_stn[:,-1-1)==1,:),1)*0.99),'Replace',false)
                    data_stn(data_stn[:,-1-1)==1,:)=[]
                    data_stn=[data_stn rmovr]
                else                    
                    data_stn(data_stn[:,-1-1)==1,:)=[]
                -1
                
                matlab.loadmat(os.path.join(path_data, 'EA_GOCI6km/cases_mat/',str(yr),'/cases_EA6km_',str(yr),'_',
                    str(doy, '#03i'),'_',str(utc,'#02i'),'.mat')) # data_tbl
                data = data_tbl[:,header) 
                data = table2array(data)                
                clear data_tbl
                
                # Load station data
                stn_6km = stn(stn[:,1) == doy & stn[:,2) ==yr & stn[:,5)== utc ,:)           
                                  
                if np.all(stn_6km)==0 # no observation data in some utc
                    stn_idx = matlab.ismember(stn_6km_location[:,2), stn_6km[:,13))
                    stn_conc = stn_6km[:,[11,13,1,5,2]) # PM25, stn_num, doy_num,time,yr
                    stn_conc[:,5]=0# PM10, stn_num, doy_num,time,yr, ovr
                    stn_conc[:,6] =stn_6km_location(stn_idx,5)# PM10, stn_num, doy_num,time,yr, ovr, stn_location
                   
                    data_1 = stn_conc(stn_conc[:,1)<=20,:)                    # (x0.1)
                    data_2 = stn_conc(stn_conc[:,1)>20 &stn_conc[:,1)<=40,:)   # (x0.3)
                    data_3 = stn_conc(stn_conc[:,1)>40 &stn_conc[:,1)<=60,:)   # (x0.5)
                    data_4 = stn_conc(stn_conc[:,1)>60 & stn_conc[:,1)<=120,:)  # (x1)
                    data_5 = stn_conc(stn_conc[:,1)>120 & stn_conc[:,1)<=240,:)  # (x3)
                    data_6 = stn_conc(stn_conc[:,1)>240 & stn_conc[:,1)<=360,:)  # (x13)
                    data_7 = stn_conc(stn_conc[:,1)>360 & stn_conc[:,1)<=480,:)  # (x30)
                    data_8 = stn_conc(stn_conc[:,1)>480,:)  # (x37)
                    
                    data_1 = rmmissing(data_1,1)
                    data_2 = rmmissing(data_2,1)
                    data_3 = rmmissing(data_3,1)
                    if size(data_1,1)>1
                        data_1 = datasample(data_1, round(size(data_1,1)*0.1),'Replace',false)
                    -1
                    if size(data_2,1)>1
                        data_2 = datasample(data_2, round(size(data_2,1)*0.3),'Replace',false)
                    -1
                    if size(data_3,1)>1
                        data_3 = datasample(data_3, round(size(data_3,1)*0.5),'Replace',false)
                    -1
                    nndata = [data_1data_2data_3data_4data_5data_6data_7data_8]
                    
                    ndata_5 = oversampling_sh(data_5[:,1:6),stn_6km_location,size(lon_goci,1),size(lon_goci,2),2)
                    ndata_6 = oversampling_sh(data_6[:,1:6),stn_6km_location,size(lon_goci,1),size(lon_goci,2),12)
                    ndata_7 = oversampling_sh(data_7[:,1:6),stn_6km_location,size(lon_goci,1),size(lon_goci,2),29)
                    ndata_8 = oversampling_sh(data_8[:,1:6),stn_6km_location,size(lon_goci,1),size(lon_goci,2),36)
                    
                    ndata = [nndata ndata_5ndata_6ndata_7ndata_8]
                    clearvars nndata data_1 data_2 data_3 data_4 data_5 data_6 data_7 data_8 ndata_5 ndata_6 ndata_7 ndata_8
                    
                    # remove station pixel among oversampled pixels
                    # ndata = [stn_conc, stn_num, doy_num, stn_ind, stn_x, stn_y, over]
                    dup_idx = matlab.ismember(ndata[:,6],stn_6km_location[:,5))
                    dup_idx = dup_idx .* ndata[:,5] #oversampling col
                    ndata = ndata[dup_idx==0,:)
                    
                    # Extract input variables at station points & oversampling points
                    data_tmp = data(ndata[:,6],:)
                    #  data_tmp = cases(ndata[:,6],[1:2,4:-1])
                    
                    data_tmp[:,nvar+1:nvar+6) = ndata[:,(1:6)) # data. stn_PM, stn_num, doy_num, time, yr, ovr
                    data_tmp[:,nvar+7) = k #k_idx
                    
                    data_tmp(data_tmp==-9999)np.nan
                    data_tmp = rmmissing(data_tmp,1)
                    
                    data_stn = [data_stn data_tmp]
                
                    high_rate_pre = size(data_stn(data_stn[:,24)>=240,:),1)/size(data_stn[:,24),1) *100
                    low_rate_pre = size(data_stn(data_stn[:,24)<=60,:),1)/size(data_stn[:,24),1) *100
                    
                    if high_rate_pre<30 & low_rate_pre<30 & size(data_stn[:,-1)>1,1)>1000
                        print (('num of samples = #4.0f \n remove the oversampled samples in the old dataset \n',size(data_stn,1))
                        data_stn(data_stn[:,-1-1)==1 & data_stn[:,-1)<=8 & data_stn[:,24)>60 & data_stn[:,24)<240,:) = []
                    -1
                    
                    high_rate_pre = size(data_stn(data_stn[:,24)>=240,:),1)/size(data_stn[:,24),1) *100
                    low_rate_pre = size(data_stn(data_stn[:,24)<=60,:),1)/size(data_stn[:,24),1) *100
                    
                    # sample adjustment part1 -> remove oversampled data
                    if high_rate_pre>30
                        print (('high_rate_pre = #3.2f & remove the stacked samples \n',high_rate_pre)
                        data_stn(data_stn[:,-1)==1 & data_stn[:,-1-1)==1 & data_stn[:,24)>=240,:)=[]
                    -1
                    
                    if low_rate_pre>30
                        print (('low_rate_pre = #3.2f & remove stacked samples \n',low_rate_pre)
                        data_stn(data_stn[:,-1)==1 & data_stn[:,-1-1)==1 & data_stn[:,24)<=60,:) = []
                    -1
                    
                    
                    high_rate = size(data_stn(data_stn[:,24)>=240,:),1)/size(data_stn[:,24),1) *100
                    low_rate = size(data_stn(data_stn[:,24)<=60,:),1)/size(data_stn[:,24),1) *100
                    
                    # sample adjustment
                    if high_rate<30 &low_rate>30
                        print (('high_rate = #3.2f & stack more \n',high_rate)
                        print (('low_rate = #3.2f & remove stacked samples \n',low_rate)
                        # remove the low concentration samples
                        if np.all(low)==0
                            idx_low = np.where(data_stn[:,26) <= low(-1,26) & data_stn[:,24)<=60 & data_stn[:,-1)==1)
                            data_stn(idx_low,:) = []
                        -1
                        
                    elif high_rate<30 & low_rate<30
                        print (('high_rate = #3.2f & stack more \n',high_rate)
                        print (('low_rate = #3.2f & stack more \n',low_rate)
                        
                    elif high_rate>30 &low_rate<30
                        print (('high_rate = #3.2f & remove the stacked samples \n',high_rate)
                        print (('low_rate = #3.2f & stack more \n',low_rate)
                        # remove the high concentration samples
                        if np.all(high)==0
                            idx_high = np.where(data_stn[:,26) <= high(-1,26) & data_stn[:,24)>=240 & data_stn[:,-1)==1)
                            data_stn(idx_high,:) = []
                        -1
                    elif high_rate>30 & low_rate>30
                        print (('high_rate = #3.2f \n',high_rate)
                        print (('low_rate = #3.2f \n',low_rate)
                        # remove the high concentration samples
                        idx_high = np.where(data_stn[:,26) <= high(-1,26) & data_stn[:,24)>=240 & data_stn[:,-1)==1)
                        data_stn(idx_high,:) = []
                        # remove the low concentration samples
                        idx_low = np.where(data_stn[:,26)<= low(-1,26) & data_stn[:,24)<=60 & data_stn[:,-1)==1)
                        data_stn(idx_low,:) = []
                    -1
                    data_stn = matlab.sortrows(data_stn,30)
                    csvwrite_with_headers2([path_save,'time_conc/dataset/PM25/PM25_RTT_EA6km_',
                        str(yr),'_',str(doy,'#03i'),'_',str(utc,'#02i'),'.csv'],data_stn,header2,0,0,'#7.7f')
                    print (utc)
                -1
            -1
            print (doy)
        -1
    -1
    print (yr)
    -1
