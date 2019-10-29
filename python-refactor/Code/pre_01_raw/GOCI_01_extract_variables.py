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

for yr in YEARS:
    doy_000 = matlab.datenum(f'{yr}0000')

    for mm in MONTHS:
        curr_path = os.path.join(raw_data_path, str(yr), f'{mm:02d}')
        #os.chdir(curr_path)
        
        list_mm = glob.glob(os.path.join(curr_path, '*.hdf'))
        list_mm = [os.path.basename(f) for f in list_mm]
        doy = [matlab.datenum(x[23:31]) for x in list_mm]
        list_doy = [d-doy_000 for d in doy]
        list_utc = [int(x[31:33]) for x in list_mm]
        
        for k, fname in enumerate(list_mm):
            GOCI_aod = np.float64(matlab.hdfread(os.path.join(curr_path, fname),\
                                       'Aerosol_Optical_Depth_550nm'))
            GOCI_fmf = np.float64(matlab.hdfread(os.path.join(curr_path, fname),\
                                      'Fine_Mode_Fraction_550nm'))
            GOCI_ssa = np.float64(matlab.hdfread(os.path.join(curr_path, fname),\
                                      'Single_Scattering_Albedo_440nm'))
            GOCI_ae = np.float64(matlab.hdfread(os.path.join(curr_path, fname),\
                                     'Angstrom_Exponent_440_870nm'))
            GOCI_type = np.float64(matlab.hdfread(os.path.join(curr_path, fname),\
                                       'Aerosol_Type'))
            GOCI_num_used_pixels = np.float64(matlab.hdfread(os.path.join(curr_path, fname),\
                                       'No_of_Used_500m_Pixels_for_One_6km_Product_Pixel'))
            GOCI_ndvi = np.float64(matlab.hdfread(os.path.join(curr_path, fname),\
                                       'NDVI_from_TOA_Reflectance_660_865nm'))
            GOCI_dai = np.float64(matlab.hdfread(os.path.join(curr_path, fname),\
                                      'Dust_Aerosol_Index_from_412_443nm'))
            
            GOCI_aod[(GOCI_aod<-0.05) | (GOCI_aod>3.6)] = np.nan
            GOCI_fmf[(GOCI_fmf<0) | (GOCI_fmf>1)] = np.nan
            GOCI_ssa[(GOCI_ssa<0) | (GOCI_ssa>1)] = np.nan
            GOCI_ae[(GOCI_ae<0) | (GOCI_ae>3)] = np.nan
            GOCI_type[(GOCI_type<0) | (GOCI_type>6)] = np.nan
            GOCI_ndvi[(GOCI_ndvi<-1) | (GOCI_ndvi>1)] = np.nan
            
            fname_temp = f'{yr}_{list_doy[k]:03d}_{list_utc[k]:02d}.mat'
            
            
            
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
        print (mm)
    print (yr)