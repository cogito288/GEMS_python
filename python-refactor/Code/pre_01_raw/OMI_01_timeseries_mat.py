### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import glob
import time

### Setting path
#data_base_dir = os.path.join(project_path, 'Data')
#path_read = os.path.join(data_base_dir, 'Raw', 'OMI') 
#path_write = os.path.join(data_base_dir, 'Preprocessed_raw', 'OMI')
data_base_dir = os.path.join('/', 'share', 'irisnas5', 'GEMS', 'GEMS_python')
path_read = os.path.join('/','share','irisnas6','Data','OMI','00raw')
path_write = os.path.join(data_base_dir, 'Preprocessed_raw', 'OMI_tempConv')

### Setting period
YEARS = [2016]

### OMNO2d
print ('OMNO2d')
for yr in YEARS:
    tStart = time.time()
    doy_000 = matlab.datenum(f'{yr}0000')
    file_list = glob.glob(os.path.join(path_read, 'L3_grid', 'OMNO2d', str(yr), '*.he5'))
    file_list.sort()
    
    if yr%4==0: days = 366
    else: days = 365
        
    data_yr = np.ones((1036800, days))*np.nan
    for read_fname in file_list:
        temp = os.path.basename(read_fname)
        doy = matlab.datenum(temp[19:23]+temp[24:28])-doy_000
        print (f'Reading OMNO2d {yr}_{doy:03d}')
        data = matlab.h5read(read_fname, 
                         '/HDFEOS/GRIDS/ColumnAmountNO2/Data Fields/ColumnAmountNO2TropCloudScreened')
        data = np.float64(data.T); # 720X1440 
        data[data<=-1.2676506e+30] = np.nan # Assign NaN value to pixel that is out of valid range
        data = data * 3.7216e-17   
        data_yr[:, doy-1] = data.ravel(order='F')
    out_fname = os.path.join(path_write, f'OMNO2d_{yr}_DU.mat')
    matlab.check_make_dir(os.path.dirname(out_fname))
    data_yr[np.isnan(data_yr)] = -9999 
    matlab.savemat(out_fname, {'data_yr':data_yr})
    tElapsed = time.time() - tStart
    print (f'{tElapsed} second')
    del data, data_yr
print ('==========================================================')


### OMSO2e
print ('OMSO2e')
for yr in YEARS:
    tStart = time.time()
    doy_000 = matlab.datenum(f'{yr}0000')
    file_list = glob.glob(os.path.join(path_read, 'L3_grid', 'OMSO2e', str(yr), '*.he5'))
    file_list.sort()
    
    if yr%4==0: days = 366
    else: days = 365
        
    data_yr = np.ones((1036800, days))*np.nan        
    for read_fname in file_list:
        temp = os.path.basename(read_fname)
        doy = matlab.datenum(temp[19:23]+temp[24:28])-doy_000
        print (f'Reading OMSO2e {yr}_{doy:03d}')
        data = matlab.h5read(read_fname,
                              '/HDFEOS/GRIDS/OMI Total Column Amount SO2/Data Fields/ColumnAmountSO2_PBL')
        rcf = matlab.h5read(read_fname,
                             '/HDFEOS/GRIDS/OMI Total Column Amount SO2/Data Fields/RadiativeCloudFraction')
        sza = matlab.h5read(read_fname,
                             '/HDFEOS/GRIDS/OMI Total Column Amount SO2/Data Fields/SolarZenithAngle')
        data = np.float64(data.T); data[data<=-1.2676506e+30] = np.nan 
        data[data<-10] = np.nan; data[data>2000] = np.nan
        rcf = np.float64(rcf.T); rcf[rcf<=-1.2676506e+30] = np.nan
        sza = np.float64(sza.T); sza[sza<=-1.2676506e+30] = np.nan
        data[rcf>=0.3]=np.nan
        data[sza>=78]=np.nan
        data_yr[:, doy-1] = data.ravel(order='F')
    out_fname = os.path.join(path_write, f'OMSO2e_m_{yr}.mat')
    matlab.check_make_dir(os.path.dirname(out_fname))
    data_yr[np.isnan(data_yr)] = -9999 
    matlab.savemat(out_fname, {'data_yr':data_yr})
    tElapsed = time.time() - tStart
    print (f'{tElapsed} second')
    del data, rcf, sza, data_yr
print ('==========================================================')    

