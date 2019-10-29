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
data_path = os.path.join(project_path, 'Data')
work_path = os.path.join(data_path, 'pre', 'OMI_L3_tempConv')
# addpath(genpath([path_data,'/matlab_func/']))  % Add the path of external function (matlab_func) folder with subfolders

pname_list = ['OMNO2d','OMSO2e_m','OMDOAO3e_m','OMHCHOG']

mask = np.zeros((720, 1440))
mask[340:552, 1020:1308] = 1
mask = mask.flatten()


### Temporal convolution with gaussian
# for i in range(4):
i = 3
pname = pname_list[i]

### Load data
YEARS = range(2005, 2019+1)
for yr in YEARS:
    # data_yr = sio.loadmat(os.path.join(work_path, f'{pname}_{yr}.mat'))
    data_yr = sio.loadmat(os.path.join(work_path, f'{pname}_trop_CS_{yr}_DU.mat'))
    data_subset = data_yr[mask==1, :]
    data = np.concatenate((data, data_subset), axis=1)
data_org = data
data[data==-9999] = np.nan
sigma = 1
data_conv = np.full(data.shape, np.nan)

for k in range(data.shape[0]):
    for t in range(5478): # for 15 years
        w_sum = 0; x_sum = 0;
        for n in range(5478): # for 15 years
            if np.isnan(data[k,n])==0:
                w = np.exp((-(k-n)**2)/(2*sigma**2)) #  calcuate weights using t,n(days) with sigma # (k+1)-(n-1)=k-n
                x = data[k, n]*w
                w_sum = w_sum+w
                x_sum = x_sum+x
        data_conv[k,t] = x_sum/w_sum
    print (k)
# sio.savemat(os.path.join(work_path, f'tempConv_{pname}_sigma_{sigma}_2005_2019.mat'), mdict={'data_conv':data_conv, 'data':data})
sio.savemat(os.path.join(work_path, f'tempConv_{pname}_trop_CS_sigma{sigma}_2005_2019.mat'), mdict={'data_conv':data_conv, 'data':data})