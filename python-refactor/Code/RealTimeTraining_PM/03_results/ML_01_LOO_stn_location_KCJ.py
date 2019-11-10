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
# path_data = '//10.72.26.56/irisnas5/Data/'
# path = '//10.72.26.56/irisnas5/GEMS/PM/00_EA6km/'
# addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'))

path_data = '/share/irisnas5/Data/'
path = '/share/irisnas5/GEMS/PM/00_EA6km/'
addpath(genpath('/share/irisnas5/Data/matlab_func/'))

# path_data = '/Volumes/irisnas5/Data/'
# path = '/Volumes/irisnas5/GEMS/PM/00_EA6km/'
# addpath(genpath('/Volumes/irisnas5/Data/matlab_func/'))

## Stations location information
matlab.loadmat(os.path.join(path_data,'Station/Station_CN/cn_stn_GOCI6km_location_weight.mat'))
matlab.loadmat(os.path.join(path_data,'Station/Station_Korea/stn_GOCI6km_location_weight_v2018.mat'))
matlab.loadmat(os.path.join(path_data,'Station/Station_JP/jp_stn_GOCI6km_location_weight.mat'))
stn_6km_location = np.concatenate((stn_GOCI6km_location, jp_stn_GOCI6km_location, cn_stn_GOCI6km_location), axis=0)
cn_dup_scode2_GOCI6km[:,end+1:jp_dup_scode2_GOCI6km.shape[1]]=0
dup_scode2_GOCI6km[:,-1+1:jp_dup_scode2_GOCI6km.shape[1]]=0
dup_scode2_6km = np.concatenate((dup_scode2_GOCI6km, cn_dup_scode2_GOCI6km, jp_dup_scode2_GOCI6km), axis=0)

del stn_GOCI6km_location, cn_stn_GOCI6km_location, jp_stn_GOCI6km_location, cn_dup_scode2_GOCI6km, dup_scode2_GOCI6km, jp_dup_scode2_GOCI6km, header_cn_stn_GOCI6km_location, header_jp_stn_GOCI6km_location

## Read data
target = ['PM10','PM25']
type_list = ['conc','time','time_conc']
YEARS = [2015, 2016]

for t in range(1,3+1):
    for i in range(1,2+1):
        data_LOO = []
        if i==1:
            header = ['station_PM10','estimated_PM10','stn_num','doy','time','year','file_num']
            header2 = ['RF_PM10_ovr','STN_PM10','stn_num']
        else
            header = ['station_PM25','estimated_PM25','stn_num','doy','time','year','file_num']
            header2 = ['RF_PM25_ovr','STN_PM25','stn_num']

        for yr in YEARS:
            if yr%4==0: days = 366
            else: days = 365

            for doy in range(1,days1+):
                yy, mm, dd = get_ymd(yr, doy) # should check 
                try:
                    fname = f'rf_{target[i]}_RTT_EA6km_{yr}_{doy:03d}*_LOO_*_val_ranger.csv'
                    list_val_rf = glob.glob(os.path.join(path, 'LOO/',type_list[t],'/RF/',target[i],fname))
                    list_val_rf = [os.path.basename(f) for f in list_val_rf]
                    
                    fname = f'rf_{target[i]}_RTT_EA6km_{yr}_{doy:03d}*_LOO_*_val*.mat'
                    list_val_mat = glob.glob(os.path.join(path, 'LOO/',type_list[t],'/dataset/',target[i],fname))
                    list_val_mat = [os.path.basename(f) for f in list_val_mat]
                    
                    RF_LOO_val = []
                    stn_val = []
                    data_val=[]
                    for f in range(len(list_val_rf)):
                        matlab.loadmat(os.path.join(path,'/LOO/',type_list[t],'/dataset/',target[i], list_val_mat[f])
                        temp_index = np.where(val_10_fold[:,-1]==0)[0][-7:-2]
                        val_selected = val_10_fold[temp_index]
                        val_selected[:,end+1] = f
                        stn_val = np.concatenate((stn_val, val_selected), axis=0)
                        
                        RF_LOO_val_tmp = pd.read_csv(os.path.join(path, 'LOO/',type_list[t],'/RF/',target[i], list_val_rf[f])
                        RF_LOO_val_tmp = RF_LOO_val_tmp.values
                        RF_LOO_val = np.concatenate((RF_LOO_val, RF_LOO_val_tmp), axis=0)
                        print (list_val_rf[f])

                    del stn_val_tmp,  rf_val_tmp
                    
                    data_val[:,[0,2:7]] = stn_val[:,[0,1:6]]
                    data_val[:,1] = RF_LOO_val #stn_PM, rf_PM stn_num, doy, time, year
                    
                    data_val[data_val==-9999] = np.nan
                    nanidx_val = np.isnan(data_val)
                    nanidx_val = np.sum(nanidx_val,axis=1)
                    data_val = data_val[nanidx_val==0,:]
                    
                    data_LOO= np.concatenate((data_LOO, data_val), axis=0)
                    print (doy)
                except:
                    pass
        fname = f'{type_list[t]}_{target[i]}_compare_RF_LOO_EA6km_val_stn_ovr_new3.csv'
        temp_df = pd.DataFrame(data_LOO, columns=header)
        temp_df.to_csv(os.path.join(path,'LOO/',type_list[t],'/stn_location/',fname), float_format='#%.7f')
