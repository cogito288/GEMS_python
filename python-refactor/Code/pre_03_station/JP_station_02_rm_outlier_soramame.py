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

### Setting path
data_base_dir = os.path.join('/', 'media', 'sf_GEMS_1', 'Data')
raw_data_path = os.path.join(data_base_dir, 'Raw', 'GOCI_AOD') 
write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_AOD')
# path = '//10.72.26.56/irisnas5/Data/Station/Station_JP/'
# addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'))
path = '/share/irisnas5/Data/Station/Station_JP/'
#addpath(genpath('/share/irisnas5/Data/matlab_func/'))

## header
# station_header
header = ['doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode']

##
YEARS = range(2017, 2019+1)
for yr in YEARS:
    if yr%4==0: days= 366; else: days=365; 
    if yr==2019: days=151; 
        
    fname = f'stn_code_data_{yr}.mat'
    mat = matlab.loadmat(os.path.join(path, 'stn_code_data', fname))
    stn_yr = mat['stn_yr']
    ndata = stn_yr
    scode = np.unique(ndata[:,])

    ndata_org = ndata
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
    ndata[ndata[:,11]>600,11]=np.nan 
    
    ndata[ndata[:,4]<9 | ndata[:,4]>16,:]=[] ########
    ndata = matlab.sortrows(ndata,[1,5,12])
    
    stn_JP = []
    for doy in range(1,days+1):
        tStart_doy = time.time()
        ndata_temp = ndata[ndata[:,0]==doy,:]
        scode_temp = np.unique(ndata_temp[:,])
        nstn_temp = scode_temp.shape[0]
        if (ndata_temp.shape[0]%nstn_temp)==0 && (ndata_temp.shape[0]>=(nstn_temp*4)):
            SO2 = ndata_temp[:, 5].reshape((nstn_temp, -1))
            CO = ndata_temp[:, 6].reshape((nstn_temp, -1))
            OX = ndata_temp[:, 7].reshape((nstn_temp, -1))
            NO2 = ndata_temp[:, 8].reshape((nstn_temp, -1))
            PM10 = ndata_temp[:, 9].reshape((nstn_temp, -1))
            PM25 = ndata_temp[:, 10].reshape((nstn_temp, -1))
            
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
            SEM[:,0] = 3.291*np.nanstd(CO)/np.sqrt(CO.shape[1])) #to remove all those outside of the 99.9# confidence limits
            SEM[:,1] = 3.291*np.nanstd(SO2)/np.sqrt(SO2.shape[1])) #to remove all those outside of the 99.9# confidence limits
            SEM[:,2] = 3.291*np.nanstd(O3)/np.sqrt(O3.shape[1])) #to remove all those outside of the 99.9# confidence limits
            SEM[:,3] = 3.291*np.nanstd(NO2)/np.sqrt(NO2.shape[1])) #to remove all those outside of the 99.9# confidence limits
            SEM[:,4] = 3.291*np.nanstd(PM10)/np.sqrt(PM10.shape[1])) #to remove all those outside of the 99.9# confidence limits
            SEM[:,5] = 3.291*np.nanstd(PM25)/np.sqrt(PM25.shape[1])) #to remove all those outside of the 99.9# confidence limits

            conc_mean = [np.nanmean(CO,axis=1),np.nanmean(SO2,axis=1), np.nanmean(O3,axis=1), np.nanmean(NO2,axis=1),np.nanmean(PM10,axis=1),np.nanmean(PM25,axis=1)]
            th[:,0] =SEM[:,0]+conc_mean[:,0]
            th[:,1] =SEM[:,1]+conc_mean[:,1]
            th[:,2] =SEM[:,2]+conc_mean[:,2]
            th[:,3] =SEM[:,3]+conc_mean[:,3]
            th[:,4] =SEM[:,4]+conc_mean[:,4]
            th[:,5] =SEM[:,5]+conc_mean[:,5]
            
            nTime = SO2.shape[1] 
            
            diff1 = SO2 - matlab.repmat(th[:,0],(1,nTime))
            diff2 = CO - matlab.repmat(th[:,1],(1,nTime))
            diff3 = OX - matlab.repmat(th[:,2],(1,nTime))
            diff4 = NO2 - matlab.repmat(th[:,3],(1,nTime))
            diff5 = PM10 - matlab.repmat(th[:,4],(1,nTime))
            diff6 = PM25 - matlab.repmat(th[:,5],(1,nTime))
            
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
            
            allvar = np.concatenate((SO2.flatten(),CO.flatten(),OX.flatten(),NO2.flatten(),PM10.flatten(),PM25.flatten()), axis=1) ##
            nanidx_allvar = np.sum(np.isnan(allvar),axis=1)==6 ##
            
            ndata_temp[:,5:11]=allvar
            ndata_temp[nanidx_allvar==1,:]=[] ##
            stn_JP = np.concatenate((stn_JP, ndata_temp), axis=0)
            
            tElapsed_doy = time.time() - tStart_doy
            print (f'{yr}_{doy} -- {tElapsed_doy:3.4f} sec')
        else
            print (f'Less than 4 hourly data in {doy:03d} (DOY) \n')
        
        
    fname = f'stn_code_data_rm_outlier_{yr}_rm.mat''
    matlab.savemat(os.path.join(path,'stn_code_data'), fname, {'stn_JP':stn_JP})
    print (yr)

