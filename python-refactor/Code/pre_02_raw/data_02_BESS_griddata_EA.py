import os
import sys
project_path = '/home/cogito/Desktop/GEMS_python/matlab2python/python-refactor'
sys.path.insert(0, project_path)

from Code.utils.matlab import *

import numpy as np
#from matplotlib.pyplot import imread
from scipy.interploate import gridata

#% path_data = '//10.72.26.46/irisnas6/Data/Aerosol/';
#% path = '//10.72.26.46/irisnas5/Work/Aerosol/';

path_data = os.path.join('/', 'share', 'irisnas6', 'Data', 'Aerosol')
#% path = '/share/irisnas6/Data/Aerosol_Work/EA_GOCI6km/';
path_bess = os.path.join('/', 'share', 'irisnas6', 'Data', 'BESS', '00raw', 'BESS_RSDN_Daily')


mat = matlab.loadmat(os.path.join(path_data, 'grid', 'grid_bess.mat')) # lon_bess, lat_bess
lon_bess = mat['lon_bess']
lat_bess = mat['lat_bess'] 

mat = matlab.loadmat(os.path.join(path_data, 'grid', 'grid_goci.mat')) # lon_goci, lat_goci
lon_goci = mat['lon_goci']
lat_goci = mat['lat_goci']

#%% Until 2016 (nc)
"""
    % for yr=2016 %:2016
    %     cd([path_data2, '00_raw_data/BESS/BESS_RSDN_Daily/',num2str(yr)])
    %     list = dir('*.nc');
    %     list = {list.name}';
    %
    %     for i=20:22 % 1:length(list)
    %         bess = ncread(list{i}, 'surface_downwelling_shortwave_flux_in_air'); % 자료 읽기
    %         bess(bess==-9999)=NaN;
    %         RSDN = griddata(lon_bess,lat_bess,bess,lon_goci,lat_goci,'linear'); %리샘플링 (0.05 degree를 6km goci 격자로)
    %         save([path,'BESS/',num2str(yr),'/EA6km_BESS_RSDN_',num2str(yr),'_',list{i}(end-5:end-3),'.mat'],'RSDN')
    %         disp([list{i},'... i=',num2str(i),' \n'])
    %     end
    %     disp(yr)
    % end
"""
##  2017 (mat)
YEARS = [2017]
for yr in YEARS:
    os.chdir(os.path.join(path_bess, str(yr)))
    flist = matlab.get_files_endswith('.', '.mat')

    for k in range(len(flist)):
        bess = matlab.loadmat(flist[k])
        RSDN = griddata(zip(lon_bess, lat_bess), bess, zip(lon_goci, lat_goci), method='linear') # %리샘플링 (0.05 degree를 6km goci 격자로)
        fname = flist[-5:]
        matlab.savemat(os.path.join(path_data, 'DA_GOCI6km', 'BESS', str(yr)), f'EA6km_BESS_RSDN_{yr}_{fname}.mat', RSDN) 
        print (flist[k])

"""
    toc
    %%  전처리
    % %%lon
    % a = 89.975;
    % b = 0;
    % for i= 1:3600;
    % a(i,1) = a(1) - b;
    % b = b + 0.05;
    % end
    % for i=1:3600;
    % lon10 (i,:) = lon(1,:);
    % end
    %
    % %lat
    % a = -179.975;
    % b = 0;
    % for i= 1:7200;
    % a(1,i) = a(1) + b;
    % b = b + 0.05;
    % end
    %
    % for i=1:7200;
    % lat10 (:,i) = lat(:,1);
    % end
"""
