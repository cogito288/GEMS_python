### Package Import
import sys
import os
base_dir = os.environ['PWD'] # os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)

from Code.utils import matlab
#from Code.utils import helpers

import scipy.io as sio
import numpy as np
import glob

### Setting path
raw_data_path = os.path.join(project_path, 'Data', 'Raw', 'GOCI_AOD') 
write_path = os.path.join(project_path, 'Data', 'Prepreossed_raw', 'GOCI_AOD')

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
    days = 366 if (yr%4)==0 else 365
    
    list_aod = glob.glob(os.path.join('AOD', str(yr), ".mat")
    list_aod2 = list(map(lambda x: (int(x[14:17]), int(x[18:20]))))   # doy, utc 
    num_utc = 8
    list_doy = np.tile(range(1,days+1),(num_utc,1))
    list_utc = np.tile(range(num_utc),(1,days))
    list_all = np.vstack((list_doy.T.flatten(), list_utc.flatten())).T
    isNotDateExist = np.full(len(list_all), True)
    isNotDateExist[[doy*8+utc for doy, utc in list_aod2]] = False
                         
    miss_list = list_all[isNotDateExist, :]
    for k in range(len(miss_list)):
        fname_temp = f'{yr}_{miss_list[k][0]:03d}_{miss_list[k][1]:02d}.mat'
        matlab.savemat(dirname=os.path.join(write_path, 'AOD', str(yr)),
                   fname=f'GOCI_AOD_{fname_temp}',
                   data={'GOCI_aod':GOCI_aod})
        matlab.savemat(dirname=os.path.join(write_path, 'FMF', str(yr)),
                   fname=f'GOCI_FMF_{fname_temp}',
                   data={'GOCI_FMF':GOCI_fmf})
        matlab.savemat(dirname=os.path.join(write_path, 'SSA', str(yr)),
                   fname=f'GOCI_SSA_{fname_temp}',
                   data={'GOCI_SSA':GOCI_ssa})
        matlab.savemat(dirname=os.path.join(write_path, 'AE', str(yr)),
                   fname=f'GOCI_AE_{fname_temp}',
                   data={'GOCI_ae':GOCI_ae})
        matlab.savemat(dirname=os.path.join(write_path, 'Type', str(yr)),
                   fname=f'GOCI_Type_{fname_temp}',
                   data={'GOCI_Type':GOCI_type})
        matlab.savemat(dirname=os.path.join(write_path, 'No_of_Used_500m_Pixels_for_One_6km_Product_Pixel', str(yr)),
                   fname=f'GOCI_num_used_pixels_{fname_temp}',
                   data={'GOCI_num_used_pixels':GOCI_num_used_pixels})
        matlab.savemat(dirname=os.path.join(write_path, 'NDVI', str(yr)),
                   fname=f'GOCI_num_used_pixels_{fname_temp}',
                   data={'GOCI_ndvi':GOCI_ndvi})
        matlab.savemat(dirname=os.path.join(write_path, 'DAI', str(yr)),
                   fname=f'GOCI_DAI_{fname_temp}',
                   data={'GOCI_dai':GOCI_dai})
        print (fname_temp)
    print (yr)