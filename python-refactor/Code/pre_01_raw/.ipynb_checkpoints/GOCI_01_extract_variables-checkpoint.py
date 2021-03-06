### Package Import
import scipy.io as sio
import os

import sys
project_path = '/home/cogito/Uncertainty/matlab2python/python-refactor'
sys.path.insert(0, project_path)

from Code.utils.matlab import *
from Code.utils.helpers import *


### Setting path
project_path = '/home/cogito/Uncertainty/matlab2python/python-refactor'
raw_data_path = os.path.join(project_path, 'Data', 'Raw', 'GOCI_AOD') 
write_path = os.path.join(project_path, 'Data', 'Prepreossed_raw', 'GOCI_AOD')

### Setting period
YEARS = [2016, 2018, 2019]
MONTHS = range(1, 12+1)

for yr in YEARS:
    doy_000 = datenum(f'{yr}0000')

    for mm in MONTHS:
        curr_path = os.path.join(raw_data_path, str(yr), '{:02d}'.format(mm))
        os.chdir(curr_path)
        
        list_mm = get_file_lists('./', ".hdf")
        list_doy = list(map(lambda x: datenum(x[23:31])-doy_000, list_mm))
        list_utc = list(map(lambda x: int(x[31:33]), list_mm))
        
        for k in range(len(list_mm)):
            GOCI_aod = get_dataset_from_hdf4(list_mm[k], 'Aerosol_Optical_Depth_550nm')
            GOCI_fmf = get_dataset_from_hdf4(list_mm[k], 'Fine_Mode_Fraction_550nm')
            GOCI_ssa = get_dataset_from_hdf4(list_mm[k], 'Single_Scattering_Albedo_440nm')
            GOCI_ae = get_dataset_from_hdf4(list_mm[k], 'Angstrom_Exponent_440_870nm')
            GOCI_type = get_dataset_from_hdf4(list_mm[k], 'Aerosol_Type')
            GOCI_num_used_pixcels = get_dataset_from_hdf4(list_mm[k], 'No_of_Used_500m_Pixels_for_One_6km_Product_Pixel')
            GOCI_ndvi = get_dataset_from_hdf4(list_mm[k], 'NDVI_from_TOA_Reflectance_660_865nm')
            GOCI_dai = get_dataset_from_hdf4(list_mm[k], 'Dust_Aerosol_Index_from_412_443nm')
            
            GOCI_aod[(GOCI_aod<-0.05) & (GOCI_aod>3.6)] = np.nan
            GOCI_fmf[(GOCI_fmf<0) & (GOCI_fmf>1)] = np.nan
            GOCI_ssa[(GOCI_ssa<0) & (GOCI_ssa>1)] = np.nan
            GOCI_ae[(GOCI_ae<0) & (GOCI_ae>3)] = np.nan
            GOCI_type[(GOCI_type<0) & (GOCI_type>6)] = np.nan
            GOCI_ndvi[(GOCI_ndvi<-1) & (GOCI_ndvi>1)] = np.nan
            
            fname_temp = f'{yr}_{list_doy[k]:03d}_{list_utc[k]:02d}.mat'
            
            sio.savemat(os.path.join(write_path, 'AOD', str(yr), f'GOCI_AOD_{fname_temp}'), mdict={'GOCI_aod':GOCI_aod})
            sio.savemat(os.path.join(write_path, 'FMF', str(yr), f'GOCI_FMF_{fname_temp}'), mdict={'GOCI_fmf':GOCI_fmf})
            sio.savemat(os.path.join(write_path, 'SSA', str(yr), f'GOCI_SSA_{fname_temp}'), mdict={'GOCI_ssa':GOCI_ssa})
            sio.savemat(os.path.join(write_path, 'AE', str(yr), f'GOCI_AE_{fname_temp}'), mdict={'GOCI_ae':GOCI_ae})
            sio.savemat(os.path.join(write_path, 'Type', str(yr), f'GOCI_Type_{fname_temp}'), mdict={'GOCI_Type':GOCI_Type})
            sio.savemat(os.path.join(write_path, 'No_of_Used_500m_Pixels_for_One_6km_Product_Pixel', str(yr), f'GOCI_num_used_pixels_{fname_tmpe}', mdict={'GOCI_num_used_pixels':GOCI_num_used_pixels}))
            sio.savemat(os.path.join(write_path, 'NDVI', str(yr), f'GOCI_NDVI_{fname_temp}'), mdict={'GOCI_ndvi':GOCI_ndvi})
            sio.savemat(os.path.join(write_path, 'DAI', str(yr), f'GOCI_DAI_{fname_temp}'), mdict={'GOCI_dai':GOCI_dai})
            print (fname_temp)
        print (mm)
    print (yr)