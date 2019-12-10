### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

from scipy.io import netcdf
import numpy as np
import glob
import time
import h5py 
import pygrib
import copy

### Setting path
data_base_dir = os.path.join('/', 'media', 'sf_GEMS', 'Data')
emis_path = os.path.join(data_base_dir, 'Raw', 'EMIS')  
write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'EMIS')  

# emiss_header = ['ISOPRENE','TRP1','MEOH','ACET','CH4','NO',
#     'NO2','NH3','CCHO','HCOOH','HCHO','CCO_OH','BALD','MEK','RCO_OH',
#     'CO','ETHENE','ALK1','ALK2','ALK3','ALK4','ALK5','ARO1','ARO2',
#     'OLE1','OLE2','RCHO','NONR','CRES','GLY','IPROD','MACR','MGLY',
#     'NR','PHEN','PROD2','SO2','SULF','PM10','PEC','PM2_5','PMFINE',
#     'PNO3','POA','PSO4','PMC','ISOP'];


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
    list_date = [str(matlab.datestr(d)) for d in list_date] # '2016-01-01' format
    list_date = [x[:4]+x[5:7]+x[8:] for x in list_date] #  '20160101' format

    for i, date in enumerate(list_date):
        doy = i+1
        fname = f'egts3d_l.{yr}.{date[4:8]}.{KNU_dir}.AQFv1.ncf'
        #try:
        ncfile = netcdf.NetCDFFile(os.path.join(curr_path, f'NIER_09h_EMIS_{date}', fname), 'r')
        var = list(ncfile.variables.keys())
        emiss_all = np.full((nr, nc, len(var)-1, 24), np.nan)  # From 01UTC to 00UTC (next day)
        
        for j in range(1, len(var)):
            temp = ncfile.variables[var[j]]
            data = copy.deepcopy(temp.data)
            # matlab ncread -> (174, 128, 15, 22)
            # pyhton netcdf read -> (22, 15, 128, 174) = (TSTEP, LAY, ROW, COL) 
            data = np.transpose(data, (3, 2, 1, 0)) # now, (174, 128, 15, 22)
            #ncfile.close()
            data = np.rot90(data)
            emiss_all[:,:,j-1,2:]=np.float64(np.squeeze(data[:,:,0,:])) # vertical layer : 1
    
            if i != 1:
                try:
                    ncfile2 = netcdf.NetCDFFile(os.path.join(curr_path, f'NIER_09h_EMIS_{list_date[i-1]}', fname), 'r')
                    temp = ncfile2.variables[var[j]]
                    data2 = copy.deepcopy(temp.data)
                    ncfile2.close()                        
                    data2 = np.rot90(data2)
                    emiss_all[:,:,j-1,:2]=np.float64(np.squeeze(data2[:,:,0,1:3])) # forecast 01-02UTC
                except:
                    pass

        for k in range(24):
            utc = k+1
            emiss = emiss_all[:,:,:,k]
            if k==23: # last
                if doy==days: # last
                    fname = f'emiss_27km_{yr+1}_001_00.mat'
                    matlab.savemat(os.path.join(write_path, KNU_dir, str(yr+1), fname), {'emiss':emiss})
                else:
                    fname = f'emiss_27km_{yr}_{doy+1:03d}_00.mat'
                    matlab.savemat(os.path.join(write_path, KNU_dir, str(yr), fname), {'emiss':emiss})
            else:
                fname = f'emiss_27km_{yr}_{doy:03d}_{utc:02d}.mat'
                matlab.savemat(os.path.join(write_path, KNU_dir, str(yr), fname), {'emiss':emiss})
        print (f'{yr}_{doy:03d}')
        #except:
        #    print (f'{yr}_{doy:03d}_no_data!!!!')
        #    pass
        print (doy)
    print (yr)
    tElapsed = time.time()-tStart
    print (f'{tElapsed} sec')

## 9 km domain
nr=82; nc=67;
YEARS = [2016] # range(2017, 2019+1)
KNU_dir = 'KNU_09_01'

for yr in YEARS:
    tStart = time.time()
    if (yr%4)==0: days=366
    else: days=365

    curr_path = os.path.join(emis_path, KNU_dir, str(yr))
    list_date = list(range(matlab.datenum(f'{yr}0101'), matlab.datenum(f'{yr}1231')+1))
    list_date = [str(matlab.datestr(d)) for d in list_date] # '2016-01-01' format
    list_date = [x[:4]+x[5:7]+x[8:] for x in list_date] #  '20160101' format

    
for i, date in enumerate(list_date):
        doy = i+1
        fname = f'egts3d_l.{yr}.{date[4:8]}.{KNU_dir}.AQFv1.ncf'
        #try:
        ncfile = netcdf.NetCDFFile(os.path.join(curr_path, f'NIER_09h_EMIS_{date}', fname), 'r')
        var = list(ncfile.variables.keys())
        emiss_all = np.full((nr, nc, len(var)-1, 24), np.nan)  # From 01UTC to 00UTC (next day)
        
        for j in range(1, len(var)):
            temp = ncfile.variables[var[j]]
            data = copy.deepcopy(temp.data)
            # matlab ncread -> (174, 128, 15, 22)
            # pyhton netcdf read -> (22, 15, 128, 174) = (TSTEP, LAY, ROW, COL) 
            data = np.transpose(data, (3, 2, 1, 0)) # now, (174, 128, 15, 22)
            #ncfile.close()
            data = np.rot90(data)
            emiss_all[:,:,j-1,2:]=np.float64(np.squeeze(data[:,:,0,:])) # vertical layer : 1
    
            if i != 1:
                try:
                    ncfile2 = netcdf.NetCDFFile(os.path.join(curr_path, f'NIER_09h_EMIS_{list_date[i-1]}', fname), 'r')
                    temp = ncfile2.variables[var[j]]
                    data2 = copy.deepcopy(temp.data)
                    ncfile2.close()                        
                    data2 = np.rot90(data2)
                    emiss_all[:,:,j-1,:2]=np.float64(np.squeeze(data2[:,:,0,1:3])) # forecast 01-02UTC
                except:
                    pass

        for k in range(24):
            utc = k+1
            emiss = emiss_all[:,:,:,k]
            if k==23: # last
                if doy==days: # last
                    fname = f'emiss_9km_{yr+1}_001_00.mat'
                    matlab.savemat(os.path.join(write_path, KNU_dir, str(yr+1), fname), {'emiss':emiss})
                else:
                    fname = f'emiss_9km_{yr}_{doy+1:03d}_00.mat'
                    matlab.savemat(os.path.join(write_path, KNU_dir, str(yr), fname), {'emiss':emiss})
            else:
                fname = f'emiss_9km_{yr}_{doy:03d}_{utc:02d}.mat'
                matlab.savemat(os.path.join(write_path, KNU_dir, str(yr), fname), {'emiss':emiss})
        print (f'{yr}_{doy:03d}')
        #except:
        #    print (f'{yr}_{doy:03d}_no_data!!!!')
        #    pass
        print (doy)
    print (yr)
    tElapsed = time.time()-tStart
    print (f'{tElapsed} sec')
