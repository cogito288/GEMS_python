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
import time
import h5py 

### Setting path
data_base_dir = os.path.join('/', 'media', 'sf_GEMS', 'Data')
rdaps_path = os.path.join(data_base_dir, 'Raw', 'RDAPS') 
path = '/share/irisnas2/Data/Aerosol/RDAPS/';
path_data = '/share/irisnas2/Data/Aerosol/00_raw_data/RDAPS/';
#run('/share/irisnas3/Data/drought/GLDAS/nctoolbox-1.1.3/nctoolbox-1.1.3/setup_nctoolbox.m');

### Setting period
YEARS = [2016] #, 2018, 2019

for yr in YEARS:
    curr_path = os.path.join(rdaps_path, str(yr))
    list_char = glob.glob(os.path.join(curr_path, '*000.*.gb2'))
    list_char = [os.path.basename(f) for f in list_char]
    list_date = [x[21:29] for x in list_char]
    list_dnum = [matlab.datenum(date) for date in list_date]
    doy_000 = matlab.datenum(f'{yr}0101')-1
    rdaps = np.full((419,491,18), np.nan) 
    
    for i, fname in enumerate(list_char):
        
        rdaps_data = ncdataset(list(i,:));
        % var = rdaps_data.variables;
        rdaps(:,:,1) = squeeze(rdaps_data.netcdf.findVariable('Temperature_height_above_ground').read().copyToNDJavaArray());
        rdaps(:,:,2) = squeeze(rdaps_data.netcdf.findVariable('Dew-point_temperature_height_above_ground').read().copyToNDJavaArray());
        rdaps(:,:,3) = squeeze(rdaps_data.netcdf.findVariable('Relative_humidity_height_above_ground').read().copyToNDJavaArray());
        rdaps(:,:,4) = squeeze(rdaps_data.netcdf.findVariable('u-component_of_wind_height_above_ground').read().copyToNDJavaArray());
        rdaps(:,:,5) = squeeze(rdaps_data.netcdf.findVariable('v-component_of_wind_height_above_ground').read().copyToNDJavaArray());
        rdaps(:,:,6) = squeeze(rdaps_data.netcdf.findVariable('Maximum_wind_speed_height_above_ground_3_Hour_Maximum').read().copyToNDJavaArray());
        rdaps(:,:,7) = squeeze(rdaps_data.netcdf.findVariable('Pressure_surface').read().copyToNDJavaArray());
        rdaps(:,:,8) = squeeze(rdaps_data.netcdf.findVariable('Planetary_boundary_layer_height_UnknownLevelType-220').read().copyToNDJavaArray());
        rdaps(:,:,9) = squeeze(rdaps_data.netcdf.findVariable('Visibility_height_above_ground').read().copyToNDJavaArray());
        rdaps(:,:,10) = squeeze(rdaps_data.netcdf.findVariable('Temperature_surface').read().copyToNDJavaArray());
        rdaps(:,:,11) = squeeze(rdaps_data.netcdf.findVariable('Maximum_temperature_height_above_ground_3_Hour_Maximum').read().copyToNDJavaArray());
        rdaps(:,:,12) = squeeze(rdaps_data.netcdf.findVariable('Minimum_temperature_height_above_ground_3_Hour_Minimum').read().copyToNDJavaArray());
        rdaps(:,:,13) = squeeze(rdaps_data.netcdf.findVariable('Total_precipitation_surface_3_Hour_Accumulation').read().copyToNDJavaArray());
        rdaps(:,:,14) = squeeze(rdaps_data.netcdf.findVariable('Frictional_velocity_height_above_ground').read().copyToNDJavaArray());
        rdaps(:,:,15) = squeeze(rdaps_data.netcdf.findVariable('Convective_available_potential_energy_surface_layer_3_Hour_Maximum').read().copyToNDJavaArray());
        rdaps(:,:,16) = squeeze(rdaps_data.netcdf.findVariable('Surface_roughness_surface').read().copyToNDJavaArray());
        rdaps(:,:,17) = squeeze(rdaps_data.netcdf.findVariable('Latent_heat_net_flux_surface_3_Hour_Average').read().copyToNDJavaArray());
        rdaps(:,:,18) = squeeze(rdaps_data.netcdf.findVariable('Specific_humidity_height_above_ground').read().copyToNDJavaArray());
        
        doy = list_dnum(i)-doy_000;
%         fname = ['RDAPS_',num2str(yr),'_',num2str(doy,'%03i'),'_',list(i,30:31),'.mat'];
        fname = ['RDAPS_',num2str(yr),'_',num2str(doy,'%03i'),'_',list(i,30:31),'_006.mat'];
        save([path,num2str(yr),'/',fname], 'rdaps');
        disp(fname)
    end
end
