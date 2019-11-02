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

### Setting path
data_base_dir = os.path.join('/', 'media', 'sf_GEMS_1', 'Data')
data_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_AOD') 
write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_filtered')

### Setting period
YEARS = [2016] #, 2018, 2019]
MONTHS = range(1, 12+1)

for yr in YEARS:
    if yr%4==0:
        days = 366
    else:
        days = 365
    if yr==2019:
        days = 147
        
    list_aod = glob.glob(os.path.join(data_path, 'AOD', str(yr), '*.mat'))
    list_aod = [os.path.basename(f) for f in list_aod]
    list_date = [x[9:20] for x in list_aod]
    for doy in range(1, days+1):
        mat = matlab.loadmat(os.path.join(write_path, 'nan_filter', f'nan_filter_{yr}_{doy:03d}.mat')) 
        nan_filter = mat['nan_filter']
        
        for m in range(1, 8+1):
            nan_utc = np.squeeze(nan_filter[:,:,m-1,:])
            nan_utc = np.sum(nan_utc, axis=2)
            nan_utc = nan_utc > 0
            
            fname = list_date[8*doy-8+m]
            mat = matlab.loadmat(os.path.join(data_path, 'AOD', str(yr), f'{list_aod[8*doy-8+m]}'))
            GOCI_aod = mat['GOCI_aod']
            mat = matlab.loadmat(os.path.join(data_path, 'FMF', str(yr), f'GOCI_FMF_{fname}.mat'))
            GOCI_fmf = mat['GOCI_fmf']
            mat = matlab.loadmat(os.path.join(data_path, 'SSA', str(yr), f'GOCI_SSA_{fname}.mat'))
            GOCI_ssa = mat['GOCI_ssa']
            mat = matlab.loadmat(os.path.join(data_path, 'AE', str(yr), f'GOCI_AE_{fname}.mat'))
            GOCI_ae = mat['GOCI_ae']
            mat = matlab.loadmat(os.path.join(data_path, 'Type', str(yr), f'GOCI_Type_{fname}.mat'))
            GOCI_type = mat['GOCI_type']
            mat = matlab.loadmat(os.path.join(data_path, 'NDVI', str(yr), f'GOCI_NDVI_{fname}.mat'))
            GOCI_ndvi = mat['GOCI_ndvi']
            mat = matlab.loadmat(os.path.join(data_path, 'DAI', str(yr), f'GOCI_DAI_{fname}.mat'))
            GOCI_dai = mat['GOCI_dai']
            
            GOCI_aod[nan_utc] = np.nan
            GOCI_fmf[nan_utc] = np.nan
            GOCI_ssa[nan_utc] = np.nan
            GOCI_ae[nan_utc] = np.nan
            GOCI_type[nan_utc] = np.nan
            GOCI_ndvi[nan_utc] = np.nan
            GOCI_dai[nan_utc] = np.nan 
            
            matlab.savemat(dirname=os.path.join(write_path, 'AOD', str(yr)),
                       fname=f'{list_aod[8*doy-8+m]}',
                       data={'GOCI_aod':GOCI_aod})
            matlab.savemat(dirname=os.path.join(write_path, 'FMF', str(yr)),
                       fname=f'GOCI_FMF_{fname}.mat',
                       data={'GOCI_FMF':GOCI_fmf})
            matlab.savemat(dirname=os.path.join(write_path, 'SSA', str(yr)),
                       fname=f'GOCI_SSA_{fname}.mat',
                       data={'GOCI_SSA':GOCI_ssa})
            matlab.savemat(dirname=os.path.join(write_path, 'AE', str(yr)),
                       fname=f'GOCI_AE_{fname}.mat',
                       data={'GOCI_ae':GOCI_ae})
            matlab.savemat(dirname=os.path.join(write_path, 'Type', str(yr)),
                       fname=f'GOCI_Type_{fname}.mat',
                       data={'GOCI_Type':GOCI_type})
            matlab.savemat(dirname=os.path.join(write_path, 'NDVI', str(yr)),
                       fname=f'GOCI_NDVI_{fname}.mat',
                       data={'GOCI_ndvi':GOCI_ndvi})
            matlab.savemat(dirname=os.path.join(write_path, 'DAI', str(yr)),
                       fname=f'GOCI_DAI_{fname}.mat',
                       data={'GOCI_dai':GOCI_dai})
            print (f'{doy:03d}_{m-1:02d}')
        print (f'doy: {doy}')
    print (f'Year: {yr}')