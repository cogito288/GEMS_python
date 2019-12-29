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
path_preprocessed = os.path.join(data_base_dir, 'Preprocessed_raw')

##
YEARS = [2015, 2016]
for yr in YEARS:
    if yr ==2016: days = 366
    else: days = 365
    for doy in range(1, days+1):
        for utc in range(7+1):
            fname = f'cases_EA6km_{yr}_{doy:03d}_{utc:02d}.mat'
            mat = matlab.loadmat(os.path.join(path_preprocessed,'EA_GOCI6km/cases_mat', fname))
            data_tbl = pd.DataFrame(
            data = data_tbl.values
            data = data[:,[3:19,27:31,34:37]] # extract specific variables for PMs
            del data_tbl
            
            data[np.isnan(data)] = -9999 # convert nan ro -9999
            nanidx[:,doy-1,utc] = data[:,1] # make a matrix
            idy, idx = np.where[data == -9999] # np.where the location where the -9999 is
            idy = np.unique(idy) # remove same number
            nanidx[idy.flatten(), doy-1, utc] = np.nan # change the value to nan value 
            nanidx[:,doy-1,utc]=np.isnan(nanidx[:,doy-1,utc]) # np.where where is nan value(nan=1, valied value=0)
            print (utc)
        print (doy)
    fname = f'nanidx_EA6km_{yr}.mat'
    matlab.savemat(os.path.join(path_nas6,'EA_GOCI6km'), fname, {'nanidx':nanidx})
    print (yr)

