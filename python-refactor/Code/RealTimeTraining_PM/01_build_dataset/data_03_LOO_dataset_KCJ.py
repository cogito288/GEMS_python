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
from scipy.spatial.distance import pdist, squareform

# path_data = '//10.72.26.56/irisnas5/Data/'
# path_save = '//10.72.26.56/irisnas5/GEMS/PM/00_EA6km/'
# addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'))
path_data = '/share/irisnas5/Data/'
path_save = '/share/irisnas5/GEMS/PM/00_EA6km/'
addpath(genpath('/share/irisnas5/Data/matlab_func/'))
# path_data = '/Volumes/irisnas5/Data/'
# path_save = '/Volumes/irisnas5/GEMS/PM/00_EA6km/'
# addpath(genpath('/Volumes/irisnas5/Data/matlab_func/'))


## Station index
matlab.loadmat(os.path.join(path_data,'Station/Station_CN/cn_stn_GOCI6km_location_weight.mat'))
matlab.loadmat(os.path.join(path_data,'Station/Station_Korea/stn_GOCI6km_location_weight_v2018.mat'])
matlab.loadmat(os.path.join(path_data,'Station/Station_JP/jp_stn_GOCI6km_location_weight.mat'))
stn_6km_location = np.concatenate((stn_GOCI6km_location, jp_stn_GOCI6km_location, cn_stn_GOCI6km_location), axis=0)
cn_dup_scode2_GOCI6km[:,end+1:jp_dup_scode2_GOCI6km.shape[1]]=0
dup_scode2_GOCI6km[:,end+1:jp_dup_scode2_GOCI6km.shape[1]]=0
dup_scode2_6km =np.concatenate((dup_scode2_GOCI6km, cn_dup_scode2_GOCI6km, jp_dup_scode2_GOCI6km), axis=0)

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
        YEARS = [2017]
        for yr in YEARS:
            if yr%4==0: days = 366
            else: days = 365
            for doy in range(1,days+1):
                try:
                    yy, mm, dd = get_ymd(yr, doy) # should check 
                    for utc in range(7+1):
                        fname = f'{target[i]}_RTT_EA6km_{yr}_{doy:03d}_{utc:02d}.csv'
                        data = pd.read_csv(os.path.join(path_save, 'RTT/',type_list[t],'dataset/',target[i], fname), header=1)
                        
                        if i==1:
                            data = data[data[:,-7]<=1000,:]
                            val_num = 30
                        elif i==2:
                            data = data[data[:,-7]<=600,:]
                            val_num = 20
                            
                        val = data[[data[:,-5]==doy & data[:,-3]==utc & data[:,-1]==0],:]
                        val_stn = val[:,-5] # stn_num
                        data[[data[:,-4]==doy & data[:,-3]==utc & data[:,-1]==0],:] = []
                        
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
                            for ii in range(num_dist.shape[0]):
                                num_tmp = num_dist[:,ii]
                                num_tmp[num_tmp==0]=[]
                                if num_tmp.shape[0]>val_num:
                                    val_group = val[num_tmp,:]
                                    idx_val = matlab.ismember(data[:,-5],val_group[:,-5])
                                    val_10_fold = val[ii,:]
                                    cal_10_fold = np.concatenate((data[idx_val,:], val[matlab.ismember(num_tmp,[ii])==0,:]), axis=0)
                                    temp_path = os.path.join(path_save,'LOO/',type_list[t],'/dataset/',target[i])
                                    fname = f'{target[i]}_RTT_EA6km_{yr}_{doy:03d}_{utc:02d}'
    
                                    matlab.savemat(temp_path, fname+f'_LOO_{ii:03d}_cal_doy_stn_ovr.mat',{'cal_10_fold':cal_10_fold})
                                    matlab.savemat(temp_path, fname+f'_LOO_{ii:03d}_val_doy_stn_ovr.mat',{'val_10_fold':val_10_fold})
                                    
                                    cal_10_fold = cal_10_fold[:,:-6]
                                    val_10_fold = val_10_fold[:,:-6]
                                    
                                    temp_df = pd.DataFrame(cal_10_fold, columns=header2[:-6])
                                    temp_df.to_csv(os.path.join(temp_path, fname+f'_LOO_{ii:03d}_cal.csv'))
                                    del temp_df
                                    temp_df = pd.DataFrame(val_10_fold, columns=header2[:-6])
                                    temp_df.to_csv(os.path.join(temp_path, fname+f'_LOO_{ii:03d}_valcsv'))
                                    del temp_df
                                    
                                    print (utc)
                                else: # station number < val_num in specific distance
                                    print ('Station number of {doy:3.0f} (DOY) & {utc:1.0f} (UTC) is under the {val_num:2.0f} in row {ii:2.0f} \n')
                                #val_num
                            #num_dist
                       # distance
                   #utc
                    print (doy)
                except:
                    print (f'{yr}_{doy:03d}')])
                #try
            #doy
            print (yr)
        # year
        print (target[i])
    #target
#type
