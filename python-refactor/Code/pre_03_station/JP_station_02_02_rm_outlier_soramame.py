### Package Import
import sys
import os
#base_dir = os.environ['GEMS_HOME']
base_dir = 'D:\github\GEMS_python'
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import copy
import numpy as np
import pandas as pd
import glob
import time

### Setting path
#data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
data_base_dir = os.path.join('//', '10.72.26.56','irisnas5', 'GEMS', 'GEMS_python')
#data_base_dir = os.path.join('/', 'share', 'irisnas5', 'GEMS', 'GEMS_python')
path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')

## header
# station_header
header = ['doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode']

##
YEARS = [2017]
for yr in YEARS:
    if yr%4==0: days= 366; 
    else: days=365; 
    #if yr==2019: days=151; 
        
    ndata = matlab.loadmat(os.path.join(path_stn_jp, 'stn_code_data', f'stn_code_data_{yr}_soramame.mat'))['stn_yr']
    ndata = ndata.astype('float')
    scode = np.unique(ndata[:,-1])

    # SO2
    ndata[:,5]=ndata[:,5]*1000; # ppm to ppb
    ndata[ndata[:,5]>400,5]=np.nan 
    # CO
    ndata[:,6]=ndata[:,6]*10; # ppm to 0.1ppm
    ndata[ndata[:,6]>200,6]=np.nan
    # OX
    ndata[:,7]=ndata[:,7]*1000; # ppm to ppb
    ndata[ndata[:,7]>400,7]=np.nan
    # NO2
    ndata[:,8]=ndata[:,8]*1000; # ppm to ppb
    ndata[ndata[:,8]>400,8]=np.nan
    # PM10
    ndata[:,9]=ndata[:,9]*1000; # [mg/m3] to [ug/m3]
    ndata[ndata[:,9]>1000,9]=np.nan 
    # PM25
    # [ug/m3]
    ndata[ndata[:,10]>600,10]=np.nan 
    
    ndata = ndata[~((ndata[:,4]<9) | (ndata[:,4]>16))]
    ind = np.lexsort((ndata[:,11],ndata[:,4], ndata[:,0]))    
    ndata = ndata[ind]
    
    stn_JP = None
    for doy in range(1,days+1):
        tStart_doy = time.time()
        ndata_temp = ndata[ndata[:,0]==doy,:]
        scode_temp = np.unique(ndata_temp[:,-1])
        nstn_temp = scode_temp.shape[0]
        if ((ndata_temp.shape[0]%nstn_temp)==0) and (ndata_temp.shape[0]>=(nstn_temp*4)):
            SO2 = ndata_temp[:, 5].reshape((nstn_temp, -1), order='F')
            CO = ndata_temp[:, 6].reshape((nstn_temp, -1), order='F')
            OX = ndata_temp[:, 7].reshape((nstn_temp, -1), order='F')
            NO2 = ndata_temp[:, 8].reshape((nstn_temp, -1), order='F')
            PM10 = ndata_temp[:, 9].reshape((nstn_temp, -1), order='F')
            PM25 = ndata_temp[:, 10].reshape((nstn_temp, -1), order='F')
            
            nanidx = np.full((nstn_temp,6), np.nan)
            nanidx[:,0] = np.sum(np.isnan(SO2),axis=1)>4
            nanidx[:,1] = np.sum(np.isnan(CO),axis=1)>4 
            nanidx[:,2] = np.sum(np.isnan(OX),axis=1)>4 
            nanidx[:,3] = np.sum(np.isnan(NO2),axis=1)>4 
            nanidx[:,4] = np.sum(np.isnan(PM10),axis=1)>4
            nanidx[:,5] = np.sum(np.isnan(PM25),axis=1)>4
            
            SEM = np.full((nstn_temp,6), np.nan)
            th = np.full((nstn_temp,6), np.nan)
            
            # Same with Japan_stn_outlier and CN_station_02_rm_outlier
            SEM[:,0] = 3.291*np.nanstd(SO2.T, axis=0, ddof=1)/np.sqrt(SO2.shape[1]) #to remove all those outside of the 99.9# confidence limits
            SEM[:,1] = 3.291*np.nanstd(CO.T, axis=0, ddof=1)/np.sqrt(CO.shape[1]) #to remove all those outside of the 99.9# confidence limits
            SEM[:,2] = 3.291*np.nanstd(OX.T, axis=0, ddof=1)/np.sqrt(OX.shape[1]) #to remove all those outside of the 99.9# confidence limits
            SEM[:,3] = 3.291*np.nanstd(NO2.T, axis=0, ddof=1)/np.sqrt(NO2.shape[1]) #to remove all those outside of the 99.9# confidence limits
            SEM[:,4] = 3.291*np.nanstd(PM10.T, axis=0, ddof=1)/np.sqrt(PM10.shape[1]) #to remove all those outside of the 99.9# confidence limits
            SEM[:,5] = 3.291*np.nanstd(PM25.T, axis=0, ddof=1)/np.sqrt(PM25.shape[1]) #to remove all those outside of the 99.9# confidence limits

            conc_mean = np.vstack([np.nanmean(SO2,axis=1), np.nanmean(CO,axis=1), np.nanmean(OX,axis=1), np.nanmean(NO2,axis=1), np.nanmean(PM10,axis=1), np.nanmean(PM25,axis=1)]).T
            th[:,0] =SEM[:,0]+conc_mean[:,0]
            th[:,1] =SEM[:,1]+conc_mean[:,1]
            th[:,2] =SEM[:,2]+conc_mean[:,2]
            th[:,3] =SEM[:,3]+conc_mean[:,3]
            th[:,4] =SEM[:,4]+conc_mean[:,4]
            th[:,5] =SEM[:,5]+conc_mean[:,5]
            
            nTime = SO2.shape[1] 
            diff1 = SO2 - np.tile(th[:,0][:, None],(1,nTime))
            diff2 = CO - np.tile(th[:,1][:, None],(1,nTime))
            diff3 = OX - np.tile(th[:,2][:, None],(1,nTime))
            diff4 = NO2 - np.tile(th[:,3][:, None],(1,nTime))
            diff5 = PM10 - np.tile(th[:,4][:, None],(1,nTime))
            diff6 = PM25 - np.tile(th[:,5][:, None],(1,nTime))
            
            SO2[diff1>0]=np.nan
            CO[diff2>0]=np.nan
            OX[diff3>0]=np.nan
            NO2[diff4>0]=np.nan
            PM10[diff5>0]=np.nan
            PM25[diff6>0]=np.nan

            SO2[nanidx[:,0]==1,:]=np.nan
            CO[nanidx[:,1]==1,:]=np.nan
            OX[nanidx[:,2]==1,:]=np.nan
            NO2[nanidx[:,3]==1,:]=np.nan
            PM10[nanidx[:,4]==1,:]=np.nan
            PM25[nanidx[:,5]==1,:]=np.nan
            
            allvar = np.vstack([SO2.ravel(order='F'),CO.ravel(order='F'),OX.ravel(order='F'),NO2.ravel(order='F'),PM10.ravel(order='F'),PM25.ravel(order='F')]).T
            nanidx_allvar = np.sum(np.isnan(allvar),axis=1)==6 
            
            ndata_temp[:,5:11]=allvar
            ndata_temp = ndata_temp[~(nanidx_allvar==1)]
            if stn_JP is None:
                stn_JP = ndata_temp
            else:
                stn_JP = np.vstack([stn_JP, ndata_temp])
            
            tElapsed_doy = time.time() - tStart_doy
            print (f'{yr}_{doy} -- {tElapsed_doy:3.4f} sec')
        else:
            print (f'Less than 4 hourly data in {doy:03d} (DOY) \n')   
    matlab.savemat(os.path.join(path_stn_jp,'stn_code_data', f'stn_code_data_rm_outlier_{yr}_rm.mat'), {'stn_JP':stn_JP})
    print (yr)
    
