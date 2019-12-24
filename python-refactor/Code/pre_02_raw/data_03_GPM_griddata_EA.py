### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
#from matplotlib.pyplot import imread
from scipy.interploate import griddata

### Setting path
data_base_dir = os.path.join(project_path, 'Data')
path_read = os.path.join(data_base_dir, 'Preprocessed_raw', 'GPM', 'AP_24h_hourly') 
path_write = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km', 'GPM_AP')

mat = matlab.loadmat(os.path.join(path_data, 'grid', 'grid_goci.mat'))
lat_goci = mat['lat_goci']
lat_goci = mat['lon_goci']
del mat

mat = matlab.loadmat(os.path.join(path_data, 'grid', 'grid_gpm.mat'))
lat_gpm = mat['lat_gpm']
lon_gpm = mat['lon_gpm']
del mat
lat_gpm = lat_gpm[1100:1400, 2900:3300] # N50 W110 S20 E150
lon_gpm = lon_gpm[1100:1400, 2900:3300] 
points = np.array(lon_gpm.ravel(order='F'), lat_gpm.ravel(order='F')).T
del lon_gpm, lat_gpm

YEARS = [2016]
for yr in YEARS:
    flist = glob.glob(os.path.join(path_read, str(yr), '*.mat'))
    for fname in flist:
        precip = matlab.loadmat(fname)
        precip = precip[1100:1400, 2900:3300]
        values = precip.ravel(order='F')
        precip = griddata(points=points, 
                          values=values,
                          xi=(lon_goci, lat_goci),
                          method='linear')
        mathalb.savemat(os.path.join(path_write, str(yr), f'EA6km_{flist[i]}.mat'), precip)
        print (os.path.basename(fname))
    print (yr)

