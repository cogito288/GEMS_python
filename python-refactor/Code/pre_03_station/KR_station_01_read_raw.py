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
import shutil
import xlrd

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_in_situ = os.path.join(data_base_dir, 'Raw') 
path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_kor = os.path.join(path_station, 'Station_KR')

"""
## 2005-2013 (xlsx, PM2.5없음)
YEARS = range(2005, 2013+1)
for yr in YEARS:
    data = None
    for i in range(1, 4+1):
        fname = f'{yr}년{i:02d}분기.xlsx'
        try:
            tmp_df = pd.read_excel(os.path.join(path_in_situ, 'AirQuality_Korea', str(yr), fname))
        except xlrd.biffh.XLRDError:
            new_fname = os.path.splitext(fname)[0]+'.csv'
            shutil.copy2(os.path.join(path_in_situ, 'AirQuality_Korea', str(yr), fname), 
                         os.path.join(path_in_situ, 'AirQuality_Korea', str(yr), new_fname))
            fname = new_fname
            tmp_df = pd.read_csv(os.path.join(path_in_situ, 'AirQuality_Korea', str(yr), fname), encoding='cp949')
            pass
        text_cols = [col for col in tmp_df.columns if tmp_df[col].dtype.name=='object']
        data_temp = tmp_df.loc[:,text_cols[2:9]]
        if data is None:
            data = data_temp
        else:
            data = pd.concat([data, data_temp])
        del tmp_df, data_temp
    data = data.values.astype('float64')
    data[data<0]=np.nan
    
    dstr = [str(int(x)) for x in data[:,1]]
    tmp_df = pd.DataFrame(dstr, columns=['time'])
    pat = '(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<hour>\d{2})'
    dvec = pd.to_datetime(tmp_df['time'].str.extract(pat, expand=True))
    dstr = dvec.dt.strftime('%Y%m%d').values
    data_datenum = [matlab.datenum(val) for val in dstr]
    doy_000 = matlab.datenum(f'{yr}00000')
    data_doy = np.array([np.floor(val-doy_000) for val in data_datenum])
    dvec = [(val.year, val.month, val.day, val.hour) for val in dvec]
    dvec = np.array(dvec)
    ndata = np.hstack([data_doy.reshape(-1,1),dvec[:,:4],data[:,2:],np.full([len(data_doy),1])*np.nan, data[:,0].reshape(-1,1)])
    # doy, yr, mon, day, time, SO2, CO, O3, NO2, PM10, (PM25), scode
    matlab.savemat(os.path.join(path_stn_kor,'stn_code_data',f'stn_code_data_{yr}.mat'), 
                   {'ndata':ndata})
"""
## 2014-2016 (csv, PM2.5 컬럼 있음)
YEARS = range(2014, 2016+1)
for yr in [2016]:
    data = None
    for i in range(1, 4+1):
        fname = f'{yr}년{i:02d}분기.xlsx'
        try:
            tmp_df = pd.read_excel(os.path.join(path_in_situ, 'AirQuality_Korea', str(yr), fname))
        except xlrd.biffh.XLRDError:
            new_fname = os.path.splitext(fname)[0]+'.csv'
            shutil.copy2(os.path.join(path_in_situ, 'AirQuality_Korea', str(yr), fname), 
                         os.path.join(path_in_situ, 'AirQuality_Korea', str(yr), new_fname))
            fname = new_fname
            tmp_df = pd.read_csv(os.path.join(path_in_situ, 'AirQuality_Korea', str(yr), fname), encoding='cp949')
            pass
        cols = [tmp_df.columns[1]]
        cols.extend(tmp_df.columns[3:10])
        data_temp = tmp_df.loc[:,cols]
        if data is None:
            data = data_temp
        else:
            data = pd.concat([data, data_temp])
        del tmp_df, data_temp
    data = data.values
    data[data<0]=np.nan

    dstr = [str(int(x)) for x in data[:,1]]
    tmp_df = pd.DataFrame(dstr, columns=['time'])
    pat = '(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<hour>\d{2})'
    dvec = pd.to_datetime(tmp_df['time'].str.extract(pat, expand=True))
    dstr = dvec.dt.strftime('%Y%m%d').values
    data_datenum = [matlab.datenum(val) for val in dstr]
    doy_000 = matlab.datenum(f'{yr}00000')
    data_doy = np.array([np.floor(val-doy_000) for val in data_datenum])
    dvec = [(val.year, val.month, val.day, val.hour) for val in dvec]
    dvec = np.array(dvec)
    ndata = np.hstack([data_doy.reshape(-1,1),dvec[:,:4],data[:,2:],data[:,0].reshape(-1,1)])
    # doy, yr, mon, day, time, SO2, CO, O3, NO2, PM10, (PM25), scode
    matlab.savemat(os.path.join(path_stn_kor,'stn_code_data',f'stn_code_data_{yr}.mat'), 
                   {'ndata':ndata})
