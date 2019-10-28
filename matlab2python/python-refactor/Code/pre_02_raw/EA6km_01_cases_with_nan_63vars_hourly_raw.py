import os
import sys
project_path = '/home/cogito/Desktop/GEMS_python/matlab2python/python-refactor'
sys.path.insert(0, project_path)

from Code.utils import matlab

import numpy as np
from matplotlib.pyplot import imread
from scipy.interploate import griddata
import time
import pandas as pd

#% path_data = '/share/irisnas5/Data/';
#% path = '/share/irisnas5/Data/EA_GOCI6km/';

#% path_data = '//10.72.26.56/irisnas5/Data/';
#% path = '//10.72.26.56/irisnas5/Data/EA_GOCI6km/';

path_data = os.path.join('/', 'share', 'irisnas5', 'Data')
path = os.path.join('/', 'share', 'irisnas5', 'Data', 'EA_GOCI6km')
path_goci = os.path.join('/', 'share', 'irisnas6','Data','GOCI_AOD','01mat','GOCI_filtered/')
#addpath(genpath([path_data,'/matlab_func/']))

#%% Load grid
matlab.loadmat(os.path.join(path_data,'grid','grid_goci.mat'))

#%% header
hd_sat = ['OMNO2d_tc','OMSO2e_tc','OMDOAO3e_tc','OMHCHOG_tc', 'AOD','AE','FMF','SSA','NDVI','RSDN','Precip','DEM'] ## satellite data(12)
hd_rdaps = ['Temp','Dew','RH','P_srf','MaxWS','PBLH','Visibility','Tsrf','Tmax','Tmin',
    'FrictionalVelocity','PotentialEnergy','SurfaceRoughness','LatentHeatFlux','SpecificHumidity',
    'stack1_maxWS','stack3_maxWS','stack5_maxWS','stack7_maxWS','WS','Wcos','Wsin','AP3h'] # numerical data(RDAPS)(23)
hd_etc = ['DOY','PopDens','RoadDens'] # etc data(3)
hd_emis = ['ISOPRENE','TRP1','CH4','NO','NO2','NH3','HCOOH','HCHO','CO','SO2',
    'PMFINE','PNO3','POA','PSO4'] # SMOKE data (14)
hd_lc = ['LCbarren','LCcrop','LCforest','LCgrass','LCsavannas','LCshrub',
    'LCurban','LCwater','LCwetland','LCveg'] # LC ratio (10)

header = hd_sat+hd_rdaps+hd_etc+hd_emis+hd_lc+['OMNO2d_trop_tc']
# header16 = [header,{'geosAOD'}]
nvar = 63

## Read stationary data
# ==== Stationary data ====
matlab.loadmat(os.path.join(path,'stationary','EA6km_SRTM_DEM_masked.mat')) # dem
matlab.loadmat(os.path.join(path,'stationary','EA6km_roadDens.mat')) # roadDens

# Read MODIS landcover ratio by class
for k in range(9):
    matlab.loadmat(os.path.join(path,'MODIS_LC_ratio',f'EA6km_{hd_lc[k][3:]}_ratio_r6_2017.mat'))
LC_veg = LC_forest+LC_grass+LC_savannas+LC_shrub
LC_ratio = [LC_barren.flatten(),LC_crop.flatten(),LC_forest.flatten(),LC_grass.flatten(),LC_savannas.flatten(),LC_shrub.flatten(),LC_urban.flatten(),LC_water.flatten(),LC_wetland.flatten(),LC_veg.flatten()]
del LC_barren, LC_crop, LC_forest, LC_grass, LC_savannas, LC_shrub, LC_urban, LC_water, LC_wetland, LC_veg

