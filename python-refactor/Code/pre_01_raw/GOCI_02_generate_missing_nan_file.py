### Package Import
import scipy.io as sio
import os

import sys
project_path = '/home/cogito/Uncertainty/matlab2python/python-refactor'
sys.path.insert(0, project_path)

from Code.utils.matlab import *
from Code.utils.helpers import *

### Setting path
data_path = os.path.join(project_path, 'Data', 'Raw', 'GOCI_AOD') 
os.chdir(data_path)

### Setting period
YEARS = [2018, 2019]
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
    
    list_aod = get_file_lists(os.path.join('AOD', str(yr)), ".mat")
    list_aod2 = list(map(lambda x: (int(x[14:17]), int(x[18:20]))))   # doy, utc 
    #list_doy = repmat(1:days,[8,1]);
    #list_utc = repmat(0:7,[1,days]);
    #list_all = [list_doy(:),list_utc];
    
    idx = ismember(list_all,list_aod2,'rows');
    miss_list = list_all(idx==0,:);
    
    for k in range(len(miss_list)):
        fname_temp = f'{yr}_{miss_list[k][0]:03d}_{miss_list[k][1]:02d}.mat'
        
        sio.savemat(os.path.join(write_path, 'AOD', str(yr), f'GOCI_AOD_{fname_temp}'), mdict={'GOCI_aod':GOCI_aod})
        sio.savemat(os.path.join(write_path, 'FMF', str(yr), f'GOCI_FMF_{fname_temp}'), mdict={'GOCI_fmf':GOCI_fmf})
        sio.savemat(os.path.join(write_path, 'SSA', str(yr), f'GOCI_SSA_{fname_temp}'), mdict={'GOCI_ssa':GOCI_ssa})
        sio.savemat(os.path.join(write_path, 'AE', str(yr), f'GOCI_AE_{fname_temp}'), mdict={'GOCI_ae':GOCI_ae})
        sio.savemat(os.path.join(write_path, 'Type', str(yr), f'GOCI_Type_{fname_temp}'), mdict={'GOCI_Type':GOCI_Type})
        sio.savemat(os.path.join(write_path, 'No_of_Used_500m_Pixels_for_One_6km_Product_Pixel', str(yr), f'GOCI_num_used_pixels_{fname_tmpe}', mdict={'GOCI_num_used_pixels':GOCI_num_used_pixels}))
        sio.savemat(os.path.join(write_path, 'NDVI', str(yr), f'GOCI_NDVI_{fname_temp}'), mdict={'GOCI_ndvi':GOCI_ndvi})
        sio.savemat(os.path.join(write_path, 'DAI', str(yr), f'GOCI_DAI_{fname_temp}'), mdict={'GOCI_dai':GOCI_dai})
        print (fname_temp)
        
    print (yr)