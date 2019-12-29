### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import copy
import numpy as np
import pandas as pd
import glob

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')

YEARS = range(2009, 2016+1)
for yr in YEARS:
    mat = matlab.loadmat(os.path.join(data_base_dir,'Station/Station_JP/stn_scode_data_add_NOX_O3',
                                      f'jp_stn_scode_data_add_NOX_O3_{yr}.mat'))
    ndata_scode = mat['ndata_scode']
    header_ndata = mat['header_ndata']
    del mat

    ind = np.lexsort((ndata_scode[:,12],ndata_scode[:,0],ndata_scode[:,4]))    
    ndata_scode = ndata_scode[ind]
    ndata_scode_nan = ndata_scode[:,[5:11,13:15]]
    ndata_scode_np.full[ndata_scode_nan>=9997]=np.nan
    ndata_scode_np.full[ndata_scode_nan<0]=np.nan
    ndata_scode[:,[5:11,13:15]]=ndata_scode_nan
    fname = f'jp_stn_scode_data_add_NOX_O3_{yr}.mat'
    matlab.savemat(os.path.join(data_base_dir,'Station/Station_JP/stn_scode_data_add_NOX_O3',
                    fname, {'ndata_scode':ndata_scode,'header_ndata':header_ndata})