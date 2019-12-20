### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
from numba import njit
import rasterio as rio
from scipy.ndimage.filters import generic_filter as gf

data_base_dir = os.path.join(project_path, 'Data')
path_modis = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS')
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
        input_file = os.path.join(path_modis, '02_LC_binary', str(yr), f"MODIS_LC_500m_EA_{col}_{yr}.tif")
        output_file = os.path.join(path_modis, "03_LC_ratio", str(yr), f"EA_{col}_ratio_r6_500m_{yr}.tif")
        
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
        