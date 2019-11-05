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

### Setting path
data_base_dir = os.path.join('/', 'media', 'sf_GEMS_1', 'Data')
raw_data_path = os.path.join(data_base_dir, 'Raw', 'GOCI_AOD') 
write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_AOD')

path_root = '/share/irisnas6/Data/GEMS_code&data/'
path_data = [path_root,'data/']
path = [path_root,'output/RealTimeTraining/EastAsia/PM10/']
#addpath(genpath([path_root,'code/matlab_func/']))

tg = ['PM10','PM25']

## Load grid
matlab.loadmat(os.path.join(path_data,'grid/grid_goci.mat'])

##
YEARS = [2015, 2016]
for yr in YEARS:
    matlab.loadmat(os.path.join(path_data,'Station_Korea/stn_GOCI6km_location_weight.mat'))
    # stn_GOCI6km_location, dup_scode2_GOCI6km,header_stn_GOCI6km_location
    matlab.loadmat(os.path.join(path_data,'Station_CN/cn_stn_GOCI6km_location_weight.mat'))
    # cn_stn_GOCI6km_location, cn_dup_scode2_GOCI6km, header_cn_stn_GOCI6km_location
    
    stn_location = np.concatenate((stn_GOCI6km_location, cn_stn_GOCI6km_location), axis=0)
    # scode1,scode2, lat_org, lon_org, pxid, lat_px, lon_px

    del stn_GOCI6km_location, dup_scode2_GOCI6km, header_stn_GOCI6km_location
    del cn_stn_GOCI6km_location, cn_dup_scode2_GOCI6km, header_cn_stn_GOCI6km_location

    fname = f'stn_rf_day_{yr}.mat'
    matlab.loadmat(os.path.join(path,'EA_GOCI6km', fname)) # 'stn_fill'
    
    for mm in range(1, 12+1):
        data_temp = stn_fill[stn_fill[:,2]==(mm-1),:]
        #         data_temp = stn_fill # yearly
        scode2_unq = np.unique(data_temp[:,12])
        data_avg = []
        for ss in range(matlab.length(scode2_unq)):
            data_temp2 = data_temp[data_temp[:,12]==scode2_unq[ss],:]
            data_temp2 = np.nanmean[data_temp2,0]
            data_avg = np.concatenate((data_avg, data_temp2), axis=0)
        
        data_avg = data_avg[:,[12,9,10]] # scode2, stn_pm10, stn_pm
        
        for k in range(data_avg.shape[0]):
            data_avg[k,3:5]=stn_location[stn_location[:,1]==data_avg[k,0],2:4]
            # scode2, stn_pm10, stn_pm25, lat_org, lon_org

        stnpm10 = data_avg[:,[:2,3:5]]
        stnpm10 = rmmissing[stnpm10,0]

        fig, ax = plt.subplots(1,1,figsize=(10,5))
        # figure; set(gcf,'Position',[1000,500,500,450])
        m_proj('lambert','long',[115 132],'lat',[31 47])
        m_gshhs_i('color','k','linewidth',1.5)
        m_grid('box','fancy','time.time()kdir','in','fontsize',13)
        hold on
        s = m_scatter(stnpm10(:,4),stnpm10(:,3),30, stnpm10(:,2),'filled') # stn_pm10
        s.MarkerEdgeColor='k'
        caxis([0 150])
        title([str(yr),' / ',str(mm,'#02i')],'fontsize',14,'fontweight','bold')
#         title(str(yr),'fontsize',14,'fontweight','bold')  # yearly
        colorbar('FontSize',12)
        print('-djpeg','-r300',[path,'EA_GOCI6km/map/PM10_stn_monthly_',str(yr),'_',str(mm,'#02i')])
#         print('-djpeg','-r300',[path,'EA_GOCI6km/map/PM10_stn_yearly_',str(yr)])  # yearly
        
        stnpm25 = data_avg(:,[1,3:5])
        stnpm25 = rmmissing(stnpm25,1)
        figure set(gcf,'Position',[1000,500,500,450])
        m_proj('lambert','long',[115 132],'lat',[31 47])
        m_gshhs_i('color','k','linewidth',1.5)
        m_grid('box','fancy','time.time()kdir','in','fontsize',13)
        hold on
        s = m_scatter(stnpm25(:,4),stnpm25(:,3),30, stnpm25(:,2),'filled') # stn_pm25
        s.MarkerEdgeColor='k'
        caxis([0 60])
        title([str(yr),' / ',str(mm,'#02i')],'fontsize',14,'fontweight','bold')
#         title(str(yr),'fontsize',14,'fontweight','bold')  # yearly
        colorbar('FontSize',12)
        print('-djpeg','-r300',[path,'EA_GOCI6km/map/PM25_stn_monthly_',str(yr),'_',str(mm,'#02i')])
#         print('-djpeg','-r300',[path,'EA_GOCI6km/map/PM25_stn_yearly_',str(yr)]) # yearly
#         
    
     # mm: month
 # yr
