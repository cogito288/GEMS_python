### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import glob
import pandas as pd

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km')
path_rtt = os.path.join(data_base_dir, 'Preprocessed_raw', 'RTT')
path_loo = os.path.join(data_base_dir, 'Preprocessed_raw', 'LOO')

path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')
path_stn_cn = os.path.join(path_station, 'Station_CN')
path_stn_kr = os.path.join(path_station, 'Station_KR')

## Stations location information
mat = matlab.loadmat(os.path.join(path_stn_cn, 'cn_stn_GOCI6km_location_weight.mat'))
cn_dup_scode2_GOCI6km = mat['cn_dup_scode2_GOCI6km']
header_cn_stn_GOCI6km_location = mat['header_cn_stn_GOCI6km_location']
df = pd.DataFrame(mat['cn_stn_GOCI6km_location'], columns=header_cn_stn_GOCI6km_location)
cn_stn_GOCI6km_location = df.values
del df, mat

#mat = matlab.loadmat(os.path.join(path_stn_kr, 'stn_GOCI6km_location_weight_v2018.mat'))
mat = matlab.loadmat(os.path.join(path_stn_kr, 'stn_GOCI6km_location_weight_v201904.mat'))
dup_scode2_GOCI6km = mat['dup_scode2_GOCI6km']
df = pd.DataFrame(mat['stn_GOCI6km_location'], columns=mat['header_stn_GOCI6km_location'])
stn_GOCI6km_location = df.values
del df, mat

mat = matlab.loadmat(os.path.join(path_stn_jp, 'jp_stn_GOCI6km_location_weight_v2017.mat'))
jp_dup_scode2_GOCI6km = mat['jp_dup_scode2_GOCI6km']
header_jp_stn_GOCI6km_location = mat['header_jp_stn_GOCI6km_location']
df = pd.DataFrame(mat['jp_stn_GOCI6km_location'], columns=header_jp_stn_GOCI6km_location)
jp_stn_GOCI6km_location = df.values
del df, mat

stn_6km_location = np.concatenate([stn_GOCI6km_location, jp_stn_GOCI6km_location, cn_stn_GOCI6km_location], axis=0)
cn_dup_scode2_GOCI6km = np.concatenate([cn_dup_scode2_GOCI6km, np.zeros((cn_dup_scode2_GOCI6km.shape[0], jp_dup_scode2_GOCI6km.shape[1]))], axis=1)
dup_scode2_GOCI6km = np.concatenate([dup_scode2_GOCI6km, np.zeros((dup_scode2_GOCI6km.shape[0], jp_dup_scode2_GOCI6km.shape[1]))], axis=1)
dup_scode2_6km = np.concatenate((dup_scode2_GOCI6km, cn_dup_scode2_GOCI6km, jp_dup_scode2_GOCI6km), axis=0)

del stn_GOCI6km_location, cn_stn_GOCI6km_location, jp_stn_GOCI6km_location, cn_dup_scode2_GOCI6km, dup_scode2_GOCI6km, jp_dup_scode2_GOCI6km, header_cn_stn_GOCI6km_location, header_jp_stn_GOCI6km_location


## Read data
target = ['PM10','PM25']
type_list = ['conc','time','time_conc']
YEARS = [2016]

for t in range(3):
    for i in range(2):
        data_LOO = []
        if i==1:
            header = ['station_PM10','estimated_PM10','stn_num','doy','time','year','file_num']
            header2 = ['RF_PM10_ovr','STN_PM10','stn_num']
        else:
            header = ['station_PM25','estimated_PM25','stn_num','doy','time','year','file_num']
            header2 = ['RF_PM25_ovr','STN_PM25','stn_num']

        for yr in YEARS:
            if yr%4==0: days = 366
            else: days = 365

            for doy in range(1,days+1):
                yy, mm, dd = matlab.get_ymd(yr, doy) # should check 
                try:
                    fname = f'rf_{target[i]}_RTT_EA6km_{yr}_{doy:03d}*_LOO_*_val_ranger.csv'
                    list_val_rf = glob.glob(os.path.join(path_loo, type_list[t],'RF/',target[i],fname))
                    list_val_rf = [os.path.basename(f) for f in list_val_rf]
                    
                    fname = f'rf_{target[i]}_RTT_EA6km_{yr}_{doy:03d}*_LOO_*_val*.mat'
                    list_val_mat = glob.glob(os.path.join(path_loo, type_list[t],'dataset/',target[i],fname))
                    list_val_mat = [os.path.basename(f) for f in list_val_mat]
                    
                    RF_LOO_val = []
                    stn_val = []
                    data_val=[]
                    for f in range(len(list_val_rf)):
                        mat = matlab.loadmat(os.path.join(path_loo,type_list[t],'dataset/',target[i], list_val_mat[f]))
                        temp_index = np.where(val_10_fold[:,-2]==0)[0][-7:-2]
                        val_selected = val_10_fold[temp_index]
                        val_selected = np.concatenate((val_selected, np.zeros((val_selected.shape[0], 1))), axis=1)
                        val_selected[:, -1] = f
                        stn_val = np.concatenate((stn_val, val_selected), axis=0)
                        
                        RF_LOO_val_tmp = pd.read_csv(os.path.join(path_loo,type_list[t],'RF/',target[i], list_val_rf[f]))
                        RF_LOO_val_tmp = RF_LOO_val_tmp.values
                        RF_LOO_val = np.concatenate((RF_LOO_val, RF_LOO_val_tmp), axis=0)
                        print (list_val_rf[f])
                    del stn_val_tmp,  rf_val_tmp
                    
                    data_val[:,[0,2,3,4,5,6]] = stn_val[:,[0,1,2,3,4,5]]
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
        temp_df.to_csv(os.path.join(path_loo, type_list[t],'stn_location/',fname), float_format='#%.7f')
