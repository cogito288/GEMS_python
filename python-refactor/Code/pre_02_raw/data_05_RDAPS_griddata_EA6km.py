import os
import sys
project_path = '/home/cogito/Desktop/GEMS_python/matlab2python/python-refactor'
sys.path.insert(0, project_path)

from Code.utils import matlab

import numpy as np
#from matplotlib.pyplot import imread
from scipy.interploate import griddata
import time

#% path_data = '//10.72.26.52/irisnas2/Data/Aerosol/';
#% path = '//10.72.26.56/irisnas5/Work/NOXO3/';
path_data = os.path.join('/', 'share', 'irisnas5', 'Data')
path = os.path.join('/', 'share', 'irisnas5', 'Data', 'EA_GOCI6km', 'RDAPS')
#addpath(genpath('/share/irisnas5/Data/matlab_func/'))

matlab.loadmat(os.path.join(path_data, 'grid', 'grid_goci.mat'))
matlab.loadmat(os.path.join(path_data, 'grid', 'grid_rdaps.mat'))

YEARS = [2019]
for yr in YEARS:
	os.chdir(os.path.join(path_data, 'pre', 'RDAPS', str(yr)))
	flist = matlab.get_files_endswith('.', '.mat')
    #%     list_utc = char(list);
    #%     list_utc = str2num(list_utc(:,16:17));
    #%     list = list(list_utc==4);
    #%     for i =3001:length(list)
	for i in range(185, 2000+1):
        #%     for i = 4501:6000
        #%     for i = 2001:3000
        #%     for i = 1001:2000
        #%     for i = 1:1000
		rdaps = matlab.loadmat(flist[i])
		T = rdaps[:, :, 0] #'Temperature_height_above_ground'
        D = rdaps[:, :, 1] # 'Dew-point_temperature_height_above_ground'
        RH = rdaaps[:, :, 2] # 'Relative_humidity_height_above_ground'
        U = rdaps[:, :, 3]  # 'u-component_of_wind_height_above_ground'
        V = rdaps[:, :, 4] # 'v-component_of_wind_height_above_ground'
        maxWS = rdaps[:,:,5] # % 'Maximum_wind_speed_height_above_ground_3_Hour_Maximum'
        P_srf = rdaps[:,:,6] #% 'Pressure_surface'
        PBLH = rdaps[:,:,7] #% 'Planetary_boundary_layer_height_UnknownLevelType-220'
        Visibility = rdaps[:,:,8] #% 'Visibility_height_above_ground'
        Tsrf = rdaps[:,:,9] #% 'Temperature_surface'
        Tmax = rdaps[:,:,10] #% 'Maximum_temperature_height_above_ground_3_Hour_Maximum'
        Tmin = rdaps[:,:,11] #% 'Minimum_temperature_height_above_ground_3_Hour_Minimum'
        AP3h = rdaps[:,:,12] #% 'Total_precipitation_surface_3_Hour_Accumulation'
        FrictionalVelocity = rdaps[:,:,13] #% 'Frictional_velocity_height_above_ground'
        PotentialEnergy = rdaps[:,:,14] #% 'Convective_available_potential_energy_surface_layer_3_Hour_Maximum')
        SurfaceRoughness = rdaps[:,:,15] #% 'Surface_roughness_surface'
        LatentHeatFlux = rdaps[:,:,16] #% 'Latent_heat_net_flux_surface_3_Hour_Average'
        SpecificHumidity = rdaps[:,:,17] #% 'Specific_humidity_height_above_ground'
        
        T = griddata(zip(lon_rdaps,lat_rdaps),T,zip(lon_goci,lat_goci),method='linear') - 273.15
        D = griddata(zip(lon_rdaps,lat_rdaps),D,zip(lon_goci,lat_goci),method='linear') - 273.15
        RH = griddata(zip(lon_rdaps,lat_rdaps),RH,zip(lon_goci,lat_goci),method='linear')
        U = griddata(zip(lon_rdaps,lat_rdaps),U,zip(lon_goci,lat_goci),method='linear')
        V = griddata(zip(lon_rdaps,lat_rdaps),V,zip(lon_goci,lat_goci),method='linear')
        maxWS = griddata(zip(lon_rdaps,lat_rdaps),maxWS,zip(lon_goci,lat_goci),method='linear')
        P_srf = griddata(zip(lon_rdaps,lat_rdaps),P_srf,zip(lon_goci,lat_goci),method='linear')
        PBLH = griddata(zip(lon_rdaps,lat_rdaps),PBLH,zip(lon_goci,lat_goci),method='linear')
        Visibility = griddata(zip(lon_rdaps,lat_rdaps),Visibility,zip(lon_goci,lat_goci),method='linear')
        Tsrf = griddata(zip(lon_rdaps,lat_rdaps),Tsrf,zip(lon_goci,lat_goci),method='linear') - 273.15
        Tmax = griddata(zip(lon_rdaps,lat_rdaps),Tmax,zip(lon_goci,lat_goci),method='linear') - 273.15
        Tmin = griddata(zip(lon_rdaps,lat_rdaps),Tmin,zip(lon_goci,lat_goci),method='linear') - 273.15
        AP3h = griddata(zip(lon_rdaps,lat_rdaps),AP3h,zip(lon_goci,lat_goci),method='linear')
        FrictionalVelocity = zip(griddata(lon_rdaps,lat_rdaps),FrictionalVelocity,zip(lon_goci,lat_goci),method='linear')
        PotentialEnergy = griddata(zip(lon_rdaps,lat_rdaps),PotentialEnergy,zip(lon_goci,lat_goci),method='linear')
        SurfaceRoughness = griddata(zip(lon_rdaps,lat_rdaps),SurfaceRoughness,zip(lon_goci,lat_goci),method='linear')
        LatentHeatFlux = griddata(zip(lon_rdaps,lat_rdaps),LatentHeatFlux,zip(lon_goci,lat_goci),method='linear')
        SpecificHumidity = griddata(zip(lon_rdaps,lat_rdaps),SpecificHumidity,zip(lon_goci,lat_goci),method='linear')
        
        matlab.savemat(os.path.join(path,'Temp/',str(yr)),f'EA6km_T_{flist[i][6:17]}',T)
        matlab.savemat(os.path.join(path,'Dew/',str(yr)),f'EA6km_D_{flist[i][6:17]',D)
        matlab.savemat(os.path.join(path,'RH/',str(yr)),f'EA6km_RH_{flist[i][6:17]}',RH)
        matlab.savemat(os.path.join(path,'Uwind/',str(yr)),f'EA6km_U_{flist[i][6:17]}',U)
        matlab.savemat(os.path.join(path,'Vwind/',str(yr)),f'EA6km_V_{flist[i][6:17]}',V)
        matlab.savemat(os.path.join(path,'MaxWS/',str(yr)),f'EA6km_maxWS_{flist[i][6:17]}',maxWS)
        matlab.savemat(os.path.join(path,'Pressure/',str(yr)),f'EA6km_Pressure_srf_{flist[i][6:17]}',P_srf)
        matlab.savemat(os.path.join(path,'PBLH/',str(yr)),f'EA6km_PBLH_{flist[i][6:17]}',PBLH)
        matlab.savemat(os.path.join(path,'Visibility/',str(yr)),f'EA6km_Visibility_{flist[i][6:17]}',Visibility)
        matlab.savemat(os.path.join(path,'Temp_surface/',str(yr)),f'EA6km_Tsrf_{flist[i][6:17]}',Tsrf)
        matlab.savemat(os.path.join(path,'Temp_max/',str(yr)),f'EA6km_Tmax_{flist[i][6:17]}',Tmax)
        matlab.savemat(os.path.join(path,'Temp_min/',str(yr)),f'EA6km_Tmin_{flist[i][6:17]}',Tmin)
        matlab.savemat(os.path.join(path,'AP3h/',str(yr)),f'EA6km_AP3h_{flist[i][6:17]}',AP3h)
        matlab.savemat(os.path.join(path,'FrictionalVelocity/',str(yr)),f'EA6km_FrictionalVelocity_{flist[i][6:17]}',FrictionalVelocity)
        matlab.savemat(os.path.join(path,'PotentialEnergy/',str(yr)),f'EA6km_PotentialEnergy_{flist[i][6:17]}',PotentialEnergy)
        matlab.savemat(os.path.join(path,'SurfaceRoughness/',str(yr)),f'EA6km_SurfaceRoughness_{flist[i][6:17]}',SurfaceRoughness)
        matlab.savemat(os.path.join(path,'LatentHeatFlux/',str(yr)),f'EA6km_LatentHeatFlux_{flist[i][6:17]}',LatentHeatFlux)
        matlab.savemat(os.path.join(path,'SpecificHumidity/',str(yr)),f'EA6km_SpecificHumidity_{flist[i][6:17]}',SpecificHumidity)
        print (f'{flist[i][6:-4]} ... i={i}')
	print (yr)    
