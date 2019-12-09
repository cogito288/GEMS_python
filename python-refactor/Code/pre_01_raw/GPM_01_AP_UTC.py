### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import glob
import copy

### Setting path
data_base_dir = os.path.join('/', 'media', 'sf_GEMS', 'Data')
raw_data_path = os.path.join(data_base_dir, 'Raw', 'GPM', '3IMERGHH') 
write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'GPM', 'AP_24h_hourly')

# Accumulated Precipitation : From the time in the day before To the time in the day
"""
% path_data = '//10.72.26.45/irisnas7/RAW_DATA/GPM/00raw/3IMERGHH/';
% path = '//10.72.26.45/irisnas7/RAW_DATA/GPM/01mat/AP_24h_hourly/';
path_data = '/share/irisnas7/RAW_DATA/GPM/00raw/3IMERGHH/';
path = '/share/irisnas7/RAW_DATA/GPM/01mat/AP_24h_hourly/';
"""

"""
name = '2014/3B-HHR.MS.MRG.3IMERG.20141231-S000000-E002959.0000.V04A.HDF5'
lat_gpm = matlab.h5read(os.path.join(raw_data_path, name), '/Grid/lat')
lon_gpm = matlab.h5read(os.path.join(raw_data_path, name), '/Grid/lon')
lat_gpm = np.float64(lat_gpm); lon_gpm = np.float64(lon_gpm)
lat_gpm, lon_gpm = np.meshgrid(lat_gpm, lon_gpm)
matlab.savemat('grid_gpm.mat', {'lon_gpm':lon_gpm, 'lat_gpm':lat_gpm})
"""

YEARS = [2016]
for yr in YEARS:
    list_gpm = glob.glob(os.path.join(raw_data_path, str(yr), '*/*.HDF5'))
    list_gpm.sort()
    doy0 = matlab.datenum(str(yr-1)+'1231')
    # First day UTC 00
    list_temp = list_gpm[:48]
   
    size = (1800, 3600, 24)
    gpm = np.zeros(size)
    doy = matlab.datenum(os.path.basename(list_temp[0])[21:29])-doy0+1
    print (f'doy: {doy}')
    for j, fname in enumerate(list_temp):
        gpm_temp = matlab.h5read(fname, '/Grid/precipitationCal')
        gpm_temp = np.float64(gpm_temp)
        gpm_temp[gpm_temp<-9999] = 0 #np.nan
        gpm_temp[np.isnan(gpm_temp)] = 0
        gpm[:,:,int(j/2)] += gpm_temp

    precip = np.nansum(gpm, axis=2)
    precip *= 0.5
    ap_fname = os.path.join(write_path, str(yr), f'gpm_AP_{yr}_{doy:03d}_UTC00.mat')
    print (f'Saving ... {ap_fname}')
    matlab.savemat(ap_fname, {'precip':precip})

    for aa in range(2, len(list_gpm)-48, 2):
        gpm[:, :, 0:23] = gpm[:, :, 1:]
        gpm[:, :, -1] = 0

        list_temp = list_gpm[aa+46:aa+48]
        doy = matlab.datenum(os.path.basename(list_gpm[aa])[21:29])-doy0+1
        UTC = os.path.basename(list_gpm[aa])[31:33]
        for j in range(2):
            print (f'Reading ... {list_temp[j]}')
            gpm_temp = matlab.h5read(list_temp[j], '/Grid/precipitationCal')
            gpm_temp = np.float64(gpm_temp)
            gpm_temp[gpm_temp<-9999] = 0 #np.nan
            gpm_temp[np.isnan(gpm_temp)] = 0
            gpm[:, :, -1] += gpm_temp
        
        precip = np.nansum(gpm, axis=2)
        precip *= 0.5
        ap_fname = os.path.join(write_path, str(yr), f'gpm_AP_{yr}_{doy:03d}_UTC{UTC}.mat')
        print (f'Saving ... {ap_fname}')
        matlab.savemat(ap_fname, {'precip':precip})
    print (year)
