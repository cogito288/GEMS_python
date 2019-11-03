### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import scipy.io as sio
from scipy.io import netcdf
import numpy as np
import glob
import time
import h5py 
import pygrib

### Setting path
data_base_dir = os.path.join('/', 'media', 'sf_GEMS', 'Data')
emis_path = os.path.join(data_base_dir, 'Raw', 'EMIS')  
write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'EMIS')  
# emis_path = '/lustre/gpu_storage/Data/Aerosol/00_raw_data/EMIS/';
#path_data = '/share/irisnas5/Data/';
#path = [path_data,'pre/EMIS/'];


# emiss_header = ['ISOPRENE','TRP1','MEOH','ACET','CH4','NO',
#     'NO2','NH3','CCHO','HCOOH','HCHO','CCO_OH','BALD','MEK','RCO_OH',
#     'CO','ETHENE','ALK1','ALK2','ALK3','ALK4','ALK5','ARO1','ARO2',
#     'OLE1','OLE2','RCHO','NONR','CRES','GLY','IPROD','MACR','MGLY',
#     'NR','PHEN','PROD2','SO2','SULF','PM10','PEC','PM2_5','PMFINE',
#     'PNO3','POA','PSO4','PMC','ISOP'];

## 9 km domain
nr=82; nc=67;
YEARS = [2016] # range(2017, 2019+1)
KNU_dir = 'KNU_27_01'

for yr in YEARS:
    if (yr%4)==0: days=366
    else: days=365

    curr_path = os.path.join(emis_path, KNU_dir, str(yr))
    list_date = list(range(matlab.datenum(f'{yr}0101'), matlab.datenum(f'{yr}1231')+1))
    list_date = [str(d) for d in list_date]    
    list_char = [f'NIER_09h_EMIS_{d}' for d in list_date]
    list_char = [os.path.basename(f) for f in list_char]

    for doy in range(1, days+1):
        fname = f'egts3d_l.{yr}.{list_date[doy][4:8]}.{KNU_dir}.AQFv1.ncf'
        try:
            ncfile = netcdf.NetCDFFile(os.path.join(curr_path, list_char[doy-1], fname), 'r')
            var = list(ncfile.variables.keys())
            emiss_all = np.full((nr, nc, len(var)-1, 24), np.nan)  # From 01UTC to 00UTC (next day)
            
            for j in range(2, len(var)+1):
                temp = ncfile.variables[var[j]]
                data = temp[:]
                data = np.rot90(data)
                ncfile.close()
                emiss_all[:,:,j-2,2:]=np.float64(np.squeeze(data[:,:,0,:])) # vertical layer : 1
                    
                
                if doy != 1:
                    try:
                        ncfile = netcdf.NetCDFFile(os.path.join(curr_path, list_char[doy-2], fname), 'r')
                        temp = ncfile.variables[var[j]]
                        data2 = temp[:]
                        data2 = np.rot90(data2)
                        ncfile.close()
                        emiss_all[:,:,j-2,:2]=np.float64(np.squeeze(data2[:,:,0,1:3])) # forecast 01-02UTC
                    except:
                        pass
                    
            for utc in range(1, 24+1):
                emiss = emiss_all[:,:,:,utc]
                if utc==24:
                    if doy==days:
                        fname = f'emiss_9km_{yr+1}_001_00.mat'
                        matlab.savemat(os.path.join(write_path, KNU_dir, str(yr+1)), fname, {'emiss':emiss})
                    else:
                        fname = f'emiss_9km_{yr}_{doy:03d}_{utc:02d}.mat'
                        matlab.savemat(os.path.join(write_path, KNU_dir, str(yr)), fname, {'emiss':emiss})
            print (f'{yr}_{doy:03d}')
        except:
            print (f'{yr}_{doy:03d}_no_data!!!!')
            pass
        print (doy)
    print (yr)


