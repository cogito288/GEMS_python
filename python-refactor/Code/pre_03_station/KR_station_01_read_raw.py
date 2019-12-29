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
path_insiu = os.path.join(data_base_dir, 'Raw', 'AirQuality_SouthKorea')

## 2005-2013 (xlsx, PM2.5없음)
YEARS = range(2005, 2013+1)
for yr in YEARS:
    data = None
    for i in range(1, 4+1):
        fname = f'{yr}년{i:02d}분기.xlsx'
        tmp_df = pd.read_excel(os.path.join(path_insiu,str(yr), fname))
        text_cols = [col if tmp_df[col].dtype.name=='object' for col in tmp_df.columns]
        txt = tmp_df[text_cols]
        data_temp = txt.roc[:,text_cols[2:9]]
        if data is None:
            data = data_temp
        else:
            data = pd.concat([data, data_temp])
        del tmp_df, data_temp
    dvec = pd.to_datetime(data[:,1], format='%Y%m%d%H') #    dvec = datevec(data(:,2),'yyyymmddHH')
    data_datenum = matlab.datenum(data[:,1]) # 'yyyymmddHH'
    doy_000 = matlab.datenum(f'{yr}00000')
    data_doy = np.floor(data_datenum-doy_000)

    data = data.astype('float64')
    data[data<0]=np.nan

    ndata = np.hstack([data_doy,dvec(:,1:4),data(:,3:),np.full(data_doy.shape, np.nan),data(:,1)])
    # doy, yr, mon, day, time, SO2, CO, O3, NO2, PM10, (PM25), scode
    matlab.savemat(os.path.join(data_base_dir, 'Station/Station_Korea', 'stn_code_data', f'stn_code_data_{yr}.mat'),
                   {'ndata':ndata})

