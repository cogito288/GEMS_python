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
data_base_dir = os.path.join('/', 'media', 'sf_GEMS', 'Data')
raw_data_path = os.path.join(data_base_dir, 'Raw', 'GOCI_AOD') 
write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_AOD')

### Setting period
YEARS = [2016] #, 2018, 2019]
MONTHS = range(1, 12+1)

GOCI_aod = np.full([473, 463], np.nan)
GOCI_fmf = np.full([473, 463], np.nan)
GOCI_ssa = np.full([473, 463], np.nan)
GOCI_ae = np.full([473, 463], np.nan)
GOCI_type = np.full([473, 463], np.nan)
GOCI_num_used_pixels = np.full([473, 463], np.nan)
GOCI_ndvi = np.full([473, 463], np.nan)
GOCI_dai = np.full([473, 463], np.nan)


for yr in YEARS:
    if yr%4==0: days = 366
    else: days = 365
    
    list_aod = glob.glob(os.path.join(write_path, 'AOD', str(yr), '*.mat'))
    list_aod = [os.path.basename(x) for x in list_aod]
    list_aod2 = [(int(x[14:17]), int(x[18:20])) for x in list_aod] # doy, utc 
    num_utc = 8
    
    list_doy = range(1, days+1)
    list_utc = range(num_utc)
    list_all = []
    for doy in list_doy:
        for utc in list_utc:
            list_all.append((doy, utc))
    list_all = np.asarray(list_all)

    list_aod2_to_index = [(doy-1)*num_utc+utc for doy, utc in list_aod2]
    all_index = set(list(range(len(list_all))))
    miss_index = list(all_index.difference(list_aod2_to_index))
    miss_list = list_all[miss_index]
                         
    for doy, utc in miss_list:
        fname_temp = f'{yr}_{doy:03d}_{utc:02d}.mat'
        
        matlab.savemat(
                   fname=os.path.join(write_path, 'AOD', str(yr),f'GOCI_AOD_{fname_temp}'),
                   data={'GOCI_aod':GOCI_aod})
        matlab.savemat(
                   fname=os.path.join(write_path, 'FMF', str(yr),f'GOCI_FMF_{fname_temp}'),
                   data={'GOCI_fmf':GOCI_fmf})
        matlab.savemat(
                   fname=os.path.join(write_path, 'SSA', str(yr),f'GOCI_SSA_{fname_temp}'),
                   data={'GOCI_ssa':GOCI_ssa})
        matlab.savemat(
                   fname=os.path.join(write_path, 'AE', str(yr),f'GOCI_SSA_{fname_temp}'),
                   data={'GOCI_ae':GOCI_ae})
        matlab.savemat(
                   fname=os.path.join(write_path, 'Type', str(yr),f'GOCI_Type_{fname_temp}'),
                   data={'GOCI_type':GOCI_type})
        matlab.savemat(
                   fname=os.path.join(write_path, 'No_of_Used_500m_Pixels_for_One_6km_Product_Pixel', str(yr),f'GOCI_num_used_pixels_{fname_temp}'),
                   data={'GOCI_num_used_pixels':GOCI_num_used_pixels})
        matlab.savemat(
                   fname=os.path.join(write_path, 'NDVI', str(yr),f'GOCI_NDVI_{fname_temp}'),
                   data={'GOCI_ndvi':GOCI_ndvi})
        matlab.savemat(
                   fname=os.path.join(write_path, 'DAI', str(yr),f'GOCI_DAI_{fname_temp}'),
                   data={'GOCI_dai':GOCI_dai})
        print (fname_temp)
    print (yr)