## 27 km domain
nr=128; nc=174;
YEARS = [2016] # range(2017, 2019+1)
KNU_dir = 'KNU_27_01'
for yr in YEARS:
    tStart = time.time()
    if (yr%4)==0: days=366
    else: days=365

    curr_path = os.path.join(emis_path, KNU_dir, str(yr))
    list_date = list(range(matlab.datenum(f'{yr}0101'), matlab.datenum(f'{yr}1231')+1))
    list_date = [str(d) for d in list_date]    
    list_char = [f'NIER_09h_EMIS_{d}' for d in list_date]
    list_char = [os.path.basename(f) for f in list_char]

    for doy in range(1, days+1):
        fname = f'egts3d_l.{yr}.{list_date[doy][4:8]}.{KNU_dir}.AQFv1.ncf'
        try:
            ncfile = netcdf.NetCDFFile(os.path.join(curr_path, list_char[doy-1], fname), 'r')
            var = list(ncfile.variables.keys())
            emiss_all = np.full((nr, nc, len(var)-1, 24), np.nan)  # From 01UTC to 00UTC (next day)
            
            for j in range(2, len(var)+1):
                temp = ncfile.variables[var[j]]
                data = temp[:]
                data = np.rot90(data)
                ncfile.close()
                emiss_all[:,:,j-2,2:]=np.float64(np.squeeze(data[:,:,0,:])) # vertical layer : 1
        
                if doy != 1:
                    try:
                        ncfile = netcdf.NetCDFFile(os.path.join(curr_path, list_char[doy-2], fname), 'r')
                        temp = ncfile.variables[var[j]]
                        data2 = temp[:]
                        data2 = np.rot90(data2)
                        ncfile.close()
                        emiss_all[:,:,j-2,:2]=np.float64(np.squeeze(data2[:,:,0,1:3])) # forecast 01-02UTC
                    except:
                        pass

            for utc in range(1, 24+1):
                emiss = emiss_all[:,:,:,utc]
                if utc==24:
                    if doy==days:
                        fname = f'emiss_27km_{yr+1}_001_00.mat'
                        matlab.savemat(os.path.join(write_path, KNU_dir, str(yr+1)), fname, {'emiss':emiss})
                    else:
                        fname = f'emiss_27km_{yr}_{doy+1:03d}_00.mat'
                        matlab.savemat(os.path.join(write_path, KNU_dir, str(yr)), fname, {'emiss':emiss})
                else:
                    fname = f'emiss_27km_{yr}_{doy:03d}_{utc:02d}.mat'
                    matlab.savemat(os.path.join(write_path, KNU_dir, str(yr)), fname, {'emiss':emiss})
            print (f'{yr}_{doy:03d}')
        except:
            print (f'{yr}_{doy:03d}_no_data!!!!')
            pass
        print (doy)
    print (yr)
    tElapsed = time.time()-tStart
    print (f'{tElapsed} sec')


    ## yyyy_001_01, yyyy_001_02 누락된거 만들기
    # yr=2019;
    # fname = [emis_path,'KNU_27_01/',str(yr-1),
    #     '/NIER_09h_EMIS_',str(yr-1),'1231/egts3d_l.',str(yr),'.0101.KNU_27_01.AQFv1.ncf'];
    # data_info = ncinfo(fname);
    # var = {data_info.Variables.Name}';
    # emiss_all = nan(nr,nc,length(var)-1,2);
    # for j=2:length(var)
    #     eval(sprintf(['data=rot90(ncread(fname, \''',var{j},'\''));']));
    #     emiss_all(:,:,j-1,:)=double(squeeze(data(:,:,1,2:3))); # vertical layer : 1
    # end
    # 
    # for utc = 1:2
    #     emiss = emiss_all(:,:,:,utc);
    #     save([path,'KNU_27_01/',str(yr),'/emiss_27km_',str(yr),
    #         '_001_',str(utc,'#02i'),'.mat'],'emiss')
    # end
