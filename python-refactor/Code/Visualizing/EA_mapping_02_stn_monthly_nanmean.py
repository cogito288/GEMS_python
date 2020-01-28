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

path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')
path_stn_cn = os.path.join(path_station, 'Station_CN')
path_stn_kr = os.path.join(path_station, 'Station_KR')

path_output = os.path.join(data_base_dir, 'output', 'RealTimeTraining', 'EastAsia')
matlab.check_make_dir(path_output)

tg = ['PM10','PM25']

## Load grid
mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_goci.mat'))
lon_goci, lat_goci = mat['lon_goci'], mat['lat_goci']
del mat

##
YEARS = [2016]
for yr in YEARS:
    #mat = matlab.loadmat(os.path.join(path_stn_kr, 'stn_GOCI6km_location_weight_v2018.mat'))
    mat = matlab.loadmat(os.path.join(path_stn_kr, 'stn_GOCI6km_location_weight_v201904.mat'))
    dup_scode2_GOCI6km = mat['dup_scode2_GOCI6km']
    df = pd.DataFrame(mat['stn_GOCI6km_location'], columns=mat['header_stn_GOCI6km_location'])
    stn_GOCI6km_location = df.values
    del df, mat
    
    mat = matlab.loadmat(os.path.join(path_stn_cn, 'cn_stn_GOCI6km_location_weight.mat'))
    cn_dup_scode2_GOCI6km = mat['cn_dup_scode2_GOCI6km']
    header_cn_stn_GOCI6km_location = mat['header_cn_stn_GOCI6km_location']
    df = pd.DataFrame(mat['cn_stn_GOCI6km_location'], columns=header_cn_stn_GOCI6km_location)
    cn_stn_GOCI6km_location = df.values
    del df, mat

    stn_location = np.concatenate((stn_GOCI6km_location,cn_stn_GOCI6km_location), axis=0)
    # scode1,scode2, lat_org, lon_org, pxid, lat_px, lon_px
    
    del stn_GOCI6km_location, dup_scode2_GOCI6km, cn_stn_GOCI6km_location, cn_dup_scode2_GOCI6km, header_cn_stn_GOCI6km_location

    fname = f'stn_rf_day_{yr}.mat'
    matlab.loadmat(os.path.join(path_ea_goci, fname)) # 'stn_fill'
    
    for mm in range(1, 12+1):
        data_temp = stn_fill[stn_fill[:,2]==(mm-1),:]
        #         data_temp = stn_fill # yearly
        scode2_unq = np.unique(data_temp[:,12])
        data_avg = []
        for ss in range(matlab.length(scode2_unq)):
            data_temp2 = data_temp[data_temp[:,12]==scode2_unq[ss],:]
            data_temp2 = np.nanmean(data_temp2, axis=0)
            data_avg = np.concatenate((data_avg, data_temp2), axis=0)
        
        data_avg = data_avg[:,[12,9,10]] # scode2, stn_pm10, stn_pm
        
        for k in range(data_avg.shape[0]):
            data_avg[k,3:5]=stn_location[stn_location[:,1]==data_avg[k,0], 2,3]
            # scode2, stn_pm10, stn_pm25, lat_org, lon_org

        stnpm10 = data_avg[:,[0,1,3,4]]
        stnpm10 = stnpm10[~np.isnan(stnpm10).any(axis=1)] #rmmissing[stnpm10,0]

        korea_east = 132
        korea_west = 115
        korea_north = 47
        korea_south = 31
        
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplots(1,1,1, projection=ccrs.LambertConformal(central_longitude=(korea_east+korea_west)/2))
        ax.set_extent([korea_west, korea_east, korea_south, korea_north])
        ax.gridlines()
        ax.scatter(stnpm10[:, 3], stnpm10[:, 2], s=3, c=stnpm10[:,1], markeredgecolor='k')
        ax.set_title(f"{yr}/{mm:02d}", fontsize=14)
        ax.colorbar(fontsize=12)
        plt.show()   
        
        print('-djpeg','-r300', path_output,f'EA_GOCI6km/map/PM10_stn_monthly_{yr}_{mm:02d}')
        #         print('-djpeg','-r300',[path,'EA_GOCI6km/map/PM10_stn_yearly_',str(yr)])  # yearly
        
        stnpm25 = data_avg[:,[0,2,3,4]]
        stnpm25 = stnpm25[~np.isnan(stnpm25).any(axis=1)] #rmmissing(stnpm25,1)

        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplots(1,1,1,            projection=ccrs.LambertConformal(central_longitude=(korea_east+korea_west)/2))
        ax.set_extent([korea_west, korea_east, korea_south, korea_north])
        ax.gridlines()
        ax.scatter(stnpm25[:, 3], stnpm25[:, 2], s=3, c=stnpm25[:,1], markeredgecolor='k')
        ax.set_title(f"{yr}/{mm:02d}", fontsize=14)
        ax.colorbar(fontsize=12)
        plt.show()
        
        print('-djpeg','-r300',path_output,f'EA_GOCI6km/map/PM25_stn_monthly_{yr}_{mm:02d}')
        #         print('-djpeg','-r300',[path,'EA_GOCI6km/map/PM25_stn_yearly_',str(yr)]) # yearly
