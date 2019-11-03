import arcpy
from arcpy import env
import glob
import re
arcpy.CheckOutExtension("spatial")

path_data="\\\\10.72.26.46\\irisnas6\\Data\\MODIS_tile\\00raw\\MYD13A2\\"
path="\\\\10.72.26.46\\irisnas6\\Data\\MODIS_tile\\02region\\EastAsia\\MYD13A2\\"
#Extent = "112.99111237331 23.9931929698016 146.998439892367 48.0049852944791"
#mask = "\\\\10.72.26.56\\irisnas5\\Data\\Aerosol\\SRTM\\SRTM_DEM_mask.tif"

for j in range(2019,2020):
    print(j)
    env.workspace=""+path+""
    path_data_temp=""+path_data+"\\"+str(j)+""
    flist = glob.glob(""+str(path_data_temp)+"\\*.hdf")
    flist.sort();
    nfile = len(flist)
    npath = len(path_data_temp)

    path_mosaic = ""+path+"01mosaic\\"+str(j)+""
    for k in range(56,nfile,14): # range(0,nfile,14):
        flist_temp = flist[k:k+14]
        doy = flist_temp[0][npath+14:npath+17]

        for m in range(0,14):
            # Extract Subdataset
            a = flist_temp[m]
            b = "NDVI_"+str(doy)+"_"+str(m+1)+".tif"
            arcpy.ExtractSubDataset_management(a, b, "0")
            if m==0:
                tiles = b
            else:
                tiles = ""+tiles+";"+b+""
                    
        # Mosaic
        
        fname = "MYD13A2_"+str(j)+"_"+str(doy)+".tif"
        arcpy.MosaicToNewRaster_management(tiles, path_mosaic, fname, "", "16_BIT_SIGNED", "", "1", "LAST", "FIRST")

        for m in range(0,14):
            arcpy.Delete_management(""+path+"\\NDVI_"+str(doy)+"_"+str(m+1)+".tif")
                
        print(doy)
