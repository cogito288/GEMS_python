### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
from numba import njit

### Setting path
#data_base_dir = os.path.join(project_path, 'Data')
#path_read = os.path.join(data_base_dir, 'Preprocessed_raw', 'OMI') 
data_base_dir = os.path.join('/', 'share', 'irisnas5', 'GEMS', 'GEMS_python')
path_read = os.path.join(data_base_dir, 'Preprocessed_raw', 'OMI_tempConv')

### Setting period
#YEARS = [2016] #, 2018, 2019
pname_list = ['OMNO2d','OMSO2e_m','OMDOAO3e_m','OMHCHOG']

mask = np.zeros((720, 1440))
mask[340:552, 1020:1308] = 1
mask = mask.ravel(order='F')

### Temporal convolution with gaussian
for pname in pname_list:
    print (pname)
    ### Load data
    YEARS = [2014,2015,2016,2017,2018]
    def read_and_mask(yr):
        if os.path.isfile(os.path.join(path_read, f'{pname}_{yr}_DU.mat')):
            data_yr = matlab.loadmat(os.path.join(path_read, f'{pname}_{yr}_DU.mat'))['data_yr']
        elif os.path.isfile(os.path.join(path_read, f'{pname}_trop_CS_{yr}_DU.mat')):
            data_yr = matlab.loadmat(os.path.join(path_read, f'{pname}_trop_CS_{yr}_DU.mat'))['data_yr']
        elif os.path.isfile(os.path.join(path_read, f'{pname}_{yr}.mat')):
            data_yr = matlab.loadmat(os.path.join(path_read, f'{pname}_{yr}.mat'))['data_yr']
        else:
            raise ValueError(f'{pname}_{yr}.mat does not exists though variation tried.')
        data_subset = data_yr[mask==1, :]
        return data_subset
    data = np.concatenate([read_and_mask(yr) for yr in YEARS], axis=1)  # hstack
    data[data==-9999] = np.nan
    sigma = 1
    print (f' data shape : {data.shape}')
    
    #@njit(error_model='numpy')
    def calculate(data):
        data_conv = np.full(data.shape, np.nan)
        for k in range(data.shape[0]):
            for t in range(data.shape[1]):
                t_ = t+1
                w_sum = 0; x_sum = 0;
                for n in range(data.shape[1]):
                    n_ = n+1
                    if np.isnan(data[k,n])==0:
                        w = np.exp((-(t_-n_)**2)/(2*sigma**2)) #  calcuate weights using t,n(days) with sigma # (k+1)-(n-1)=k-n
                        x = data[k, n]*w
                        w_sum += w
                        x_sum += x
                try:
                    data_conv[k,t] = x_sum/w_sum
                except ZeroDivisionError:
                    data_conv[k,t] = np.nan
            print (k)
        return data_conv
    data_conv = calculate(data)
    matlab.savemat(os.path.join(path_read, f'tempConv_{pname}_sigma{sigma}_{YEARS[0]}_{YEARS[len(YEARS)-1]}.mat'), 
                   {'data_conv':data_conv, 'data':data})
    #matlab.savemat(os.path.join(path_read, f'tempConv_{pname}_trop_CS_sigma{sigma}_2005_2019.mat'),
    #                {'data_conv':data_conv, 'data':data})
