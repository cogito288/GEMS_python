### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import time
import numpy as np
import pandas as pd
import h5py

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km')
path_goci_filter = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_filtered')

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_goci.mat')) # lon_goci, lat_goci
lon_goci, lat_goci = mat['lon_goci'], mat['lat_goci']
del mat

#%% header
hd_sat = ['OMNO2d_tc','OMSO2e_tc','OMDOAO3e_tc','OMHCHOG_tc', 'AOD','AE','FMF','SSA','NDVI','RSDN','Precip','DEM'] ## satellite data(12)
hd_rdaps = ['Temp','Dew','RH','P_srf','MaxWS','PBLH','Visibility','Tsrf','Tmax','Tmin',
    'FrictionalVelocity','PotentialEnergy','SurfaceRoughness','LatentHeatFlux','SpecificHumidity',
    'stack1_maxWS','stack3_maxWS','stack5_maxWS','stack7_maxWS','WS','Wcos','Wsin','AP3h'] # numerical data(RDAPS)(23)
hd_etc = ['DOY','PopDens','RoadDens'] # etc data(3)
hd_emis = ['ISOPRENE','TRP1','CH4','NO','NO2','NH3','HCOOH','HCHO','CO','SO2',
    'PMFINE','PNO3','POA','PSO4'] # SMOKE data (14)
hd_lc = ['LC_barren','LC_crop','LC_forest','LC_grass','LC_savannas','LC_shrub',
    'LC_urban','LC_water','LC_wetland','LC_veg'] # LC ratio (10)

header = hd_sat+hd_rdaps+hd_etc+hd_emis+hd_lc+['OMNO2d_trop_tc']
nvar = 63

## Read stationary data
# ==== Stationary data ====
#dem = matlab.loadmat(os.path.join(path_ea_goci, 'stationary', 'EA6km_SRTM_DEM_masked.mat'))['dem'] # dem
dem = matlab.loadmat(os.path.join(path_ea_goci, 'stationary', 'EA6km_SRTM_DEM.mat'))['dem'] # dem
roadDens = matlab.loadmat(os.path.join(path_ea_goci, 'stationary', 'EA6km_roadDens.mat'))['roadDens'] # roadDens

# Read MODIS landcover ratio by class
LC_vars = dict()
for k in range(9):
    LC_vars[hd_lc[k]] = matlab.loadmat(os.path.join(path_ea_goci,'MODIS_LC_ratio',f'EA6km_{hd_lc[k][3:]}_ratio_r6_2016.mat'))[hd_lc[k]]
LC_vars['LC_veg'] = LC_vars['LC_forest']+LC_vars['LC_grass']+LC_vars['LC_savannas']+LC_vars['LC_shrub']
LC_ratio = np.array([LC_vars['LC_barren'].ravel(order='F'), LC_vars['LC_crop'].ravel(order='F'), LC_vars['LC_forest'].ravel(order='F'), LC_vars['LC_grass'].ravel(order='F'), LC_vars['LC_savannas'].ravel(order='F'), LC_vars['LC_shrub'].ravel(order='F'), LC_vars['LC_urban'].ravel(order='F'), LC_vars['LC_water'].ravel(order='F'), LC_vars['LC_wetland'].ravel(order='F'), LC_vars['LC_veg'].ravel(order='F')]).T
del LC_vars


