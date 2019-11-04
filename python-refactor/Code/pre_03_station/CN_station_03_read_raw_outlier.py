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
path = '/share/irisnas5/Data/Station/Station_CN/'
# addpath(genpath('/share/irisnas5/Data/matlab_func/'))

stn_info_cn = pd.read_csv(os.path.join(path_data,'Station/Station_CN/cn_stn_code_lonlat_period.csv'),header=1)
# scode1, scode2, lon, lat, op_start, op_

## read files 서희가 만든 china stn 파일 불러와서 년도별로 파일 묶기
# header_ndata = {'doy','yr','mon','day','CST','AQI','PM25','PM25_24h',
#     'PM10','PM10_24h','SO2','SO2_24h','NO2','NO2_24h','O3','O3_24h',
#     'O3_8h','O3_8h_24h','CO','CO_24h','scode'}
# 
# for yr=2015:2016
#     cd([path_data,'Station_CN/rm_outlier/',num2str(yr)])
#     list = dir('*.mat')
#     list = {list.name}'
#     
#     ndata = []
#     for k = 1:length(list)
#         load(list{k}) #stn_CN
#         ndata = [ndata; stn_CN]
#         print (list{k})
#     
#     matlab.savemat(os.path.join(path_data,'Station_CN/stn_code_data/stn_code_data_rm_outlier_',num2str(yr)],'ndata','header_ndata','-v7.3')
# 

# list15=dir('stn_code_data_rm_*2015*')
# list15={list15.name}'
# ndata = importdata(list15{1})
# for k=2:length(list15)
#     load(list15{k})
#     ndata=[ndata;stn_CN]
# 
# matlab.savemat(os.path.join(path_data,'Station_CN/stn_code_data/stn_code_data_rm_outlier_',num2str(yr)],'ndata','header_ndata','-v7.3')
# 
# list16=dir('stn_code_data_rm_*2016*')
# list16={list16.name}'
# ndata = importdata(list16{1})
# for k=2:length(list16)
#     load(list16{k})
#     ndata=[ndata;stn_CN]
# 
# matlab.savemat(os.path.join(path_data,'Station_CN/stn_code_data/stn_code_data_rm_outlier_',num2str(yr)],'ndata','header_ndata','-v7.3')

## stn_scode_data for China
header_ndata = ['doy','yr','mon','day','CST','AQI','PM25','PM25_24h',
    'PM10','PM10_24h','SO2','SO2_24h','NO2','NO2_24h','O3','O3_24h',
    'O3_8h','O3_8h_24h','CO','CO_24h','scode','scode2']

YEARS = [2016] # range(2015, 2019+1)
for yr in YEARS:
    fname = f'stn_code_data_rm_outlier_{yr}.mat'
    ndata=matlab.loadmat(os.path.join(path_data,'Station/Station_CN/stn_code_data/', fname))
    ndata[:,-1]=0

    ndata_scode = []
    # Assign scode2
    for j in range(1, stn_info_cn.shape[0]):
        ndata_temp = ndata[ndata[:,-1]==stn_info_cn[j,0],:]
        for k in range(1,5+1): 
            ndata_temp2 = ndata_temp[ndata_temp[:,2]==k,:]
            if np.all(ndata_temp2==0):
                yrmon = yr*100+k
                idx = (stn_info_cn[j,4]<=yrmon)&(stn_info_cn[j,5]>=yrmon)
                if idx==1:
                    ndata_temp2[:,]=stn_info_cn[j,1]
                    ndata_scode= np.concatenate((ndata_scode,ndata_temp2), axis=1)
                
            
        
        if (j%100)==0:
            fname = f'stn_scode_data_{yr}_{j-99:04d}.mat'
            matlab.savemat(path, fname, {'ndata_scode':ndata_scode})
            ndata_scode = []
        elif j==stn_info_cn.shape[0]:
            fname = f'stn_scode_data_{yr}_1501.mat'
            matlab.savemat(path, fname, {'ndata_scode':ndata_scode})
    
        print (f'{j} / {stn_info_cn.shape[0]}')


    ndata_scode = []
    for k in range(1, 1501+1, 100):
        fname = f'stn_scode_data_{yr}_{k:04d}.mat'
        ndata_scode_temp = matlab.loadmat(os.path.join(path, fname))
        ndata_scode = np.concatenate((ndata_scode, ndata_scode_temp), axis=1)

    fname = f'cn_stn_scode_data_rm_outlier_{yr}.mat'
    matlab.savemat(os.path.join(path,'stn_scode_data'), fname, {'ndata_scode':ndata_scode,'header_ndata':header_ndata})
    print (yr)

