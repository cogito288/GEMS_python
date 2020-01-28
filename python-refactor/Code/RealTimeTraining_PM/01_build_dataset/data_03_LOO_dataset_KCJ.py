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
from scipy.spatial.distance import pdist, squareform

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

## Read data
target = ['PM10','PM25']
type_list = ['conc','time','time_conc']

##
for t in [1]:
    for i in [1]: ########
        header = ['AOD','AE','FMF','SSA','NDVI','RSDN','Precip','DEM','LCurban', # satellite data(9)
            'Temp','Dew','RH','P_srf','MaxWS','PBLH','Visibility', # numerical data(RDAPS)(16)
            'stack1_np.maxWS','stack3_np.maxWS','stack5_np.maxWS','stack7_np.maxWS', # stacked np.maxWS(20)
            'DOY','PopDens','RoadDens'] #, etc data(24)
        nvar = 23
        
        if i==1:
            header2 = header+['PM10','stn_num','doy_num','time','yr','ovr','k_ind']
        else:
            header2 = header+['PM25','stn_num','doy_num','time','yr','ovr','k_ind']
        YEARS = [2016]
        for yr in YEARS:
            if yr%4==0: days = 366
            else: days = 365
                
            for doy in range(1,days+1):
                try:
                    yy, mm, dd = matlab.get_ymd(yr, doy)
                    for utc in range(7+1):
                        fname = f'{target[i]}_RTT_EA6km_{yr}_{doy:03d}_{utc:02d}.csv'
                        data = pd.read_csv(os.path.join(path_rtt, type_list[t],'dataset/',target[i], fname))
                        
                        if i==1:
                            data = data[data[:,-7]<=1000,:]
                            val_num = 30
                        elif i==2:
                            data = data[data[:,-7]<=600,:]
                            val_num = 20
                            
                        val = data[[(data[:,-5]==doy) & (data[:,-3]==utc) & (data[:,-1]==0)],:]
                        val_stn = val[:,-6] # stn_num
                        idx = (data[:,-5]==doy) & (data[:,-3]==utc) & (data[:,-1]==0)
                        data = data[~idx, :]
                        
                        cal_10_fold = []
                        val_10_fold = []  
                        if val_stn.shape[0]>val_num:
                            val_lonlat=[]
                            for lo in range(val_stn.shape[0]):
                                val_lonlat[lo,:] = stn_6km_location[np.where(stn_6km_location[:,1]==val[lo,24])[0],:]
                            dist_tmp = pdist(val_lonlat[:,5:7])
                            dist = squareform(dist_tmp)
                            
                            num_dist = np.zeros(val_stn.shape[0])
                            for l in range(val_stn.shape[0]):
                                row, col = np.where(dist[:,l]<1) # 3 km
                                zero_values = np.zeros((val_stn.shape[0]-row.shape[0],1))
                                num_dist[:,l]=np.concatenate((row, zero_values), axis=0)
                                
                            del dist_tmp, val_lonlat, dist, zero_values
                            num = []
                            for ii in range(num_dist.shape[1]):
                                num_tmp = num_dist[:,ii]
                                num_tmp = num_tmp[num_tmp!=0]
                                if num_tmp.shape[0]>val_num:
                                    val_group = val[num_tmp,:]
                                    idx_val = np.isin(data[:,-6],val_group[:,-6])
                                    
                                    val_10_fold = val[ii,:]
                                    cal_10_fold = np.concatenate((data[idx_val,:], val[np.isin(num_tmp,[ii])==0,:]), axis=0)
                                    
                                    temp_path = os.path.join(path_ea_goci,'LOO/',type_list[t],'/dataset/',target[i])
                                    fname = f'{target[i]}_RTT_EA6km_{yr}_{doy:03d}_{utc:02d}'
                                    matlab.savemat(temp_path, fname+f'_LOO_{ii:03d}_cal_doy_stn_ovr.mat',{'cal_10_fold':cal_10_fold})
                                    matlab.savemat(temp_path, fname+f'_LOO_{ii:03d}_val_doy_stn_ovr.mat',{'val_10_fold':val_10_fold})
                                    
                                    cal_10_fold = cal_10_fold[:,:-7]
                                    val_10_fold = val_10_fold[:,:-7]
                                    
                                    temp_df = pd.DataFrame(cal_10_fold, columns=header2[:-7])
                                    temp_df.to_csv(os.path.join(temp_path, fname+f'_LOO_{ii:03d}_cal.csv'))
                                    del temp_df
                                    
                                    temp_df = pd.DataFrame(val_10_fold, columns=header2[:-7])
                                    temp_df.to_csv(os.path.join(temp_path, fname+f'_LOO_{ii:03d}_val.csv'))
                                    del temp_df
                                    
                                    print (utc)
                                else: # station number < val_num in specific distance
                                    print (f'Station number of {doy:3.0f} (DOY) & {utc:1.0f} (UTC) is under the {val_num:2.0f} in row {ii:2.0f} \n')
                                #val_num
                            #num_dist
                       # distance
                   #utc
                    print (doy)
                except:
                    print (f'{yr}_{doy:03d}')
                #try
            #doy
            print (yr)
        # year
        print (target[i])
    #target
#type