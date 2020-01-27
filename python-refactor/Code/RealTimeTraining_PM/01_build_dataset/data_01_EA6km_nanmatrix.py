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
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km') 

##
YEARS = [2016]
for yr in YEARS:
    if yr%4==0: days= 366
    else: days=365
        
    nanidx = np.zeros((218999, days, 7)) # python needs to predefine and does not allow size-growing up directly. 
    for doy in range(1, days+1):
        for utc in range(7+1):
            fname = f'cases_EA6km_{yr}_{doy:03d}_{utc:02d}.mat'
            mat = matlab.loadmat(os.path.join(path_ea_goci, 'cases_mat', str(yr), fname))
            # data[:,[3:19,27:31,34:37]] # extract specific variables for PMs
            tmp_cols = ['OMHCHOG_tc', 'AOD', 'AE', 'FMF', 'SSA', 'NDVI', 'RSDN', 'Precip', 'DEM', 'Temp', 'Dew', 'RH', 'P_srf', 'MaxWS', 'PBLH', 'Visibility', 'stack1_maxWS', 'stack3_maxWS', 'stack5_maxWS', 'stack7_maxWS', 'AP3h', 'DOY', 'PopDens']
            df = pd.DataFrame(columns=tmp_cols)
            for col in tmp_cols:
                df[col] = np.squeeze(mat[col])
            data = df.values 
            del df, mat
            data[np.isnan(data)] = -9999 # convert nan ro -9999
            nanidx[:,doy-1,utc] = data[:,0] # make a matrix
            idy, idx = np.where(data == -9999) # np.where the location where the -9999 is
            idy = np.unique(idy) # remove same number
            nanidx[idy.ravel(order='F'), doy-1, utc] = np.nan # change the value to nan value 
            nanidx[:,doy-1,utc]=np.isnan(nanidx[:,doy-1,utc]) # np.where where is nan value(nan=1, valied value=0)
            print (utc)
        print (doy)
    fname = f'nanidx_EA6km_{yr}.mat'
    matlab.savemat(os.path.join(path_nas6,'EA_GOCI6km', fname), {'nanidx':nanidx})
    print (yr)