### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import glob
import time
import pandas as pd


### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km')

path_nox_korea = os.path.join(data_base_dir, 'Preprocessed_raw', 'NOX03', 'Korea')
matlab.check_make_dir(path_nox_korea)
path_korea_cases = os.path.join(data_base_dir, 'Preprocessed_raw', 'Korea', 'cases')

path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')
path_stn_cn = os.path.join(path_station, 'Station_CN')
path_stn_kr = os.path.join(path_station, 'Station_KR')

path_data = '/share/irisnas5/Data/'
path= '/share/irisnas5/GEMS/PM/00_EA6km/'
season_name = ['Spring','Summer','Fall','Winter']
season_name2 = ['MAM','JJA','SON','DJF']
type_list = ['conc','time','time_conc']
target = ['PM10','PM25']

## Load grid
mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_korea.mat'))
lat_kor, lon_kor = mat['lat_kor'], mat['lon_kor']
del mat

season_num = [61,153,245,336]
YEARS = [2016]
for t in [0,2]: #1:2:3
    for i in [0,1]:
        for yr in YEARS: #2015:2017
            if yr%4==0:
                days = 366
                daysInMonths = [31,29,31,30,31,30,31,31,30,31,30,31]
            else:
                days = 365
                daysInMonths = [31,28,31,30,31,30,31,31,30,31,30,31]
            fname = f"{target[i]}_RTT_EA6km_{yr}.mat"
            matlab.loadmat(os.path.join(path_ea_goci, 'RF_map/',type_list[t],target[i],'annual/',fname))

            for s in range(1,4+1):
                if s==4:
                    ssss = list(range(1, 60+1))+list(range(336,days+1))
                else:
                    ss = season_num[:,s-1:s+1]
                    sss= season_num[:,s]-1
                    ssss = list(range(ss,sss+1))
                
                season = annual[:,ssss]
                
                del ss, sss, ssss
                
                season_avg = np.reshape(np.nanmean(season,axis=1),lon_goci.shape)
                
                nan_ratio_ss = np.sum(np.isnp.full(season),axis=1)/season.shape[1]
                nan_ratio_ss = nan_ratio_ss.reshape(lon_goci.shape)
                
                season_avg_m = season_avg
                season_avg_m[nan_ratio_ss>0.95] = np.nan
                
                #reshaping and mapping
                m_kc_cloud(lon_goci,lat_goci,season_avg_m)
                #             colormap(jet)
                """
                if i==1
                    caxis([0 150])
                else
                    caxis([0 60])
                
                colorbar('FontSize',12)
                """
#                 mode_name = strrep(version{v},string('_'),string(' '))
                name_titile = f"{yr} {season_name[s]} ({season_name2[s]})"
                
                #hold on 
                #title(name_titile,'fontweight','bold','FontSize',16)
                
                #save map image
                name = os.path.join(path, 'RF_map/',type_list[t], target[i],'seasonal/', f"{target[i]}_RTT_season_map_{yr}_{season_name[s]}")
                print('-djpeg','-r300',name)
                #close all
    print (target[i])
print (type_list[t])



