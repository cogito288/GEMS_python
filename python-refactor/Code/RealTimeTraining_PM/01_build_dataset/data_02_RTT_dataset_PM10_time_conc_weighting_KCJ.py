### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import pandas as pd
import random

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km')

path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')
path_stn_cn = os.path.join(path_station, 'Station_CN')
path_stn_kr = os.path.join(path_station, 'Station_KR')

path_rtt = os.path.join(path_ea_goci, 'RTT') # path_save 

## Station index
mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_goci.mat'))
lon_goci, lat_goci = mat['lon_goci'], mat['lat_goci']
del mat

mat = matlab.loadmat(os.path.join(path_stn_cn, 'cn_stn_GOCI6km_location_weight.mat'))
cn_dup_scode2_GOCI6km = mat['cn_dup_scode2_GOCI6km']
header_cn_stn_GOCI6km_location = mat['header_cn_stn_GOCI6km_location']
df = pd.DataFrame(mat['cn_stn_GOCI6km_location'], columns=header_cn_stn_GOCI6km_location)
cn_stn_GOCI6km_location = df.values
del df, mat

#mat = matlab.loadmat(os.path.join(path_stn_kr, 'stn_GOCI6km_location_weight_v2018.mat'))
mat = matlab.loadmat(os.path.join(path_stn_kr, 'stn_GOCI6km_location_weight_v201904.mat'))
dup_scode2_GOCI6km = mat['dup_scode2_GOCI6km']
df = pd.DataFrame(mat['stn_GOCI6km_location'], columns=mat['header_stn_GOCI6km_location'])
stn_GOCI6km_location = df.values
del df, mat

mat = matlab.loadmat(os.path.join(path_stn_jp, 'jp_stn_GOCI6km_location_weight_v2017.mat'))
jp_dup_scode2_GOCI6km = mat['jp_dup_scode2_GOCI6km']
header_jp_stn_GOCI6km_location = mat['header_jp_stn_GOCI6km_location']
df = pd.DataFrame(mat['jp_stn_GOCI6km_location'], columns=header_jp_stn_GOCI6km_location)
jp_stn_GOCI6km_location = df.values
del df, mat

stn_6km_location = np.concatenate([stn_GOCI6km_location, jp_stn_GOCI6km_location, cn_stn_GOCI6km_location], axis=0)
cn_dup_scode2_GOCI6km = np.concatenate([cn_dup_scode2_GOCI6km, np.zeros((cn_dup_scode2_GOCI6km.shape[0], jp_dup_scode2_GOCI6km.shape[1]))], axis=1)
dup_scode2_GOCI6km = np.concatenate([dup_scode2_GOCI6km, np.zeros((dup_scode2_GOCI6km.shape[0], jp_dup_scode2_GOCI6km.shape[1]))], axis=1)
dup_scode2_6km = np.concatenate((dup_scode2_GOCI6km, cn_dup_scode2_GOCI6km, jp_dup_scode2_GOCI6km), axis=0)

del stn_GOCI6km_location, cn_stn_GOCI6km_location, jp_stn_GOCI6km_location, cn_dup_scode2_GOCI6km, dup_scode2_GOCI6km, jp_dup_scode2_GOCI6km, header_cn_stn_GOCI6km_location, header_jp_stn_GOCI6km_location

## header
header = ['AOD','AE','FMF','SSA','NDVI','RSDN','Precip','DEM','LCurban', # satellite data(9)
    'Temp','Dew','RH','P_srf','MaxWS','PBLH','Visibility', # numerical data(RDAPS)(16)
    'stack1_np.maxWS','stack3_np.maxWS','stack5_np.maxWS','stack7_np.maxWS', # stacked np.maxWS(20)
    'DOY','PopDens','RoadDens'] #, etc data(23)    
header2 = header+['PM10','stn_num','doy_num','time','yr','ovr','k_ind']

nvar = 23
## Read data
data_stn = []
high = []
low = []

