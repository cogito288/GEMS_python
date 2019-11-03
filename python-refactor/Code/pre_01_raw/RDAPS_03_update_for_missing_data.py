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
import pygrib
from scipy.interpolate import griddata

### Setting path
data_base_dir = os.path.join('/', 'media', 'sf_GEMS', 'Data')
path_kor = os.path.join(data_base_dir, 'Preprocessed_raw', 'Korea') 
path_EA = os.path.join(data_base_dir, 'Preprocessed_raw', 'output_EA6km') 
rdaps_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'RDAPS') 
#path = os.path.join(project_data, 'Data', 'Aerosol', 'Aerosol_Work', 'Korea')
#data_path = os.path.join(project_data, 'Data', 'Aerosol')

### Setting period
YEARS = [2016] #, 2018, 2019

"""
## 2015082006
for j in range(1, 5+1):
    rdaps = np.multiply((data06 - data00), j/6) + data00 # 01 to 05 UTC
    matlab.matlab.savematmat(rdaps_path, f'RDAPS_2015_232_{j:02d}', {'rdaps':rdaps}) 
    rdaps = np.multiply((data12 - data06), j/6) + data00 # 07 to 11 UTC
    matlab.matlab.savematmat(rdaps_path, f'RDAPS_2015_232_{j+6:02d}', {'rdaps':rdaps}) 


for utc in range(1, 11+1):
    
    yr_doy_utc = f'2015_232_{utc:02d}'
    mat = matlab.loadmat(os.path.join(rdaps_path, yr_doy_utc+'.mat'))
    rdaps = mat['rdpas']
    
    T_org = rdaps[:,:,0] # 'Temperature_height_above_ground'
    D_org = rdaps[:,:,1] # 'Dew-point_temperature_height_above_ground'
    RH_org = rdaps[:,:,2] # 'Relative_humidity_height_above_ground'
    U_org = rdaps[:,:,3] # 'u-component_of_wind_height_above_ground'
    V_org = rdaps[:,:,4] # 'v-component_of_wind_height_above_ground'
    maxWS_org = rdaps[:,:,5] # 'Maximum_wind_speed_height_above_ground_3_Hour_Maximum'
    P_srf_org = rdaps[:,:,6] # 'Pressure_surface'
    PBLH_org = rdaps[:,:,7] # 'Planetary_boundary_layer_height_UnknownLevelType-220'
    Visibility_org = rdaps[:,:,8] # 'Visibility_height_above_ground'
    Tsrf_org = rdaps[:,:,9] # 'Temperature_surface'
    Tmax_org = rdaps[:,:,10] # 'Maximum_temperature_height_above_ground_3_Hour_Maximum'
    Tmin_org = rdaps[:,:,11] # 'Minimum_temperature_height_above_ground_3_Hour_Minimum'
    AP3h_org = rdaps[:,:,12] # 'Total_precipitation_surface_3_Hour_Accumulation'
    FrictionalVelocity_org = rdaps[:,:,13] # 'Frictional_velocity_height_above_ground'
    PotentialEnergy_org = rdaps[:,:,14] # 'Convective_available_potential_energy_surface_layer_3_Hour_Maximum']
    SurfaceRoughness_org = rdaps[:,:,15] # 'Surface_roughness_surface'
    LatentHeatFlux_org = rdaps[:,:,16] # 'Latent_heat_net_flux_surface_3_Hour_Average'
    SpecificHumidity_org = rdaps[:,:,17] # 'Specific_humidity_height_above_ground'
    
    T = griddata(zip(lon_rdaps,lat_rdaps),T_org,zip(lon_goci,lat_goci),method='linear') -273.15
    D = griddata(zip(lon_rdaps,lat_rdaps),D_org,zip(lon_goci,lat_goci),method='linear') -273.15
    RH = griddata(zip(lon_rdaps,lat_rdaps),RH_org,zip(lon_goci,lat_goci),method='linear')
    U = griddata(zip(lon_rdaps,lat_rdaps),U_org,zip(lon_goci,lat_goci),method='linear')
    V = griddata(zip(lon_rdaps,lat_rdaps),V_org,zip(lon_goci,lat_goci),method='linear')
    maxWS = griddata(zip(lon_rdaps,lat_rdaps),maxWS_org,zip(lon_goci,lat_goci),method='linear')
    P_srf = griddata(zip(lon_rdaps,lat_rdaps),P_srf_org,zip(lon_goci,lat_goci),method='linear')
    PBLH = griddata(zip(lon_rdaps,lat_rdaps),PBLH_org,zip(lon_goci,lat_goci),method='linear')
    Visibility = griddata(zip(lon_rdaps,lat_rdaps),Visibility_org,zip(lon_goci,lat_goci),method='linear')
    Tsrf = griddata(zip(lon_rdaps,lat_rdaps),Tsrf_org,zip(lon_goci,lat_goci),method='linear') - 273.15
    Tmax = griddata(zip(lon_rdaps,lat_rdaps),Tmax_org,zip(lon_goci,lat_goci),method='linear') - 273.15
    Tmin = griddata(zip(lon_rdaps,lat_rdaps),Tmin_org,zip(lon_goci,lat_goci),method='linear') - 273.15
    AP3h = griddata(zip(lon_rdaps,lat_rdaps),AP3h_org,zip(lon_goci,lat_goci),method='linear')
    FrictionalVelocity = griddata(zip(lon_rdaps,lat_rdaps),FrictionalVelocity_org,zip(lon_goci,lat_goci),method='linear')
    PotentialEnergy = griddata(zip(lon_rdaps,lat_rdaps),PotentialEnergy_org,zip(lon_goci,lat_goci),method='linear')
    SurfaceRoughness = griddata(zip(lon_rdaps,lat_rdaps),SurfaceRoughness_org,zip(lon_goci,lat_goci),method='linear')
    LatentHeatFlux = griddata(zip(lon_rdaps,lat_rdaps),LatentHeatFlux_org,zip(lon_goci,lat_goci),method='linear')
    SpecificHumidity = griddata(zip(lon_rdaps,lat_rdaps),SpecificHumidity_org,zip(lon_goci,lat_goci),method='linear')
    
    matlab.savemat(os.path.join(path_EA,'RDAPS/Temp/',str(yr)),f'EA6km_T_{yr_doy_utc}.mat',{'T':T})
    matlab.savemat(os.path.join(path_EA,'RDAPS/Dew/',str(yr)),f'EA6km_D_{yr_doy_utc}.mat',{'D':D})
    matlab.savemat(os.path.join(path_EA,'RDAPS/RH/',str(yr)),f'EA6km_RH_{yr_doy_utc}.mat',{'RH':RH})
    matlab.savemat(os.path.join(path_EA,'RDAPS/Uwind/',str(yr)),f'EA6km_U_{yr_doy_utc}.mat',{'U':U})
    matlab.savemat(os.path.join(path_EA,'RDAPS/Vwind/',str(yr)),f'EA6km_V_{yr_doy_utc}.mat',{'V':V})
    matlab.savemat(os.path.join(path_EA,'RDAPS/MaxWS/',str(yr)),f'EA6km_maxWS_{yr_doy_utc}.mat',{'maxWS':maxWS})
    matlab.savemat(os.path.join(path_EA,'RDAPS/Pressure/',str(yr)),f'EA6km_Pressure_srf_{yr_doy_utc}.mat',{'P_srf':P_srf})
    matlab.savemat(os.path.join(path_EA,'RDAPS/PBLH/',str(yr)),f'EA6km_PBLH_{yr_doy_utc}.mat','PBLH')
    matlab.savemat(os.path.join(path_EA,'RDAPS/Visibility/',str(yr)),f'EA6km_Visibility_{yr_doy_utc}.mat',{'Visibility':Visibility})
    matlab.savemat(os.path.join(path_EA,'RDAPS/Temp_surface/',str(yr)),f'EA6km_Tsrf_{yr_doy_utc}.mat',{'Tsrf':Tsrf})
    matlab.savemat(os.path.join(path_EA,'RDAPS/Temp_max/',str(yr)),f'EA6km_Tmax_{yr_doy_utc}.mat',{'Tmax':Tmax})
    matlab.savemat(os.path.join(path_EA,'RDAPS/Temp_min/',str(yr)),f'EA6km_Tmin_{yr_doy_utc}.mat',{'Tmin':Tmin})
    matlab.savemat(os.path.join(path_EA,'RDAPS/AP3h/',str(yr)),f'EA6km_AP3h_{yr_doy_utc}.mat',{'AP3h':AP3h})
    matlab.savemat(os.path.join(path_EA,'RDAPS/FrictionalVelocity/',str(yr)),f'EA6km_FrictionalVelocity_{yr_doy_utc}.mat',{'FrictionalVelocity':FrictionalVelocity})
    matlab.savemat(os.path.join(path_EA,'RDAPS/PotentialEnergy/',str(yr)),f'EA6km_PotentialEnergy_{yr_doy_utc}.mat',{'PotentialEnergy':PotentialEnergy})
    matlab.savemat(os.path.join(path_EA,'RDAPS/SurfaceRoughness/',str(yr)),f'EA6km_SurfaceRoughness_{yr_doy_utc}.mat',{'SurfaceRoughness':SurfaceRoughness})
    matlab.savemat(os.path.join(path_EA,'RDAPS/LatentHeatFlux/',str(yr)),f'EA6km_LatentHeatFlux_{yr_doy_utc}.mat',{'LatentHeatFlux':LatentHeatFlux})
    matlab.savemat(os.path.join(path_EA,'RDAPS/SpecificHumidity/',str(yr)),f'EA6km_SpecificHumidity_{yr_doy_utc}.mat',{'SpecificHumidity':SpecificHumidity})
    
    T = griddata(zip(lon_rdaps,lat_rdaps),T_org,zip(lon_kor,lat_kor),method='linear') -273.15
    D = griddata(zip(lon_rdaps,lat_rdaps),D_org,zip(lon_kor,lat_kor),method='linear') -273.15
    RH = griddata(zip(lon_rdaps,lat_rdaps),RH_org,zip(lon_kor,lat_kor),method='linear')
    U = griddata(zip(lon_rdaps,lat_rdaps),U_org,zip(lon_kor,lat_kor),method='linear')
    V = griddata(zip(lon_rdaps,lat_rdaps),V_org,zip(lon_kor,lat_kor),method='linear')
    maxWS = griddata(zip(lon_rdaps,lat_rdaps),maxWS_org,zip(lon_kor,lat_kor),method='linear')
    P_srf = griddata(zip(lon_rdaps,lat_rdaps),P_srf_org,zip(lon_kor,lat_kor),method='linear')
    PBLH = griddata(zip(lon_rdaps,lat_rdaps),PBLH_org,zip(lon_kor,lat_kor),method='linear')
    Visibility = griddata(zip(lon_rdaps,lat_rdaps),Visibility_org,zip(lon_kor,lat_kor),method='linear')
    Tsrf = griddata(zip(lon_rdaps,lat_rdaps),Tsrf_org,zip(lon_kor,lat_kor),method='linear') - 273.15
    Tmax = griddata(zip(lon_rdaps,lat_rdaps),Tmax_org,zip(lon_kor,lat_kor),method='linear') - 273.15
    Tmin = griddata(zip(lon_rdaps,lat_rdaps),Tmin_org,zip(lon_kor,lat_kor),method='linear') - 273.15
    FrictionalVelocity = griddata(zip(lon_rdaps,lat_rdaps),FrictionalVelocity_org,zip(lon_kor,lat_kor),method='linear')
    PotentialEnergy = griddata(zip(lon_rdaps,lat_rdaps),PotentialEnergy_org,zip(lon_kor,lat_kor),method='linear')
    SurfaceRoughness = griddata(zip(lon_rdaps,lat_rdaps),SurfaceRoughness_org,zip(lon_kor,lat_kor),method='linear')
    LatentHeatFlux = griddata(zip(lon_rdaps,lat_rdaps),LatentHeatFlux_org,zip(lon_kor,lat_kor),method='linear')
    SpecificHumidity = griddata(zip(lon_rdaps,lat_rdaps),SpecificHumidity_org,zip(lon_kor,lat_kor),method='linear')

    
    matlab.savemat(os.path.join(path_kor,'RDAPS/Temp/',str(yr)),'/kor_T_{yr_doy_utc}.mat',{'T':T})
    matlab.savemat(os.path.join(path_kor,'RDAPS/Dew/',str(yr)),'/kor_D_{yr_doy_utc}.mat',{'D':D})
    matlab.savemat(os.path.join(path_kor,'RDAPS/RH/',str(yr)),'/kor_RH_{yr_doy_utc}.mat',{'RH':RH})
    matlab.savemat(os.path.join(path_kor,'RDAPS/Uwind/',str(yr)),'/kor_U_{yr_doy_utc}.mat',{'U':U})
    matlab.savemat(os.path.join(path_kor,'RDAPS/Vwind/',str(yr)),'/kor_V_{yr_doy_utc}.mat',{'V':V})
    matlab.savemat(os.path.join(path_kor,'RDAPS/MaxWS/',str(yr)),'/kor_maxWS_{yr_doy_utc}.mat',{'maxWS':maxWS})
    matlab.savemat(os.path.join(path_kor,'RDAPS/Pressure/',str(yr)),'/kor_Pressure_srf_{yr_doy_utc}.mat',{'P_srf':P_srf})
    matlab.savemat(os.path.join(path_kor,'RDAPS/PBLH/',str(yr)),'/kor_PBLH_{yr_doy_utc}.mat','PBLH')
    matlab.savemat(os.path.join(path_kor,'RDAPS/Visibility/',str(yr)),'/kor_Visibility_{yr_doy_utc}.mat',{'Visibility':Visibility})
    matlab.savemat(os.path.join(path_kor,'RDAPS/Temp_surface/',str(yr)),'/kor_Tsrf_{yr_doy_utc}.mat',{'Tsrf':Tsrf})
    matlab.savemat(os.path.join(path_kor,'RDAPS/Temp_max/',str(yr)),'/kor_Tmax_{yr_doy_utc}.mat',{'Tmax':Tmax})
    matlab.savemat(os.path.join(path_kor,'RDAPS/Temp_min/',str(yr)),'/kor_Tmin_{yr_doy_utc}.mat',{'Tmin':Tmin})
    matlab.savemat(os.path.join(path_kor,'RDAPS/AP3h/',str(yr)),'/kor_AP3h_{yr_doy_utc}.mat',{'AP3h':AP3h})
    matlab.savemat(os.path.join(path_kor,'RDAPS/FrictionalVelocity/',str(yr)),'/kor_FrictionalVelocity_{yr_doy_utc}.mat',{'FrictionalVelocity':FrictionalVelocity})
    matlab.savemat(os.path.join(path_kor,'RDAPS/PotentialEnergy/',str(yr)),'/kor_PotentialEnergy_{yr_doy_utc}.mat',{'PotentialEnergy':PotentialEnergy})
    matlab.savemat(os.path.join(path_kor,'RDAPS/SurfaceRoughness/',str(yr)),'/kor_SurfaceRoughness_{yr_doy_utc}.mat',{'SurfaceRoughness':SurfaceRoughness})
    matlab.savemat(os.path.join(path_kor,'RDAPS/LatentHeatFlux/',str(yr)),'/kor_LatentHeatFlux_{yr_doy_utc}.mat',{'LatentHeatFlux':LatentHeatFlux})
    matlab.savemat(os.path.join(path_kor,'RDAPS/SpecificHumidity/',str(yr)),'/kor_SpecificHumidity_{yr_doy_utc}.mat',{'SpecificHumidity':SpecificHumidity})
    print (i)
""" 
## 2016 0128-0214 18시 자료
raw_rdaps_path = os.path.join(data_base_dir, 'Raw', 'RDAPS')
rdaps_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'RDAPS')  #path = '/share/irisnas5/Data/pre/RDAPS/' # rdaps_path = '/share/irisnas7/RAW_DATA/UM/RDAPS/analysis/'
# addpath(genpath('/share/irisnas5/Data/matlab_func/'))
# setup_nctoolbox



