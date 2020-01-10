import os
import sys
project_path = '/home/cogito/Desktop/GEMS_python/matlab2python/python-refactor'
sys.path.insert(0, project_path)

from Code.utils import matlab

import numpy as np
#from matplotlib.pyplot import imread
from scipy.interploate import griddata
import time

#% path_data = '//10.72.26.56/irisnas5/Data/';
#% path = '//10.72.26.56/irisnas5/Data/EA_GOCI6km/';
path_data = os.path.join('/', 'share', 'irisnas5', 'Data')
path = os.path.join('/', 'share', 'irisnas5', 'Data', 'EA_GOCI6km')
#% addpath(genpath([path_data,'/matlab_func/']))  % Add the path of external function (matlab_func) folder with subfolders

matlab.loadmat(os.path.join(path_data, 'grid', 'grid_goci.mat')
mat = matlab.loadmat(os.path.join(path_data, 'grid', 'grid_omi_25.mat'))
lon_omi = mat['lon_omi'] 
lat_omi = mat['lat_omi']

lon_omi = lon_omi[340:560, 1020:1320]
lat_omi = lat_omi[340:560, 1020,1320]

dlist = map(lambda x: x+matlab.datenum('20050000'), list(range(1, 5478+1)))
dvec = map(lambda x: matlab.datestr(x), dlist) 
# np.arange(np.datetime64('2005-01-01'), np.datetime64('2019-12-31'))

for p in [1] # [1,2,3,4]
	if p == 1:
		pname = 'OMNO2d'
		matlab.loadmat(os.path.join(path_data, 'pre', 'OMI_tempConv'), f'tempConv_{pname}_trop_CS_sigma1_2005_2019.mat')
	elif: p == 2:
		pname = 'OMSO2e_m'
		matlab.loadmat(os.path.join(path_data, 'pre', 'OMI_tempConv'), f'tempConv_{pname[:6]}_sigma2_2005_2019.mat')
	elif p == 3:
		pname = 'OMDOAO3e_m'
		matlab.loadmat(os.path.join(path_data, 'pre', 'OMI_tempConv'), f'tempConv_{pname}_sigma1_2005_2019.mat')
	else:
        pname = 'OMHCHOG'
		matlab.loadmat(os.path.join(path_data, 'pre', 'OMI_tempConv'), f'tempConv_{pname}_sigma1_2005_2019.mat')
    
    #%     data2 = reshape(data,[220,300,5478]);
    data_conv_all = data_conv.reshape(220, 300, 5478)
   	YEARS = list(range(2017, 2019+1))
	for yr in YEARS:
		tStart = time.time()
		if yt%4==0:
			days = 366
		else:
			days = 365
       
        data_conv_yr = data_conv_all[:, :, map(lambda x: x.astpye(object).year==yr)]
        #data_conv_yr = data_conv_all(:,:,dvec(:,1)==yr);
        
        for doy in range(days):
            data_temp = data_conv_yr[:,:,doy]
            if p == 1:
                omno2d = griddata(zip(lon_omi, lat_omi), data_temp, zip(lon_goci, lat_goci), methods='linear')
                matlab.savemat(os.path.join(path, 'OMI_tempConv', f'{pname}_trop_CS_{yr}'), 'EA6km_{pname}_trop_CS_{yr}_{doy:03d}.mat', omno2d)
            elif p == 2:
                omso2e_m = griddata(zip(lon_omi, lat_omi), data_temp, zip(lon_goci, lat_goci), methods='linear')
                matlab.savemat(os.path.join(path, 'OMI_tempConv', pname, str(yr), 'EA6km_{pname}_{yr}_{doy:03d}.mat', omso2e_m)
            elif p == 3:
                omdoao3e_m = griddata(zip(lon_omi, lat_omi), data_temp, zip(lon_goci, lat_goci), methods='linear')
                matlab.savemat(os.path.join(path, 'OMI_tempConv', pname, str(yr), 'EA6km_{pname}_{yr}_{doy:03d}.mat', omdoao3e_m)
            else:
                omhchog = griddata(zip(lon_omi, lat_omi), data_temp, zip(lon_goci, lat_goci), methods='linear')
                matlab.savemat(os.path.join(path, 'OMI_tempConv', pname, str(yr), 'EA6km_{pname}_{yr}_{doy:03d}.mat', omhchog)
            print (f'{pname}_{yr}_{doy:03d}')
        tElapsed = time.time() - tStart
        print (f'{pname}_{yr} ... {tElapsed:3.2f}, sec')

