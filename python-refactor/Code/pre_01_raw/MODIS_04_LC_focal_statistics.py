### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import rasterio as rio
from numba import njit
from scipy.ndimage.filters import generic_filter as gf
import time

data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_mcd_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS', 'MCD12Q1')
class_name = ["forest","shrub","savannas","grass","wetland","crop","urban","snow","barren","water"]

@njit
def njit_mean(data):
    return np.mean(data)
radius = 6
y,x = np.ogrid[-radius:radius+1, -radius:radius+1]
mask = x**2 + y**2 <= radius**2

YEARS = [2016]
for yr in YEARS:
    for col in class_name:
        tStart = time.time()
        input_file = os.path.join(path_mcd_processed, '02_LC_binary', str(yr), f"MODIS_LC_500m_EA_{col}_{yr}.tif")
        output_file = os.path.join(path_mcd_processed, "03_LC_ratio", str(yr), f"EA_{col}_ratio_r6_500m_{yr}.tif")
        
        matlab.check_make_dir(os.path.dirname(output_file))
        
        with rio.open(input_file) as src:
            band = src.read(1).astype('float64')
            circular_mean = gf(band, njit_mean, footprint=mask)
            kwargs = src.meta.copy()
            kwargs.update({
              'dtype':'float64',
              'compress':'LZW',
            })
            with rio.open(output_file, 'w', **kwargs) as dst:
                dst.write(circular_mean, 1)
        print (os.path.basename(output_file))
        tElapsed = time.time() - tStart
        print (f'time taken : {tElapsed}')