# 변수 뽑기
fname_list = ['r120v070ereaunish000.2016012818.gb2','r120v070ereaunish000.2016012918.gb2', \
    'r120v070ereaunish000.2016013018.gb2','r120v070ereaunish000.2016013118.gb2', \
    'r120v070ereaunish000.2016020118.gb2','r120v070ereaunish000.2016020218.gb2', \
    'r120v070ereaunish000.2016020318.gb2','r120v070ereaunish000.2016020418.gb2', \
    'r120v070ereaunish000.2016020518.gb2','r120v070ereaunish000.2016020618.gb2', \
    'r120v070ereaunish000.2016020718.gb2','r120v070ereaunish000.2016020818.gb2', \
    'r120v070ereaunish000.2016020918.gb2','r120v070ereaunish000.2016021018.gb2', \
    'r120v070ereaunish000.2016021118.gb2','r120v070ereaunish000.2016021218.gb2', \
    'r120v070ereaunish000.2016021318.gb2','r120v070ereaunish000.2016021418.gb2']
yr=2016
for k in range(1, 18+1):
    rdaps = np.full((419,491,18), np.nan)

    rdaps_data = pygrib.open(os.path.join(raw_rdaps_path, str(yr), fname_list[k]))        
    data = rdaps_data.select(name='Temperature', typeOfLevel='heightAboveGround')[0].values
    rdaps[:,:,0] = np.squeeze(data)
    data = rdaps_data.select(name='Dew point temperature', typeOfLevel='heightAboveGround')[0].values
    rdaps[:,:,1] = np.squeeze(data)
    data = rdaps_data.select(name='Relative humidity', typeOfLevel='heightAboveGround')[0].values
    rdaps[:,:,2] = np.squeeze(data)
    data = rdaps_data.select(name='10 metre U wind component', typeOfLevel='heightAboveGround')[0].values
    rdaps[:,:,3] = np.squeeze(data)
    data = rdaps_data.select(name='10 metre V wind component', typeOfLevel='heightAboveGround')[0].values
    rdaps[:,:,4] = np.squeeze(data)
    data = rdaps_data.select(name='Maximum wind speed', typeOfLevel='heightAboveGround')[0].values
    rdaps[:,:,5] = np.squeeze(data)
    data = rdaps_data.select(name='Surface pressure')[0].values
    rdaps[:,:,6] = np.squeeze(data)
    data = rdaps_data.select(name='Planetary boundary layer height')[0].values
    rdaps[:,:,7] = np.squeeze(data)
    data = rdaps_data.select(name='Visibility', typeOfLevel='heightAboveGround')[0].values
    rdaps[:,:,8] = np.squeeze(data)
    data = rdaps_data.select(name='Temperature', typeOfLevel='surface')[0].values
    rdaps[:,:,9] = np.squeeze(data)
    data = rdaps_data.select(name='Maximum temperature', typeOfLevel='heightAboveGround')[0].values
    rdaps[:,:,10] = np.squeeze(data)
    data = rdaps_data.select(name='Minimum temperature', typeOfLevel='heightAboveGround')[0].values
    rdaps[:,:,11] = np.squeeze(data)
    data = rdaps_data.select(parameterName='Total precipitation')[0].values
    rdaps[:,:,12] = np.squeeze(data)
    data = rdaps_data.select(name='Frictional velocity', typeOfLevel='heightAboveGround')[0].values
    rdaps[:,:,13] = np.squeeze(data)
    data = rdaps_data.select(name='Convective available potential energy')[0].values
    rdaps[:,:,14] = np.squeeze(data)
    data = rdaps_data.select(name='Surface roughness', typeOfLevel='surface')[0].values
    rdaps[:,:,15] = np.squeeze(data)
    data = rdaps_data.select(name='Latent heat net flux', typeOfLevel='surface')[0].values
    rdaps[:,:,16] = np.squeeze(data)
    data = rdaps_data.select(name='Specific humidity', typeOfLevel='heightAboveGround')[0].values
    rdaps[:,:,17] = np.squeeze(data)

    fname_save = f'RDAPS_2016_{k+27:03d}_18.mat'
    matlab.savemat(os.path.join(rdaps_path, str(yr)), fname_save,{'rdaps':rdaps})
    print (k)


