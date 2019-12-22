import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import glob
import re
import tempfile

data_base_dir = os.path.join(project_path, 'Data')
path_modis = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS')
class_name = ["forest","shrub","savannas","grass","wetland","crop","urban","snow","barren","water"]

path_data = os.path.join(project_path, "\\\\10.72.26.46\\irisnas6\\Data\\MODIS_tile\\00raw\\MYD13A2\\"
path="\\\\10.72.26.46\\irisnas6\\Data\\MODIS_tile\\02region\\EastAsia\\MYD13A2\\"

YEARS = [2019]
for j in YEARS: 
    print(j)
    #env.workspace=""+path+""
    path_data_temp=os.path.join(path_data, str(j)) #""+path_data+"\\"+str(j)+""
    flist = glob.glob(os.path.join(path_data_temp, "*.hdf"))
    flist.sort()
    nfile = len(flist)
    npath = len(path_data_temp)

    path_mosaic = os.path.join(path, "01mosaic", j)
    for k in range(56,nfile,14): # range(0,nfile,14):
        flist_temp = flist[k:k+14]
        doy = flist_temp[0][npath+14:npath+17]

        tiles = []
        for m in range(0,14):
            # Extract Subdataset
            src_dataset = flist_temp[m]
            dst_dataset = f"NDVI_{doy}_{m+1}.tif"
            #arcpy.ExtractSubDataset_management(a, b, "0")
            cmd = ["gdal_translate", src_dataset, dst_dataset, "-b", "0"]
            subprocess.call(cmd)
            tiles.append(dst_dataset)
                    
        # Mosaic
        
        fname = f"MYD13A2_{j}_{doy}.tif"
        #arcpy.MosaicToNewRaster_management(tiles, path_mosaic, fname, "", "16_BIT_SIGNED", "", "1", "LAST", "FIRST")
        # MosaicToNewRaster(input_rasters, output_location, raster_dataset_name_with_extension, {coordinate_system_for_the_raster}, {pixel_type}, {cellsize}, number_of_bands, {mosaic_method}, {mosaic_colormap_mode})
        out_fname = os.path.join(path_mosaic, fnam)
        cmd = ["gdal_merge.py", "-o", out_fname, "-ot", "Int16"]
        cmd.append(tiles)
        subprocess.call(cmd)
        for m in range(0,14):
            #arcpy.Delete_management(""+path+"\\NDVI_"+str(doy)+"_"+str(m+1)+".tif")
            os.remove(os.path.join(path, f"NDVI_{doy}_{m+1}.tif"))
        print(doy)
