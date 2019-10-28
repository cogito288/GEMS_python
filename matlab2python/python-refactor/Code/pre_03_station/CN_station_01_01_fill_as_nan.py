##################### Start of File ##################### clear all;  clc
import os
import sys
project_path = '/home/cogito/Desktop/GEMS_python/matlab2python/python-refactor'
sys.path.insert(0, project_path)

from Code.utils import matlab

import numpy as np
#from matplotlib.pyplot import imread
from scipy.interploate import griddata
import time
import pandas as pd
import glob

#% path_data = '//10.72.26.56/irisnas5/Data/';
#% addpath(genpath('/share/irisnas5/Data/matlab_func/'))


#path_data = '//10.72.26.46/irisnas6/Data/Aerosol/';
#path = '//10.72.26.46/irisnas6/Work/Aerosol/';
path_data = os.path.join('/', 'share', 'irisnas6', 'Data', 'Aerosol')
path = os.path.join('/', 'share', 'irisnas6', 'Work', 'Aerosol')
#% addpath(genpath('/share/irisnas6/Work/Aerosol/matlab_func/'))
tmp_df = pd.read_csv(os.path.join(path_data. 'Station_CN', 'cn_stn_code_lonlat_period.csv', header=1)
stn_info_cn = tmp_df.values
#stn_info_cn = csvread([path_data,'Station_CN/cn_stn_code_lonlat_period.csv'],1);

#% scode1, scode2, lon, lat, op_start, op_end
#%% read files 서희가 만든 china stn 파일 불러와서 빈 날짜 시간 nan으로 채우기
#% header_ndata = {'doy','yr','mon','day','CST','AQI','PM25','PM25_24h',...
#%     'PM10','PM10_24h','SO2','SO2_24h','NO2','NO2_24h','O3','O3_24h',...
#%     'O3_8h','O3_8h_24h','CO','CO_24h','scode'};

yr = 2015
ndata = matlab.loadmat(os.path.join(path_data,'Station_CN/stn_code_data/',f'stn_code_data_rm_outlier_{yr}.mat'))
unq_doy = np.unique(ndata[:,0] # % 1, 262, 비었음
unq_scode = np.unique(ndata[:,20])
aa = np.full((matlab.length(unq_scode), 21), np.nan)
aa[:,1]=yr
aa[:,20]=unq_scode


#% doy1
aa1=aa
aa1[:,[0,2:3]]=1
ndata_doy1=[]
for CST in range(8, 15+1):
    aa1_temp = aa1
    aa1_temp[:,4]=CST
    ndata_doy1=np.concatenate((ndata_doy1, aa1_temp), axis=0)

#% doy 262
aa2=aa
aa2[:,0]=262
aa2[:,2]=9
aa2[:,3]=19
ndata_doy262=[]
temp_tbl = pd.read.csv(os.path.join('Z:\In_situ\AirQuality_China\china_sites\2015/china_sites_20150919.csv'))
scode_char = temp_tbl.columns[3:] #temp_tbl.Properties.VariableNames(4:end)';
scode_num = [float(x[1:5]) for x in scode_char] # map(lambda x:
aa2[:,20] = scode_num

temp = temp_tbl[list(temp_tbl.columns[1])+list(temp_tbl.columns[3:])].values #temp=table2array(temp_tbl(:,[2,4:]))
for CST in range(8, 15+1):
    aa2_temp = aa2
    aa2_temp[:,4]=CST
    
    temp2 = temp[temp[:,0]==CST,1:]
    temp2 = temp2
    
    if np.all(temp2==0): #isempty(temp2)==0
        aa2_temp[:,5:20]=temp2

    ndata_doy262 = np.concatenate((ndata_doy262, aa2_temp), axis=0)

ndata_1 = ndata[ndata[:,0]<262,:]
ndata_2 = ndata[ndata[:,0]>262,:]
ndata = np.concatenate((ndata_doy1, ndata_1, ndata_doy262, ndata_2), axis=0)

# temp = csvread([path_data,'Station_CN/temp262.csv'],1)

list16=glob.glob('stn_code_data_rm_*2016*')
ndata = pd.read_csv(list16[0])
for k in range(1, len(list16)):
    matlab.loadmat(list16[k])
    ndata=np.concatenate((ndata,stn_CN), axis=0)

matlab.savemat(os.path.join(path_data,'Station_CN/stn_code_data'), f'stn_code_data_rm_outlier_{yr}.mat', {'ndata':ndata,'header_ndata':header_ndata})
##################### End of File ##################### 