%% 2015082006 
for j=1:5
    rdaps = (data06 - data00).*(j/6) + data00; % 01 to 05 UTC
    save(['RDAPS_2015_232_',num2str(j,'%02i')],'rdaps');
    rdaps = (data12 - data06).*(j/6) + data06; % 07 to 11 UTC
    save(['RDAPS_2015_232_',num2str(j+6,'%02i')],'rdaps');
end

path_kor='/share/irisnas5/Data/Korea/';
path_EA='/share/irisnas5/Data/EA_GOCI6km/';

for utc=1:11
    yr_doy_utc = ['2015_232_',num2str(utc,'%02i')];
    load(['RDAPS_2015_232_',num2str(utc,'%02i')])
    T_org = rdaps(:,:,1); % 'Temperature_height_above_ground'
    D_org = rdaps(:,:,2); % 'Dew-point_temperature_height_above_ground'
    RH_org = rdaps(:,:,3); % 'Relative_humidity_height_above_ground'
    U_org = rdaps(:,:,4); % 'u-component_of_wind_height_above_ground'
    V_org = rdaps(:,:,5); % 'v-component_of_wind_height_above_ground'
    maxWS_org = rdaps(:,:,6); % 'Maximum_wind_speed_height_above_ground_3_Hour_Maximum'
    P_srf_org = rdaps(:,:,7); % 'Pressure_surface'
    PBLH_org = rdaps(:,:,8); % 'Planetary_boundary_layer_height_UnknownLevelType-220'
    Visibility_org = rdaps(:,:,9); % 'Visibility_height_above_ground'
    Tsrf_org = rdaps(:,:,10); % 'Temperature_surface'
    Tmax_org = rdaps(:,:,11); % 'Maximum_temperature_height_above_ground_3_Hour_Maximum'
    Tmin_org = rdaps(:,:,12); % 'Minimum_temperature_height_above_ground_3_Hour_Minimum'
    AP3h_org = rdaps(:,:,13); % 'Total_precipitation_surface_3_Hour_Accumulation'
    FrictionalVelocity_org = rdaps(:,:,14); % 'Frictional_velocity_height_above_ground'
    PotentialEnergy_org = rdaps(:,:,15); % 'Convective_available_potential_energy_surface_layer_3_Hour_Maximum')
    SurfaceRoughness_org = rdaps(:,:,16); % 'Surface_roughness_surface'
    LatentHeatFlux_org = rdaps(:,:,17); % 'Latent_heat_net_flux_surface_3_Hour_Average'
    SpecificHumidity_org = rdaps(:,:,18); % 'Specific_humidity_height_above_ground'
    
    T = griddata(lon_rdaps,lat_rdaps,T_org,lon_goci,lat_goci,'linear') -273.15;
    D = griddata(lon_rdaps,lat_rdaps,D_org,lon_goci,lat_goci,'linear') -273.15;
    RH = griddata(lon_rdaps,lat_rdaps,RH_org,lon_goci,lat_goci,'linear');
    U = griddata(lon_rdaps,lat_rdaps,U_org,lon_goci,lat_goci,'linear');
    V = griddata(lon_rdaps,lat_rdaps,V_org,lon_goci,lat_goci,'linear');
    maxWS = griddata(lon_rdaps,lat_rdaps,maxWS_org,lon_goci,lat_goci,'linear');
    P_srf = griddata(lon_rdaps,lat_rdaps,P_srf_org,lon_goci,lat_goci,'linear');
    PBLH = griddata(lon_rdaps,lat_rdaps,PBLH_org,lon_goci,lat_goci,'linear');
    Visibility = griddata(lon_rdaps,lat_rdaps,Visibility_org,lon_goci,lat_goci,'linear');
    Tsrf = griddata(lon_rdaps,lat_rdaps,Tsrf_org,lon_goci,lat_goci,'linear') - 273.15;
    Tmax = griddata(lon_rdaps,lat_rdaps,Tmax_org,lon_goci,lat_goci,'linear') - 273.15;
    Tmin = griddata(lon_rdaps,lat_rdaps,Tmin_org,lon_goci,lat_goci,'linear') - 273.15;
    AP3h = griddata(lon_rdaps,lat_rdaps,AP3h_org,lon_goci,lat_goci,'linear');
    FrictionalVelocity = griddata(lon_rdaps,lat_rdaps,FrictionalVelocity_org,lon_goci,lat_goci,'linear');
    PotentialEnergy = griddata(lon_rdaps,lat_rdaps,PotentialEnergy_org,lon_goci,lat_goci,'linear');
    SurfaceRoughness = griddata(lon_rdaps,lat_rdaps,SurfaceRoughness_org,lon_goci,lat_goci,'linear');
    LatentHeatFlux = griddata(lon_rdaps,lat_rdaps,LatentHeatFlux_org,lon_goci,lat_goci,'linear');
    SpecificHumidity = griddata(lon_rdaps,lat_rdaps,SpecificHumidity_org,lon_goci,lat_goci,'linear');
    
    save([path_EA,'RDAPS/Temp/',num2str(yr),'/EA6km_T_',yr_doy_utc],'T')
    save([path_EA,'RDAPS/Dew/',num2str(yr),'/EA6km_D_',yr_doy_utc],'D')
    save([path_EA,'RDAPS/RH/',num2str(yr),'/EA6km_RH_',yr_doy_utc],'RH')
    save([path_EA,'RDAPS/Uwind/',num2str(yr),'/EA6km_U_',yr_doy_utc],'U')
    save([path_EA,'RDAPS/Vwind/',num2str(yr),'/EA6km_V_',yr_doy_utc],'V')
    save([path_EA,'RDAPS/MaxWS/',num2str(yr),'/EA6km_maxWS_',yr_doy_utc],'maxWS')
    save([path_EA,'RDAPS/Pressure/',num2str(yr),'/EA6km_Pressure_srf_',yr_doy_utc],'P_srf')
    save([path_EA,'RDAPS/PBLH/',num2str(yr),'/EA6km_PBLH_',yr_doy_utc],'PBLH')
    save([path_EA,'RDAPS/Visibility/',num2str(yr),'/EA6km_Visibility_',yr_doy_utc],'Visibility')
    save([path_EA,'RDAPS/Temp_surface/',num2str(yr),'/EA6km_Tsrf_',yr_doy_utc],'Tsrf')
    save([path_EA,'RDAPS/Temp_max/',num2str(yr),'/EA6km_Tmax_',yr_doy_utc],'Tmax')
    save([path_EA,'RDAPS/Temp_min/',num2str(yr),'/EA6km_Tmin_',yr_doy_utc],'Tmin')
    save([path_EA,'RDAPS/AP3h/',num2str(yr),'/EA6km_AP3h_',yr_doy_utc],'AP3h')
    save([path_EA,'RDAPS/FrictionalVelocity/',num2str(yr),'/EA6km_FrictionalVelocity_',yr_doy_utc],'FrictionalVelocity')
    save([path_EA,'RDAPS/PotentialEnergy/',num2str(yr),'/EA6km_PotentialEnergy_',yr_doy_utc],'PotentialEnergy')
    save([path_EA,'RDAPS/SurfaceRoughness/',num2str(yr),'/EA6km_SurfaceRoughness_',yr_doy_utc],'SurfaceRoughness')
    save([path_EA,'RDAPS/LatentHeatFlux/',num2str(yr),'/EA6km_LatentHeatFlux_',yr_doy_utc],'LatentHeatFlux')
    save([path_EA,'RDAPS/SpecificHumidity/',num2str(yr),'/EA6km_SpecificHumidity_',yr_doy_utc],'SpecificHumidity')
    
    T = griddata(lon_rdaps,lat_rdaps,T_org,lon_kor,lat_kor,'linear') -273.15;
    D = griddata(lon_rdaps,lat_rdaps,D_org,lon_kor,lat_kor,'linear') -273.15;
    RH = griddata(lon_rdaps,lat_rdaps,RH_org,lon_kor,lat_kor,'linear');
    U = griddata(lon_rdaps,lat_rdaps,U_org,lon_kor,lat_kor,'linear');
    V = griddata(lon_rdaps,lat_rdaps,V_org,lon_kor,lat_kor,'linear');
    maxWS = griddata(lon_rdaps,lat_rdaps,maxWS_org,lon_kor,lat_kor,'linear');
    P_srf = griddata(lon_rdaps,lat_rdaps,P_srf_org,lon_kor,lat_kor,'linear');
    PBLH = griddata(lon_rdaps,lat_rdaps,PBLH_org,lon_kor,lat_kor,'linear');
    Visibility = griddata(lon_rdaps,lat_rdaps,Visibility_org,lon_kor,lat_kor,'linear');
    Tsrf = griddata(lon_rdaps,lat_rdaps,Tsrf_org,lon_kor,lat_kor,'linear') - 273.15;
    Tmax = griddata(lon_rdaps,lat_rdaps,Tmax_org,lon_kor,lat_kor,'linear') - 273.15;
    Tmin = griddata(lon_rdaps,lat_rdaps,Tmin_org,lon_kor,lat_kor,'linear') - 273.15;
    FrictionalVelocity = griddata(lon_rdaps,lat_rdaps,FrictionalVelocity_org,lon_kor,lat_kor,'linear');
    PotentialEnergy = griddata(lon_rdaps,lat_rdaps,PotentialEnergy_org,lon_kor,lat_kor,'linear');
    SurfaceRoughness = griddata(lon_rdaps,lat_rdaps,SurfaceRoughness_org,lon_kor,lat_kor,'linear');
    LatentHeatFlux = griddata(lon_rdaps,lat_rdaps,LatentHeatFlux_org,lon_kor,lat_kor,'linear');
    SpecificHumidity = griddata(lon_rdaps,lat_rdaps,SpecificHumidity_org,lon_kor,lat_kor,'linear');
   
    save([path_kor,'RDAPS/Temp/',num2str(yr),'/kor_T_',yr_doy_utc],'T')
    save([path_kor,'RDAPS/Dew/',num2str(yr),'/kor_D_',yr_doy_utc],'D')
    save([path_kor,'RDAPS/RH/',num2str(yr),'/kor_RH_',yr_doy_utc],'RH')
    save([path_kor,'RDAPS/Uwind/',num2str(yr),'/kor_U_',yr_doy_utc],'U')
    save([path_kor,'RDAPS/Vwind/',num2str(yr),'/kor_V_',yr_doy_utc],'V')
    save([path_kor,'RDAPS/MaxWS/',num2str(yr),'/kor_maxWS_',yr_doy_utc],'maxWS')
    save([path_kor,'RDAPS/Pressure/',num2str(yr),'/kor_Pressure_srf_',yr_doy_utc],'P_srf')
    save([path_kor,'RDAPS/PBLH/',num2str(yr),'/kor_PBLH_',yr_doy_utc],'PBLH')
    save([path_kor,'RDAPS/Visibility/',num2str(yr),'/kor_Visibility_',yr_doy_utc],'Visibility')
    save([path_kor,'RDAPS/Temp_surface/',num2str(yr),'/kor_Tsrf_',yr_doy_utc],'Tsrf')
    save([path_kor,'RDAPS/Temp_max/',num2str(yr),'/kor_Tmax_',yr_doy_utc],'Tmax')
    save([path_kor,'RDAPS/Temp_min/',num2str(yr),'/kor_Tmin_',yr_doy_utc],'Tmin')
    save([path_kor,'RDAPS/FrictionalVelocity/',num2str(yr),'/kor_FrictionalVelocity_',yr_doy_utc],'FrictionalVelocity')
    save([path_kor,'RDAPS/PotentialEnergy/',num2str(yr),'/kor_PotentialEnergy_',yr_doy_utc],'PotentialEnergy')
    save([path_kor,'RDAPS/SurfaceRoughness/',num2str(yr),'/kor_SurfaceRoughness_',yr_doy_utc],'SurfaceRoughness')
    save([path_kor,'RDAPS/LatentHeatFlux/',num2str(yr),'/kor_LatentHeatFlux_',yr_doy_utc],'LatentHeatFlux')
    save([path_kor,'RDAPS/SpecificHumidity/',num2str(yr),'/kor_SpecificHumidity_',yr_doy_utc],'SpecificHumidity')

