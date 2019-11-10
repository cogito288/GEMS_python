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
# path = '//10.72.26.56/irisnas5/GEMS/PM/00_EA6km/'
# genpath(addpath('//10.72.26.46/irisnas5/Data/matlab_func/'))
path = '/share/irisnas5/GEMS/PM/00_EA6km/'
addpath(genpath('/share/irisnas5/Data/matlab_func/'))

## Read data
target = ['PM10','PM25']
type_list = ['conc','time','time_conc']
YEARS = [2015, 2016]


for t in range(1,3+1):
    for i in range(1,2+1):
        if i==1:
            header = ['station_PM10','RF_PM10','stn','doy','time','year']
        else:
            header = ['station_PM25','RF_PM25','stn','doy','time','year']
            
        for yr in YEARS:
            val_rf = []
            val_stn = []
            data_val=[]
            if yr%4==0: days = 366
            else: days = 365
            
            for doy in range(1,days1+):
                for utc in range(7+1):
                    try:
                        fname = f'rf_{target[i]}_RTT_EA6km_{yr}_{doy:03d}_{utc:02d}_val.csv'
                        val_rf_tmp = pd.read_csv(os.path.join(path, 'RTT/',type_list[t],'/RF/',target{i},fname))
                        val_rf_tmp = val_rf_tmp.values
                        val_rf =np.concatenate((val_rf, val_rf_tmp), axis=0)
                        
                        fname = f'rf_{target[i]}_RTT_EA6km_{yr}_{doy:03d}_{utc:02d}.csv'
                        data = pd.read_csv(os.path.join(path, 'RTT/',type_list[t],'/dataset/',target{i},fname))
                        val_stn_tmp = data[data[:,-1]==240 & data[:,-1]==0,:]
                        val_stn = np.concatente((val_stn, val_stn_tmp[:,[-6,-5:-2]), axis=0)
                        val_stn = val_stn[val_stn[:,0]>0,:]
                        print (utc)
                    except:
                        print ('There is no rf file \n')
                        print (utc)
                print (doy)
            print (yr)
        data_val[:,[0,2:6]] = val_stn[:,[0,1:5]]
        data_val[:,1] = val_rf
        data_val[data_val==-9999] = np.nan
        data_val = rmmissing[data_val,0]

        fname = f'{type_list[t]}_{target[i]}_compare_RTT_val_stn_ovr_EA6km_{yr}_new.csv'  
        temp_df = pd.DataFrame(data_val, columns=header)
        temp_df.to_csv(os.path.join(path,'RTT/',type_list[t],'/stn_location/',fname), float_format='%7.7f')