## 2014-2016 (csv, PM2.5 컬럼 있음)
YEARS = range(2014, 2016+1)
for yr in YEARS:
    data = None
    for i in range(1, 4+1):
        fname = f'{yr}년{i:02d}분기.xlsx'
        tmp_df = pd.read_excel(os.path.join(path_insiu,str(yr), fname))
        data_temp = tmp_df.roc[:,[tmp_df.columns[1]+tmp_df.columns[3:10]]
        if data is None:
            data = data_temp
        else:
            data = pd.concat([data, data_temp])
        del tmp_df, data_temp
    data = data.values
    data[data<0]=np.nan

    dstr = [str(x) for x in data[:,1]]
    dvec = pd.to_datetime(dstr,format='%Y%m%d%H')
    data_datenum = matlab.datenum(dstr)
    doy_000 = matlab.datenum(f'{yr}00000')
    data_doy = np.floor(data_datenum-doy_000)
    ndata = np.hstack([data_doy,dvec[:,:4],data[:,2:],data[:,0]])
    # doy, yr, mon, day, time, SO2, CO, O3, NO2, PM10, (PM25), scode
    matlab.savemat(os.path.join(data_base_dir,'Station_KR','stn_code_data',f'stn_code_data_{yr}.mat'), 
                   {'ndata':ndata})

## 2017-2018 2분기 (xlsx, PM2.5 있음)
YEARS = [2018]
for yr in YEARS:
    data = None
    for i in range(1, 4+1):
        fname = f'{yr}년{i:02d}분기.xlsx'
        tmp_df = pd.read_excel(os.path.join(path_insiu,str(yr), fname))
        data_temp = tmp_df.roc[:,[tmp_df.columns[1]+tmp_df.columns[3:10]]
        if data is None:
            data = data_temp
        else:
            data = pd.concat([data, data_temp])
        del tmp_df, data_temp
    data = data.values
    data_1 = np.float64(data[:, 0])
    data_2 = data[:, data.columns[1:]].values
    data = np.hstack([data_1, data_2])
    data[data<0]=np.nan

    dstr = [str(x) for x in data[:,2]]
    dvec = pd.to_datetime(dstr,format='%Y%m%d%H')
    data_datenum = matlab.datenum(dstr)
    doy_000 = matlab.datenum(f'{yr}00000')
    data_doy = np.floor(data_datenum-doy_000)
    ndata = np.hstack([data_doy,dvec[:,:4],data[:,2:],data[:,0]])
    # doy, yr, mon, day, time, SO2, CO, O3, NO2, PM10, (PM25), scode
    matlab.savemat(os.path.join(data_base_dir,'Station_KR','stn_code_data', f'stn_code_data_{yr}.mat'), 
                   {'ndata':ndata})

## 2018 3분기 - 4분기 (xlsx, PM2.5있음.. 근데 중간에 망 정보가 들어가면서 컬럼 위치가 변경됨)
i=4
fname = f'{yr}년{i:02d}분기.xlsx'
tmp_df = pd.read_excel(os.path.join(path_insiu, str(yr), fname))
data_temp = tmp_df.roc[:,[tmp_df.columns[2]]+tmp_df.columns[4:11]]
data = pd.concat([data, data_temp])

## 201810_201904 
data = None
tmp_df = pd.read_excel(os.path.join(path_insiu,'201810_201904', '201810_201904_pt1.csv'))
cols = [tmp_df.columns[1]]+tmp_df.columns[5:7]+[tmp_df.columns[9]]+[tmp_df.columns[8]]+[tmp_df.columns[10]]+[tmp_df.columns[11]]
data_temp = tmp_df.roc[:,cols]
data = pd.concat([data, data_temp])

tmp_df = pd.read_excel(os.path.join(path_insiu,'201810_201904', '201810_201904_pt2.csv'))
cols = [tmp_df.columns[1]]+tmp_df.columns[5:7]+[tmp_df.columns[9]]+[tmp_df.columns[8]]+[tmp_df.columns[10]]+[tmp_df.columns[11]]
data_temp = tmp_df.roc[:,cols]
data = pd.concat([data, data_temp], axis=0)

data = data.values
data[data<0]=np.nan

dstr = [str(x) for x in data[:,1]]
dvec = pd.to_datetime(dstr,format='%Y%m%d%H')
yr=2019
yr_idx = (dvec[:,0]==yr)
dvec=dvec[yr_idx,:]
dstr=dstr[yr_idx,:]
data=data[yr_idx,:]
data_datenum = matlab.datenum(dstr) 

doy_000 = datenum(f'{yr}00000')
data_doy = np.floor(data_datenum-doy_000)

ndata = np.hstack([data_doy,dvec[:,:4],data[:,2:],data[:,0]])
# doy, yr, mon, day, time, SO2, CO, O3, NO2, PM10, (PM25), scode

fname = f'stn_code_data_{yr}.mat'
matlab.savemat(os.path.join(data_base_dir,'Station_KR','stn_code_data', fname), 
               {'ndata':ndata})

## 12월 31일 24시 -> 1월 1일 00시 
#path = '/share/irisnas5/Data/Station/Station_Korea/'

yr=2005
fname = f'stn_code_data_{yr}.mat'
matlab.loadmat(os.path.join(data_base_dir,'Station_KR','stn_code_data', fname))
data_mv = ndata[ndata[:,1]==(yr+1),:]
doy_unq = np.unique(data_mv[:,0])

# if length(doy_unq)==1
data_mv[:,0]=1
# else
#     stop
# 

ndata[ndata[:,1]==(yr+1),:]=[]
fname = f'stn_code_data_{yr}.mat'
matlab.savemat(os.path.join(data_base_dir,'Station_KR','stn_code_data'), fname, {'ndata':ndata})

YEARS = [2016, 2017]
for yr in YEARS: #2006:2017
    fname = f'stn_code_data_{yr}.mat'
    ndata = matlab.loadmat(os.path.join(data_base_dir,'Station_KR','stn_code_data', fname)['ndata']
    ndata = np.vstack([data_mv, ndata])
    data_mv = ndata[ndata[:,1]==(yr+1),:]
    doy_unq = np.unique(data_mv[:,0])

    if len(doy_unq)==1:
        data_mv[:,0]=1
        ndata = np.delete(ndata, ndata[:,1]==(yr+1), axis=0)
        fname = f'stn_code_data_{yr}.mat'
        matlab.savemat(os.path.join(data_base_dir,'Station_KR','stn_code_data', fname), {'ndata':ndata})
    else:
        raise ValueError('len(doy_unq)!=1')

    fname = f'stn_code_data_{yr}_001_00.mat'
    matlab.savemat(os.path.join(data_base_dir,'Station_KR','stn_code_data', fname), {'data_mv':data_mv})