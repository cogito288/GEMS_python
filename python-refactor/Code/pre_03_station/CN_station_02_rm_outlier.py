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
import time

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 

YEARS = [2016] # range(2015, 2019+1)
for yr in YEARS:
    if yr%4==0: days= 366; 
    else: days=365; 
    if yr==2019: days=151;
    
    ndata = matlab.loadmat(os.path.join(path_station, 'Station_CN', 'stn_code_data', f'stn_code_data_{yr}.mat'))['stn_doy']
    scode = np.unique(ndata[:,-1])
    # CO
    ndata[:,18]=ndata[:,18]/1.15 # (mg/m3) to ppm (1 ppm = 1.15 mg m-3)
    ndata[ndata[:,18]>20,18]= np.nan
    # SO2 
    ndata[:,10]=ndata[:,10]/2.62; # (?g/m3) to ppb (1 ppb = 2.62 ?g m-3)
    ndata[ndata[:,10]>400,10]=np.nan
    # NO2
    ndata[:,12]=ndata[:,12]/1.88; # (?g/m3) to ppb (1 ppb = 1.88 ?g m-3)
    ndata[ndata[:,12]>400,12]=np.nan
    # O3
    ndata[:,14]=ndata[:,14]/1.96; # (?g/m3) to ppb (1 ppb = 1.96 ?g m-3)
    ndata[ndata[:,14]>400,14]=np.nan
    # PM25 (ug/m3)
    ndata[ndata[:,6]>600,6]=np.nan
    # PM10 (ug/m3)
    ndata[ndata[:,8]>1000,8]=np.nan
    ndata = ndata[~((ndata[:,4]<8) | (ndata[:,4]>15))]
    
    ind = np.lexsort((ndata[:,20],ndata[:,4],ndata[:,0]))    # sort 20->4->0. 0 is primary
    ndata = ndata[ind]
    
    stn_CN = None
    for doy in range(1,days+1):
        tStart_doy = time.time()
        ndata_temp = ndata[ndata[:,0]==doy,:]
        scode_temp = np.unique(ndata_temp[:,-1])
        nstn_temp = scode_temp.shape[0]
        if (ndata_temp.shape[0]%nstn_temp==0) and (ndata_temp.shape[0]>=(nstn_temp*4)):
            CO = ndata_temp[:, 18].reshape((nstn_temp, -1), order='F')
            SO2 = ndata_temp[:,10].reshape((nstn_temp, -1), order='F')
            O3 = ndata_temp[:,14].reshape((nstn_temp, -1), order='F')
            NO2 = ndata_temp[:,12].reshape((nstn_temp, -1), order='F')
            PM10 = ndata_temp[:,8].reshape((nstn_temp, -1), order='F')
            PM25 = ndata_temp[:,6].reshape((nstn_temp, -1), order='F')

            nanidx = np.full((nstn_temp,6), np.nan)
            nanidx[:,0] = np.sum(np.isnan(CO), axis=1)>4
            nanidx[:,1] = np.sum(np.isnan(SO2), axis=1)>4
            nanidx[:,2] = np.sum(np.isnan(O3), axis=1)>4
            nanidx[:,3] = np.sum(np.isnan(NO2),axis=1)>4
            nanidx[:,4] = np.sum(np.isnan(PM10),axis=1)>4
            nanidx[:,5] = np.sum(np.isnan(PM25),axis=1)>4

            SEM = np.full((nstn_temp,6), np.nan)
            th = np.full((nstn_temp,6), np.nan)

            SEM[:,0] = 3.291*np.nanstd(CO.T, axis=0, ddof=1).T/np.sqrt(CO.shape[1]) #to remove all those outside of the 99.9# confidence limits
            SEM[:,1] = 3.291*np.nanstd(SO2.T, axis=0, ddof=1).T/np.sqrt(SO2.shape[1]) #to remove all those outside of the 99.9# confidence limits
            SEM[:,2] = 3.291*np.nanstd(O3.T, axis=0, ddof=1).T/np.sqrt(O3.shape[1]) #to remove all those outside of the 99.9# confidence limits
            SEM[:,3] = 3.291*np.nanstd(NO2.T, axis=0, ddof=1).T/np.sqrt(NO2.shape[1]) #to remove all those outside of the 99.9# confidence limits
            SEM[:,4] = 3.291*np.nanstd(PM10.T, axis=0, ddof=1).T/np.sqrt(PM10.shape[1]) #to remove all those outside of the 99.9# confidence limits
            SEM[:,5] = 3.291*np.nanstd(PM25.T, axis=0, ddof=1).T/np.sqrt(PM25.shape[1]) #to remove all those outside of the 99.9# confidence limits
            conc_mean = np.vstack([np.nanmean(CO,axis=1), np.nanmean(SO2,axis=1), np.nanmean(O3,axis=1), np.nanmean(NO2,axis=1), np.nanmean(PM10,axis=1), np.nanmean(PM25,axis=1)]).T
            th[:,0] =SEM[:,0]+conc_mean[:,0]
            th[:,1] =SEM[:,1]+conc_mean[:,1]
            th[:,2] =SEM[:,2]+conc_mean[:,2]
            th[:,3] =SEM[:,3]+conc_mean[:,3]
            th[:,4] =SEM[:,4]+conc_mean[:,4]
            th[:,5] =SEM[:,5]+conc_mean[:,5]

            nTime = CO.shape[1]
            diff1 = CO - np.tile(th[:,0][:, None],(1,nTime))
            diff2 = SO2 - np.tile(th[:,1][:, None],(1,nTime))
            diff3 = O3 - np.tile(th[:,2][:, None],(1,nTime))
            diff4 = NO2 - np.tile(th[:,3][:, None],(1,nTime))
            diff5 = PM10 - np.tile(th[:,4][:, None],(1,nTime))
            diff6 = PM25 - np.tile(th[:,5][:, None],(1,nTime))

            CO[diff1>0]=np.nan
            SO2[diff2>0]=np.nan
            O3[diff3>0]=np.nan
            NO2[diff4>0]=np.nan
            PM10[diff5>0]=np.nan
            PM25[diff6>0]=np.nan

            CO[nanidx[:,0]==1,:]=np.nan
            SO2[nanidx[:,1]==1,:]=np.nan
            O3[nanidx[:,2]==1,:]=np.nan
            NO2[nanidx[:,3]==1,:]=np.nan
            PM10[nanidx[:,4]==1,:]=np.nan
            PM25[nanidx[:,5]==1,:]=np.nan

            ndata_temp[:,[6,8,10,12,14,18]]=np.vstack([PM25.ravel(order='F'),PM10.ravel(order='F'),SO2.ravel(order='F'),NO2.ravel(order='F'),O3.ravel(order='F'),CO.ravel(order='F')]).T
            if stn_CN is None:
                stn_CN = ndata_temp
            else:
                stn_CN = np.vstack([stn_CN, ndata_temp])

            tElapsed_doy = time.time()-tStart_doy
            print (f'{yr}_{doy}--{tElapsed_doy:3.4f} sec')
        else:
            print ('Less than 4 hourly data in {doy:03d} (DOY) \n')
    fname = f'stn_code_data_rm_outlier_{yr}.mat'
    matlab.savemat(os.path.join(path_station, 'Station_CN', 'stn_code_data',fname), {'stn_CN':stn_CN})
    print (yr)