YEARS = [2016]
for yr in YEARS:
    if yr%4==0: days = 366
    else: days = 365
    
    fname = f'Station_GOCI6km_{yr}_weight.mat'
    mat = matlab.loadmat(os.path.join(path_stn_kr, fname))
    stn_GOCI6km_yr = mat['stn_GOCI6km_yr']
    del mat
    
    fname = f'cn_Station_GOCI6km_rm_outlier_{yr}_weight.mat'
    mat = matlab.loadmat(os.path.join(path_stn_cn, fname))
    cn_stn_GOCI6km_yr = mat['cn_stn_GOCI6km_yr']
    
    if yr < 2017:
        fname = f'jp_Station_GOCI6km_{yr}_weight.mat'
    else:
        fname = f'jp_Station_GOCI6km_rm_outlier_{yr}_weight.mat'
    mat = matlab.loadmat(os.path.join(path_stn_jp, fname))
    jp_stn_GOCI6km_yr = mat['jp_stn_GOCI6km_yr']
    del mat
    
    
    jp_stn_GOCI6km_yr = jp_stn_GOCI6km_yr[(jp_stn_GOCI6km_yr[:,4]>=9) & (jp_stn_GOCI6km_yr[:,4]<=16),0:13]
    stn_GOCI6km_yr = stn_GOCI6km_yr[(stn_GOCI6km_yr[:,4]>=9) & (stn_GOCI6km_yr[:,4]<=16),:]
    stn_GOCI6km_yr[:,4] = stn_GOCI6km_yr[:,4]-9
    jp_stn_GOCI6km_yr[:,4] = jp_stn_GOCI6km_yr[:,4]-9
    cn_stn_GOCI6km_yr[:,4] = cn_stn_GOCI6km_yr[:,4]-8
    tmp_axis = [0,1,2,3,4,10,18,14,12,8,6,20,21]
    stn = np.concatenate((stn_GOCI6km_yr, jp_stn_GOCI6km_yr, cn_stn_GOCI6km_yr[:,tmp_axis]), axis=0)
    del stn_GOCI6km_yr, jp_stn_GOCI6km_yr, cn_stn_GOCI6km_yr

    for doy in range(1,days+1):
        if len(data_stn)==0: # empty
            None # Do nothing
        elif data_stn[data_stn[:,28]==1,:].shape[0]>1:
            tmp_data = data_stn[data_stn[:,-2]==1,:]
            mask = np.random.choice(tmp_data.shape[0], np.round(tmp_data.shape[0]*0.9).astype(int), replace=False)
            rmovr = tmp_data[mask, :]
            idx = (data_stn[:, -2]!=1)
            data_stn = data_stn[idx, :] #data_stn[data_stn[:,-1]==1,:]=[]
            data_stn = np.concatenate([data_stn, rmovr], axis=0)
        else:
            idx = (data_stn[:, -2]!=1)
            data_stn = data_stn[idx, :] #data_stn[data_stn[:,-1]==1,:]=[]
        
        if doy <=30:
        #if doy <=30 and yr == 2015:
            for utc in range(7+1):
                if len(data_stn)==0: # etmpty
                    None # Do nothing
                elif data_stn[data_stn[:,28]==1,:].shape[0]>1:
                    tmp_data = data_stn[data_stn[:,-2]==1,:]
                    mask = np.random.choice(tmp_data.shape[0], np.round(tmp_data.shape[0]*0.99).astype(int), replace=False)
                    rmovr = tmp_data[mask, :]
                    idx = (data_stn[:, -2]!=1)
                    data_stn = data_stn[idx, :]
                    data_stn = np.concatenate((data_stn, rmovr), axis=0)
                else:                   
                    idx = (data_stn[:, -2]!=1)
                    data_stn = data_stn[idx, :]
                
                fname = f'cases_EA6km_{yr}_{doy:03d}_{utc:02d}.mat'
                mat = matlab.loadmat(os.path.join(path_ea_goci, 'cases_mat',str(yr), fname)) # data_tbl
                df = pd.DataFrame(columns = mat['header'])
                for col in mat['header']:
                    df[col] = mat[col]
                data = df.values
                del df, mat
                
                # Load station data
                stn_6km = stn[(stn[:,0]==doy) & (stn[:,1] ==yr) & (stn[:,4]==utc),:]
                
                if len(stn_6km)!=0: # no observation data in some utc
                    stn_idx = np.isin(stn_6km_location[:,1], stn_6km[:,12])
                    stn_conc = stn_6km[:,[9,12,0,4,1]] # PM10, stn_num, doy_num,time,yr
                    stn_conc = np.hstack([stn_conc, np.zeros((stn_conc.shape[0], 2))]) 
                    # stn_conc[:,5] = 0 # PM10, stn_num, doy_num,time,yr, ovr
                    stn_conc[:,6] = stn_6km_location[stn_idx,4]# PM10, stn_num, doy_num,time,yr, ovr, stn_location
                   
                    data_1 = stn_conc[stn_conc[:,0]<=20,:]            # (x0.03)
                    data_2 = stn_conc[(stn_conc[:,0]>20) & (stn_conc[:,0]<=40),:] # (x0.07)
                    data_3 = stn_conc[(stn_conc[:,0]>40) & (stn_conc[:,0]<=60),:] # (x0.1)
                    data_4 = stn_conc[(stn_conc[:,0]>60) & (stn_conc[:,0]<=80),:]  # (x0.2)
                    data_5 = stn_conc[(stn_conc[:,0]>80) & (stn_conc[:,0]<=100),:]  # (x0.4)
                    data_6 = stn_conc[(stn_conc[:,0]>100) & (stn_conc[:,0]<=120),:]  # (x0.6)
                    data_7 = stn_conc[(stn_conc[:,0]>120) & (stn_conc[:,0]<=180),:]  # (x1)
                    data_8 = stn_conc[(stn_conc[:,0]>180) & (stn_conc[:,0]<=270),:]  # (x3)
                    data_9 = stn_conc[(stn_conc[:,0]>270) & (stn_conc[:,0]<=360),:] # (x9)
                    data_10 = stn_conc[(stn_conc[:,0]>360) & (stn_conc[:,0]<=540),:] # (x16)
                    data_11 = stn_conc[stn_conc[:,0]>540,:]            # (x37)
                    
                    data_1 = data_1[~np.isnan(data_1).any(axis=1)] # delete row if any of element is nan
                    data_2 = data_1[~np.isnan(data_2).any(axis=1)]
                    data_3 = data_1[~np.isnan(data_3).any(axis=1)]
                    data_4 = data_1[~np.isnan(data_4).any(axis=1)]
                    data_5 = data_1[~np.isnan(data_5).any(axis=1)]
                    data_6 = data_1[~np.isnan(data_6).any(axis=1)]
                    if data_1.shape[0]>1:
                        mask = np.random.choice(data_1.shape[0], np.round(data_1.shape[0]*0.03).astype(int), replace=False)
                        data_1 = data_1[mask, :]
                    if data_2.shape[0]>1:
                        mask = np.random.choice(data_2.shape[0], np.round(data_2.shape[0]*0.07).astype(int), replace=False)
                        data_2 = data_2[mask, :]                        
                    if data_3.shape[0]>1:
                        mask = np.random.choice(data_3.shape[0], np.round(data_3.shape[0]*0.1).astype(int), replace=False)
                        data_3 = data_3[mask, :]
                    if data_4.shape[0]>1:
                        mask = np.random.choice(data_4.shape[0], np.round(data_4.shape[0]*0.2).astype(int), replace=False)
                        data_4 = data_4[mask, :]
                    if data_5.shape[0]>1:
                        mask = np.random.choice(data_5.shape[0], np.round(data_5.shape[0]*0.4).astype(int), replace=False)
                        data_5 = data_5[mask, :]
                    if data_6.shape[0]>1:
                        mask = np.random.choice(data_6.shape[0], np.round(data_6.shape[0]*0.6).astype(int), replace=False)
                        data_6 = data_6[mask, :]
                    
                    nndata = np.concatenate((data_1,data_2,data_3,data_4,data_5,data_6,data_7,data_8,data_9,data_10,data_11), axis=0)
                    ndata_8 = matlab.oversampling_sh(data_8[:,:6],stn_6km_location,lon_goci.shape[0],lon_goci.shape[1],2,
                                                     patch_path=os.path.join(path_grid_raw, 'ovr_patch_order.mat'))
                    ndata_9 = matlab.oversampling_sh(data_9[:,:6],stn_6km_location,lon_goci.shape[0],lon_goci.shape[1],8,
                                                     patch_path=os.path.join(path_grid_raw, 'ovr_patch_order.mat'))
                    ndata_10 = matlab.oversampling_sh(data_10[:,:6],stn_6km_location,lon_goci.shape[0],lon_goci.shape[1],15,
                                                      patch_path=os.path.join(path_grid_raw, 'ovr_patch_order.mat'))
                    ndata_11 = matlab.oversampling_sh(data_11[:,:6],stn_6km_location,lon_goci.shape[0],lon_goci.shape[1],36,
                                                      patch_path=os.path.join(path_grid_raw, 'ovr_patch_order.mat'))
                    ndata = np.concatenate((nndata, ndata_8,ndata_9,ndata_10,ndata_11), axis=0)
                    del nndata, data_1, data_2, data_3, data_4, data_5, data_6, data_7, data_8, data_9, data_10, data_11, ndata_8, ndata_9, ndata_10, ndata_11
                                        
                    # remove station pixel among oversampled pixels
                    # ndata = [stn_conc, stn_num, doy_num, stn_ind, stn_x, stn_y, over]
                    dup_idx = np.isin(ndata[:,6],stn_6km_location[:,4])
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
                    data_stn = matlab.sortrows(data_stn,[29])
                    print (utc)
            print (doy)
            if doy >= 30 & utc == 7:
                fname = f'PM10_RTT_EA6km_{yr}_{doy:03d}_{utc:02d}.csv'
                temp_df = pd.DataFrame(data_stn, columns=header2)
                temp_df.to_csv(os.path.join(path_rtt, 'time_conc/dataset/PM10', fname), float_format='%7.7f')
                print (doy)
        else:
            for utc in range(7):
                k=240          
                # leave the high concentration samples
                print (data_stn)
                extra_samples = data_stn[data_stn[:,-1]==1,:]
                high_tmp = extra_samples[extra_samples[:,23]>=400,:]
                low_tmp = extra_samples[extra_samples[:,23]<=100,:]
                    
                if len(high_tmp)==0: #empty
                    None
                else:
                    high = np.concatenate((high, high_tmp), axis=0)
                    high[:,-1] = high[:,-1]+1
                    high_uniq = np.unique(high[:,:29], axis=1)
                    high_uniq = np.hstack([high_uniq, np.ones(high_uniq.shape[0])*2])
                    high = high_uniq
                
                if len(low_tmp)==0: #empty
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
                
                if len(data_stn)==0: # etmpty
                    None # Do nothing
                elif data_stn[data_stn[:,28]==1,:].shape[0]>1:
                    rmovr = random.sample(data_stn[data_stn[:,-2]==1,:], np.round(data_stn[data_stn[:,-2]==1,:].shape[0]*0.99).astype(int))
                    idx = (data_stn[:, -2]!=1)
                    data_stn = data_stn[idx, :]
                    data_stn = np.concatenate((data_stn, rmovr), axis=0)
                else:                   
                    idx = (data_stn[:, -2]!=1)
                    data_stn = data_stn[idx, :]
                
                fname = f'cases_EA6km_{yr}_{doy:03d}_{utc:02d}.mat'
                mat = matlab.loadmat(os.path.join(path_ea_goci, 'cases_mat',str(yr), fname)) # data_tbl
                df = pd.DataFrame(columns = mat['header'])
                for col in mat['header']:
                    df[col] = mat[col]
                data = df.values
                del df, mat
                
                # Load station data
                stn_6km = stn[(stn[:,0] == doy) & (stn[:,1] ==yr) & (stn[:,4]== utc),:]
                
                if len(stn_6km)!=0: # no observation data in some utc
                    stn_idx = np.isin(stn_6km_location[:,1], stn_6km[:,12])
                    stn_conc = stn_6km[:,[9,12,0,4,1]] # PM10, stn_num, doy_num,time,yr
                    stn_conc = np.hstack([stn_conc, np.zeros((stn_conc.shape[0], 2))]) 
                    # stn_conc[:,5] = 0 # PM10, stn_num, doy_num,time,yr, ovr
                    stn_conc[:,6] = stn_6km_location[stn_idx,4]# PM10, stn_num, doy_num,time,yr, ovr, stn_location
                   
                    data_1 = stn_conc[stn_conc[:,0]<=20,:]            # (x0.03)
                    data_2 = stn_conc[(stn_conc[:,0]>20) & (stn_conc[:,0]<=40),:] # (x0.07)
                    data_3 = stn_conc[(stn_conc[:,0]>40) & (stn_conc[:,0]<=60),:] # (x0.1)
                    data_4 = stn_conc[(stn_conc[:,0]>60) & (stn_conc[:,0]<=80),:]  # (x0.2)
                    data_5 = stn_conc[(stn_conc[:,0]>80) & (stn_conc[:,0]<=100),:]  # (x0.4)
                    data_6 = stn_conc[(stn_conc[:,0]>100) & (stn_conc[:,0]<=120),:]  # (x0.6)
                    data_7 = stn_conc[(stn_conc[:,0]>120) & (stn_conc[:,0]<=180),:]  # (x1)
                    data_8 = stn_conc[(stn_conc[:,0]>180) & (stn_conc[:,0]<=270),:]  # (x3)
                    data_9 = stn_conc[(stn_conc[:,0]>270) & (stn_conc[:,0]<=360),:] # (x9)
                    data_10 = stn_conc[(stn_conc[:,0]>360) & (stn_conc[:,0]<=540),:] # (x16)
                    data_11 = stn_conc[stn_conc[:,0]>540,:]            # (x37)
                    
                    
                    data_1 = data_1[~np.isnan(data_1).any(axis=1)] # delete row if any of element is nan
                    data_2 = data_1[~np.isnan(data_2).any(axis=1)]
                    data_3 = data_1[~np.isnan(data_3).any(axis=1)]
                    data_4 = data_1[~np.isnan(data_4).any(axis=1)]
                    data_5 = data_1[~np.isnan(data_5).any(axis=1)]
                    data_6 = data_1[~np.isnan(data_6).any(axis=1)]
                    if data_1.shape[0]>1:
                        mask = np.random.choice(data_1.shape[0], np.round(data_1.shape[0]*0.03).astype(int), replace=False)
                        data_1 = data_1[mask, :]
                    if data_2.shape[0]>1:
                        mask = np.random.choice(data_2.shape[0], np.round(data_2.shape[0]*0.07).astype(int), replace=False)
                        data_2 = data_2[mask, :]                        
                    if data_3.shape[0]>1:
                        mask = np.random.choice(data_3.shape[0], np.round(data_3.shape[0]*0.1).astype(int), replace=False)
                        data_3 = data_3[mask, :]
                    if data_4.shape[0]>1:
                        mask = np.random.choice(data_4.shape[0], np.round(data_4.shape[0]*0.2).astype(int), replace=False)
                        data_4 = data_4[mask, :]
                    if data_5.shape[0]>1:
                        mask = np.random.choice(data_5.shape[0], np.round(data_5.shape[0]*0.4).astype(int), replace=False)
                        data_5 = data_5[mask, :]
                    if data_6.shape[0]>1:
                        mask = np.random.choice(data_6.shape[0], np.round(data_6.shape[0]*0.6).astype(int), replace=False)
                        data_6 = data_6[mask, :]
                        
                    nndata = np.concatenate((data_1,data_2,data_3,data_4,data_5,data_6,data_7,data_8,data_9,data_10,data_11), axis=0)
                    
                    ndata_8 = matlab.oversampling_sh(data_8[:,:6],stn_6km_location,lon_goci.shape[0],lon_goci.shape[1],2,
                                                     patch_path=os.path.join(path_grid_raw, 'ovr_patch_order.mat'))
                    ndata_9 = matlab.oversampling_sh(data_9[:,:6],stn_6km_location,lon_goci.shape[0],lon_goci.shape[1],8,
                                                     patch_path=os.path.join(path_grid_raw, 'ovr_patch_order.mat'))
                    ndata_10 = matlab.oversampling_sh(data_10[:,:6],stn_6km_location,lon_goci.shape[0],lon_goci.shape[1],15,
                                                      patch_path=os.path.join(path_grid_raw, 'ovr_patch_order.mat'))
                    ndata_11 = matlab.oversampling_sh(data_11[:,:6],stn_6km_location,lon_goci.shape[0],lon_goci.shape[1],36,
                                                      patch_path=os.path.join(path_grid_raw, 'ovr_patch_order.mat'))
                    ndata = np.concatenate((nndata, ndata_8,ndata_9,ndata_10,ndata_11), axis=0)
                    del nndata, data_1, data_2, data_3, data_4, data_5, data_6, data_7, data_8, data_9, data_10, data_11, ndata_8, ndata_9, ndata_10, ndata_11
                    # remove station pixel among oversampled pixels
                    # ndata = [stn_conc, stn_num, doy_num, stn_ind, stn_x, stn_y, over]
                    dup_idx = np.isin(ndata[:,6],stn_6km_location[:,4])
                    dup_idx = np.multiply(dup_idx, ndata[:,5]) #oversampling col
                    ndata = ndata[dup_idx==0,:]

                    # Extract input variables at station points & oversampling points
                    data_tmp = data[ndata[:,6],:]
                    
                    data_tmp[:,nvar:nvar+6] = ndata[:,:6] # data. stn_PM, stn_num, doy_num, time, yr, ovr
                    k=((doy-1)*8)+(utc+1)
                    data_tmp[:,nvar+6] = k #k_idx
                                            
                    data_tmp[data_tmp==-9999] = np.nan
                    data_tmp = data_tmp[~np.isnan(data_tmp).any(axis=1)]
                    idx = data_tmp[:, 23]>10000
                    data_tmp = data_tmp[~idx, :] #data_tmp[data_tmp[:,23]>1000,:] =[]
                    data_stn = np.concatenate((data_stn, data_tmp), axis=0)
                    
                    high_rate_pre = data_stn[data_stn[:,23]>=400,:].shape[0]/data_stn[:,23].shape[0]*100
                    low_rate_pre = data_stn[data_stn[:,23]<=100,:].shape[0]/data_stn[:,23].shape[0]*100
                    if high_rate_pre<30 & low_rate_pre<30 & (data_stn[:,-1]>1).shape[0]>10000:
                        print (f'num of samples = {data_stn:4.0f} \n remove the oversampled samples in the oldest dataset \n')
                        idx = data_stn[:,-2]==1 & data_stn[:,-1]<=8 & data_stn[:,23]>100 & data_stn[:,23]<400
                        data_stn = data_stn[~idx,:]
                        
                    high_rate_pre = data_stn[data_stn[:,23]>=400,:].shape[0]/data_stn[:,23].shape[0]*100
                    low_rate_pre = data_stn[data_stn[:,23]<=100,:].shape[0]/data_stn[:,23].shape[0]*100
                    # sample adjustment part1 -> remove the oversampled data
                    if high_rate_pre>30:
                        print (f'high_rate_pre = {high_rate_pre:3.2f} & remove the stacked samples \n')
                        idx = data_stn[:,-1]==1 & data_stn[:,-2]==1 & data_stn[:,23]>=400
                        data_stn = data_stn[~idx,:]
                    if low_rate_pre>30:
                        print (f'low_rate_pre = {low_rate_pre:3.2f} & remove stacked samples \n')
                        idx = data_stn[:,-1]==1 & data_stn[:,-2]==1 & data_stn[:,23]<=100
                        data_stn = data_stn[~idx,:]
                        
                    high_rate_pre = data_stn[data_stn[:,23]>=400,:].shape[0]/data_stn[:,23].shape[0]*100
                    low_rate_pre = data_stn[data_stn[:,23]<=100,:].shape[0]/data_stn[:,23].shape[0]*100
                    
                    # sample adjustment
                    if high_rate<30 & low_rate>30:
                        print (f'high_rate = {high_rate:3.2f} & stack more \n')
                        print (f'low_rate = {low_rate:3.2f} & remove stacked samples \n')
                        # remove the low concentration samples
                        if len(low)!=0:
                            idx_low = np.where(data_stn[:,25] <= low[-1,25] & data_stn[:,23]<=100 & data_stn[:,-1]==1)[0] # remove the low concentration samples under than doy
                            data_stn = data_stn[~idx_low,:]
                    elif high_rate<30 & low_rate<30:
                        print (f'high_rate = {high_rate:3.2f} & stack more \n')
                        print (f'low_rate = {low_rate:3.2f} & stack more \n')
                        
                    elif high_rate>30 & low_rate<30:
                        print (f'high_rate = {high_rate:3.2f} & remove stacked samples \n')
                        print (f'low_rate = {low_rate:3.2f} & stack more \n')
                        # remove the high concentration samples
                        if len(high)!=0:
                            idx_high = np.where(data_stn[:,25] <= high[-1,25] & data_stn[:,23]>=400 & data_stn[:,-1]==1)[0]
                            data_stn = data_stn[~idx_high,:] 
                            
                    elif high_rate>30 & low_rate>30:
                        print (f'high_rate = {high_rate:3.2f}\n')
                        print (f'low_rate = {low_rate:3.2f}\n')
                        # remove the high concentration samples
                        idx_high = np.where(data_stn[:,25] <= high[-1,25] & data_stn[:,23]>=400 & data_stn[:,-1]==1)[0]
                        data_stn = data_stn[~idx_high,:]
                        # remove the low concentration samples
                        idx_low = np.where(data_stn[:,25] <= low[-1,25] & data_stn[:,23]<=100 & data_stn[:,-1]==1)[0]
                        data_stn = data_stn[~idx_low,:]
 
                    data_stn = matlab.sortrows(data_stn,[29])
                    fname = f'PM10_RTT_EA6km_{yr}_{doy:03d}_{utc:02d}.csv'
                    temp_df = pd.DataFrame(data_stn, columns=header2)
                    temp_df.to_csv(os.path.join(path_rrt,'time_conc/dataset/PM10', fname), float_format='%7.7f')
                    print (utc)
            print (doy)
            
    print (yr)