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
omi_path = os.path.join(data_base_dir, 'Raw', 'OMI') 

### Setting period
YEARS = [2016] #, 2018, 2019


def create_L3(year, read_path, flist, write_path, fname, data_type):
    print (f"Creating {fname}")
    doy_000 = matlab.datenum(f'{year}0000')
    if data_type == 'OMDOAO3e':
        list_doy = [matlab.datenum(f'{x[21:25]}{x[26:30]}')-doy_000 for x in flist]
    else:
        list_doy = [matlab.datenum(f'{x[19:23]}{x[24:28]}')-doy_000 for x in flist]
    size = (1036800, days)
    
    # Create data_yr
    with h5py.File(os.path.join(write_path, fname), 'w') as f:
        data_yr = f.create_dataset('data_yr', shape=size, 
                                   dtype=np.float64, fillvalue=-9999, chunks=True)
        for i, read_fname in enumerate(flist[:2]):
            print (f"Reading {read_fname}")
            if data_type == 'OMNO2d':
                data = matlab.h5read(os.path.join(read_path, read_fname), 
                                 '/HDFEOS/GRIDS/ColumnAmountNO2/Data Fields/ColumnAmountNO2TropCloudScreened')
                data = np.float64(data); 
                data[data<=-1.2676506e+30] = np.nan # Assign NaN value to pixel that is out of valid range
                data = data * 3.7216e-17   
            
            elif data_type in ['OMSO2e', 'OMDOAO3e']:
                if data_type == 'OMSO2e':
                    data = matlab.h5read(os.path.join(read_path, read_fname), 
                                          '/HDFEOS/GRIDS/OMI Total Column Amount SO2/Data Fields/ColumnAmountSO2_PBL')
                    rcf = matlab.h5read(os.path.join(read_path, read_fname), 
                                         '/HDFEOS/GRIDS/OMI Total Column Amount SO2/Data Fields/RadiativeCloudFraction')
                    sza = matlab.h5read(os.path.join(read_path, read_fname), 
                                         '/HDFEOS/GRIDS/OMI Total Column Amount SO2/Data Fields/SolarZenithAngle')
                elif data_type == 'OMDOAO3e':
                    data = matlab.h5read(os.path.join(read_path, read_fname), 
                                          '/HDFEOS/GRIDS/ColumnAmountO3/Data Fields/ColumnAmountO3')
                    rcf = matlab.h5read(os.path.join(read_path, read_fname), 
                                        '/HDFEOS/GRIDS/ColumnAmountO3/Data Fields/CloudFraction')
                    sza = matlab.h5read(os.path.join(read_path, read_fname), 
                                         '/HDFEOS/GRIDS/ColumnAmountO3/Data Fields/SolarZenithAngle')
                    
                data = np.float64(data); data[data<=-1.2676506e+30] = np.nan # Assign NaN value to pixel that is out of valid range
                rcf = np.float64(rcf); rcf[rcf<=-1.2676506e+30] = np.nan
                sza = np.float64(sza); sza[sza<=-1.2676506e+30] = np.nan

                # Filtering SO2_VCD with the condition of radiative cloud fraction and
                # solar zenith angle    
                data[rcf>=0.3]=np.nan
                data[sza>=78]=np.nan
            
            data[np.isnan(data)] = -9999 # trick. data_yr(isnan(data_yr))=-9999;
            data_yr[:, list_doy[i]] = data.flatten() # Put daily data as column vector
            # header = [f'd{x:03d}' for x in range(1, days+1)] # Not used after
    print (f"Created {fname}")

### OMNO2d
print ('OMNO2d')
for yr in YEARS:
    tStart = time.time()
    curr_path = os.path.join(omi_path, 'L3', 'OMNO2d', str(yr))
    list_char = glob.glob(os.path.join(curr_path, '*.he5'))
    list_char = [os.path.basename(f) for f in list_char]
    
    if yr%4==0: days = 366
    else: days = 365
        
    write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'OMI_tempConv')
    fname = f'OMNO2d_{yr}_DU.mat'
    matlab.check_make_dir(write_path) # For debugging
    
    create_L3(year=yr, read_path=curr_path, flist=list_char,
                       write_path=write_path, fname=fname, data_type='OMNO2d')
    print (yr)
    tElapsed = time.time() - tStart
    print (f'{tElapsed} second')
    
### OMSO2e
print ('OMSO2e')
for yr in YEARS:
    tStart = time.time()
    curr_path = os.path.join(omi_path, 'L3', 'OMSO2e', str(yr))
    list_char = glob.glob(os.path.join(curr_path, '*.he5'))
    list_char = [os.path.basename(f) for f in list_char]
    
    if yr%4==0: days = 366
    else: days = 365
        
    write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'OMI_L3_tempConv')
    fname = f'OMSO2d_{yr}_DU.mat'
    matlab.check_make_dir(write_path) # For debugging
    
    create_L3(year=yr, read_path=curr_path, flist=list_char,
                       write_path=write_path, fname=fname, data_type='OMSO2e')
    print (yr)
    tElapsed = time.time() - tStart
    print (f'{tElapsed} second')
    
