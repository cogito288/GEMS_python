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
path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 

## STN_header
# Korea station_header
# {'DOY','year','month','day','time','SO2','CO','O3','NO2','PM10','PM25','Lat','Lon','station'}

# Japan station_header
# {'DOY','year','month','day','time','SO2','CO','OX','NO2','PM10','PM25','Lat','Lon','station'}

# China station header
# {'doy','yr','mm','dd','time','AQI','PM2.5','PM2.5_24h','PM10',...
#   'PM10_24h','SO2','SO2_24h','NO2','NO2_24h','O3','O3_24h','O3_8h','O3_8h_24h','CO','CO_24h','stn_num'}

##
stn_JP = None
YEARS = [2016]
for yr in YEARS:
    if yr%4==0:  days= 366; 
    else: days=365;
    stn_yr = matlab.loadmat(os.path.join(path_station, 'Station_JP', f'stn_code_data_{yr}.mat'))['stn_yr']
    stn_yr = stn_yr.astype('float64')
    stn_yr[stn_yr==-9999] = np.nan
    stn_num = np.unique(stn_yr[:,-1])
    
    stn_doy = None
    PM10 = np.zeros((len(stn_num), 9))
    PM25 = np.zeros((len(stn_num), 9))
    O3 = np.zeros((len(stn_num), 9))
    NO2 = np.zeros((len(stn_num), 9))
    CO = np.zeros((len(stn_num), 9))
    SO2 = np.zeros((len(stn_num), 9))
    for doy in range(1,days+1):
        for i in range(1, len(stn_num)+1):
            for tt in range(9, 16+1): # tt: china local time(GEMS time resoluion(9-16KST))
                try:
                    stn = stn_yr[(stn_yr[:,0]==doy) & (stn_yr[:,4]==tt),:]
                    stn[stn[:,5]>20,5] =np.nan
                    stn[stn[:,6]>400,6] =np.nan
                    stn[stn[:,7]>400,7] =np.nan
                    stn[stn[:,8]>300,8] =np.nan
                    stn[stn[:,9]>600,9] =np.nan
                    stn[stn[:,10]>1000,10] =np.nan
                    CO[i,tt-8] = stn[i,5]
                    SO2[i,tt-8] = stn[i,6]
                    O3[i,tt-8] = stn[i,7]
                    NO2[i,tt-8] = stn[i,8]
                    PM10[i,tt-8] =stn[i,9]
                    PM25[i,tt-8] =stn[i,10]
                    print (tt)
                except:
                    CO[i,tt-8] =np.nan
                    SO2[i,tt-8] =np.nan
                    O3[i,tt-8] =np.nan
                    NO2[i,tt-8] =np.nan
                    PM10[i,tt-8] =np.nan
                    PM25[i,tt-8] = np.nan                          
                    print (f'NO file in {doy:3.0f} (DOY) \n')
            print (i)
        
        SEM[:,0] = 3.291*np.nanstd(CO)/np.sqrt(CO.shape[1]) #to remove all those outside of the 99.9# confidence limits
        SEM[:,1] = 3.291*np.nanstd(SO2)/np.sqrt(SO2.shape[1]) #to remove all those outside of the 99.9# confidence limits
        SEM[:,2] = 3.291*np.nanstd(O3)/np.sqrt(O3.shape[1]) #to remove all those outside of the 99.9# confidence limits
        SEM[:,3] = 3.291*np.nanstd(NO2)/np.sqrt(NO2.shape[1]) #to remove all those outside of the 99.9# confidence limits
        SEM[:,4] = 3.291*np.nanstd(PM10)/np.sqrt(PM10.shape[1]) #to remove all those outside of the 99.9# confidence limits
        SEM[:,5] = 3.291*np.nanstd(PM25)/np.sqrt(PM25.shape[1]) #to remove all those outside of the 99.9# confidence limits
        conc_mean = np.concatenate([np.nanmean(CO,axis=1),np.nanmean(SO2,axis=1), np.nanmean(O3,axis=1), np.nanmean(NO2,axis=1),np.nanmean(PM10,axis=1),np.nanmean(PM25,axis=1)], axis=1)
        th[:,0] =SEM[:,0]+conc_mean[:,0]
        th[:,1] =SEM[:,1]+conc_mean[:,1]
        th[:,2] =SEM[:,2]+conc_mean[:,2]
        th[:,3] =SEM[:,3]+conc_mean[:,3]
        th[:,4] =SEM[:,4]+conc_mean[:,4]
        th[:,5] =SEM[:,5]+conc_mean[:,5]
        for ii in range(1497+1):
            CO[ii,CO[ii,:]>th[ii,0]]=np.nan
            SO2[ii,SO2[ii,:]>th[ii,1]]=np.nan
            O3[ii,O3[ii,:]>th[ii,2]]=np.nan
            NO2[ii,NO2[ii,:]>th[ii,3]]=np.nan
            PM10[ii,PM10[ii,:]>th[ii,4]]=np.nan
            PM25[ii,PM25[ii,:]>th[ii,5]]=np.nan
        
        try:
            stn_tt = []
            for tt2 in range(9,16+1):
                stn = ndata[ndata[:,0]==doy & ndata[:,4]==tt,:]
                stn[:,5:11] = np.hstack([PM25[:,tt2-8], PM10[:,tt2-8], SO2[:,tt-8], NO2[:,tt-8], O3[:,tt-8], CO[:,tt-8]])
                stn_tt = np.concatenate((stn_tt, stn), axis=0)           
        except:
            print (f'NO file in {doy:3.0f} (DOY) \n')
        print (doy)
        if stn_doy is None:
            stn_doy = stn_tt
        else:
            stn_doy = np.vstack([stn_doy, stn_tt])
    if stn_JP is None:
        stn_JP = stn_doy
    else:
        stn_JP = np.vstack([stn_JP, stn_doy])
    fname = f'stn_code_data_rm_outlier_{yr}.mat'
    matlab.savemat(os.path.join(path_station,'stn_code_data', fname), {'stn_JP':stn_JP})
    print (yr)