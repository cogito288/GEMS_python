### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = base_dir
sys.path.insert(0, project_path)
from Code.utils import matlab

import copy
import numpy as np
import pandas as pd
import glob

### Setting path
data_base_dir = os.path.join(base_dir, 'Data')
path_in_situ = os.path.join(data_base_dir, 'Raw', 'In_situ')
path_station = os.path.join(data_base_dir, 'Station')
path_stn_cn = os.path.join(path_station, 'Station_CN')

### Setting period
YEARS = range(2015,2019+1)

for yr in YEARS: 
    if yr%4==0: days= 366
    else: days=365
        
    flist = glob.glob(os.path.join(path_in_situ, 'AirQuality_China', str(yr),'*.csv'))
    flist = [os.path.basename(fname) for fname in flist]
    
    stn_yr = None
    for doy in range(1,days+1):
        _, mm, dd = matlab.get_ymd(yr, doy) #converting doy to day and month
        fname = f'china_sites_{yr}{mm:02d}{dd:02d}.csv'
        
        print (fname)
        #print (fname in flist)
        if fname in flist: 
            stn_tmp = pd.read_csv(os.path.join(path_in_situ, 'AirQuality_China', str(yr), fname))
            
            # observation matrix
            stn_value = stn_tmp.iloc[:,3:].values
            stn_hour = stn_tmp['hour'].values
            stn_type = stn_tmp['type'][0:15]
            
            # station number matrix
            scode = stn_tmp.columns[3:]
            scode = [int(a[0:4]) for a in scode]
            scode_unq, ia = np.unique(scode, return_index=True)
            stn_value = stn_value[:,ia]
            
            # header
            header = ['doy','yr','mm','dd','CST']+list(stn_type)+['scode']
            #{'doy','yr','mm','dd','CST','AQI','PM2.5','PM2.5_24h','PM10',...
            #   'PM10_24h','SO2','SO2_24h','NO2','NO2_24h','O3','O3_24h','O3_8h','O3_8h_24h','CO','CO_24h','scode'}
            
            stn_doy = None
            for CST in range(23+1): # CST: china local time
                stn = np.full((len(scode_unq), 21), np.nan)
                stn[:,0] = doy
                stn[:,1] = yr
                stn[:,2] = mm
                stn[:,3] = dd
                stn[:,4] = CST
                stn[:,20] = scode_unq
                
                ttidx = np.sum(stn_hour==CST)
                #print (ttidx)
                if ttidx==15:
                    stn[:,5:20] = stn_value[stn_hour==CST].T
                else:
                    #nan, without time
                    print (f'NO data in {CST:2.0f} (Local Time) on {doy:03d}')
                if stn_doy is None:
                    stn_doy = stn
                else:
                    stn_doy = np.concatenate((stn_doy, stn), axis=0)
        else:
            stn_doy = np.full((0, 21), np.nan)
            print(f'NO file in {doy:03d} (DOY)')
        if stn_yr is None:
            stn_yr = stn_doy
        else:
            stn_yr=np.concatenate((stn_yr, stn_doy), axis=0)
        
    fname = f'stn_code_data_{yr}.mat'
    matlab.savemat(os.path.join(path_stn_cn,'stn_code_data', fname), {'stn_yr':stn_yr})
    print (yr)