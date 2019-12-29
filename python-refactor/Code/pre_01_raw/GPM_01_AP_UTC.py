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
import time

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_gpm_raw = os.path.join(data_base_dir, 'Raw', 'GPM', '3IMERGHH') 
path_gpm_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'GPM', 'AP_24h_hourly')

YEARS = [2016]
for yr in YEARS:
    list_gpm = glob.glob(os.path.join(path_gpm_raw, str(yr), '*/*.HDF5'))
    list_gpm.sort()
    doy0 = matlab.datenum(str(yr-1)+'1231')
    # First day UTC 00
    list_temp = list_gpm[:48]
   
    size = (1800, 3600, 48)
    gpm = np.zeros(size)
    doy = matlab.datenum(os.path.basename(list_temp[0])[21:29])-doy0+1
    print (f'doy: {doy}')
    for j, fname in enumerate(list_temp[:48]):
        gpm_temp = matlab.h5read(fname, '/Grid/precipitationCal')
        gpm_temp = np.float64(gpm_temp)
        gpm_temp[gpm_temp<-9999] = np.nan
        gpm[:,:,j] += gpm_temp

    precip = np.nansum(gpm, axis=2)
    precip *= 0.5
    ap_fname = os.path.join(path_gpm_processed, str(yr), f'gpm_AP_{yr}_{doy:03d}_UTC00.mat')
    print (f'Saving ... {ap_fname}')
    matlab.savemat(ap_fname, {'precip':precip})

    #for aa in range(2, len(list_gpm), 2):
    for aa in range(2, len(list_gpm)-48+1, 2):
        tStart = time.time()
        gpm[:, :, 0:46] = gpm[:, :, 2:]
        gpm[:, :, -1] = 0
        gpm[:, :, -2] = 0

        #list_temp = list_gpm[aa:aa+2]
        list_temp = list_gpm[aa+45:aa+48]
        doy = matlab.datenum(os.path.basename(list_gpm[aa])[21:29])-doy0+1
        UTC = os.path.basename(list_gpm[aa])[31:33]
        for j in range(2):
            print (f'Reading ... {list_temp[j]}')
            gpm_temp = matlab.h5read(list_temp[j], '/Grid/precipitationCal')
            gpm_temp = np.float64(gpm_temp)
            gpm_temp[gpm_temp<-9999] = np.nan
            gpm[:, :, 46+j] = gpm_temp
        
        precip = np.nansum(gpm, axis=2)
        precip *= 0.5
        ap_fname = os.path.join(path_gpm_processed, str(yr), f'gpm_AP_{yr}_{doy:03d}_UTC{UTC}.mat')
        print (f'Saving ... {ap_fname}')
        matlab.savemat(ap_fname, {'precip':precip})
        tElapsed = time.time() - tStart
        print (f'time taken : {tElapsed}')
    print (yr)
