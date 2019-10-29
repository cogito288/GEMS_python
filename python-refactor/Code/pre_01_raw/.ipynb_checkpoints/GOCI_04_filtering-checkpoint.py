### Package Import
import os
import scipy.io as sio

import sys
project_path = '/home/cogito/Uncertainty/matlab2python/python-refactor'
sys.path.insert(0, project_path)

from Code.utils.matlab import *
from Code.utils.helpers import *

### Setting path
# path_data = '/share/irisnas6/Data/GOCI_AOD/01mat/GOCI/';
# path = '/share/irisnas6/Data/GOCI_AOD/01mat/GOCI_filtered/';
data_path = os.path.join(project_path, 'Data', 'Prepreossed_raw', 'GOCI_AOD') 
write_path = os.path.join(project_path, 'Data', 'Prepreossed_raw', 'GOCI_filtered')
os.chdir(data_path)


YEARS = [2018, 2019]
MONTHS = range(1, 12+1)

for yr in YEARS:
    days = 366 if (yr%4)==0 else 365
    if yr==2019: days = 147;
    
    list_aod = get_file_lists(os.path.join(data_path, 'AOD', str(yr)), '.mat')
    list_date = list(map(lambda x: int(x[9:20]), list_aod))
    
    for doy in range(1, days+1):
        nan_filter = sio.loadmat(os.path.join(write_path, 'nan_filter', f'nan_filter_{yr}_{doy:03d}.mat')) 
        
        for m in range(1, 8+1):
            nan_utc = np.sqeeze(nan_filter[:,:,m-1,:])
            nan_utc = np.sum(nan_utc, axis=2)
            nan_utc = nan_utc > 0
            
            fname = list_data[8*doy-8+m, :]
            GOCI_aod = sio.loadmat(os.path.join('AOD', str(yr), f'list_aod[8*doy-8+m].mat'))
            GOCI_fmf = sio.loadmat(os.path.join('FMF', str(yr), f'GOCI_FMF_{fname}.mat'))
            GOCI_ae = sio.loadmat(os.path.join('AE', str(yr), f'GOCI_AE_{fname}.mat'))
            GOCI_type = sio.loadmat(os.path.join('Type', str(yr), f'GOCI_Type_{fname}.mat'))
            GOCI_ndvi = sio.loadmat(os.path.join('NDVI', str(yr), f'GOCI_NDVI_{fname}.mat'))
            GOCI_dai = sio.loadmat(os.path.join('DAI', str(yr), f'GOCI_DAI_{fname}.mat'))
            
            GOCI_aod[nan_utc] = np.nan
            GOCI_fmf[nan_utc] = np.nan
            GOCI_ssa[nan_utc] = np.nan
            GOCI_ae[nan_utc] = np.nan
            GOCI_type[nan_utc] = np.nan
            GOCI_ndvi[nan_utc] = np.nan
            GOCI_dai[nan_utc] = np.nan 
            
            sio.savemat(os.path.join(write_path, 'AOD', str(yr), f'list_aod{8*doy-8+m}.mat'), mdict={'GOCI_aod':GOCI_aod})  
            sio.savemat(os.path.join(write_path, 'FMF', str(yr), f'GOCI_FMF_{fname}.mat'), mdict={'GOCI_fmf':GOCI_fmf})
            sio.savemat(os.path.join(write_path, 'SSA', str(yr), f'GOCI_SSA_{fname}.mat'), mdict={'GOCI_ssa':GOCI_ssa})
            sio.savemat(os.path.join(write_path, 'AE', str(yr), f'GOCI_AE_{fname}.mat'), mdict={'GOCI_ae':GOCI_ae})
            sio.savemat(os.path.join(write_path, 'Type', str(yr), f'GOCI_Type_{fname}.mat'), mdict={'GOCI_Type':GOCI_Type})
            sio.savemat(os.path.join(write_path, 'NDVI', str(yr), f'GOCI_NDVI_{fname}.mat'), mdict={'GOCI_ndvi':GOCI_ndvi})
            sio.savemat(os.path.join(write_path, 'DAI', str(yr), f'GOCI_DAI_{fname}.mat'), mdict={'GOCI_dai':GOCI_dai})
            print (f'{doy:03d}_{m-1:02d}')