end

%% 2016 0128-0214 18시 자료
path_data = '/share/irisnas5/Data/';
path_rdaps = '/share/irisnas7/RAW_DATA/UM/RDAPS/analysis/';
path = '/share/irisnas5/Data/pre/RDAPS/';
% addpath(genpath('/share/irisnas5/Data/matlab_func/'))
% setup_nctoolbox

yr=2016;

% 변수 뽑기
fname_list = {'r120v070ereaunish000.2016012818.gb2','r120v070ereaunish000.2016012918.gb2',...
    'r120v070ereaunish000.2016013018.gb2','r120v070ereaunish000.2016013118.gb2',...
    'r120v070ereaunish000.2016020118.gb2','r120v070ereaunish000.2016020218.gb2',...
    'r120v070ereaunish000.2016020318.gb2','r120v070ereaunish000.2016020418.gb2',...
    'r120v070ereaunish000.2016020518.gb2','r120v070ereaunish000.2016020618.gb2',...
    'r120v070ereaunish000.2016020718.gb2','r120v070ereaunish000.2016020818.gb2',...
    'r120v070ereaunish000.2016020918.gb2','r120v070ereaunish000.2016021018.gb2',...
    'r120v070ereaunish000.2016021118.gb2','r120v070ereaunish000.2016021218.gb2',...
    'r120v070ereaunish000.2016021318.gb2','r120v070ereaunish000.2016021418.gb2'};

