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
path_in_situ = os.path.join(data_base_dir, 'Raw') 
path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 

### Setting period
YEARS = [2016] #, 2018, 2019]
for yr in YEARS: 
    if yr%4==0: days= 366
    else: days=365
    if yr==2019: days=151
        
    flist = glob.glob(os.path.join(path_in_situ, 'AirQuality_China', 'china_sites', str(yr),'*.csv'))
    flist = [os.path.basename(fname) for fname in flist]
    
    stn_yr = None
    for doy in range(1,days+1):
        stn_doy=[]
        _, mm, dd = matlab.get_ymd(yr, doy) #converting doy to day and month
        fname = f'china_sites_{yr}{mm:02d}{dd:02d}.csv'
        
        print (fname)
        if fname in flist: 
            stn_tmp = pd.read_csv(os.path.join(path_in_situ, 'AirQuality_China', 'china_sites', str(yr), fname))
            
            # observation matrix
            stn_value = stn_tmp.values
            stn_date = stn_tmp['date'].values.reshape(-1,1)
            stn_value = np.hstack([stn_date, stn_value]) # observation with time
            
            # station number matrix
            stn_num = stn_tmp.columns[3:]
            stn_num = [col.replace('A','') for col in stn_num]
            stn_num = [float(col) for col in stn_num]
            if len(stn_num) != stn_value[1:,:].shape[0]:
                idx = len(stn_num) - stn_value[1:,:].shape[0]
                nan_arr = np.zeros([idx, stn_value.shape[1]])*np.nan
                stn_value = np.vstack([stn_value, nan_arr])
             
            # header
            header = ['doy','yr','mm','dd','time']+list(stn_tmp.columns[1:16])+[stn_tmp.columns[2]]+['stn_num'] # characters(header)
            #{'doy','yr','mm','dd','time','AQI','PM2.5','PM2.5_24h','PM10',...
            #   'PM10_24h','SO2','SO2_24h','NO2','NO2_24h','O3','O3_24h','O3_8h','O3_8h_24h','CO','CO_24h','stn_num'}
            stn_doy = None
            for tt in range(23+1): # tt: china local time
                stn = np.full((len(stn_num), 21), np.nan)
                stn[:,0] = doy
                stn[:,1] = yr
                stn[:,2] = mm
                stn[:,3] = dd
                stn[:,4] = tt
                stn[:,20] = stn_num
                
                ttidx = np.sum(stn_tmp[stn_tmp['hour']==tt][stn_tmp.columns[3:]].values)
                print (ttidx)
                if ttidx>0:
                    stn[:,5:20] = stn_tmp[stn_tmp['hour']==tt][stn_tmp.columns[3:]].values.T # without time
                else:
                    #nan, without time
                    print (f'NO data in {tt:2.0f} (Local Time) on {doy:03d}')     
                if stn_doy is None:
                    stn_doy = stn
                else:
                    stn_doy = np.vstack([stn_doy, stn])
        else:
            print(f'NO file in {doy:03d} (DOY) ')
            # 여기에 아예 빈날 nan matrix 생성해서 넣는걸로 수정..
        if stn_yr is None:
            stn_yr = stn_doy
        else:
            stn_yr=np.vstack([stn_yr, stn_doy])   
    fname = f'stn_code_data_{yr}_finxed_ms.mat'
    matlab.savemat(os.path.join(path_station, 'Station_CN', 'stn_code_data', fname), {'stn_yr':stn_yr})
    print (yr)