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

### Setting path
data_base_dir = os.path.join('/', 'media', 'sf_GEMS', 'Data')
raw_data_path = os.path.join(data_base_dir, 'Raw', 'BESS') 
write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'BESS')

mat = matlab.loadmat(os.path.join(data_base_dir, 'grid', 'grid_bess.mat')) # lon_bess, lat_bess
lon_bess = mat['lon_bess']
lat_bess = mat['lat_bess'] 
del mat

mat = matlab.loadmat(os.path.join(data_base_dir, 'grid', 'grid_goci.mat')) # lon_goci, lat_goci
lon_goci = mat['lon_goci']
lat_goci = mat['lat_goci']
del mat

#%% Until 2016 (nc)
YEARS = [2016]
for yr in YEARS:
    file_list = glob.glob(os.path.join(raw_data_path, str(yr), '*.nc'))
    file_list.sort()
    for fname in file_list:
        print (f'Reading ... {fname}')
        ncfile = netCDF4.Dataset(fname)
        bess = np.array(ncfile.variables['surface_downwelling_shortwave_flux_in_air']).T 
        ncfile.close()
        bess = bess.astype('float32')
        bess[bess==-9999] = np.nan
        points = np.array((lon_bess.flatten(), lat_bess.flatten())).T
        values = bess.flatten()
        RSDN = griddata(points, values, (lon_goci, lat_goci), method='linear')
        print (RSDN)
        write_fname = f'EA6km_BESS_RSDN_{yr}_{os.path.basename(fname)[-6:-3]}.mat'
        matlab.savemat(os.path.join(write_path, str(yr), write_fname), {'RSDN':RSDN})
        print (fname)
        break
    print (yr)
"""
##  2017 (mat)
YEARS = [2017]
for yr in YEARS:
    os.chdir(os.path.join(path_bess, str(yr)))
    flist = matlab.get_files_endswith('.', '.mat')

    for k in range(len(flist)):
        bess = matlab.loadmat(flist[k])
        RSDN = griddata(zip(lon_bess, lat_bess), bess, zip(lon_goci, lat_goci), method='linear') # %리샘플링 (0.05 degree를 6km goci 격자로)
        fname = flist[-5:]
        matlab.savemat(os.path.join(path_data, 'DA_GOCI6km', 'BESS', str(yr)), f'EA6km_BESS_RSDN_{yr}_{fname}.mat', RSDN) 
        print (flist[k])
"""