for k=1:18
    rdaps = NaN(419,491,18);
    rdaps_data = ncdataset([path_rdaps,'2016/',fname_list{k}]);
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
    
    fname_save = ['RDAPS_2016_',num2str(k+27,'%03i'),'_18.mat'];
    save([path,'2016/',fname_save],'rdaps') 
end


%% linear interpolation
cd([path, '2016'])

for doy=28:45
data12=importdata([path,'2016/RDAPS_2016_',num2str(doy,'%03i'),'_12.mat']);
data18=importdata([path,'2016/RDAPS_2016_',num2str(doy,'%03i'),'_18.mat']);
data24=importdata([path,'2016/RDAPS_2016_',num2str(doy+1,'%03i'),'_00.mat']);

for j=1:5
    rdaps = (data18 - data12).*(j/6) + data12; % 13 to 17 UTC
    save(['RDAPS_2016_',num2str(doy,'%03i'),'_',num2str(j+12,'%02i')],'rdaps');
    rdaps = (data24 - data18).*(j/6) + data18; % 19 to 23 UTC
    save(['RDAPS_2016_',num2str(doy,'%03i'),'_',num2str(j+18,'%02i')],'rdaps');
end
disp(doy)
end

%%

path_kor='/share/irisnas5/Data/Korea/';
path_EA='/share/irisnas5/Data/EA_GOCI6km/';

