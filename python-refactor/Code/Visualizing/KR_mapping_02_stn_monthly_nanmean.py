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
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km')

path_korea_cases = os.path.join(data_base_dir, 'Preprocessed_raw', 'Korea', 'cases')
matlab.check_make_dir(path_korea_cases)

path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')
path_stn_cn = os.path.join(path_station, 'Station_CN')
path_stn_kr = os.path.join(path_station, 'Station_KR')


tg = ['PM10','PM25']

## Load grid
mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_korea.mat'))
lat_kor, lon_kor = mat['lat_kor'], mat['lon_kor']
del mat

mat = matlab.loadmat(os.path.join(path_stn_kr, 'stn_1km_location_weight_v201904.mat')) # stn_1km_location
stn_1km_location = mat['stn_1km_location']
del mat
# scode1,scode2, lat_org, lon_org, pxid, lat_px, lon_px

stn_location = stn_1km_location
# scode1,scode2, lat_org, lon_org, pxid, lat_px, lon_px

##
YEARS = [2016]
for yr in YEARS:
    stn_fill = matlab.loadmat(os.path.join(path_korea_cases, f'KR_1km_stn_rf_day_{yr}.mat'))['stn_fill'] # 'stn_fill'
 
    for mm in range(1,12+1):
        data_temp = stn_fill[stn_fill[:,2]==mm,:]
        #         data_temp = stn_fill # yearly
        scode2_unq = np.unique(data_temp[:,12])
        data_avg = []
        for ss in len(scode2_unq):
            data_temp2 = data_temp[data_temp[:,12]==scode2_unq[ss],:]
            data_temp2 = np.nanmean(data_temp2, axis=0)
            data_avg = np.concatenate((data_avg, data_temp2), axis=0)
        data_avg = data_avg[:,[12,9,10]] # scode2, stn_pm10, stn_pm
        
        for k in range(data_avg.shape[0]): 
            data_avg[k,3:5]=stn_location[stn_location[:,1]==data_avg[k,0],2,3] 
            # scode2, stn_pm10, stn_pm25, lat_org, lon_org
        stnpm10 = data_avg[:,[0,1,2,3]]
        stnpm10 = stnpm10[~np.isnan(stnpm10).any(axis=1)]  #rmmissing(stnpm10,1)
        
        east = 131.5
        west = 123
        north = 39
        south = 33
        
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplots(1,1,1, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()
        ax.scatter(stnpm10[:, 3], stnpm10[:, 2], s=3, c=stnpm10[:,1], markeredgecolor='k')
        ax.set_title(f"{yr}/{mm:02d}", fontsize=25)
        ax.colorbar(fontsize=12)
        plt.show()   
        
        print('-djpeg','-r300', path_korea_cases,f'Korea/RF_pred/PM10_stn_monthly_{yr}_{mm:02d}')
        #         print('-djpeg','-r300',[path,'Korea/RF_pred/PM10_stn_yearly_',str(yr)])  # yearly
        
        stnpm25 = data_avg[:,[0,2,3]]
        stnpm25 = stnpm25[~np.isnan(stnpm25).any(axis=1)]  #rmmissing(stnpm25,1)
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplots(1,1,1, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()
        ax.scatter(stnpm25[:, 3], stnpm25[:, 2], s=3, c=stnpm25[:,1], markeredgecolor='k')
        ax.set_title(f"{yr}/{mm:02d}", fontsize=25)
        ax.colorbar(fontsize=12)
        plt.show()   
        
        print('-djpeg','-r300',path_korea_cases,f'Korea/RF_pred/PM25_stn_monthly_{yr}_{mm:02}')
        #         print('-djpeg','-r300',[path,'Korea/RF_pred/PM25_stn_yearly_',str(yr)]) # yearly
