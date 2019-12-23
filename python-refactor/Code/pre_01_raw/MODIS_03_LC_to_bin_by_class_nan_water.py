### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import rasterio as rio
import glob
import time 

data_base_dir = os.path.join(project_path, 'Data')
path_modis = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS', 'MCD12Q1')
class_name = ["forest","shrub","savannas","grass","wetland","crop","urban","snow","barren","water"]

YEARS = [2016]
for yr in YEARS:
    src_dataset = os.path.join(path_modis, '03masked_N50W110S20E150', f'm_MODIS_LC_500m_{yr}.tif')
    dst_dataset = os.path.join(path_modis, '01_reclassified', f'reclass_MODIS_LC_500m_EA_{yr}.tif')
    matlab.check_make_dir(os.path.dirname(dst_dataset)) # Debugging
    matlab.check_make_dir(os.path.join(path_modis, '02_LC_binary', str(yr))) # Debugging
    
    with rio.open(src_dataset) as src:
        band = src.read(1).copy()
        band[(band>=1) & (band<6)] = 1
        band[(band>=6) & (band<8)] = 2
        band[(band>=8) & (band<10)] = 3
        band[band==10] = 4
        band[band==11] = 5
        band[(band==12) | (band==14)] = 6
        band[band==13] = 7
        band[band==15] = 8
        band[band==16] = 9
        band[(band==17) | (band==src.meta['nodata'])] = 10
        
        kwargs = src.meta.copy()
        kwargs.update({
                'nodata':None,
                'compress':'LZW',
        })
        with rio.open(dst_dataset, 'w', **kwargs) as dst:
            dst.write_band(1, band)
    print (os.path.basename(dst_dataset))
    
    with rio.open(dst_dataset) as dst:
        band = dst.read(1).copy()
        for ii, col in enumerate(class_name):
            dst_dataset02 = os.path.join(path_modis, "02_LC_binary", str(yr), f"MODIS_LC_500m_EA_{col}_{yr}.tif")
            band2 = band.copy()
            band2 = np.where(band2==(ii+1), 1, 0)
            band2 = band2.astype('uint8')
            kwargs = dst.meta.copy()
            kwargs.update({
                    'dtype': 'uint8',
                    'compress':'LZW',
            })
            with rio.open(dst_dataset02, 'w', **kwargs) as dst02:
                dst02.write_band(1, band2)
            print (os.path.basename(dst_dataset02))