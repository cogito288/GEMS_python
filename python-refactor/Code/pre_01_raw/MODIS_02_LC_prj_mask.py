### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import glob
import time 
import tempfile
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling


### Setting path
data_base_dir = os.path.join(project_path, 'Data')
path_mosaic = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS')
mask = os.path.join(data_base_dir, 'Raw', 'mask', 'r_rec_N50W110S20E150.tif')
#path_modis="\\\\10.72.26.46\\irisnas6\\Data\\MODIS_tile\\02region\\EastAsia\\MCD12Q1\\"

flist = glob.glob(os.path.join(path_mosaic, '01mosaic', "*.tif"))
flist.sort()

for src_dataset in flist:
    last_num = os.path.basename(src_dataset)[-8:] # b 2016.tif
    print (src_dataset)
    
    matlab.check_make_dir(os.path.join(path_mosaic, '02prj_GCS_WGS84')) # debugging
    matlab.check_make_dir(os.path.join(path_mosaic, '03masked_N50W110S20E150')) # debugging
    
    dst_dataset02 = os.path.join(path_mosaic, '02prj_GCS_WGS84', f'GCS_EA_MCD12Q1_{last_num}') # c
    dst_dataset03 = os.path.join(path_mosaic, '03masked_N50W110S20E150', f'm_MODIS_LC_500m_{last_num}') # d

    dst_crs = 'EPSG:4326'
    with rio.open(src_dataset) as src:
        transform, width, height = calculate_default_transform(src.crs, dst_crs, src.width, src.height, *src.bounds, resolution=5.11542231032757E-03)
        kwargs = src.meta.copy()
        kwargs.update({
	    		'crs': dst_crs,
		    	'transform': transform,
			    'width': width,
    			'height': height,
                'nodata':255,
                'compress':'LZW',
        })

        with rio.open(dst_dataset02, 'w', **kwargs) as dst:
            for i in range(1, src.count+1):
	            reproject(
    		        source=rio.band(src, i),
	    		    destination=rio.band(dst, i),
    	    		src_transform=src.transform,
	     	    	src_crs=src.crs,
            	    dst_transform=transform,
		            dst_crs=dst_crs,
          			resampling=Resampling.nearest,
    	    		#src_nodata=255.0,
                )
            print (dst.meta)

    # Process: Extract by Mask
    #cmd = ["gdaltindex", "temp_mask.shp", mask]
    #print (cmd)
    #subprocess.call(cmd)

    #cmd = ["gdalwarp", "-cutline", "temp_mask.shp", 
    #       dst_dataset02, dst_dataset03]
    #subprocess.call(cmd)

    #cmd = ["rm", "temp_mask.shp"]
    #subprocess.call(cmd)
    #arcpy.gp.ExtractByMask_sa(dst_dataset02, mask, dst_dataset03)
    #arcpy.env.snapRaster = tempEnvironment0
    
    print(os.path.basename(src_dataset))
