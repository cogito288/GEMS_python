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
import time
import pandas as pd


# path_data = '//10.72.26.46/irisnas6/Data/Aerosol/'
# path = '//10.72.26.46/irisnas6/Work/NOXO3/Korea/'

path_data = '/share/irisnas6/Data/Aerosol/'
path = '/share/irisnas6/Work/NOXO3/Korea/'
#addpath(genpath('/share/irisnas6/Work/Aerosol/matlab_func/'))

matlab.loadmat(os.path.join(path_data,'grid/grid_korea.mat'])
m_bnd = m_shaperead([path,'boundary/BND_SIDO_GCS'])

# sel_NO2 = [1,3:4,7:17,21:24,28:49,53]
# sel_O3 = [1:23,25,28:49,53]

yr=2015
# yr=2016

if yr%4==0: days = 366
else: days = 365


nanidx_no2 = matlab.loadmat(os.path.join(path,f'cases/nanidx_no2_{yr}.mat'))['nanidx_no2'] # nanidx_no2
nanidx_o3 = matlab.loadmat(os.path.join(path,f'cases/nanidx_o3_{yr}.mat'))['nanidx_o3'] # nanidx_o3

fname0 = 'FBselected'

for doy in range(1,days+1):
    fname = f"{yr}_{doy:03d}"
    
    data_no2 = pd.read_csv(os.path.join(path,'RF_pred/NO2_',fname0, f'/rf_NO2_{fname0}_log_cases_{fname}_04.csv'))
    if np.sum(nanidx_no2[:,doy]) < 231340:
        data_no2[nanidx_no2[:,doy]==1] = np.nan
        data_no2 = data_no2.reshape(lat_kor.shape)

        fig = matlab.m_kor(lon_kor,lat_kor,data_no2)
        ax = fig.axes
        
        #caxis([0 30])
        #hold on
        for k in range(len(m_bnd.ncst)):
            #m_line(m_bnd.ncst{k}[:,1),m_bnd.ncst{k}[:,2),'color','k','linewidth',1)
            ax.plot(m_bnd.ncst[k][:, 0], m_bnd.ncst[k][:, 1], c='k')
        #colorbar('FontSize',18)
        print('-djpeg','-r300',[path,f'map/RF_{fname0}_NO2/NO2_{fname}_04'])
    
    
    data_o3 = pd.read_csv(os.path.join(path,f'RF_pred/O3_{fname0}/rf_O3_{fname0}_log_cases_{fname}_04.csv'))
    if np.sum(nanidx_o3[:,doy]) < 231340:
        data_o3[nanidx_o3[:,doy]==1] = np.nan
        data_o3 = data_o3.reshape(lat_kor.shape)
        
        fig = matlab.m_kor(lon_kor,lat_kor,data_o3)
        ax = fig.axes
        
        #m_kor(lon_kor,lat_kor,data_o3)
        #caxis([0 80])
        #hold on
        for k in range(len(m_bnd.ncst)):
            #m_line(m_bnd.ncst{k}[:,1),m_bnd.ncst{k}[:,2),'color','k','linewidth',1)
            ax.plot(m_bnd.ncst[k][:, 0], m_bnd.ncst[k][:, 1], c='k')
        
        #colorbar('FontSize',18)
        print('-djpeg','-r300',[path,f'map/RF_{fname0}_O3/O3_{fname}_04'])
    print (fname)

