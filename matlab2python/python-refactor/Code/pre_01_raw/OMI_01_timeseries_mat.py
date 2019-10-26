### Package import
import os
import h5py
import time
import numpy as np

### Common
import sys
project_path = 'C:\\Users\\user\\Downloads\\matlab2python\\matlab2python\\python-refactor'
#project_path = '/home/cogito/Uncertainty/matlab2python/python-refactor'
sys.path.insert(0, project_path)
from Code.utils import matlab
from Code.utils import helpers

### Setting path
omi_path = os.path.join(project_path, 'Data', 'Raw', 'OMI')
data_path = os.path.join(project_path, 'Data')
# addpath(genpath([path_data,'/matlab_func/']))                     % Add the path of external function (matlab_func) folder with subfolders

YEARS = range(2015, 2017+1)
### OMNO2d
for yr in YEARS:
    os.chdir(os.path.join(omi_path, 'L3_grid', 'OMNO2d', str(yr)))
    list_char = matlab.dir('.', '.he5')
    doy_000 = datenum(f'{yr}0000')
    list_doy = map(lambda x: x[19:23]+x[23:28]-doy_000, list_char)
    if yr%4==0:
        days = 366
    else:
        days = 365
    
    data_yr = np.full(1036800, np.nan)
    for i in range(len(list_char)):
        # data = matlab.h5read(list_char[i], '/HDFEOS/GRIDS/ColumnAmountNO2/Data Fields/ColumnAmountNO2CloudScreened')
        data = matlab.h5read(list_char[i], '/HDFEOS/GRIDS/ColumnAmountNO2/Data Fields/ColumnAmountNO2TropCloudScreened')
        data = np.float64(data); 
        data[data<=-1.2676506e+30] = np.nan # Assign NaN value to pixel that is out of valid range
        data = data * 3.7216e-17;                                   # molec/cm2 to DU
        data_yr[:, list_doy[i]] = data.flatten() # Put daily data as column vector
        print (f'OMNO2d_{yr}_{list_doy[i]:03d}')
    data_yr(isnan(data_yr))=-9999;
    prefix = np.tile('d', [days, 1]) % prefix for header
    header = map(lambda x: f'{x:03d}', prefix) # header = cellstr([prefix,num2str([1:days]','%03i')]);
    sio.savemat(os.path.join(data_path, 'pre', 'OMI_tempConv', f'OMNO2d_{yr}_DU.mat'), mdict={'data_yr':data_yr})
    
### OMSO2e
for yr in YEARS:
    os.chdir(os.path.join(omi_path, 'L3_grid', 'OMSO2e', str(yr)))
    list_char = matlab.dir('.', '.he5')
    doy_000 = datenum(f'{yr}0000')
    list_doy = map(lambda x: x[19:23]+x[23:28]-doy_000, list_char)
    if yr%4==0:
        days = 366
    else:
        days = 365
    
    data_yr = np.full(1036800, np.nan)
    for i in range(len(list_char)):
        data = mathlab.h5read(list_char[i],'/HDFEOS/GRIDS/OMI Total Column Amount SO2/Data Fields/ColumnAmountSO2_PBL')
        rcf = mathlab.h5read(list_char[i],'/HDFEOS/GRIDS/OMI Total Column Amount SO2/Data Fields/RadiativeCloudFraction')
        sza = mathlab.h5read(list_char[i],'/HDFEOS/GRIDS/OMI Total Column Amount SO2/Data Fields/SolarZenithAngle')
    
        # Assign NaN value to pixel that is out of valid range
        data = np.float64(data) # data[data<=-1.2676506e+30]=np.nan;
        rcf = np.float64(rcf) # rcf[rcf<=-1.2676506e+30]=np.nan;
        sza = np.float64[sza] # sza[sza<=-1.2676506e+30]=np.nan;
        
        # Filtering SO2_VCD with the condition of radiative cloud fraction and
        # solar zenith angle
        data2 = data;
        data2[rcf>=0.3]=np.nan;
        data2[sza>=78]=np.nan;
        
        data_yr[, list_doy(i)] = data2.flatten() # Put daily data as column vector
        print (f'OMSO2e_m_{yr}_{list_doy[i]:03d}')
    data_yr(isnan(data_yr))=-9999;
    prefix = np.tile('d', [days, 1]) % prefix for header
    header = map(lambda x: f'{x:03d}', prefix) # header = cellstr([prefix,num2str([1:days]','%03i')]);
    sio.savemat(os.path.join(data_path, 'OMI_L3_tempConv', f'OMSO2d_{yr}_DU.mat'), mdict={'data_yr':data_yr})

