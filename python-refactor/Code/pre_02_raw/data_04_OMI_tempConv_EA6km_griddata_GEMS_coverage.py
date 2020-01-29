### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import time
import numpy as np
from scipy.interpolate import griddata

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_omi_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'OMI') # Read
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km') 
path_ea_goci_omi = os.path.join(path_ea_goci, 'OMI_tempConv') # Write

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_goci.mat')) # lon_goci, lat_goci
lon_goci, lat_goci = mat['lon_goci'], mat['lat_goci']
del mat

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_omi_25.mat'))
lon_omi, lat_omi = mat['lon_omi'], mat['lat_omi']
del mat

lon_omi = lon_omi[340:560, 1020:1320]
lat_omi = lat_omi[340:560, 1020,1320]

points = np.array([lon_omi.ravel(order='F'), lat_omi.ravel(order='F')]).T
del lon_omi, lat_omi
print (f'points shape : {points.shape}')

dlist = list(map(lambda x: x+matlab.datenum('20050000'), list(range(1, 5478+1))))
dvec = list(map(lambda x: matlab.datestr(x), dlist))

pname_list = ['OMNO2d', 'OMSO2e_m', 'OMDOAO3e_m', 'OMHCHOG']
for pname in pname_list:
    if pname == 'OMNO2d':
        data_conv = matlab.loadmat(os.path.join(path_omi_processed, f'tempConv_{pname}_trop_CS_sigma1_2005_2019.mat'))['data_conv']
    elif pname == 'OMSO2e_m':
        data_conv = matlab.loadmat(os.path.join(path_omi_processed, f'tempConv_{pname[:6]}_sigma2_2005_2019.mat'))['data_conv']
    elif pname == 'OMDOAO3e_m':
        data_conv = matlab.loadmat(os.path.join(path_omi_processed, f'tempConv_{pname}_sigma1_2005_2019.mat'))['data_conv']
    elif pname == 'OMHCHOG':
        data_conv = matlab.loadmat(os.path.join(path_omi_processed, f'tempConv_{pname}_sigma1_2005_2019.mat'))['data_conv']
    
    data_conv_all = data_conv.reshape(220, 300, 5478)
    YEARS = [2016]
    for yr in YEARS:
        if yr%4==0: days = 366
        else: days = 365
        
        #data_conv_yr = data_conv_all[:, :, [val.astype(object).year==yr for val in dvec]]       
        data_conv_yr = data_conv_all[:, :, map(lambda x: x.astpye(object).year==yr)]
        #data_conv_yr = data_conv_all(:,:,dvec(:,1)==yr);
        
        for doy in range(1, days+1):
            tStart = time.time()
            values = data_conv_yr[:,:,doy-1].ravel(order='F')
            if pname == 'OMNO2d':
                omno2d = griddata(points, values, (lon_goci, lat_goci), 'linear')
                matlab.savemat(os.path.join(path_ea_goci_omi, f'{pname}_trop_CS', str(yr), f'EA6km_{pname}_trop_CS_{yr}_{doy:03d}.mat'), 
                               {'omno2d':omno2d})
            elif pname == 'OMSO2e_m':
                omso2e_m = griddata(points, values, (lon_goci, lat_goci), 'linear')
                matlab.savemat(os.path.join(path_ea_goci_omi, pname, str(yr), f'EA6km_{pname}_{yr}_{doy:03d}.mat'), 
                               {'omso2e_m':omso2e_m})
            elif pname == 'OMDOAO3e_m':
                omdoao3e_m = griddata(points, values, (lon_goci, lat_goci), 'linear')
                matlab.savemat(os.path.join(path_ea_goci_omi, pname, str(yr), f'EA6km_{pname}_{yr}_{doy:03d}.mat'), 
                               {'omdoao3e_m':omdoao3e_m})
            elif pname == 'OMHCHOG':
                omhchog = griddata(points, values, (lon_goci, lat_goci), 'linear')
                matlab.savemat(os.path.join(path_ea_goci_omi, pname, str(yr), f'EA6km_{pname}_{yr}_{doy:03d}.mat'),
                              {'omhchog':omhchog})
            print (f'{pname}_{yr}_{doy:03d}')
            tElapsed = time.time() - tStart
            print (f'{pname}_{yr} ... {tElapsed:3.2f}, sec')