### OMDOAO3e
print ('OMDOAO3e')
for yr in YEARS:
    tStart = time.time()
    doy_000 = matlab.datenum(f'{yr}0000')
    file_list = glob.glob(os.path.join(path_read, 'L3_grid', 'OMDOAO3e', str(yr), '*.he5'))
    file_list.sort()
    
    if yr%4==0: days = 366
    else: days = 365
        
    data_yr = np.ones((1036800, days))*np.nan        
    for read_fname in file_list:
        temp = os.path.basename(read_fname)
        doy = matlab.datenum(temp[21:25]+temp[26:30])-doy_000
        print (f'Reading OMDOAO3e {yr}_{doy:03d}')
        data = matlab.h5read(read_fname,
                              '/HDFEOS/GRIDS/ColumnAmountO3/Data Fields/ColumnAmountO3')
        rcf = matlab.h5read(read_fname,
                             '/HDFEOS/GRIDS/ColumnAmountO3/Data Fields/CloudFraction')
        sza = matlab.h5read(read_fname,
                             '/HDFEOS/GRIDS/ColumnAmountO3/Data Fields/SolarZenithAngle')
        data = np.float64(data.T); data[data<=-1.2676506e+30] = np.nan 
        rcf = np.float64(rcf.T); rcf[rcf<=-1.2676506e+30] = np.nan
        sza = np.float64(sza.T); sza[sza<=-1.2676506e+30] = np.nan
        data[rcf>=0.3]=np.nan
        data[sza>=78]=np.nan
        data_yr[:, doy-1] = data.ravel(order='F')
    out_fname = os.path.join(path_write, f'OMDOAO3e_m_{yr}.mat')
    matlab.check_make_dir(os.path.dirname(out_fname))
    data_yr[np.isnan(data_yr)] = -9999 
    matlab.savemat(out_fname, {'data_yr':data_yr})
    tElapsed = time.time() - tStart
    print (f'{tElapsed} second')
    del data, rcf, sza, data_yr
print ('==========================================================')

### OMHCHOG
print ('OMHCHOG')
for yr in YEARS:
    tStart = time.time()
    doy_000 = matlab.datenum(f'{yr}0000')
    file_list = glob.glob(os.path.join(path_read, 'L2_grid', 'OMHCHOG', str(yr), '*.he5'))
    file_list.sort()
    
    if yr%4==0: days = 366
    else: days = 365

    data_yr = np.ones((1036800, days))*np.nan        
    for read_fname in file_list:
        temp = os.path.basename(read_fname)
        doy = matlab.datenum(temp[21:25]+temp[26:30])-doy_000
        print (f'Reading OMHCHOG {yr}_{doy:03d}')
        data = matlab.h5read(read_fname,
                              '/HDFEOS/GRIDS/OMI Total Column Amount HCHO/Data Fields/ColumnAmountDestriped')
        data = np.float64(data); data = np.transpose(data, (1,0,2));
        data[data<=-1.0e+30] = np.nan
        VCD = data * 3.7216e-17
        
        QA = matlab.h5read(read_fname,
                              '/HDFEOS/GRIDS/OMI Total Column Amount HCHO/Data Fields/MainDataQualityFlag')
        QA = np.float64(QA); QA = np.transpose(QA, (1,0,2));
        QA[QA<=-30000] = np.nan
        
        sza = matlab.h5read(read_fname,
                                '/HDFEOS/GRIDS/OMI Total Column Amount HCHO/Data Fields/SolarZenithAngle')
        sza = np.float64(sza); sza = np.transpose(sza, (1,0,2));
        sza[sza<=-1.0e+30] = np.nan
        
        VCD_filtered = np.zeros(VCD.shape)
        for k in range(15):
            VCD_temp = VCD[:,:,k]
            QA_temp = QA[:,:,k]
            sza_temp = sza[:,:,k]

            VCD_temp[QA_temp!=0] = np.nan #  Good columns (0) / Suspect columns (1) / Bad columns (2) / missing (<0)
            VCD_temp[sza_temp>88] = np.nan
            VCD_filtered[:,:,k] = VCD_temp
            del VCD_temp, QA_temp, sza_temp
        VCD_avg = np.nanmean(VCD_filtered, axis=2)
        data_yr[:, doy-1] = VCD_avg.ravel(order='F')
        del data, VCD, QA, sza
    out_fname = os.path.join(path_write, f'OMHCHOG_{yr}.mat')
    data_yr[np.isnan(data_yr)] = -9999 
    matlab.savemat(out_fname, {'data_yr':data_yr})
    tElapsed = time.time() - tStart
    print (f'{tElapsed} second')
    del data_yr
print ('==========================================================')
