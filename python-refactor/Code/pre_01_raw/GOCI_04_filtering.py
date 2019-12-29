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

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_goci_aod = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_AOD')
path_goci_filter = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_filtered')

### Setting period
YEARS = [2016] #, 2018, 2019]
num_utc = 8

for yr in YEARS:
    if yr%4==0: days = 366
    else: days = 365
    if yr==2019:
        days = 147
        
    list_aod = glob.glob(os.path.join(path_goci_aod, 'AOD', str(yr), '*.mat'))
    list_aod = [os.path.basename(f) for f in list_aod]
    list_aod.sort()
    list_date = [x[9:20] for x in list_aod]
    for doy in range(1, days+1):
        fname = os.path.join(path_goci_filter, 'nan_filter', f'nan_filter_{yr}_{doy:03d}.mat')
        nan_filter = matlab.loadmat(fname)['nan_filter']

        for utc in range(num_utc):
            tStart = time.time()
            nan_utc = np.squeeze(nan_filter[:,:,utc,:])
            nan_utc = np.sum(nan_utc, axis=2)
            nan_utc = nan_utc > 0


            def do_mask_nan_utc(fname, key):
                read_name = os.path.join(path_goci_aod, fname)
                write_name = os.path.join(path_goci_filter, fname)

                arr = matlab.loadmat(read_name)[key]
                arr[nan_utc] = np.nan
                matlab.savemat(fname=write_name, data={key:arr})

            key = 'GOCI_aod'
            fname = os.path.join('AOD', str(yr), f'GOCI_AOD_{yr}_{doy:03d}_{utc:02d}.mat')
            do_mask_nan_utc(fname, key)

            key = 'GOCI_fmf'
            fname = os.path.join('FMF', str(yr), f'GOCI_FMF_{yr}_{doy:03d}_{utc:02d}.mat')
            do_mask_nan_utc(fname, key)

            key = 'GOCI_ssa'
            fname = os.path.join('SSA', str(yr), f'GOCI_SSA_{yr}_{doy:03d}_{utc:02d}.mat')
            do_mask_nan_utc(fname, key)

            key = 'GOCI_ae'
            fname = os.path.join('AE', str(yr), f'GOCI_AE_{yr}_{doy:03d}_{utc:02d}.mat')
            do_mask_nan_utc(fname, key)

            key = 'GOCI_type'
            fname = os.path.join('Type', str(yr), f'GOCI_Type_{yr}_{doy:03d}_{utc:02d}.mat')
            do_mask_nan_utc(fname, key)

            key = 'GOCI_ndvi'
            fname = os.path.join('NDVI', str(yr), f'GOCI_NDVI_{yr}_{doy:03d}_{utc:02d}.mat')
            do_mask_nan_utc(fname, key)

            key = 'GOCI_dai'
            fname = os.path.join('DAI', str(yr), f'GOCI_DAI_{yr}_{doy:03d}_{utc:02d}.mat')
            do_mask_nan_utc(fname, key)
            tElapsed = time.time() - tStart
            print (f'time taken : {tElapsed}')
            print (f'{doy:03d}_{utc:02d}')
        print (f'doy: {doy}')
    print (f'Year: {yr}')
