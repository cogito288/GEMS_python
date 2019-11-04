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


## # for local
#path_data = '//10.72.26.46/irisnas6/Data/in_situ/AirQuality_China/china_sites/'
#path = '//10.72.26.56/irisnas5/Data/Station/Station_CN/'
#addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'))


## # for server
path_data = '/share/irisnas6/Data/in_situ/AirQuality_China/china_sites/'
path = '/share/irisnas5/Data/Station/Station_CN/'
## addpath(genpath('/share/irisnas5/Data/matlab_func/'))


### Setting period
YEARS = [2016] #, 2018, 2019]

## cd(path)
for yr in YEARS: 
    if yt#4==0: days= 366
    else: days=365
    if yr==2019: days=151

        
    flist = glob.glob(os.path.join(path_data,str(yr),'/*.csv'))
    flist = [os.path.basename(f) for f in flist]
    
    stn_yr = []
    for doy in range(1,days):
        stn_doy=[]
        [mm,dd]=ddd2mmdd(yr,doy) #converting doy to day and month
        fname = [f'china_sites_{yr}{m:02d}{d:02d}.csv' for m, d in zip(mm,dd)]
        
        if fname in flist: #ismember(fname,flist)
            num,txt,stn_tmp = pd.read_excel(os.path.join(path_data, str(yr), fname)
            #[num,txt,stn_tmp]=xlsread([path_data, str(yr),'/',fname])
            
            # observation matrix
            stn_value = stn_tmp.data
            stn_date = str2double(stn_tmp.textdata(2:end,2))
            stn_value = np.concatenate((stn_date,stn_value), axis=1) # observation with time
            
            # station number matrix
            stn_num = stn_tmp.textdata(1,4:end)
            stn_num = regexprep(stn_num, 'A', '') #stn_num 내에 문자(A) 없애주기
            stn_num = str2double(stn_num)
            if stn_num.shape[0] != stn_value[1:,:].shape[0]:
                idx = stn_num.shape[0] - stn-value[1:,:].shape[0]
                stn_value[end+1:end+idx,:] = np.nan
            
            # header
            header = ['doy','yr','mm','dd','time',stn_tmp.textdata(2:16,3)]+stn_num # characters(header)
            #{'doy','yr','mm','dd','time','AQI','PM2.5','PM2.5_24h','PM10',...
            #   'PM10_24h','SO2','SO2_24h','NO2','NO2_24h','O3','O3_24h','O3_8h','O3_8h_24h','CO','CO_24h','stn_num'}
            
            for tt in range(23+1): # tt: china local time
                stn=np.full((stn_num.shape[0], 21), np.nan)
                stn[:,0] =doy
                stn[:,1] =yr
                stn[:,2] =mm
                stn[:,3] =dd
                stn[:,4] =tt
                stn[:,20] =stn_num
                
                ttidx = nmp.sum(stn_value[0,:]==tt)
                if ttidx>0:
                    stn[:,5:20] = stn_value[1:,stn_value[0,:]==tt] # without time
                else:
                    #nan, without time
                    print (f'NO data in {tt:2.0f} (Local Time) on {doy:03d}\n',tt,doy)
#                     stn=[] 이거 대신에 np.nan matrix 넣는걸로 수정..
               
                stn_doy=np.concatenate((stn_doy stn), axis=1)
        else:
            print('NO file in #03i (DOY) \n',doy)
            # 여기에 아예 빈날 np.nan matrix 생성해서 넣는걸로 수정..
        stn_yr=np.concatenate((stn_yr stn_doy), axis=1)
    fname = stn_code_data_{yr}_finxed_ms.mat
    matlab.savemat(os.path.join(path, 'stn_code_data'), objective = stn_code_data_[yr]_fixed_ms.mat'],{'stn_yr':stn_yr})   print (yr)

