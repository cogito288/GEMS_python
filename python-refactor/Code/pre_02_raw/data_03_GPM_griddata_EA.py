import os
import sys
project_path = '/home/cogito/Desktop/GEMS_python/matlab2python/python-refactor'
sys.path.insert(0, project_path)

from Code.utils.matlab import *

import numpy as np
#from matplotlib.pyplot import imread
from scipy.interploate import griddata

#% path_data = '//10.72.26.56/irisnas5/Data/';
#% path_gpm = '//10.72.26.45/irisnas7/RAW_DATA/GPM/01mat/AP_24h_hourly/';

path_data = os.path.join('/', 'share', 'irisnas6', 'Data')
path_gpm = os.path.join('/', 'share', 'irisnas7', 'RAW_Data', 'GPM', '01mat', 'AP_24h_hourly')
# % addpath(genpath('/share/irisnas6/Work/Aerosol/matlab_func/'))

mat = matlab.loadmat(os.path.join(path_data, 'grid', 'grid_goci.mat'))
lat_goci = mat['lat_goci']
lat_goci = mat['lon_goci']

mat = matlab.loadmat(os.path.join(path_data, 'grid', 'grid_gpm.mat'))
lat_gpm = mat['lat_gpm']
lon_gpm = mat['lon_gpm']

lat_gpm = lat_gpm[1100:1400, 2900:3300] # N50 W110 S20 E150
lon_gpm = lon_gpm[1100:1400, 2900:3300] 

YEARS = [2018]
for yr in YEARS:
	flist = matlab.get_files_end_wth(os.path.join(path_gpm, str(yr)), '.mat')
	for i in range(7001-1, len(flist)+1):
		precip = matlab.loadmat(flist[i])
		precip = precip[1100:1400, 2900:3300]
		precip = griddata(zip(lon_gpm, lat_gpm), precip, zip(lon_goci, lat_goci), method='linear')
		mathalb.savemat(os.path.join(path_data, 'EA_GOCI6km', 'GPM_AP', str(yr)), f'EA6km_{flist[i]}.mat', precip)
		print (flist[i][7:-4], f'...i={i}')

   	print (yr)