### OMDOAO3e
for yr in YEARS:
    tStart = time.time()
    os.chdir(os.path.join(omi_path, 'L3_grid', 'OMDOAO3e', str(yr)))
    list_char = matlab.dir('.', '.he5')
    doy_000 = datenum(f'{yr}0000')
    list_doy = map(lambda x: x[19:23]+x[23:28]-doy_000, list_char)
    if yr%4==0:
        days = 366
    else:
        days = 365
    
    data_yr = np.full(1036800, np.nan)
    for i in range(len(list_char)):
        data = mathlab.h5read(list_char[i],'/HDFEOS/GRIDS/ColumnAmountO3/Data Fields/ColumnAmountO3')
        cf = mathlab.h5read(list_char[i],'/HDFEOS/GRIDS/ColumnAmountO3/Data Fields/CloudFraction')
        sza = mathlab.h5read(list_char[i],'/HDFEOS/GRIDS/ColumnAmountO3/Data Fields/SolarZenithAngle')
    
        # Assign NaN value to pixel that is out of valid range
        data = np.float64(data) # data[data<=-1.2676506e+30]=np.nan;
        cf = np.float64(cf) # rcf[rcf<=-1.2676506e+30]=np.nan;
        sza = np.float64[sza] # sza[sza<=-1.2676506e+30]=np.nan;
        
        # Filtering SO2_VCD with the condition of radiative cloud fraction and
        # solar zenith angle
        data2 = data;
        data2[cf>=0.3]=np.nan;
        data2[sza>=78]=np.nan;
        
        data_yr[, list_doy(i)] = data2.flatten() # Put daily data as column vector
        print (f'OMDOAO3e_m_{yr}_{list_doy[i]:03d}')
    data_yr(isnan(data_yr))=-9999;
    prefix = np.tile('d', [days, 1]) % prefix for header
    header = map(lambda x: f'{x:03d}', prefix) # header = cellstr([prefix,num2str([1:days]','%03i')]);
    sio.savemat(os.path.join(data_path, 'OMI_L3_tempConv', f'OMSO2d_{yr}_DU.mat'), mdict={'data_yr':data_yr})
    tElapsed = time.time() - tStart
    print (f'{tElapsed} second')

### OMHCHOG
for yr in YEARS:
    os.chdir(os.path.join(omi_path, 'L2_grid', 'OMHCHOG', str(yr)))
    list_char = matlab.dir('.', '.he5')
    doy_000 = datenum(f'{yr}0000')
    list_doy = map(lambda x: x[19:23]+x[23:28]-doy_000, list_char)
    if yr%4==0:
        days = 366
    else:
        days = 365
    
    data_yr = np.full(1036800, np.nan)
    for i in range(len(list_char)):
        data = mathlab.h5read(list_char[i],'/HDFEOS/GRIDS/OMI Total Column Amount HCHO/Data Fields/ColumnAmountDestriped')
        # Assign NaN value to pixel that is out of valid range
        data = np.float64(matlab.permute(data,[2,1,3]))
        data[data<=-1.0e+30] = np.nan
        VCD = data * 3.7216e-17                                  # molec/cm2 to DU
        
        QA = matlab.h5read(list_char[i],'/HDFEOS/GRIDS/OMI Total Column Amount HCHO/Data Fields/MainDataQualityFlag')
        QA = np.float64(permute(QA, [2,1,3]))
        QA[QA<=-30000] = np.nan
        
        sza = matlab.h5read(list_char[i],'/HDFEOS/GRIDS/OMI Total Column Amount HCHO/Data Fields/SolarZenithAngle')
        sza = np.float64(matlab.permute(sza,[2,1,3]))
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
        data_yr[, list_doy(i)] = VCD_avg.flatten() # Put daily data as column vector
        print (f'OMHCHOG_{yr}_{list_doy[i]:03d}')
        
        if list_doy[i]%50==0:
            data_sub = data_yr[:, list_doy[i]-48:list_doy[i]]
            sio.savemat(os.path.join(data_path, 'pre', 'OMI_L3_tempConv', f'OMHCHOG_{yr}_{list_doy[i]:03d}.mat'), mdict={'data_sub':data_sub})
    # Gathering part files
    data_yr = []
    for m in range(50, 350+1, 50):
        data_sub = sio.loadmat(os.path.join(data_path, 'pre', 'OMI_L3_tempConv', f'OMHCHOG_{yr}_{list_doy[i]:03d}.mat'))
        data_yr = np.concatenate((data_yr, data_sub), axis=1) # data_yr=[data_yr,data_sub];
    data_sub = sio.loadmat(os.path.join(data_path, 'pre', 'OMI_L3_tempConv', f'OMHCHOG_{yr}_end.mat'))
    data_yr = np.concatenate((data_yr, data_sub), axis=1)
        
    data_yr(isnan(data_yr))=-9999;
    prefix = np.tile('d', [days, 1]) % prefix for header
    header = map(lambda x: f'{x:03d}', prefix) # header = cellstr([prefix,num2str([1:days]','%03i')]);
    sio.savemat(os.path.join(data_path, 'OMI_L3_tempConv', f'OMHCHOG_{yr}_DU.mat'), mdict={'data_yr':data_yr})