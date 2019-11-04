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

# for local
# path_data = '//10.72.26.46/irisnas6/Data/In_situ/AirQuality_Japan/'
# path = '//10.72.26.56/irisnas5/Data/Station/Station_JP/'
# addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'))

path_data = '/share/irisnas6/Data/In_situ/AirQuality_Japan/'
path = '/share/irisnas5/Data/Station/Station_JP/'
# addpath(genpath('/share/irisnas5/Data/matlab_func/'))

header = ['doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode']

YEARS = [2017]
for yr in YEARS:
    for mm in range(1, 12+1):
        list_stn = glob.glob(os.path.join(path_data, f'{yr_soramame}', f'{yr}{mm:02d}_00', '*.csv'))
        
        stn_mm=[]
        for fname in list_stn:
            stn_tbl_temp = pd.read_csv(fname)
            
            scode = stn_tbl_temp[:,0].values
            dstr = stn_tbl_temp[:,1].values
            date_list = [f'{d[:5]}{d[6:8]}{d[9:}]' for d in dstr] #yyyy/mm/dd -> yyyymmdd
            # dvec = datevec(dstr,'yyyy/mm/dd') # dvec[:, :3] yyyymmdd?
            dnum = matlab.datenum(date_list) # datenum(dstr,'yyyy/mm/dd')
            doy_000 = matlab.datenum(f'{yr}00000')
            doy = dnum - doy_000
            stn_value = stn_tbl_temp[:,2:15].values
            
            data = np.concatenate((doy, date_list, stn_value[:,[0,1,5,6,3,10,11]], scode), axis=1)
            # {'doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode'}
            stn_mm = np.concatenate((stn_mm, data), axis=0)
        
        matlab.savemat(os.path.join(path,'stn_code_data/stn_code_data_',num2str(yr),'_',num2str(mm,'#02i'),'.mat'],'stn_mm','-v7.3')
        print (mm)
            
    
    print ('Stack monthly data to yearly data')
    stn_yr = []
    for mm in range(1, 12+1):
        fname = f'stn_code_data_{yr}_{mm:02d}.mat'
        matlab.loadmat(os.path.join(path,'stn_code_data', fname))
        stn_yr= np.concatenate((stn_yr, stn_mm), axis=0)
    
    fname = f'stn_code_data_{yr}_2.mat'
    matlab.savemat(os.path.join(path, 'stn_code_data'), fname],{'stn_yr':stn_yr})
    print (yr)
