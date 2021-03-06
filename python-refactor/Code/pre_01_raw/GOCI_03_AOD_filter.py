### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import glob
import time
from numba import njit

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_goci_aod = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_AOD')
path_goci_filter = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_filtered')

### Setting period
YEARS = [2016] #, 2018, 2019]
num_utc = 8

@njit # for speed up using numba
def moving_window_2d(utc, bfr_arr, nan_arr):
    # arr is GOCI_aod_bfr
    for j in range(3, 465+1):
        for i in range(3, 475+1):
            box = bfr_arr[i-3:i+2, j-3:j+2]
            # 1. Buddy check: No. of available 5 x 5 pixels < 15
            # → masking a center pixel
            numnan = np.sum(np.isnan(box))
            if numnan > 10:
                nan_arr[i-3, j-3, utc-1, 0] = 1
            # 2. Local variance check : AOD variance of  5 x 5 pixels > 0.5
            # → masking a center pixel
            box_var = np.nanvar(box.T.flatten()) #, ddof=1)
            if box_var > 0.5:
                nan_arr[i-3, j-3, utc-1, 0] = 1
    return nan_arr


for yr in YEARS:
    if yr%4==0: days = 366
    else: days = 365
    if yr==2019:
        days = 148
    
    list_aod = glob.glob(os.path.join(path_goci_aod, 'AOD', str(yr), '*.mat'))
    list_aod = [os.path.basename(f) for f in list_aod]
    list_aod.sort()
    list_date = [x[9:20] for x in list_aod]

    for doy in range(1, days+1):
        nan_filter = np.zeros((473, 463, 8, 4))
        data = np.full([473, 463, 8], np.nan)    
        for utc in range(num_utc):
            tStart = time.time()
            fname = os.path.join(path_goci_aod, 'AOD', 
                                 str(yr), f'GOCI_AOD_{yr}_{doy:03d}_{utc:02d}.mat')
            GOCI_aod = matlab.loadmat(fname)['GOCI_aod']
            data[:, :, utc] = GOCI_aod

            fname = os.path.join(path_goci_aod, 'No_of_Used_500m_Pixels_for_One_6km_Product_Pixel', 
                                 str(yr), f'GOCI_num_used_pixels_{yr}_{doy:03d}_{utc:02d}.mat')
            GOCI_num_used_pixels = matlab.loadmat(fname)['GOCI_num_used_pixels']

            GOCI_aod_bfr = np.full([477, 467], np.nan) # buffer for 5x5 moving windows
            GOCI_aod_bfr[2:-2, 2:-2] = GOCI_aod

            nan_filter = moving_window_2d(utc, GOCI_aod_bfr, nan_filter)

            # 3. Sub-pixel cloud fraction check: Cloud fraction of each 6 km resolution pixel > 0.25
            # → masking a pixel
            cf = np.divide((58 - GOCI_num_used_pixels), 58)
            cf_idx = cf > 0.25
            nan_filter[:, :, utc, 2] = cf_idx

        # 4. Diurnal variation check: (Maximum - Mininum) of AOD > 0.74
        # → masking pixels
        data_min = np.nanmin(data, axis=2)
        data_max = np.nanmax(data, axis=2)
        data_diff = data_max - data_min
        d_idx = data_diff > 0.74
        d_idx = d_idx[:, :, None]
        nan_filter[:, :, :, 3] = np.tile(d_idx, (1, 1, 8))
        print (nan_filter.sum())
        fname = f'nan_filter_{yr}_{doy:03d}.mat'
        matlab.savemat(os.path.join(path_goci_filter, 'nan_filter', fname), {'nan_filter':nan_filter})
        tElapsed = time.time() - tStart
        print (f'time taken : {tElapsed}')
        print (f'Created {fname}')
    print (yr)