YEARS = [2019]
for yr in YEARS:
	if yr%4==0:
		days = 366
	else:
		days = 365
	if yr==2019:
		days = 114
    # ==== Yearly data ====
    # Read population density
    popDens = matlab.loadmat(os.path.join(path,'PopDens','EA6km_popDens_{yr}.mat'))
    
    # nanidx = zeros(218999,days)
	for doy in range(1, days+1):
		yr_doy = f'{yr}_{doy:03d}'
        # ==== Daily data ====
        # Read MODIS(AQUA) 16-days NDVI (ndvi)
        if doy<9:
            matlab.loadmat(os.path.join(path, 'MODIS_NDVI',str(yr-1),f'EA_MODIS_NDVI_{yr-1}_361.mat'))
        else:
			num = np.ceil((doy-8)/16)*16-7
            matlab.loadmat(os.path.join(path, 'MODIS_NDVI',str(yr),f'/EA_MODIS_NDVI_{yr}_{num:03d}.mat'))
        if yr<2019:
            ndvi = np.float64(ndvi) 
			ndvi[ndvi==-32768] = np.nan
			ndvi = np.divide(ndivi, 10000)
			ndvi[ndvi<-1] = np.nan
			ndvi[ndvi>1] = np.nan
        # Load OMI temporal convolutioned data
        omno2d=matlab.loadmat(os.path.join(path,'OMI_tempConv','OMNO2d',str(yr),f'/EA6km_OMNO2d_{yr_doy}.mat'))
        ################     omno2d=omno2d * 3.7216e-17 # molec/cm2 to DU
        omno2d[omno2d<0]=np.nan
        omno2d_trop=matlab.loadmat(os.path.join(path,'OMI_tempConv','OMNO2d_trop_CS',str(yr),f'EA6km_OMNO2d_trop_CS_{yr_doy}.mat'))
        omno2d_trop[omno2d_trop<0]=np.nan
        omso2e_m=matlab.loadmat(os.path.join(path,'OMI_tempConv/OMSO2e_m/',str(yr),f'EA6km_OMSO2e_m_{yr_doy}.mat'))
        omso2e_m[omso2e_m<0]=np.nan
        omdoao3e_m=matlab.loadmat(os.path.join(path,'OMI_tempConv/OMDOAO3e_m/',str(yr),f'EA6km_OMDOAO3e_m_{yr_doy}.mat'))
        omdoao3e_m[omdoao3e_m<0]=np.nan
        omhchog=matlab.loadmat(os.path.join(path,'OMI_tempConv/OMHCHOG/',str(yr),f'EA6km_OMHCHOG_{yr_doy}.mat'))
        omhchog[omhchog<0]=np.nan
        
        # Read BESS soalr radiation at 13:30 (RSDN)
        if yr==2017:
            matlab.loadmat(os.path.join(path,'BESS/',str(yr),f'EA6km_BESS_RSDN_{yr_doy}'))
       	for utc in range(7+1): 
            tStart = time.time()
            # ===== Hourly data =====
            yr_doy_utc = f'{yr_doy}_{utc:02i}' 
            
            # Read GOCI AOD products (GOCI_aod, GOCI_ae, GOCI_fmf, GOCI_ssa)
            matlab.loadmat(os.path.join(path_goci,'AOD/',str(yr),'/GOCI_AOD_{yr_doy_utc'))
            matlab.loadmat(os.path.join(path_goci,'AE/',str(yr),'/GOCI_AE_{yr_doy_utc'))
            matlab.loadmat(os.path.join(path_goci,'FMF/',str(yr),'/GOCI_FMF_{yr_doy_utc'))
            matlab.loadmat(os.path.join(path_goci,'SSA/',str(yr),'/GOCI_SSA_{yr_doy_utc'))
            
            # Read GPM accumulated precipitation (precip)
            try:
                matlab.loadmat(os.path.join(path,'GPM_AP/',str(yr),f'EA6km_gpm_AP_{yr_doy}_UTC{utc:02d}.mat'))
            except:
                matlab.loadmat(os.path.join(path,'GPM_AP/',str(yr),f'EA6km_gpm_AP_{yr_doy}_UTC{utc:02d}_early.mat'))
            
            # Read UM (RDAPS) data
            T = matlab.loadmat(os.path.join(path,'RDAPS/Temp/',str(yr),f'EA6km_T_{yr_doy_utc}.mat')) # T
            D = matlab.loadmat(os.path.join(path,'RDAPS/Dew/',str(yr),f'EA6km_D_{yr_doy_utc}.mat')) # D
            RH = matlab.loadmat(os.path.join(path,'RDAPS/RH/',str(yr),f'EA6km_RH_{yr_doy_utc}.mat')) # RH
            R_srf = matlab.loadmat(os.path.join(path,'RDAPS/Pressure/',str(yr),f'EA6km_Pressure_srf_{yr_doy_utc}.mat')) # P_srf
            maxWS = matlab.loadmat(os.path.join(path,'RDAPS/MaxWS/',str(yr),f'EA6km_maxWS_{yr_doy_utc}.mat')) # maxWS
            PBLH = matlab.loadmat(os.path.join(path,'RDAPS/PBLH/',str(yr),f'EA6km_PBLH_{yr_doy_utc}.mat')) # PBLH
            Visibility = matlab.loadmat(os.path.join(path,'RDAPS/Visibility/',str(yr),f'EA6km_Visibility_{yr_doy_utc}.mat')) # Visibility
            
            Tsrf = matlab.loadmat(os.path.join(path,'RDAPS/Temp_surface/',str(yr),f'EA6km_Tsrf_{yr_doy_utc}.mat')) # Tsrf
            Tmax = matlab.loadmat(os.path.join(path,'RDAPS/Temp_max/',str(yr),f'EA6km_Tmax_{yr_doy_utc}.mat')) # Tmax
            Tmin = matlab.loadmat(os.path.join(path,'RDAPS/Temp_min/',str(yr),f'EA6km_Tmin_{yr_doy_utc}.mat')) # Tmin
            FrictionalVelocity = matlab.loadmat(os.path.join(path,'RDAPS/FrictionalVelocity/',str(yr),f'EA6km_FrictionalVelocity_{yr_doy_utc}.mat')) # 'FrictionalVelocity'
            PotentialEnergy = matlab.loadmat(os.path.join(path,'RDAPS/PotentialEnergy/',str(yr),f'EA6km_PotentialEnergy_{yr_doy_utc}.mat')) # 'PotentialEnergy'
            SurfaceRoughness = matlab.loadmat(os.path.join(path,'RDAPS/SurfaceRoughness/',str(yr),f'EA6km_SurfaceRoughness_{yr_doy_utc}.mat')) # 'SurfaceRoughness'
            LetenHeatFlux = matlab.loadmat(os.path.join(path,'RDAPS/LatentHeatFlux/',str(yr),f'EA6km_LatentHeatFlux_{yr_doy_utc}.mat')) # 'LatentHeatFlux'
            SpecificHumidity = matlab.loadmat(os.path.join(path,'RDAPS/SpecificHumidity/',str(yr),f'EA6km_SpecificHumidity_{yr_doy_utc}.mat')) # 'SpecificHumidity'
            U = matlab.loadmat(os.path.join(path,'RDAPS/Uwind/',str(yr),f'EA6km_U_{yr_doy_utc}.mat')) # 'U'
            V = matlab.loadmat(os.path.join(path,'RDAPS/Vwind/',str(yr),f'EA6km_V_{yr_doy_utc}.mat')) # 'V'
            stack1 = matlab.loadmat(os.path.join(path,'RDAPS/stackMaxWS/',str(yr),'/stack1_EA6km_maxWS_{yr_doy_utc}.mat')) # 'stack1'
            stack3 = matlab.loadmat(os.path.join(path,'RDAPS/stackMaxWS/',str(yr),'/stack3_EA6km_maxWS_{yr_doy_utc}.mat')) # 'stack3'
            stack5 = matlab.loadmat(os.path.join(path,'RDAPS/stackMaxWS/',str(yr),'/stack5_EA6km_maxWS_{yr_doy_utc}.mat')) # 'stack5'
            stack7 = matlab.loadmat(os.path.join(path,'RDAPS/stackMaxWS/',str(yr),'/stack7_EA6km_maxWS_{yr_doy_utc}.mat')) # 'stack7'
            AP3h = matlab.loadmat(os.path.join(path,'RDAPS/AP3h/',str(yr),f'EA6km_AP3h_{yr_doy_utc}.mat'))
            
            WS = np.sqrt(np.power(U, 2) + np.power(V,2))
            Wcos = np.divide(U, WS)
            Wsin = np.divide(V, WS)
            
            # Load SMOKE emission data
            EA_emis = matlab.loadmat(os.path.join(path,'EMIS/',str(yr),f'/EA6km_EMIS_{yr_doy_utc}.mat')) # EA_emis
            EA_emis = EA_emis.reshape(-1,14)
            
            # Assign loaded data into matrix
            nn = lat_goci.shape[0]*lat_goci.shape[1]
            data = np.zeros((nn,nvar))
            
            # satellite data(12)
            data[:,0] = omno2d.flatten() # OMNO2d_tc
            data[:,1] = omso2e_m.flatten() # OMSO2e_tc
            data[:,2] = omdoao3e_m.flatten() # OMDOAO3e_tc
            data[:,3] = omhchog.flatten() # OMHCHOG_tc
            data[:,4] = GOCI_aod.flatten() # GOCI AOD
            data[:,5] = GOCI_ae.flatten() # GOCI AE
            data[:,6] = GOCI_fmf.flatten() # GOCI FMF
            data[:,7] = GOCI_ssa.flatten() # GOCI SSA
            data[:,8] = ndvi.flatten() # MODIS NDVI
            if yr<2018
                data[:,9] = RSDN.flatten() # BESS Solar Radiation
            end
            data[:,10] = precip.flatten() # Precipitation
            data[:,11] = dem.flatten() # DEM
            
            # numerical data(RDAPS)
            data[:,12] = T.flatten() # Temperature
            data[:,13] = D.flatten() # Dew_temperature
            data[:,14] = RH.flatten() # RH
            data[:,15] = P_srf.flatten() # Surface Pressure
            data[:,16] = maxWS.flatten() # Max wind speed
            data[:,17] = PBLH.flatten() # PBLH
            data[:,18] = Visibility.flatten() # Visibility
            data[:,19] = Tsrf.flatten()
            data[:,20] = Tmax.flatten()
            data[:,21] = Tmin.flatten()
            data[:,22] = FrictionalVelocity.flatten()
            data[:,23] = PotentialEnergy.flatten()
            data[:,24] = SurfaceRoughness.flatten()
            data[:,25] = LatentHeatFlux.flatten()
            data[:,26] = SpecificHumidity.flatten()
            data[:,27] = stack1.flatten()
            data[:,28] = stack3.flatten()
            data[:,29] = stack5.flatten()
            data[:,30] = stack7.flatten()
            data[:,31] = WS.flatten()
            data[:,32] = Wcos.flatten()
            data[:,33] = Wsin.flatten()
            data[:,34] = AP3h.flatten()
            
            # ancillary data
            data[:,35] = np.sin((doy-112)*2*np.pi/365.25) # DOY
            data[:,36] = popDens.flatten() # Population Density
            data[:,37] = roadDens.flatten() # Road Density
            data[:,38:52)=EA_emis
            data[:,52:62)=LC_ratio
            
            # additional variables
            data[:,62)=omno2d_trop.flatten()
            data[np.isnan(data)] = -9999
            if yr>=2018: # BESS 없음
                data[:,9]=[]
                header_temp = header[:9]+header[10:]
                
                tmp_df = pd.DataFrame(data, columns=header_temp)
                tmp_df.to_csv(os.path.join(path, 'cases_csv',str(yr),f'cases_EA6km_{yr_doy_utc}.csv', )
                del tmp_df

                data[data==-9999] = np.nan
                data_tbl = pd.DataFrame(data,columns=header_temp)
                matlab.savemat(os.path.join(path, 'cases_mat', str(yr)), f'cases_EA6km_{yr_doy_utc}.mat', data_tbl.to_dict('list'))
            else:
                tmp_df = pd.DataFrame(data, columns=header)
                tmp_df.to_csv(os.path.join(path, 'cases_csv',str(yr),f'cases_EA6km_{yr_doy_utc}.csv', )
                del tmp_df

                data[data==-9999] = np.nan
                data_tbl = pd.DataFrame(data,columns=header)
                matlab.savemat(os.path.join(path, 'cases_mat', str(yr)), f'cases_EA6km_{yr_doy_utc}.mat', data_tbl.to_dict('list'))
            #     nanidx_temp = sum(isnan(data),2)>0
            #     nanidx(:,doy)=nanidx_temp
            tElapsed = time.time() - tStart
            print (f'{yr_doy_utc} ... {tElapsed} sec')
        print (doy) 
    # save([path,'cases/EA_GOCI_nanidx_',str(yr)],'nanidx')
    print (yr)
