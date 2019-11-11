### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import scipy.io as sio
import numpy as np
import glob
import time
import h5py 
import pygrib
import re
from osgeo import gdal
import tempfile
#import arcpy
#from arcpy import env

flist = ['/home/sehyun/GEMS_python/python-refactor/Code/pre_01_raw/GOCI_01_02.py',
'/home/sehyun/GEMS_python/python-refactor/Code/pre_01_raw/GOCI_03_AOD_filter.py',
'/home/sehyun/GEMS_python/python-refactor/Code/pre_01_raw/GOCI_04_filtering.py',
'/home/sehyun/GEMS_python/python-refactor/Code/pre_01_raw/GOCI_05_BL_1km.py',]

for filename in flist:
    cme = ['/home/sehyun/GEMS_python/venv/bin/python', filename]
    subprocess.call(cmd)
    break
