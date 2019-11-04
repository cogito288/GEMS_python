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

# path_data = '//10.72.26.56/irisnas5/Data/'
path_data = '/share/irisnas5/Data/'
path = '/share/irisnas5/Data/Station/Station_JP/'
# addpath(genpath('/share/irisnas6/Work/Aerosol/matlab_func/'))

stn_info = pd.read_csv(os.path.join(path,'jp_stn_code_lonlat_period_filtered_yyyymmdd.csv'),header=1)
# scode1, scode2, lon, lat, op_start, op_

## read stn_code_data file
header_ndata = ['doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode','scode2']

yr=2019
fname = f'stn_code_data_rm_outlier_{yr}_rm.mat'
ndata = matlab.loadmat(os.path.join(path,'stn_code_data', fname))
# ndata(:,12:13)=[]; # O3, NOX
ndata[ndata==-9999]=np.nan

## stn_scode_data for Japan

ndata[:,12]=0 # add column for scode2

ndata_scode = []
# Assign scode2
for j in range(stn_info.shape[0]): 
    ndata_temp = ndata[ndata[:,11]==stn_info[j,0],:]
    for k in range(5): # 1:5 ############
        for dd in range(1,31+1): # 1:31
            ndata_temp2 = ndata_temp[ndata_temp[:,2]==k & ndata_temp[:,3]==dd,:]
            if np.all(ndata_temp2==0):
                yyyymmdd = yr*10000+k*100+dd
                idx = (stn_info[j,4] < yyyymmdd) & (stn_info[j,5] >= yyyymmdd)
                if idx==1:
                    ndata_temp2[:,]=stn_info[j,1]
                    ndata_scode=np.concatenate((ndata_scode,ndata_temp2), axis=0)
                
            
        
    
    if j%100==0:
        fname = f'stn_scode_data_{yr}_{j-99:04d}.mat'
        matlab.savemat(path, fname, {'ndata_scode':ndata_scode})
        ndata_scode = []
    elif j==stn_info.shape[0]:
        fname = f'stn_scode_data_{yr}_2401.mat'
        matlab.savemat(path, fname, {'ndata_scode':ndata_scode})
    
    print (f'{j} / {stn_info.shape[0]}')


ndata_scode = []
for k in range(1, 2401+1, 100): 
    fname = os.path.join(path,'stn_scode_data_{yr}_{k:04d}.mat'
    ndata_scode_temp = matlab.loadmat(fname)
    ndata_scode = np.concatenate((ndata_scode, ndata_scode_temp), axis=0)

fname = f'jp_stn_scode_data_rm_outlier_{yr}.mat'
matlab.savemat(path, fname, {'ndata_scode':ndata_scode,'header_ndata':header_ndata})

for k in range(1, 2401+1, 100): 
    fname = os.path.join(path,'stn_scode_data_{yr}_{k:04d}.mat'
    os.remove(fname)  #delete(fname)

## stack
# yr=2009
# for k=1401:1416
#     ndata_scode(ndata_scode(:,13)==stn_info(k,2),:)=[]
# 
# ndata_scode_all=ndata_scode
# matlab.savemat(os.path.join(path_data,'Station_JP/stn_scode_data_',num2str(yr),'_1_1400'],'ndata_scode_all','header_ndata','-v7.3')
# matlab.loadmat(os.path.join(path_data,'Station_JP/stn_scode_data_',num2str(yr),'_1_1400'])
# matlab.loadmat(os.path.join(path_data,'Station_JP/stn_scode_data_',num2str(yr),'_1401_1700'])
# ndata_scode_all = [ndata_scode_all;ndata_scode]
# matlab.loadmat(os.path.join(path_data,'Station_JP/stn_scode_data_',num2str(yr),'_1701_2000'])
# ndata_scode_all = [ndata_scode_all;ndata_scode]
# matlab.loadmat(os.path.join(path_data,'Station_JP/stn_scode_data_',num2str(yr),'_2001_'])
# ndata_scode_all = [ndata_scode_all;ndata_scode]
# ndata_scode=ndata_scode_all
# matlab.savemat(os.path.join(path_data,'Station_JP/stn_scode_data_',num2str(yr)],'ndata_scode','header_ndata','-v7.3')
