### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
#base_dir = 'D:\github\GEMS_python'
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import copy
import numpy as np 
import pandas as pd
import glob

### Setting path
# data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
# data_base_dir = os.path.join('//', '10.72.26.56','irisnas5', 'GEMS', 'GEMS_python')
data_base_dir = os.path.join('/', 'share', 'irisnas5', 'GEMS', 'GEMS_python')
# path_in_situ = os.path.join(data_base_dir, 'Raw')
# path_in_situ = os.path.join('//','10.72.26.46','irisnas6','Data','In_situ')
path_in_situ = os.path.join('/','share','irisnas6','Data','In_situ')
path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_kr = os.path.join(path_station, 'Station_KR')

cols=['측정소코드','측정일시','SO2','CO','O3','NO2','PM10','PM25']

## 
YEARS = range(2014, 2018+1)
for yr in YEARS:
    flist = glob.glob(os.path.join(path_in_situ,'AirQuality_SouthKorea',str(yr),'*'))
    flist.sort()
    data = None
    for fname in flist:
        fname_body, fname_ext = os.path.splitext(fname)
        if fname_ext=='.csv':
            try:
                tmp_df = pd.read_csv(fname)
            except:
                tmp_df = pd.read_csv(fname,encoding='euc-kr')
        else:
            tmp_df = pd.read_excel(fname)

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
    ndata = np.hstack([data_doy.reshape(-1,1),dvec,data[:,2:],data[:,0].reshape(-1,1)])
    # doy, yr, mon, day, time, SO2, CO, O3, NO2, PM10, PM25, scode
    matlab.savemat(os.path.join(path_stn_kr,'stn_code_data',f'stn_code_data_{yr}.mat'), 
                   {'ndata':ndata})
    
## 12월 31일 24시 -> 1월 1일 00시 
for yr in YEARS:
    fname = f'stn_code_data_{yr}.mat'
    ndata = matlab.loadmat(os.path.join(path_stn_kr,'stn_code_data', fname))['ndata']
    if yr!=YEARS[0]:
        fname_mv = f'stn_code_data_{yr}_001_00.mat'
        data_mv = matlab.loadmat(os.path.join(path_stn_kr,'stn_code_data', fname_mv))['data_mv']
        ndata = np.vstack([data_mv, ndata])
        del data_mv
    data_mv = ndata[ndata[:,1]==(yr+1),:]
    doy_unq = np.unique(data_mv[:,0])

    if len(doy_unq)==1:
        data_mv[:,0]=1
        idx= ndata[:,1]==(yr+1)
        ndata = ndata[~idx]
        matlab.savemat(os.path.join(path_stn_kr,'stn_code_data', fname), {'ndata':ndata})
    else:
        raise ValueError('len(doy_unq)!=1')

    fname_mv2 = f'stn_code_data_{yr+1}_001_00.mat'
    matlab.savemat(os.path.join(path_stn_kr,'stn_code_data', fname_mv2), {'data_mv':data_mv})
