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
path_raw_goci = os.path.join(data_base_dir, 'Raw', 'GOCI_AOD') 
path_goci_aod = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_AOD')

### Setting period
YEARS = [2016] #, 2018, 2019]
MONTHS = range(1, 12+1)

for yr in YEARS:
    doy_000 = matlab.datenum(f'{yr}0000')
    for mm in MONTHS:        
        file_list = glob.glob(os.path.join(path_raw_goci, str(yr), f'{mm:02d}', '*.hdf'))
        file_list.sort()
        for fname in file_list:
            tStart = time.time()
            doy = matlab.datenum(os.path.basename(fname)[23:31])
            doy = doy-doy_000
            utc = int(os.path.basename(fname)[31:33])
            GOCI_aod = matlab.hdfread(fname, 'Aerosol_Optical_Depth_550nm').astype('float64')
            GOCI_fmf = matlab.hdfread(fname, 'Fine_Mode_Fraction_550nm').astype('float64')
            GOCI_ssa = matlab.hdfread(fname, 'Single_Scattering_Albedo_440nm').astype('float64')
            GOCI_ae = matlab.hdfread(fname, 'Angstrom_Exponent_440_870nm').astype('float64')
            GOCI_type = matlab.hdfread(fname, 'Aerosol_Type').astype('float64')
            GOCI_num_used_pixels = matlab.hdfread(fname, 'No_of_Used_500m_Pixels_for_One_6km_Product_Pixel').astype('float64')
            GOCI_ndvi = matlab.hdfread(fname, 'NDVI_from_TOA_Reflectance_660_865nm').astype('float64')
            GOCI_dai = matlab.hdfread(fname, 'Dust_Aerosol_Index_from_412_443nm').astype('float64')
            
            GOCI_aod[(GOCI_aod<-0.05) | (GOCI_aod>3.6)] = np.nan
            GOCI_fmf[(GOCI_fmf<0) | (GOCI_fmf>1)] = np.nan
            GOCI_ssa[(GOCI_ssa<0) | (GOCI_ssa>1)] = np.nan
            GOCI_ae[(GOCI_ae<0) | (GOCI_ae>3)] = np.nan
            GOCI_type[(GOCI_type<0) | (GOCI_type>6)] = np.nan
            GOCI_ndvi[(GOCI_ndvi<-1) | (GOCI_ndvi>1)] = np.nan
            
            fname_temp = f'{yr}_{doy:03d}_{utc:02d}.mat'
            matlab.savemat(
                       fname=os.path.join(path_goci_aod, 'AOD', str(yr),f'GOCI_AOD_{fname_temp}'),
                       data={'GOCI_aod':GOCI_aod})
            matlab.savemat(
                       fname=os.path.join(path_goci_aod, 'FMF', str(yr),f'GOCI_FMF_{fname_temp}'),
                       data={'GOCI_fmf':GOCI_fmf})
            matlab.savemat(
                       fname=os.path.join(path_goci_aod, 'SSA', str(yr),f'GOCI_SSA_{fname_temp}'),
                       data={'GOCI_ssa':GOCI_ssa})
            matlab.savemat(
                       fname=os.path.join(path_goci_aod, 'AE', str(yr),f'GOCI_AE_{fname_temp}'),
                       data={'GOCI_ae':GOCI_ae})
            matlab.savemat(
                       fname=os.path.join(path_goci_aod, 'Type', str(yr),f'GOCI_Type_{fname_temp}'),
                       data={'GOCI_type':GOCI_type})
            matlab.savemat(
                       fname=os.path.join(path_goci_aod, 'No_of_Used_500m_Pixels_for_One_6km_Product_Pixel', str(yr),f'GOCI_num_used_pixels_{fname_temp}'),
                       data={'GOCI_num_used_pixels':GOCI_num_used_pixels})
            matlab.savemat(
                       fname=os.path.join(path_goci_aod, 'NDVI', str(yr),f'GOCI_NDVI_{fname_temp}'),
                       data={'GOCI_ndvi':GOCI_ndvi})
            matlab.savemat(
                       fname=os.path.join(path_goci_aod, 'DAI', str(yr),f'GOCI_DAI_{fname_temp}'),
                       data={'GOCI_dai':GOCI_dai})
            print (fname_temp)
            tElapsed = time.time() - tStart
            print (f'Time taken : {tElapsed}')
        print (mm)
    print (yr)