## linear interpolation
curr_path = os.path.join(rdaps_path, str(yr))

for doy in range(28, 45+1):
    data12=matlab.loadmat(os.path.join(rdaps_path,'2016', f'RDAPS_2016_{doy:03d}_12.mat'))
    data18=matlab.loadmat(os.path.join(rdaps_path,'2016', f'RDAPS_2016_{doy:03d}_18.mat'))
    data24=matlab.loadmat(os.path.join(rdaps_path,'2016', f'RDAPS_2016_{doy+1:03d}_00.mat'))
    
    for j in range(1,5+1):
        rdaps = np.multiply((data18 - data12), (j/6)) + data12 # 13 to 17 UTC
        matlab.savemat(curr_path, f'RDAPS_2016_{doy:03d}_{j+12:02d}.mat',{'rdaps':rdaps})
        rdaps = np.multiply((data24 - data18), (j/6)) + data18 # 19 to 23 UTC
        matlab.savemat(curr_path, f'RDAPS_2016_{doy:03d}_{j+18:02d}.mat',{'rdaps':rdaps})
    print (doy)

##

path_kor='/share/irisnas5/Data/Korea/'
path_EA='/share/irisnas5/Data/EA_GOCI6km/'

for doy in range(28,45+1):
    for utc in range(13,23):
        yr_doy_utc = f'{yr}_{doy:03d}_{utc:02d}'
        mat = matlab.loadmat(os.path.join(rdaps_path, yr_doy_utc+'.mat'))
        rdaps = mat['rdpas']

        T_org = rdaps[:,:,0] # 'Temperature_height_above_ground'
        D_org = rdaps[:,:,1] # 'Dew-point_temperature_height_above_ground'
        RH_org = rdaps[:,:,2] # 'Relative_humidity_height_above_ground'
        U_org = rdaps[:,:,3] # 'u-component_of_wind_height_above_ground'
        V_org = rdaps[:,:,4] # 'v-component_of_wind_height_above_ground'
        maxWS_org = rdaps[:,:,5] # 'Maximum_wind_speed_height_above_ground_3_Hour_Maximum'
        P_srf_org = rdaps[:,:,6] # 'Pressure_surface'
        PBLH_org = rdaps[:,:,7] # 'Planetary_boundary_layer_height_UnknownLevelType-220'
        Visibility_org = rdaps[:,:,8] # 'Visibility_height_above_ground'
        Tsrf_org = rdaps[:,:,9] # 'Temperature_surface'
        Tmax_org = rdaps[:,:,10] # 'Maximum_temperature_height_above_ground_3_Hour_Maximum'
        Tmin_org = rdaps[:,:,11] # 'Minimum_temperature_height_above_ground_3_Hour_Minimum'
        AP3h_org = rdaps[:,:,12] # 'Total_precipitation_surface_3_Hour_Accumulation'
        FrictionalVelocity_org = rdaps[:,:,13] # 'Frictional_velocity_height_above_ground'
        PotentialEnergy_org = rdaps[:,:,14] # 'Convective_available_potential_energy_surface_layer_3_Hour_Maximum']
        SurfaceRoughness_org = rdaps[:,:,15] # 'Surface_roughness_surface'
        LatentHeatFlux_org = rdaps[:,:,16] # 'Latent_heat_net_flux_surface_3_Hour_Average'
        SpecificHumidity_org = rdaps[:,:,17] # 'Specific_humidity_height_above_ground'

        T = griddata(zip(lon_rdaps,lat_rdaps),T_org,zip(lon_goci,lat_goci),method='linear') -273.15
        D = griddata(zip(lon_rdaps,lat_rdaps),D_org,zip(lon_goci,lat_goci),method='linear') -273.15
        RH = griddata(zip(lon_rdaps,lat_rdaps),RH_org,zip(lon_goci,lat_goci),method='linear')
        U = griddata(zip(lon_rdaps,lat_rdaps),U_org,zip(lon_goci,lat_goci),method='linear')
        V = griddata(zip(lon_rdaps,lat_rdaps),V_org,zip(lon_goci,lat_goci),method='linear')
        maxWS = griddata(zip(lon_rdaps,lat_rdaps),maxWS_org,zip(lon_goci,lat_goci),method='linear')
        P_srf = griddata(zip(lon_rdaps,lat_rdaps),P_srf_org,zip(lon_goci,lat_goci),method='linear')
        PBLH = griddata(zip(lon_rdaps,lat_rdaps),PBLH_org,zip(lon_goci,lat_goci),method='linear')
        Visibility = griddata(zip(lon_rdaps,lat_rdaps),Visibility_org,zip(lon_goci,lat_goci),method='linear')
        Tsrf = griddata(zip(lon_rdaps,lat_rdaps),Tsrf_org,zip(lon_goci,lat_goci),method='linear') - 273.15
        Tmax = griddata(zip(lon_rdaps,lat_rdaps),Tmax_org,zip(lon_goci,lat_goci),method='linear') - 273.15
        Tmin = griddata(zip(lon_rdaps,lat_rdaps),Tmin_org,zip(lon_goci,lat_goci),method='linear') - 273.15
        AP3h = griddata(zip(lon_rdaps,lat_rdaps),AP3h_org,zip(lon_goci,lat_goci),method='linear')
        FrictionalVelocity = griddata(zip(lon_rdaps,lat_rdaps),FrictionalVelocity_org,zip(lon_goci,lat_goci),method='linear')
        PotentialEnergy = griddata(zip(lon_rdaps,lat_rdaps),PotentialEnergy_org,zip(lon_goci,lat_goci),method='linear')
        SurfaceRoughness = griddata(zip(lon_rdaps,lat_rdaps),SurfaceRoughness_org,zip(lon_goci,lat_goci),method='linear')
        LatentHeatFlux = griddata(zip(lon_rdaps,lat_rdaps),LatentHeatFlux_org,zip(lon_goci,lat_goci),method='linear')
        SpecificHumidity = griddata(zip(lon_rdaps,lat_rdaps),SpecificHumidity_org,zip(lon_goci,lat_goci),method='linear')

        matlab.savemat(os.path.join(path_EA,'RDAPS/Temp/',str(yr)),f'EA6km_T_{yr_doy_utc}.mat',{'T':T})
        matlab.savemat(os.path.join(path_EA,'RDAPS/Dew/',str(yr)),f'EA6km_D_{yr_doy_utc}.mat',{'D':D})
        matlab.savemat(os.path.join(path_EA,'RDAPS/RH/',str(yr)),f'EA6km_RH_{yr_doy_utc}.mat',{'RH':RH})
        matlab.savemat(os.path.join(path_EA,'RDAPS/Uwind/',str(yr)),f'EA6km_U_{yr_doy_utc}.mat',{'U':U})
        matlab.savemat(os.path.join(path_EA,'RDAPS/Vwind/',str(yr)),f'EA6km_V_{yr_doy_utc}.mat',{'V':V})
        matlab.savemat(os.path.join(path_EA,'RDAPS/MaxWS/',str(yr)),f'EA6km_maxWS_{yr_doy_utc}.mat',{'maxWS':maxWS})
        matlab.savemat(os.path.join(path_EA,'RDAPS/Pressure/',str(yr)),f'EA6km_Pressure_srf_{yr_doy_utc}.mat',{'P_srf':P_srf})
        matlab.savemat(os.path.join(path_EA,'RDAPS/PBLH/',str(yr)),f'EA6km_PBLH_{yr_doy_utc}.mat','PBLH')
        matlab.savemat(os.path.join(path_EA,'RDAPS/Visibility/',str(yr)),f'EA6km_Visibility_{yr_doy_utc}.mat',{'Visibility':Visibility})
        matlab.savemat(os.path.join(path_EA,'RDAPS/Temp_surface/',str(yr)),f'EA6km_Tsrf_{yr_doy_utc}.mat',{'Tsrf':Tsrf})
        matlab.savemat(os.path.join(path_EA,'RDAPS/Temp_max/',str(yr)),f'EA6km_Tmax_{yr_doy_utc}.mat',{'Tmax':Tmax})
        matlab.savemat(os.path.join(path_EA,'RDAPS/Temp_min/',str(yr)),f'EA6km_Tmin_{yr_doy_utc}.mat',{'Tmin':Tmin})
        matlab.savemat(os.path.join(path_EA,'RDAPS/AP3h/',str(yr)),f'EA6km_AP3h_{yr_doy_utc}.mat',{'AP3h':AP3h})
        matlab.savemat(os.path.join(path_EA,'RDAPS/FrictionalVelocity/',str(yr)),f'EA6km_FrictionalVelocity_{yr_doy_utc}.mat',{'FrictionalVelocity':FrictionalVelocity})
        matlab.savemat(os.path.join(path_EA,'RDAPS/PotentialEnergy/',str(yr)),f'EA6km_PotentialEnergy_{yr_doy_utc}.mat',{'PotentialEnergy':PotentialEnergy})
        matlab.savemat(os.path.join(path_EA,'RDAPS/SurfaceRoughness/',str(yr)),f'EA6km_SurfaceRoughness_{yr_doy_utc}.mat',{'SurfaceRoughness':SurfaceRoughness})
        matlab.savemat(os.path.join(path_EA,'RDAPS/LatentHeatFlux/',str(yr)),f'EA6km_LatentHeatFlux_{yr_doy_utc}.mat',{'LatentHeatFlux':LatentHeatFlux})
        matlab.savemat(os.path.join(path_EA,'RDAPS/SpecificHumidity/',str(yr)),f'EA6km_SpecificHumidity_{yr_doy_utc}.mat',{'SpecificHumidity':SpecificHumidity})

        T = griddata(zip(lon_rdaps,lat_rdaps),T_org,zip(lon_kor,lat_kor),method='linear') -273.15
        D = griddata(zip(lon_rdaps,lat_rdaps),D_org,zip(lon_kor,lat_kor),method='linear') -273.15
        RH = griddata(zip(lon_rdaps,lat_rdaps),RH_org,zip(lon_kor,lat_kor),method='linear')
        U = griddata(zip(lon_rdaps,lat_rdaps),U_org,zip(lon_kor,lat_kor),method='linear')
        V = griddata(zip(lon_rdaps,lat_rdaps),V_org,zip(lon_kor,lat_kor),method='linear')
        maxWS = griddata(zip(lon_rdaps,lat_rdaps),maxWS_org,zip(lon_kor,lat_kor),method='linear')
        P_srf = griddata(zip(lon_rdaps,lat_rdaps),P_srf_org,zip(lon_kor,lat_kor),method='linear')
        PBLH = griddata(zip(lon_rdaps,lat_rdaps),PBLH_org,zip(lon_kor,lat_kor),method='linear')
        Visibility = griddata(zip(lon_rdaps,lat_rdaps),Visibility_org,zip(lon_kor,lat_kor),method='linear')
        Tsrf = griddata(zip(lon_rdaps,lat_rdaps),Tsrf_org,zip(lon_kor,lat_kor),method='linear') - 273.15
        Tmax = griddata(zip(lon_rdaps,lat_rdaps),Tmax_org,zip(lon_kor,lat_kor),method='linear') - 273.15
        Tmin = griddata(zip(lon_rdaps,lat_rdaps),Tmin_org,zip(lon_kor,lat_kor),method='linear') - 273.15
        FrictionalVelocity = griddata(zip(lon_rdaps,lat_rdaps),FrictionalVelocity_org,zip(lon_kor,lat_kor),method='linear')
        PotentialEnergy = griddata(zip(lon_rdaps,lat_rdaps),PotentialEnergy_org,zip(lon_kor,lat_kor),method='linear')
        SurfaceRoughness = griddata(zip(lon_rdaps,lat_rdaps),SurfaceRoughness_org,zip(lon_kor,lat_kor),method='linear')
        LatentHeatFlux = griddata(zip(lon_rdaps,lat_rdaps),LatentHeatFlux_org,zip(lon_kor,lat_kor),method='linear')
        SpecificHumidity = griddata(zip(lon_rdaps,lat_rdaps),SpecificHumidity_org,zip(lon_kor,lat_kor),method='linear')


        matlab.savemat(os.path.join(path_kor,'RDAPS/Temp/',str(yr)),'/kor_T_{yr_doy_utc}.mat',{'T':T})
        matlab.savemat(os.path.join(path_kor,'RDAPS/Dew/',str(yr)),'/kor_D_{yr_doy_utc}.mat',{'D':D})
        matlab.savemat(os.path.join(path_kor,'RDAPS/RH/',str(yr)),'/kor_RH_{yr_doy_utc}.mat',{'RH':RH})
        matlab.savemat(os.path.join(path_kor,'RDAPS/Uwind/',str(yr)),'/kor_U_{yr_doy_utc}.mat',{'U':U})
        matlab.savemat(os.path.join(path_kor,'RDAPS/Vwind/',str(yr)),'/kor_V_{yr_doy_utc}.mat',{'V':V})
        matlab.savemat(os.path.join(path_kor,'RDAPS/MaxWS/',str(yr)),'/kor_maxWS_{yr_doy_utc}.mat',{'maxWS':maxWS})
        matlab.savemat(os.path.join(path_kor,'RDAPS/Pressure/',str(yr)),'/kor_Pressure_srf_{yr_doy_utc}.mat',{'P_srf':P_srf})
        matlab.savemat(os.path.join(path_kor,'RDAPS/PBLH/',str(yr)),'/kor_PBLH_{yr_doy_utc}.mat','PBLH')
        matlab.savemat(os.path.join(path_kor,'RDAPS/Visibility/',str(yr)),'/kor_Visibility_{yr_doy_utc}.mat',{'Visibility':Visibility})
        print (yr_doy_utc)
    print (doy)

