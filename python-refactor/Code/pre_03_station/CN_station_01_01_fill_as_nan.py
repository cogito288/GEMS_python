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
data_base_dir = os.path.join(project_path, 'Data')
raw_path = os.path.join(data_base_dir, 'Raw') 
station_path = os.path.join(data_base_dir, 'Station') 

# % scode1, scode2, lon, lat, op_start, op_end
stn_info_cn = pd.read_csv(os.path.join(station_path, 'Station_CN', 'cn_stn_code_lonlat_period.csv', header=1)

#%% read files 서희가 만든 china stn 파일 불러와서 빈 날짜 시간 nan으로 채우기
header_ndata = ['doy','yr','mon','day','CST','AQI','PM25','PM25_24h',
     'PM10','PM10_24h','SO2','SO2_24h','NO2','NO2_24h','O3','O3_24h',
     'O3_8h','O3_8h_24h','CO','CO_24h','scode']
                          
yr = 2015
ndata = matlab.loadmat(os.path.join(station_path, 'Station_CN', 'stn_code_data', f'stn_code_data_rm_outlier_{yr}.mat'))['ndata']
unq_doy = np.unique(ndata[:,0]) # % 1, 262, 비었음
unq_scode = np.unique(ndata[:,20])
aa = np.full((len(unq_scode), 21), np.nan)
aa[:,1]=yr
aa[:,20]=unq_scode


#% doy1
aa1 = aa
aa1[:,0]=1
aa1[:,2:4]=1
for i, CST in enumerate(range(8, 15+1)):
    aa1_temp = aa1
    aa1_temp[:,4]=CST
    if i==0:
        ndata_doy1 = aa1_temp
    else:
        ndata_doy1=np.concatenate((ndata_doy1, aa1_temp), axis=0)

#% doy 262
aa2=aa
aa2[:,0]=262
aa2[:,2]=9
aa2[:,3]=19
ndata_doy262=[]
temp_tbl = pd.read.csv(os.path.join(raw_path, 'AirQuality_China', 'china_sites', str(yr), 'china_sites_20150919.csv'))
scode_char = temp_tbl.columns[3:] 
scode_num = [float(x[1:5]) for x in scode_char] 
aa2[:,20] = scode_num

cols = temp_tbl.columns
temp = temp_tbl[[cols[1]]+cols[4:]] #temp=table2array(temp_tbl(:,[2,4:]))
temp_cols = temp.columns
for i, CST in enumerate(range(8, 15+1)):
    aa2_temp = aa2
    aa2_temp[:,4]=CST
    
    temp2 = temp[temp[temp_cols[0]]==CST][temp_cols[1:]]
    
    if not temp2.empty:
        aa2_temp[:,5:20]=temp2
    if i==0:
        ndata_doy262 = aa2_temp
    else:
        ndata_doy262 = np.concatenate((ndata_doy262, aa2_temp), axis=0)

ndata_1 = ndata[ndata[:,0]<262,:]
ndata_2 = ndata[ndata[:,0]>262,:]
ndata = np.concatenate((ndata_doy1, ndata_1, ndata_doy262, ndata_2), axis=0)

list16 = glob.glob('stn_code_data_rm_*2016*')
ndata = pd.read_csv(list16[0])
for k in range(1, len(list16)):
    stn_CN = matlab.loadmat(list16[k])['stn_CN']
    ndata=np.concatenate((ndata,stn_CN), axis=0)

matlab.savemat(os.path.join(station_path,'Station_CN', 'stn_code_data', f'stn_code_data_rm_outlier_{yr}.mat'), {'ndata':ndata,'header_ndata':header_ndata})