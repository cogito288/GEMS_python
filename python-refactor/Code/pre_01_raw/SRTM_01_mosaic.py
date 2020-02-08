### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = base_dir
sys.path.insert(0, project_path)
from Code.utils import matlab

import glob
import time
import rasterio
from rasterio.merge import merge

### Setting path
data_base_dir = os.path.join(base_dir, 'Data')
path_srtm_raw = os.path.join(data_base_dir, 'Raw', 'SRTM_DEM', '3Arc_Void_Filled')
path_srtm_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'SRTM_DEM')

flist = glob.glob(os.path.join(path_srtm_raw, "*.tif"))
flist.sort()
nfile = len(flist)

# Mosaic
input_files = []
for fname in flist:
    src = rasterio.open(fname)
    input_files.append(src)
    
mosaic, out_trans = merge(input_files)

matlab.check_make_dir(path_srtm_processed)
dst_fname = os.path.join(path_srtm_processed, 'SRTM_DEM_3Arc_Void_Filled_mosaic.tif')

tStart = time.time()
mosaic[mosaic==-32767]=-9999
out_meta = src.meta.copy()
out_meta.update({"nodata":-9999,
                 "height": mosaic.shape[1],
                 "width": mosaic.shape[2],
                 "transform": out_trans,
                 "compress":"LZW"})
with rasterio.open(dst_fname,"w",**out_meta) as dest:
    dest.write(mosaic)

tElapsed = time.time() - tStart
print (f'time taken : {tElapsed}')
