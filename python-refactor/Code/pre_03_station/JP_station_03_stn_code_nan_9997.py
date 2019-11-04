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
import pandas as pd

### Setting path
data_base_dir = os.path.join('/', 'media', 'sf_GEMS_1', 'Data')
raw_data_path = os.path.join(data_base_dir, 'Raw', 'GOCI_AOD') 
write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_AOD')

path_data = '/share/irisnas5/Data/'

YEARS = range(2009, 2016+1)
for yr in YEARS:
    fname = f'jp_stn_scode_data_add_NOX_O3_{yr}.mat'
    mat = matlab.loadmat(os.path.join(path_data,'Station/Station_JP/stn_scode_data_add_NOX_O3', fname))
    ndata_scode = mat['ndata_scode']
    header_ndata = mat['header_ndata']
    del mat

    ndata_scode = matlab.sortrows(ndata_scode,[13,1,5])
    ndata_scode_nan = ndata_scode[:,[5:11,13:15]]
    ndata_scode_np.full[ndata_scode_nan>=9997]=np.nan
    ndata_scode_np.full[ndata_scode_nan<0]=np.nan
    ndata_scode(:,[5:11,13:15])=ndata_scode_nan
    fname = f'jp_stn_scode_data_add_NOX_O3_{yr}.mat'
    matlab.savemat(os.path.join(path_data,'Station/Station_JP/stn_scode_data_add_NOX_O3'),
                    fname, {'ndata_scode':ndata_scode,'header_ndata':header_ndata})
