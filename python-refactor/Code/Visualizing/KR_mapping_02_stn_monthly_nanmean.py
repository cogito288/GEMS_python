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
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


path_data = '//10.72.26.46/irisnas6/Data/Aerosol/'
path = '//10.72.26.46/irisnas6/Work/Aerosol/'
# path_data = '/share/irisnas6/Data/Aerosol/'
# path = '/share/irisnas6/Work/Aerosol/'
# addpath(genpath('/share/irisnas6/Work/Aerosol/matlab_func/'))


tg = ['PM10','PM25']

## Load grid
matlab.loadmat(os.path.join(path_data,'grid/grid_korea.mat'])
mat = matlab.loadmat(os.path.join(path_data,'Station_Korea/stn_1km_location_weight.mat')) # stn_1km_location
stn_1km_location = mat['stn_1km_location']
del mat

stn_location = stn_1km_location
# scode1,scode2, lat_org, lon_org, pxid, lat_px, lon_px

##
YEARS = [2015, 2016]
for yr in YEARS:
    stn_fill = matlab.loadmat(os.path.join(path,f'Korea/cases/KR_1km_stn_rf_day_{yr}.mat'])['stn_fill'] # 'stn_fill'
 
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
        
        for k in range(1, data_avg.shape[0]): 
            data_avg[k,3:5]=stn_location[stn_location[:,1]==data_avg[k,0],2:4] 
            # scode2, stn_pm10, stn_pm25, lat_org, lon_org
        stnpm10 = data_avg[:,[0:2,2:5]]
        stnpm10 = stnpm10[~np.isnan(stnpm10, axis=0)] #rmmissing(stnpm10,1)
        east = 131.5
        west = 123
        north = 39
        south = 33
        
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplots(1,1,1, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()
        ax.scatter(stnpm10[:, 3], stnpm10[:, 2], s=3, c=stnpm10[:,1])
        ax.set_title(f"{yr}/{mm:02d}", fontsize=25)
        plt.show()   
        
        #figure set(gcf,'Position',[1000,100,900,800])
        #m_proj('lambert','long',[124 131.5],'lat',[33 39])
        #m_gshhs_i('color','k','linewidth',2)
        #m_grid('box','fancy','time.time()kdir','in','fontsize',20)
        #hold on
        #s = m_scatter(stnpm10[:,4),stnpm10[:,3),70, stnpm10[:,2),'filled') # stn_pm10
        #s.MarkerEdgeColor='k'
        #caxis([0 80])
        #title([str(yr),' / ',str(mm,'#02i')],'fontsize',25,'fontweight','bold')
#         title(str(yr),'fontsize',25,'fontweight','bold')  # yearly
        #colorbar('FontSize',18)
        print('-djpeg','-r300',[path,f'Korea/RF_pred/PM10_stn_monthly_{yr}_{mm:02d'])
#         print('-djpeg','-r300',[path,'Korea/RF_pred/PM10_stn_yearly_',str(yr)])  # yearly
        
        stnpm25 = data_avg[:,[0,2:5]]
        stnpm25 = stnpm25[~np.isnan(stnpm25, axis=0)] #rmmissing(stnpm25,1)
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplots(1,1,1, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()
        ax.scatter(stnpm25[:, 3], stnpm25[:, 2], s=3, c=stnpm25[:,1])
        ax.set_title(f"{yr}/{mm:02d}", fontsize=25)
        plt.show()   
        
        #figure set(gcf,'Position',[1000,100,900,800])
        #m_proj('lambert','long',[124 131.5],'lat',[33 39])
        #m_gshhs_i('color','k','linewidth',2)
        #m_grid('box','fancy','time.time()kdir','in','fontsize',20)
        #hold on
        #s = m_scatter(stnpm25[:,4),stnpm25[:,3),70, stnpm25[:,2),'filled') # stn_pm25
        #s.MarkerEdgeColor='k'
        #caxis([0 40])
        #title([str(yr),' / ',str(mm,'#02i')],'fontsize',25,'fontweight','bold')
#         title(str(yr),'fontsize',25,'fontweight','bold')  # yearly
        #colorbar('FontSize',18)
        print('-djpeg','-r300',[path,f'Korea/RF_pred/PM25_stn_monthly_{yr}_{mm:02}'])
#         print('-djpeg','-r300',[path,'Korea/RF_pred/PM25_stn_yearly_',str(yr)]) # yearly
#         
     # mm: month
 # yr