### OMDOAO3e
print ('OMDOAO3e')
for yr in YEARS:
    tStart = time.time()
    curr_path = os.path.join(omi_path, 'L3', 'OMDOAO3e', str(yr))
    list_char = glob.glob(os.path.join(curr_path, '*.he5'))
    list_char = [os.path.basename(f) for f in list_char]

    if yr%4==0: days = 366
    else: days = 365

    write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'OMI_L3_tempConv')
    fname = f'OMDOAO3e_m_{yr}.mat'
    matlab.check_make_dir(write_path) # For debugging
    
    create_L3(year=yr, read_path=curr_path, flist=list_char,
                       write_path=write_path, fname=fname, data_type='OMDOAO3e')
    print (yr)
    tElapsed = time.time() - tStart
    print (f'{tElapsed} second')
    
### OMHCHOG
print ('OMHCHOG')
for yr in YEARS:
    tStart = time.time()
    curr_path = os.path.join(omi_path, 'L2', 'OMHCHOG', str(yr))
    list_char = glob.glob(os.path.join(curr_path, '*.he5'))
    list_char = [os.path.basename(f) for f in list_char]

    if yr%4==0: days = 366
    else: days = 365

    write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'OMI_L3_tempConv')
    fname = f'OMHCHOG_{yr}.mat'
    matlab.check_make_dir(write_path) # For debugging
    
    doy_000 = matlab.datenum(f'{yr}0000')
    list_doy = [matlab.datenum(f'{x[21:25]}{x[26:30]}')-doy_000 for x in list_char]
    
    print (f"Creating {fname}")
    size = (1036800, days)
    with h5py.File(os.path.join(write_path, fname), 'w') as f:
        data_yr = f.create_dataset('data_yr', shape=size, 
                                   dtype=np.float64, fillvalue=-9999, chunks=True)
        for i, read_fname in enumerate(list_char[:2]):
            print (f"Reading {fname}")
            data = matlab.h5read(os.path.join(curr_path, read_fname),
                                  '/HDFEOS/GRIDS/OMI Total Column Amount HCHO/Data Fields/ColumnAmountDestriped')
            QA = matlab.h5read(os.path.join(curr_path, read_fname),
                               '/HDFEOS/GRIDS/OMI Total Column Amount HCHO/Data Fields/MainDataQualityFlag')
            
            sza = matlab.h5read(os.path.join(curr_path, read_fname),
                                '/HDFEOS/GRIDS/OMI Total Column Amount HCHO/Data Fields/SolarZenithAngle')
            
            # Assign NaN value to pixel that is out of valid range
            data = np.float64(matlab.permute(data,(1,0,2)))
            data[data<=-1.0e+30] = np.nan
            VCD = data * 3.7216e-17
            
            QA = np.float64(matlab.permute(QA, (1,0,2)))
            QA[QA<=-30000] = np.nan
            
            sza = np.float64(matlab.permute(sza,(1,0,2)))
            sza[sza<=-1.0e+30] = np.nan
            
            VCD_filtered = np.zeros(VCD.shape)
            for k in range(15):
                VCD_temp = VCD[:,:,k]
                QA_temp = QA[:,:,k]
                sza_temp = sza[:,:,k]

                VCD_temp[QA_temp!=0] = np.nan #  Good columns (0) / Suspect columns (1) / Bad columns (2) / missing (<0)
                VCD_temp[sza_temp>88] = np.nan
                VCD_filtered[:,:,k] = VCD_temp
            VCD_avg = np.nanmean(VCD_filtered, axis=2)
            VCD_avg[np.isnan(VCD_avg)] = -9999 # data_yr(isnan(data_yr))=-9999;
            data_yr[:, list_doy[i]] = VCD_avg.flatten() # Put daily data as column vector
            
            # header = [f'd{x:03d}' for x in range(1, days+1)] # Not used after
            
            if list_doy[i]%50==0:
                tmp_fname = f'OMHCHOG_{yr}_{list_doy[i]:03d}.mat'
                data_sub = data_yr[:, list_doy[i]-48:list_doy[i]]
                matlab.savemat(write_path, tmp_fname, {'data_sub':data_sub})
                print (f"Created {tmp_fname}")
            elif i==matlab.length(list_char):
                tmp_fname = f'OMHCHOG_{yr}_end.mat'
                data_sub = data_yr[:, 350:]
                matlab.savemat(write_path, tmp_fname, {'data_sub':data_sub})
    print (f"Created {fname}")
    
    i = len(list_char)-1
    # Gathering part files
    data_yr = []
    for m in range(50, 350+1, 50):
        tmp_fname = f'OMHCHOG_{yr}_{list_doy[i]:03d}.mat'
        mat = matlab.loadmat(os.path.join(write_path, tmp_fname))
        data_sub = mat['data_sub']
        data_yr = np.concatenate((data_yr, data_sub), axis=1) # data_yr=[data_yr,data_sub];
        
    tmp_fname = f'OMHCHOG_{yr}_end.mat'
    mat = matlab.loadmat(os.path.join(write_path, tmp_fname))
    data_sub = mat['data_sub']
    data_yr = np.concatenate((data_yr, data_sub), axis=1)
    np.where(np.isnan(data_yr), -9999, data_yr) # data_yr(isnan(data_yr))=-9999;
    # header = [f'd{x:03d}' for x in range(1, days+1)] # Not used after   
    
    tmp_fname = f'OMHCHOG_{yr}_DU.mat'
    matlab.savemat(write_path, tmp_fname, {'data_yr':data_yr})
    
    
    print (yr)
    tElapsed = time.time() - tStart
    print (f'{tElapsed} second')