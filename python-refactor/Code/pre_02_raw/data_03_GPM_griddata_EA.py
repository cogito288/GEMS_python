### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import glob
import numpy as np
from scipy.interpolate import griddata
import time

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_gpm_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'GPM', 'AP_24h_hourly') # read
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km') 
path_ea_goci_gpm = os.path.join(path_ea_goci, 'Preprocessed_raw', 'EA_GOCI6km', 'GPM_AP') # Write

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_goci.mat'))
lat_goci, lon_goci = mat['lat_goci'], mat['lon_goci']
del mat

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_gpm.mat'))
lat_gpm, lon_gpm = mat['lat_gpm'], mat['lon_gpm']
del mat
lat_gpm = lat_gpm[1100:1400, 2900:3300] # N50 W110 S20 E150
lon_gpm = lon_gpm[1100:1400, 2900:3300] 
points = np.array([lon_gpm.ravel(order='F'), lat_gpm.ravel(order='F')]).T
del lon_gpm, lat_gpm
print (f'points shape : {points.shape}')

YEARS = [2016]
for yr in YEARS:
    flist = glob.glob(os.path.join(path_gpm_processed, str(yr), '*.mat'))
    flist.sort()
    for fname in flist:
        tStart = time.time()
        precip = matlab.loadmat(fname)['precip']
        precip = precip[1100:1400, 2900:3300]
        values = precip.ravel(order='F')
        precip = griddata(points=points, 
                          values=values,
                          xi=(lon_goci, lat_goci),
                          method='linear')
        matlab.savemat(os.path.join(path_ea_goci_gpm, str(yr), f'EA6km_{os.path.basename(fname)}'), 
                      {'precip':precip})
        del precip
        print (os.path.basename(fname))
        tElapsed = time.time() - tStart
        print (f'time taken : {tElapsed}')
    print (yr)