for doy=28:45
for utc=13:23
    yr_doy_utc = ['2016_',num2str(doy,'%03i'),'_',num2str(utc,'%02i')];
    load(['RDAPS_',yr_doy_utc])
    T_org = rdaps(:,:,1); % 'Temperature_height_above_ground'
    D_org = rdaps(:,:,2); % 'Dew-point_temperature_height_above_ground'
    RH_org = rdaps(:,:,3); % 'Relative_humidity_height_above_ground'
    U_org = rdaps(:,:,4); % 'u-component_of_wind_height_above_ground'
    V_org = rdaps(:,:,5); % 'v-component_of_wind_height_above_ground'
    maxWS_org = rdaps(:,:,6); % 'Maximum_wind_speed_height_above_ground_3_Hour_Maximum'
    P_srf_org = rdaps(:,:,7); % 'Pressure_surface'
    PBLH_org = rdaps(:,:,8); % 'Planetary_boundary_layer_height_UnknownLevelType-220'
    Visibility_org = rdaps(:,:,9); % 'Visibility_height_above_ground'
    Tsrf_org = rdaps(:,:,10); % 'Temperature_surface'
    Tmax_org = rdaps(:,:,11); % 'Maximum_temperature_height_above_ground_3_Hour_Maximum'
    Tmin_org = rdaps(:,:,12); % 'Minimum_temperature_height_above_ground_3_Hour_Minimum'
    AP3h_org = rdaps(:,:,13); % 'Total_precipitation_surface_3_Hour_Accumulation'
    FrictionalVelocity_org = rdaps(:,:,14); % 'Frictional_velocity_height_above_ground'
    PotentialEnergy_org = rdaps(:,:,15); % 'Convective_available_potential_energy_surface_layer_3_Hour_Maximum')
    SurfaceRoughness_org = rdaps(:,:,16); % 'Surface_roughness_surface'
    LatentHeatFlux_org = rdaps(:,:,17); % 'Latent_heat_net_flux_surface_3_Hour_Average'
    SpecificHumidity_org = rdaps(:,:,18); % 'Specific_humidity_height_above_ground'
    
    T = griddata(lon_rdaps,lat_rdaps,T_org,lon_goci,lat_goci,'linear') -273.15;
    D = griddata(lon_rdaps,lat_rdaps,D_org,lon_goci,lat_goci,'linear') -273.15;
    RH = griddata(lon_rdaps,lat_rdaps,RH_org,lon_goci,lat_goci,'linear');
    U = griddata(lon_rdaps,lat_rdaps,U_org,lon_goci,lat_goci,'linear');
    V = griddata(lon_rdaps,lat_rdaps,V_org,lon_goci,lat_goci,'linear');
    maxWS = griddata(lon_rdaps,lat_rdaps,maxWS_org,lon_goci,lat_goci,'linear');
    P_srf = griddata(lon_rdaps,lat_rdaps,P_srf_org,lon_goci,lat_goci,'linear');
    PBLH = griddata(lon_rdaps,lat_rdaps,PBLH_org,lon_goci,lat_goci,'linear');
    Visibility = griddata(lon_rdaps,lat_rdaps,Visibility_org,lon_goci,lat_goci,'linear');
    Tsrf = griddata(lon_rdaps,lat_rdaps,Tsrf_org,lon_goci,lat_goci,'linear') - 273.15;
    Tmax = griddata(lon_rdaps,lat_rdaps,Tmax_org,lon_goci,lat_goci,'linear') - 273.15;
    Tmin = griddata(lon_rdaps,lat_rdaps,Tmin_org,lon_goci,lat_goci,'linear') - 273.15;
    AP3h = griddata(lon_rdaps,lat_rdaps,AP3h_org,lon_goci,lat_goci,'linear');
    FrictionalVelocity = griddata(lon_rdaps,lat_rdaps,FrictionalVelocity_org,lon_goci,lat_goci,'linear');
    PotentialEnergy = griddata(lon_rdaps,lat_rdaps,PotentialEnergy_org,lon_goci,lat_goci,'linear');
    SurfaceRoughness = griddata(lon_rdaps,lat_rdaps,SurfaceRoughness_org,lon_goci,lat_goci,'linear');
    LatentHeatFlux = griddata(lon_rdaps,lat_rdaps,LatentHeatFlux_org,lon_goci,lat_goci,'linear');
    SpecificHumidity = griddata(lon_rdaps,lat_rdaps,SpecificHumidity_org,lon_goci,lat_goci,'linear');
    
    save([path_EA,'RDAPS/Temp/',num2str(yr),'/EA6km_T_',yr_doy_utc],'T')
    save([path_EA,'RDAPS/Dew/',num2str(yr),'/EA6km_D_',yr_doy_utc],'D')
    save([path_EA,'RDAPS/RH/',num2str(yr),'/EA6km_RH_',yr_doy_utc],'RH')
    save([path_EA,'RDAPS/Uwind/',num2str(yr),'/EA6km_U_',yr_doy_utc],'U')
    save([path_EA,'RDAPS/Vwind/',num2str(yr),'/EA6km_V_',yr_doy_utc],'V')
    save([path_EA,'RDAPS/MaxWS/',num2str(yr),'/EA6km_maxWS_',yr_doy_utc],'maxWS')
    save([path_EA,'RDAPS/Pressure/',num2str(yr),'/EA6km_Pressure_srf_',yr_doy_utc],'P_srf')
    save([path_EA,'RDAPS/PBLH/',num2str(yr),'/EA6km_PBLH_',yr_doy_utc],'PBLH')
    save([path_EA,'RDAPS/Visibility/',num2str(yr),'/EA6km_Visibility_',yr_doy_utc],'Visibility')
    save([path_EA,'RDAPS/Temp_surface/',num2str(yr),'/EA6km_Tsrf_',yr_doy_utc],'Tsrf')
    save([path_EA,'RDAPS/Temp_max/',num2str(yr),'/EA6km_Tmax_',yr_doy_utc],'Tmax')
    save([path_EA,'RDAPS/Temp_min/',num2str(yr),'/EA6km_Tmin_',yr_doy_utc],'Tmin')
    save([path_EA,'RDAPS/AP3h/',num2str(yr),'/EA6km_AP3h_',yr_doy_utc],'AP3h')
    save([path_EA,'RDAPS/FrictionalVelocity/',num2str(yr),'/EA6km_FrictionalVelocity_',yr_doy_utc],'FrictionalVelocity')
    save([path_EA,'RDAPS/PotentialEnergy/',num2str(yr),'/EA6km_PotentialEnergy_',yr_doy_utc],'PotentialEnergy')
    save([path_EA,'RDAPS/SurfaceRoughness/',num2str(yr),'/EA6km_SurfaceRoughness_',yr_doy_utc],'SurfaceRoughness')
    save([path_EA,'RDAPS/LatentHeatFlux/',num2str(yr),'/EA6km_LatentHeatFlux_',yr_doy_utc],'LatentHeatFlux')
    save([path_EA,'RDAPS/SpecificHumidity/',num2str(yr),'/EA6km_SpecificHumidity_',yr_doy_utc],'SpecificHumidity')
    
    T = griddata(lon_rdaps,lat_rdaps,T_org,lon_kor,lat_kor,'linear') -273.15;
    D = griddata(lon_rdaps,lat_rdaps,D_org,lon_kor,lat_kor,'linear') -273.15;
    RH = griddata(lon_rdaps,lat_rdaps,RH_org,lon_kor,lat_kor,'linear');
    U = griddata(lon_rdaps,lat_rdaps,U_org,lon_kor,lat_kor,'linear');
    V = griddata(lon_rdaps,lat_rdaps,V_org,lon_kor,lat_kor,'linear');
    maxWS = griddata(lon_rdaps,lat_rdaps,maxWS_org,lon_kor,lat_kor,'linear');
    P_srf = griddata(lon_rdaps,lat_rdaps,P_srf_org,lon_kor,lat_kor,'linear');
    PBLH = griddata(lon_rdaps,lat_rdaps,PBLH_org,lon_kor,lat_kor,'linear');
    Visibility = griddata(lon_rdaps,lat_rdaps,Visibility_org,lon_kor,lat_kor,'linear');
    Tsrf = griddata(lon_rdaps,lat_rdaps,Tsrf_org,lon_kor,lat_kor,'linear') - 273.15;
    Tmax = griddata(lon_rdaps,lat_rdaps,Tmax_org,lon_kor,lat_kor,'linear') - 273.15;
    Tmin = griddata(lon_rdaps,lat_rdaps,Tmin_org,lon_kor,lat_kor,'linear') - 273.15;
    FrictionalVelocity = griddata(lon_rdaps,lat_rdaps,FrictionalVelocity_org,lon_kor,lat_kor,'linear');
    PotentialEnergy = griddata(lon_rdaps,lat_rdaps,PotentialEnergy_org,lon_kor,lat_kor,'linear');
    SurfaceRoughness = griddata(lon_rdaps,lat_rdaps,SurfaceRoughness_org,lon_kor,lat_kor,'linear');
    LatentHeatFlux = griddata(lon_rdaps,lat_rdaps,LatentHeatFlux_org,lon_kor,lat_kor,'linear');
    SpecificHumidity = griddata(lon_rdaps,lat_rdaps,SpecificHumidity_org,lon_kor,lat_kor,'linear');
   
    save([path_kor,'RDAPS/Temp/',num2str(yr),'/kor_T_',yr_doy_utc],'T')
    save([path_kor,'RDAPS/Dew/',num2str(yr),'/kor_D_',yr_doy_utc],'D')
    save([path_kor,'RDAPS/RH/',num2str(yr),'/kor_RH_',yr_doy_utc],'RH')
    save([path_kor,'RDAPS/Uwind/',num2str(yr),'/kor_U_',yr_doy_utc],'U')
    save([path_kor,'RDAPS/Vwind/',num2str(yr),'/kor_V_',yr_doy_utc],'V')
    save([path_kor,'RDAPS/MaxWS/',num2str(yr),'/kor_maxWS_',yr_doy_utc],'maxWS')
    save([path_kor,'RDAPS/Pressure/',num2str(yr),'/kor_Pressure_srf_',yr_doy_utc],'P_srf')
    save([path_kor,'RDAPS/PBLH/',num2str(yr),'/kor_PBLH_',yr_doy_utc],'PBLH')
    save([path_kor,'RDAPS/Visibility/',num2str(yr),'/kor_Visibility_',yr_doy_utc],'Visibility')
    save([path_kor,'RDAPS/Temp_surface/',num2str(yr),'/kor_Tsrf_',yr_doy_utc],'Tsrf')
    save([path_kor,'RDAPS/Temp_max/',num2str(yr),'/kor_Tmax_',yr_doy_utc],'Tmax')
    save([path_kor,'RDAPS/Temp_min/',num2str(yr),'/kor_Tmin_',yr_doy_utc],'Tmin')
    save([path_kor,'RDAPS/FrictionalVelocity/',num2str(yr),'/kor_FrictionalVelocity_',yr_doy_utc],'FrictionalVelocity')
    save([path_kor,'RDAPS/PotentialEnergy/',num2str(yr),'/kor_PotentialEnergy_',yr_doy_utc],'PotentialEnergy')
    save([path_kor,'RDAPS/SurfaceRoughness/',num2str(yr),'/kor_SurfaceRoughness_',yr_doy_utc],'SurfaceRoughness')
    save([path_kor,'RDAPS/LatentHeatFlux/',num2str(yr),'/kor_LatentHeatFlux_',yr_doy_utc],'LatentHeatFlux')
    save([path_kor,'RDAPS/SpecificHumidity/',num2str(yr),'/kor_SpecificHumidity_',yr_doy_utc],'SpecificHumidity')
disp(yr_doy_utc)
end
disp(doy)
end