YEARS = [2016]
for yr in YEARS:
    print (f'Year : {yr}')
    if yr%4==0: days = 366
    else: days = 365
    if yr==2019: days = 114
    # ==== Yearly data ====
    # Read population density
    popDens = matlab.loadmat(os.path.join(path_ea_goci, 'PopDens', f'EA6km_popDens_{yr}.mat'))['popDens']
    
    for doy in range(1, days+1):
        # ==== Daily data ====
        # Read MODIS(AQUA) 16-days NDVI (ndvi)
        doy = 9
        if doy<9:
            ndvi = matlab.loadmat(os.path.join(path_ea_goci, 'MODIS_NDVI',str(yr-1),f'EA_MODIS_NDVI_{yr-1}_361.mat'))['ndvi']
        else:
            num = int(np.ceil((doy-8)/16)*16-7)
            ndvi = matlab.loadmat(os.path.join(path_ea_goci, 'MODIS_NDVI',str(yr),f'EA_MODIS_NDVI_{yr}_{num:03d}.mat'))['ndvi']
        
        if yr<2019:
            ndvi = ndvi.astype('float64')
            ndvi[ndvi==-32768] = np.nan
            ndvi = np.divide(ndvi, 10000)
            ndvi[np.abs(ndvi)>=0.99] = np.nan
        # Load OMI temporal convolutioned data
        omno2d = matlab.loadmat(os.path.join(path_ea_goci,'OMI_tempConv','OMNO2d',str(yr),f'EA6km_OMNO2d_{yr}_{doy:03d}.mat'))['omno2d']
        omno2d[omno2d<0]=np.nan

        omno2d_trop=matlab.loadmat(os.path.join(path_ea_goci,'OMI_tempConv','OMNO2d_trop_CS',str(yr),f'EA6km_OMNO2d_trop_CS_{yr}_{doy:03d}.mat'))['omno2d']
        omno2d_trop[omno2d_trop<0]=np.nan
        

        omso2e_m=matlab.loadmat(os.path.join(path_ea_goci,'OMI_tempConv/OMSO2e_m/',str(yr),f'EA6km_OMSO2e_m_{yr}_{doy:03d}.mat'))['omso2e_m']
        omso2e_m[omso2e_m<0]=np.nan
        
        omdoao3e_m=matlab.loadmat(os.path.join(path_ea_goci,'OMI_tempConv/OMDOAO3e_m/',str(yr),f'EA6km_OMDOAO3e_m_{yr}_{doy:03d}.mat'))['omdoao3e_m']
        omdoao3e_m[omdoao3e_m<0]=np.nan
        
        omhchog=matlab.loadmat(os.path.join(path_ea_goci,'OMI_tempConv/OMHCHOG/',str(yr),f'EA6km_OMHCHOG_{yr}_{doy:03d}.mat'))['omhchog']
        omhchog[omhchog<0]=np.nan

        # Read BESS soalr radiation at 13:30 (RSDN)
        if yr==2017:
            RSDN = matlab.loadmat(os.path.join(path_ea_goci,'BESS/',str(yr),f'EA6km_BESS_RSDN_{yr_doy}'))['RSDN']
       	for utc in range(7+1): 
            tStart = time.time()
            # ===== Hourly data =====
            # Read GOCI AOD products (GOCI_aod, GOCI_ae, GOCI_fmf, GOCI_ssa)
            GOCI_aod = matlab.loadmat(os.path.join(path_goci_filter,'AOD/',str(yr),f'GOCI_AOD_{yr}_{doy:03d}_{utc:02d}.mat'))['GOCI_aod']
            GOCI_ae = matlab.loadmat(os.path.join(path_goci_filter,'AE/',str(yr),f'GOCI_AE_{yr}_{doy:03d}_{utc:02d}.mat'))['GOCI_ae']
            GOCI_fmf = matlab.loadmat(os.path.join(path_goci_filter,'FMF/',str(yr),f'GOCI_FMF_{yr}_{doy:03d}_{utc:02d}.mat'))['GOCI_fmf']
            GOCI_ssa = matlab.loadmat(os.path.join(path_goci_filter,'SSA/',str(yr),f'GOCI_SSA_{yr}_{doy:03d}_{utc:02d}.mat'))['GOCI_ssa']

            # Read GPM accumulated precipitation (precip)
            try:
                precip = matlab.loadmat(os.path.join(path_ea_goci,'GPM_AP/',str(yr),f'EA6km_gpm_AP_{yr}_{doy:03d}_UTC{utc:02d}.mat'))['precip']
            except FileNotFoundError:
                precip = matlab.loadmat(os.path.join(path_ea_goci,'GPM_AP/',str(yr),f'EA6km_gpm_AP_{yr}_{doy:03d}_UTC{utc:02d}_early.mat'))['precip']
                pass
            doy =1
            # Read UM (RDAPS) data
            T = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/Temp/',str(yr),f'EA6km_T_{yr}_{doy:03d}_{utc:02d}.mat'))['T'] # T
            D = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/Dew/',str(yr),f'EA6km_D_{yr}_{doy:03d}_{utc:02d}.mat'))['D'] # D
            RH = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/RH/',str(yr),f'EA6km_RH_{yr}_{doy:03d}_{utc:02d}.mat'))['RH'] # RH
            P_srf = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/Pressure/',str(yr),f'EA6km_Pressure_srf_{yr}_{doy:03d}_{utc:02d}.mat'))['P_srf'] # P_srf
            maxWS = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/MaxWS/',str(yr),f'EA6km_maxWS_{yr}_{doy:03d}_{utc:02d}.mat'))['maxWS'] # maxWS
            PBLH = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/PBLH/',str(yr),f'EA6km_PBLH_{yr}_{doy:03d}_{utc:02d}.mat'))['PBLH'] # PBLH
            Visibility = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/Visibility/',str(yr),f'EA6km_Visibility_{yr}_{doy:03d}_{utc:02d}.mat'))['Visibility'] # Visibility
            
            Tsrf = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/Temp_surface/',str(yr),f'EA6km_Tsrf_{yr}_{doy:03d}_{utc:02d}.mat'))['Tsrf'] # Tsrf
            Tmax = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/Temp_max/',str(yr),f'EA6km_Tmax_{yr}_{doy:03d}_{utc:02d}.mat'))['Tmax'] # Tmax
            Tmin = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/Temp_min/',str(yr),f'EA6km_Tmin_{yr}_{doy:03d}_{utc:02d}.mat'))['Tmin'] # Tmin
            FrictionalVelocity = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/FrictionalVelocity/',str(yr),f'EA6km_FrictionalVelocity_{yr}_{doy:03d}_{utc:02d}.mat'))['FrictionalVelocity'] # 'FrictionalVelocity'
            PotentialEnergy = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/PotentialEnergy/',str(yr),f'EA6km_PotentialEnergy_{yr}_{doy:03d}_{utc:02d}.mat'))['PotentialEnergy'] # 'PotentialEnergy'
            SurfaceRoughness = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/SurfaceRoughness/',str(yr),f'EA6km_SurfaceRoughness_{yr}_{doy:03d}_{utc:02d}.mat'))['SurfaceRoughness'] # 'SurfaceRoughness'
            LatentHeatFlux = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/LatentHeatFlux/',str(yr),f'EA6km_LatentHeatFlux_{yr}_{doy:03d}_{utc:02d}.mat'))['LatentHeatFlux'] # 'LatentHeatFlux'
            SpecificHumidity = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/SpecificHumidity/',str(yr),f'EA6km_SpecificHumidity_{yr}_{doy:03d}_{utc:02d}.mat'))['SpecificHumidity'] # 'SpecificHumidity'
            U = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/Uwind/',str(yr),f'EA6km_U_{yr}_{doy:03d}_{utc:02d}.mat'))['U'] # 'U'
            V = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/Vwind/',str(yr),f'EA6km_V_{yr}_{doy:03d}_{utc:02d}.mat'))['V'] # 'V'
            stack1 = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/stackMaxWS/',str(yr),f'stack1_EA6km_maxWS_{yr}_{doy:03d}_{utc:02d}.mat'))['stack1'] # 'stack1'
            stack3 = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/stackMaxWS/',str(yr),f'stack3_EA6km_maxWS_{yr}_{doy:03d}_{utc:02d}.mat'))['stack3'] # 'stack3'
            stack5 = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/stackMaxWS/',str(yr),f'stack5_EA6km_maxWS_{yr}_{doy:03d}_{utc:02d}.mat'))['stack5'] # 'stack5'
            stack7 = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/stackMaxWS/',str(yr),f'stack7_EA6km_maxWS_{yr}_{doy:03d}_{utc:02d}.mat'))['stack7'] # 'stack7'
            AP3h = matlab.loadmat(os.path.join(path_ea_goci,'RDAPS/AP3h/',str(yr),f'EA6km_AP3h_{yr}_{doy:03d}_{utc:02d}.mat'))['AP3h']
            
            WS = np.sqrt(np.power(U, 2) + np.power(V,2))
            Wcos = np.divide(U, WS)
            Wsin = np.divide(V, WS)
            
            # Load SMOKE emission data
            EA_emis = matlab.loadmat(os.path.join(path_ea_goci,'EMIS/',str(yr),f'EA6km_EMIS_{yr}_{doy:03d}_{utc:02d}.mat'))['EA_emis'] # EA_emis
            EA_emis = EA_emis.reshape(-1,14)
            
            # Assign loaded data into matrix
            nn = lat_goci.shape[0]*lat_goci.shape[1]
            data = np.zeros((nn,nvar))
            
            # satellite data(12)
            data[:,0] = omno2d.ravel(order='F') # OMNO2d_tc
            data[:,1] = omso2e_m.ravel(order='F') # OMSO2e_tc
            data[:,2] = omdoao3e_m.ravel(order='F') # OMDOAO3e_tc
            data[:,3] = omhchog.ravel(order='F') # OMHCHOG_tc
            data[:,4] = GOCI_aod.ravel(order='F') # GOCI AOD
            data[:,5] = GOCI_ae.ravel(order='F') # GOCI AE
            data[:,6] = GOCI_fmf.ravel(order='F') # GOCI FMF
            data[:,7] = GOCI_ssa.ravel(order='F') # GOCI SSA
            data[:,8] = ndvi.ravel(order='F') # MODIS NDVI
            if yr<2018:
                data[:,9] = RSDN.ravel(order='F') # BESS Solar Radiation
            data[:,10] = precip.ravel(order='F') # Precipitation
            data[:,11] = dem.ravel(order='F') # DEM
            
            # numerical data(RDAPS)
            data[:,12] = T.ravel(order='F') # Temperature
            data[:,13] = D.ravel(order='F') # Dew_temperature
            data[:,14] = RH.ravel(order='F') # RH
            data[:,15] = P_srf.ravel(order='F') # Surface Pressure
            data[:,16] = maxWS.ravel(order='F') # Max wind speed
            data[:,17] = PBLH.ravel(order='F') # PBLH
            data[:,18] = Visibility.ravel(order='F') # Visibility
            data[:,19] = Tsrf.ravel(order='F')
            data[:,20] = Tmax.ravel(order='F')
            data[:,21] = Tmin.ravel(order='F')
            data[:,22] = FrictionalVelocity.ravel(order='F')
            data[:,23] = PotentialEnergy.ravel(order='F')
            data[:,24] = SurfaceRoughness.ravel(order='F')
            data[:,25] = LatentHeatFlux.ravel(order='F')
            data[:,26] = SpecificHumidity.ravel(order='F')
            data[:,27] = stack1.ravel(order='F')
            data[:,28] = stack3.ravel(order='F')
            data[:,29] = stack5.ravel(order='F')
            data[:,30] = stack7.ravel(order='F')
            data[:,31] = WS.ravel(order='F')
            data[:,32] = Wcos.ravel(order='F')
            data[:,33] = Wsin.ravel(order='F')
            data[:,34] = AP3h.ravel(order='F')
            
            # ancillary data
            data[:,35] = np.sin((doy-112)*2*np.pi/365.25) # DOY
            data[:,36] = popDens.ravel(order='F') # Population Density
            data[:,37] = roadDens.ravel(order='F') # Road Density
            data[:,38:52]=EA_emis
            data[:,52:62]=LC_ratio
            
            # additional variables
            data[:,62]=omno2d_trop.ravel(order='F')
            data[np.isnan(data)] = -9999
            
            matlab.check_make_dir(os.path.join(path_ea_goci, 'cases_csv', str(yr)))
            if yr>=2018: # BESS 없음
                data[:,9]= 0
                header_temp = header[:9]+header[10:]
            else:
                header_temp = header
            print ('data shape :', data.shape)
            tmp_df = pd.DataFrame(data, columns=header_temp)
            tmp_df.to_csv(os.path.join(path_ea_goci, 'cases_csv',str(yr),f'cases_EA6km_{yr}_{doy:03d}_{utc:02d}.csv'))
            del tmp_df
            
            data[data==-9999] = np.nan
            data_tbl = pd.DataFrame(data,columns=header_temp)
            print (data_tbl.to_dict('list').keys())
            header_temp = np.array(data_tbl.columns, dtype=h5py.string_dtype(encoding='utf-8'))
            matlab.savemat(os.path.join(path_ea_goci, 'cases_mat', str(yr), f'cases_EA6km_{yr}_{doy:03d}_{utc:02d}.mat'), 
                           {col: data_tbl[col].values for col in data_tbl.columns})
            with h5py.File(os.path.join(path_ea_goci, 'cases_mat', str(yr), f'cases_EA6km_{yr}_{doy:03d}_{utc:02d}.mat'), 'a') as dst:
                dst['header'] = header_temp
            tElapsed = time.time() - tStart
            print (f'{yr}_{doy:03d}_{utc:02d} ... {tElapsed} sec')            
        print (doy) 
    print (yr)