"""
## 2017-2018 2분기 (xlsx, PM2.5 있음)
YEARS = [2018]
for yr in YEARS:
    data = None
    for i in range(1, 4+1):
        fname = f'{yr}년{i:02d}분기.xlsx'
        try:
            tmp_df = pd.read_excel(os.path.join(path_in_situ, 'AirQuality_Korea', str(yr), fname))
        except xlrd.biffh.XLRDError:
            new_fname = os.path.splitext(fname)[0]+'.csv'
            shutil.copy2(os.path.join(path_in_situ, 'AirQuality_Korea', str(yr), fname), 
                         os.path.join(path_in_situ, 'AirQuality_Korea', str(yr), new_fname))
            fname = new_fname
            tmp_df = pd.read_csv(os.path.join(path_in_situ, 'AirQuality_Korea', str(yr), fname), encoding='cp949')
            pass
        cols = [tmp_df.columns[1]]
        cols.extend(tmp_df.columns[3:10])
        data_temp = tmp_df.loc[:,cols]
        if data is None:
            data = data_temp
        else:
            data = pd.concat([data, data_temp])
        del tmp_df, data_temp
        break
    data = data.values
    data_1 = data[:, 0].astype(np.float)
    data_2 = data[:, data.columns[1:]].values
    data = np.hstack([data_1.reshape(-1,1), data_2.reshape(-1,1)])
    data[data<0]=np.nan
    
    dstr = [str(int(x)) for x in data[:,1]]
    tmp_df = pd.DataFrame(dstr, columns=['time'])
    pat = '(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<hour>\d{2})'
    dvec = pd.to_datetime(tmp_df['time'].str.extract(pat, expand=True))
    dstr = dvec.dt.strftime('%Y%m%d').values
    data_datenum = [matlab.datenum(val) for val in dstr]
    doy_000 = matlab.datenum(f'{yr}00000')
    data_doy = np.array([np.floor(val-doy_000) for val in data_datenum])
    dvec = [(val.year, val.month, val.day, val.hour) for val in dvec]
    dvec = np.array(dvec)
    ndata = np.hstack([data_doy.reshape(-1,1),dvec[:,:4],data[:,2:],data[:,0].reshape(-1,1)])
    # doy, yr, mon, day, time, SO2, CO, O3, NO2, PM10, (PM25), scode
    matlab.savemat(os.path.join(path_stn_kor,'stn_code_data',f'stn_code_data_{yr}.mat'), 
                   {'ndata':ndata})

## 2018 3분기 - 4분기 (xlsx, PM2.5있음.. 근데 중간에 망 정보가 들어가면서 컬럼 위치가 변경됨)
i=4
fname = f'{yr}년{i:02d}분기.xlsx'
tmp_df = pd.read_excel(os.path.join(path_insiu, 'AirQuality_Korea', str(yr), fname))
cols = [tmp_df.columns[2]]
cols.extend(tmp_df.columns[4:11])
data_temp = tmp_df.loc[:,cols]
data = pd.concat([data, data_temp])

## 201810_201904 
data = None
tmp_df = pd.read_csv(os.path.join(path_insiu,'201810_201904', '201810_201904_pt1.csv'))
cols = [tmp_df.columns[1]]
cols.extend(tmp_df.columns[5:7])
cols.extend([tmp_df.columns[9], tmp_df.columns[8], tmp_df.columns[10], tmp_df.columns[11]])
data_temp = tmp_df.loc[:,cols]
data = pd.concat([data, data_temp])

tmp_df = pd.read_csv(os.path.join(path_insiu,'201810_201904', '201810_201904_pt2.csv'))
cols = [tmp_df.columns[1]]
cols.extend(tmp_df.columns[5:7])
cols.extend([tmp_df.columns[9], tmp_df.columns[8], tmp_df.columns[10], tmp_df.columns[11]])
data_temp = tmp_df.loc[:,cols]
data = pd.concat([data, data_temp])

data = data.values
data[data<0]=np.nan

dstr = [str(int(x)) for x in data[:,1]]
tmp_df = pd.DataFrame(dstr, columns=['time'])
pat = '(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<hour>\d{2})'
dvec = pd.to_datetime(tmp_df['time'].str.extract(pat, expand=True))
dstr = dvec.dt.strftime('%Y%m%d').values
dvec = [(val.year, val.month, val.day, val.hour) for val in dvec]
dvec = np.array(dvec)

yr=2019
yr_idx = (dvec[:,0]==yr)
dvec=dvec[yr_idx,:]
dstr=dstr[yr_idx,:]
data=data[yr_idx,:]

data_datenum = [matlab.datenum(val) for val in dstr]
doy_000 = matlab.datenum(f'{yr}00000')
data_doy = np.array([np.floor(val-doy_000) for val in data_datenum])
ndata = np.hstack([data_doy.reshape(-1,1),dvec[:,:4],data[:,2:],data[:,0].reshape(-1,1)])
# doy, yr, mon, day, time, SO2, CO, O3, NO2, PM10, (PM25), scode
matlab.savemat(os.path.join(path_stn_kor,'stn_code_data',f'stn_code_data_{yr}.mat'), 
               {'ndata':ndata})


## 12월 31일 24시 -> 1월 1일 00시 
#path = '/share/irisnas5/Data/Station/Station_Korea/'

yr=2005
fname = f'stn_code_data_{yr}.mat'
ndata = matlab.loadmat(os.path.join(path_stn_kor,'stn_code_data', fname))['ndata']
data_mv = ndata[ndata[:,1]==(yr+1),:]
doy_unq = np.unique(data_mv[:,0])

# if length(doy_unq)==1
data_mv[:,0]=1
# else
#     stop
# 

ndata[ndata[:,1]==(yr+1),:]=[]
fname = f'stn_code_data_{yr}.mat'
matlab.savemat(os.path.join(path_stn_kor,'stn_code_data'), fname, {'ndata':ndata})

YEARS = [2016, 2017]
for yr in YEARS: #2006:2017
    fname = f'stn_code_data_{yr}.mat'
    ndata = matlab.loadmat(os.path.join(path_stn_kor,'stn_code_data', fname)['ndata']
    ndata = np.vstack([data_mv, ndata])
    data_mv = ndata[ndata[:,1]==(yr+1),:]
    doy_unq = np.unique(data_mv[:,0])

    if len(doy_unq)==1:
        data_mv[:,0]=1
        ndata = np.delete(ndata, ndata[:,1]==(yr+1), axis=0)
        fname = f'stn_code_data_{yr}.mat'
        matlab.savemat(os.path.join(path_stn_kor,'stn_code_data', fname), {'ndata':ndata})
    else:
        raise ValueError('len(doy_unq)!=1')

    fname = f'stn_code_data_{yr}_001_00.mat'
    matlab.savemat(os.path.join(path_stn_kor,'stn_code_data', fname), {'data_mv':data_mv})
"""