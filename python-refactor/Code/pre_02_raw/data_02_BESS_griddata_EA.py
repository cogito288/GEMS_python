### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import netCDF4
import numpy as np
import glob
from scipy.interpolate import griddata
import time

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_bess_raw = os.path.join(data_base_dir, 'Raw', 'BESS') # Read
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km') 
path_ea_goci_bess = os.path.join(path_ea_goci, 'Preprocessed_raw', 'EA_GOCI6km', 'BESS') # Write

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_bess.mat')) # lon_bess, lat_bess
points = np.array([mat['lon_bess'].ravel(order='F'), mat['lat_bess'].ravel(order='F')]).T
del mat
print (f'points shape : {points.shape}')

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_goci.mat')) # lon_goci, lat_goci
lon_goci = mat['lon_goci']
lat_goci = mat['lat_goci']
del mat

YEARS = [2016]
for yr in YEARS:
    file_list = glob.glob(os.path.join(path_bess_raw, str(yr), '*.nc'))
    file_list.sort()
    for fname in file_list:
        tStart = time.time()
        print (f'Reading ... {os.path.basename(fname)}')
        if yr<=2016: # Until 2016 (nc)
            ncfile = netCDF4.Dataset(fname)
            bess = np.array(ncfile.variables['surface_downwelling_shortwave_flux_in_air']).T 
            ncfile.close()
        else: # 2017 (mat)
            bess = matlab.loadmat(fname)['bess']
        bess = bess.astype('float64')
        bess[bess==-9999] = np.nan
        values = bess.ravel(order='F')
        tStart = time.time()
        RSDN = griddata(points, values, xi=(lon_goci, lat_goci), method='linear')
        write_fname = f'EA6km_BESS_RSDN_{yr}_{os.path.basename(fname)[-6:-3]}.mat'
        matlab.savemat(os.path.join(path_ea_goci_bess, str(yr), write_fname), {'RSDN':RSDN})
        del bess, RSDN
        print (write_fname)
        tElapsed = time.time() - tStart
        print (f'time taken : {tElapsed}')
    print (yr)