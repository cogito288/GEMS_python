### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
#from matplotlib.pyplot import imread
from scipy.interploate import griddata

### Setting path
data_base_dir = os.path.join(project_path, 'Data')
path_read = os.path.join(data_base_dir, 'Preprocessed_raw', 'OMI', 'OMI_L3_tempConv') 
path_write = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km', 'OMI_tempConv')

mat = matlab.loadmat(os.path.join(data_base_dir, 'grid', 'grid_goci.mat')) # lon_goci, lat_goci
lon_goci = mat['lon_goci']
lat_goci = mat['lat_goci']
del mat

mat = matlab.loadmat(os.path.join(path_data, 'grid', 'grid_omi_25.mat')
lon_omi = mat['lon_omi'] 
lat_omi = mat['lat_omi']
del mat
                     
lon_omi = lon_omi[340:552, 1020:1308]
lat_omi = lat_omi[340:552, 1020,1308]
points = np.array(lat_omi.ravel(order='F'), lat_omi.ravel(order='F'))
del lon_omi, lat_omi

dlist = list(map(lambda x: x+matlab.datenum('20050000'), list(range(1, 5478+1))))
dvec = list(map(lambda x: matlab.datestr(x), dlist))
# np.arange(np.datetime64('2005-01-01'), np.datetime64('2019-12-31'))

pname_list = ['OMNO2d', 'OMSO2e_m', 'OMDOAO3e_m', 'OMHCHOG']
for pname in pname_list:
    if pname == 'OMNO2d':
        data_yr = matlab.loadmat(os.path.join(path_data, f'tempConv_{pname}_trop_CS_sigma1_2005_2019.mat')['data_yr']
    elif pname == 'OMSO2e_m':
        data_yr = matlab.loadmat(os.path.join(path_data, f'tempConv_{pname[:6]}_sigma2_2005_2019.mat')['data_yr']
    elif pname == 'OMDOAO3e_m':
        data_yr = matlab.loadmat(os.path.join(path_data, f'tempConv_{pname}_sigma1_2005_2019.mat')['data_yr']
    elif pname == 'OMHCHOG':
        data_yr = matlab.loadmat(os.path.join(path_data, f'tempConv_{pname}_sigma1_2005_2019.mat')['data_yr']
    
    data_conv_all = data_conv.reshape(212, 288, 5478)
    YEARS = [2016]
    for yr in YEARS:
        tStart = time.time()
        if yr%4==0: days = 366
        else: days = 365
        
        data_conv_yr = data_conv_all[:, :, [val.astype(object).year==yr for val in dvec]]
        
        for doy in range(1, days+1):
            values = data_conv_yr[:,:,doy-1].ravel(order='F')
            if pname == 'OMNO2d':
                omno2d = griddata(points, values, (lon_goci, lat_goci), methods='linear')
                matlab.savemat(os.path.join(path_write, f'{pname}_trop_CS', str(yr), 'EA6km_{pname}_trop_CS_{yr}_{doy:03d}.mat'), 
                               {'omno2d':omno2d})
            elif pname == 'OMSO2e_m':
                omso2e_m = griddata(points, values, (lon_goci, lat_goci), methods='linear')
                matlab.savemat(os.path.join(path_write, pname, str(yr), 'EA6km_{pname}_{yr}_{doy:03d}.mat'), 
                               {'omso2e_m':omso2e_m})
            elif pname == 'OMDOAO3e_m':
                omdoao3e_m = griddata(points, values, (lon_goci, lat_goci), methods='linear')
                matlab.savemat(os.path.join(path_write, pname, str(yr), 'EA6km_{pname}_{yr}_{doy:03d}.mat'), 
                               {'omdoao3e_m':omdoao3e_m})
            elif pname == 'OMHCHOG':
                omhchog = griddata(points, values, (lon_goci, lat_goci), methods='linear')
                matlab.savemat(os.path.join(path_write, pname, str(yr), 'EA6km_{pname}_{yr}_{doy:03d}.mat'),
                              {'omhchog':omhchog})
            print (f'{pname}_{yr}_{doy:03d}')
        tElapsed = time.time() - tStart
        print (f'{pname}_{yr} ... {tElapsed:3.2f}, sec')