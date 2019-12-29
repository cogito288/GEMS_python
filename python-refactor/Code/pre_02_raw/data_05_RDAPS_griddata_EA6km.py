### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import glob
import numpy as np
from scipy.interpolate import griddata
import time

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_rdaps_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'RDAPS') 
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km') 
path_ea_goci_rdaps = os.path.join(path_ea_goci, 'RDAPS') 

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_goci.mat')) # lon_goci, lat_goci
lon_goci, lat_goci = mat['lon_goci'], mat['lat_goci']
del mat

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_rdaps.mat')) 
points = np.array([mat['lon_rdaps'].ravel(order='F'), mat['lat_rdaps'].ravel(order='F')]).T
del mat
print (f'points shape : {points.shape}')

YEARS = [2016]
for yr in YEARS:
    flist = glob.glob(os.path.join(path_rdaps_processed, str(yr), '*.mat'))
    flist.sort()
    for fname in flist: # in range(1, 2000+1):
        tStart = time.time()
        rdaps = matlab.loadmat(fname)['rdaps']
        T = rdaps[:, :, 0] #'Temperature_height_above_ground'
        D = rdaps[:, :, 1] # 'Dew-point_temperature_height_above_ground'
        RH = rdaps[:, :, 2] # 'Relative_humidity_height_above_ground'
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
        
        T = griddata(points,T.ravel(order='F'),(lon_goci,lat_goci),method='linear') - 273.15
        D = griddata(points,D.ravel(order='F'),(lon_goci,lat_goci),method='linear') - 273.15
        RH = griddata(points,RH.ravel(order='F'),(lon_goci,lat_goci),method='linear')
        U = griddata(points,U.ravel(order='F'),(lon_goci,lat_goci),method='linear')
        V = griddata(points,V.ravel(order='F'),(lon_goci,lat_goci),method='linear')
        maxWS = griddata(points,maxWS.ravel(order='F'),(lon_goci,lat_goci),method='linear')
        P_srf = griddata(points,P_srf.ravel(order='F'),(lon_goci,lat_goci),method='linear')
        PBLH = griddata(points,PBLH.ravel(order='F'),(lon_goci,lat_goci),method='linear')
        Visibility = griddata(points,Visibility.ravel(order='F'),(lon_goci,lat_goci),method='linear')
        Tsrf = griddata(points,Tsrf.ravel(order='F'),(lon_goci,lat_goci),method='linear') - 273.15
        Tmax = griddata(points,Tmax.ravel(order='F'),(lon_goci,lat_goci),method='linear') - 273.15
        Tmin = griddata(points,Tmin.ravel(order='F'),(lon_goci,lat_goci),method='linear') - 273.15
        AP3h = griddata(points,AP3h.ravel(order='F'),(lon_goci,lat_goci),method='linear')
        FrictionalVelocity = griddata(points,FrictionalVelocity.ravel(order='F'),(lon_goci,lat_goci),method='linear')
        PotentialEnergy = griddata(points,PotentialEnergy.ravel(order='F'),(lon_goci,lat_goci),method='linear')
        SurfaceRoughness = griddata(points,SurfaceRoughness.ravel(order='F'),(lon_goci,lat_goci),method='linear')
        LatentHeatFlux = griddata(points,LatentHeatFlux.ravel(order='F'),(lon_goci,lat_goci),method='linear')
        SpecificHumidity = griddata(points,SpecificHumidity.ravel(order='F'),(lon_goci,lat_goci),method='linear')
        
        base_name = os.path.basename(fname)[6:17]
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'Temp/',str(yr),f'EA6km_T_{base_name}.mat'), {'T':T})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'Dew/',str(yr),f'EA6km_D_{base_name}.mat'),{'D':D})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'RH/',str(yr),f'EA6km_RH_{base_name}.mat'),{'RH':RH})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'Uwind/',str(yr),f'EA6km_U_{base_name}.mat'),{'U':U})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'Vwind/',str(yr),f'EA6km_V_{base_name}.mat'),{'V':V})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'MaxWS/',str(yr),f'EA6km_maxWS_{base_name}.mat'),{'maxWS':maxWS})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'Pressure/',str(yr),f'EA6km_Pressure_srf_{base_name}.mat'),{'P_srf':P_srf})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'PBLH/',str(yr),f'EA6km_PBLH_{base_name}.mat'),{'PBLH':PBLH})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'Visibility/',str(yr),f'EA6km_Visibility_{base_name}.mat'),{'Visibility':Visibility})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'Temp_surface/',str(yr),f'EA6km_Tsrf_{base_name}.mat'),{'Tsrf':Tsrf})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'Temp_max/',str(yr),f'EA6km_Tmax_{base_name}.mat'),{'Tmax':Tmax})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'Temp_min/',str(yr),f'EA6km_Tmin_{base_name}.mat'),{'Tmin':Tmin})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'AP3h/',str(yr),f'EA6km_AP3h_{base_name}.mat'),{'AP3h':AP3h})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'FrictionalVelocity/',str(yr),f'EA6km_FrictionalVelocity_{base_name}.mat'),{'FrictionalVelocity':FrictionalVelocity})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'PotentialEnergy/',str(yr),f'EA6km_PotentialEnergy_{base_name}.mat'),{'PotentialEnergy':PotentialEnergy})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'SurfaceRoughness/',str(yr),f'EA6km_SurfaceRoughness_{base_name}.mat'),{'SurfaceRoughness':SurfaceRoughness})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'LatentHeatFlux/',str(yr),f'EA6km_LatentHeatFlux_{base_name}.mat'),{'LatentHeatFlux':LatentHeatFlux})
        matlab.savemat(os.path.join(path_ea_goci_rdaps,'SpecificHumidity/',str(yr),f'EA6km_SpecificHumidity_{base_name}.mat'),{'SpecificHumidity':SpecificHumidity})
        print (f'{base_name}')
        tElapsed = time.time() - tStart
        print (f'{tElapsed} second')
    print (yr)    
