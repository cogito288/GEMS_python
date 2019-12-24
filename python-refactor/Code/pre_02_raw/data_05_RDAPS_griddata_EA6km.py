### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import glob
import numpy as np
#from matplotlib.pyplot import imread
from scipy.interploate import griddata

### Setting path
data_base_dir = os.path.join(project_path, 'Data')
path_read = os.path.join(data_base_dir, 'Preprocessed_raw', 'RDAPS') 
path_write = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km', 'OMI_tempConv')

path_data = os.path.join('/', 'share', 'irisnas5', 'Data')
path = os.path.join('/', 'share', 'irisnas5', 'Data', 'EA_GOCI6km', 'RDAPS')

mat = matlab.loadmat(os.path.join(data_base_dir, 'grid', 'grid_goci.mat')) # lon_goci, lat_goci
lon_goci = mat['lon_goci']
lat_goci = mat['lat_goci']
del mat

mat = matlab.loadmat(os.path.join(data_base_dir, 'grid', 'grid_rdaps.mat')) 
lon_rdaps = mat['lon_rdaps']
lat_rdaps = mat['lat_rdaps']
del mat
points = np.array([lon_rdaps.ravel(order='F'), lat_rdaps.ravel(order='F')])
del lon_rdaps, lat_rdaps

YEARS = [2016]
for yr in YEARS:
    flist = glob.glob(os.path.join(path_read, str(yr), '*.mat')
    for fname in flist: # in range(1, 2000+1):
        rdaps = matlab.loadmat(fname)['rdaps']
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
        
        T = griddata(points,T,(lon_goci,lat_goci),method='linear') - 273.15
        D = griddata(points,D,(lon_goci,lat_goci),method='linear') - 273.15
        RH = griddata(points,RH,(lon_goci,lat_goci),method='linear')
        U = griddata(points,U,(lon_goci,lat_goci),method='linear')
        V = griddata(points,V,(lon_goci,lat_goci),method='linear')
        maxWS = griddata(points,maxWS,(lon_goci,lat_goci),method='linear')
        P_srf = griddata(points,P_srf,(lon_goci,lat_goci),method='linear')
        PBLH = griddata(points,PBLH,(lon_goci,lat_goci),method='linear')
        Visibility = griddata(points,Visibility,(lon_goci,lat_goci),method='linear')
        Tsrf = griddata(points,Tsrf,(lon_goci,lat_goci),method='linear') - 273.15
        Tmax = griddata(points,Tmax,(lon_goci,lat_goci),method='linear') - 273.15
        Tmin = griddata(points,Tmin,(lon_goci,lat_goci),method='linear') - 273.15
        AP3h = griddata(points,AP3h,(lon_goci,lat_goci),method='linear')
        FrictionalVelocity = griddata(points,FrictionalVelocity,(lon_goci,lat_goci),method='linear')
        PotentialEnergy = griddata(points,PotentialEnergy,(lon_goci,lat_goci),method='linear')
        SurfaceRoughness = griddata(points,SurfaceRoughness,(lon_goci,lat_goci),method='linear')
        LatentHeatFlux = griddata(points,LatentHeatFlux,(lon_goci,lat_goci),method='linear')
        SpecificHumidity = griddata(points,SpecificHumidity,(lon_goci,lat_goci),method='linear')
        
        base_name = os.path.basename(fname)[6:17]
        matlab.savemat(os.path.join(path_write,'Temp/',str(yr,f'EA6km_T_{base_name}'), {'T':T})
        matlab.savemat(os.path.join(path_write,'Dew/',str(yr),f'EA6km_D_{base_name}'),{'D':D})
        matlab.savemat(os.path.join(path_write,'RH/',str(yr),f'EA6km_RH_{base_name}',{'RH':RH})
        matlab.savemat(os.path.join(path_write,'Uwind/',str(yr),f'EA6km_U_{base_name}',{'U':U})
        matlab.savemat(os.path.join(path_write,'Vwind/',str(yr),f'EA6km_V_{base_name}',{'V':V})
        matlab.savemat(os.path.join(path_write,'MaxWS/',str(yr),f'EA6km_maxWS_{base_name}',{'maxWS':maxWS})
        matlab.savemat(os.path.join(path_write,'Pressure/',str(yr),f'EA6km_Pressure_srf_{base_name}',{'P_srf':P_srf})
        matlab.savemat(os.path.join(path_write,'PBLH/',str(yr),f'EA6km_PBLH_{base_name}',{'PBLH':PBLH})
        matlab.savemat(os.path.join(path_write,'Visibility/',str(yr),f'EA6km_Visibility_{base_name}',{'Visibility':Visibility})
        matlab.savemat(os.path.join(path_write,'Temp_surface/',str(yr),f'EA6km_Tsrf_{base_name}',{'Tsrf':Tsrf})
        matlab.savemat(os.path.join(path_write,'Temp_max/',str(yr),f'EA6km_Tmax_{base_name}',{'Tmax':Tmax})
        matlab.savemat(os.path.join(path,'Temp_min/',str(yr),f'EA6km_Tmin_{base_name}',{'Tmin':Tmin})
        matlab.savemat(os.path.join(path_write,'AP3h/',str(yr),f'EA6km_AP3h_{base_name}',{'AP3h':AP3h})
        matlab.savemat(os.path.join(path_write,'FrictionalVelocity/',str(yr),f'EA6km_FrictionalVelocity_{base_name}',{'FrictionalVelocity':FrictionalVelocity})
        matlab.savemat(os.path.join(path_write,'PotentialEnergy/',str(yr),f'EA6km_PotentialEnergy_{base_name}',{'PotentialEnergy':PotentialEnergy})
        matlab.savemat(os.path.join(path_write,'SurfaceRoughness/',str(yr),f'EA6km_SurfaceRoughness_{base_name}',{'SurfaceRoughness':SurfaceRoughness})
        matlab.savemat(os.path.join(path_write,'LatentHeatFlux/',str(yr),f'EA6km_LatentHeatFlux_{base_name}',{'LatentHeatFlux':LatentHeatFlux})
        matlab.savemat(os.path.join(path_write,'SpecificHumidity/',str(yr),f'EA6km_SpecificHumidity_{base_name}',{'SpecificHumidity':SpecificHumidity})
        print (f'{base_name}')
	print (yr)    
