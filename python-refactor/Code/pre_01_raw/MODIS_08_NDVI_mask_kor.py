import arcpy
from arcpy import env
import glob
import re
arcpy.CheckOutExtension("spatial")

path="\\\\10.72.26.46\\irisnas6\\Data\\MODIS_tile\\02region\\EastAsia\\MYD13A2\\"
path_korea="\\\\10.72.26.46\\irisnas6\\Data\\MODIS_tile\\02region\\SouthKorea\\MYD13A2\\"
Extent = "123.995024793363 32.9983435120948 131.513769680712 39.0077492770766"
mask = "\\\\10.72.26.56\\irisnas5\\Data\\mask\\r_mask_korea.tif"

for i in range(2019,2020):
    print(i)
    env.workspace=""+path+"\\02prj_GCS_WGS84\\"+str(i)+""
    flist = glob.glob(str(env.workspace)+"\\*.tif")
    flist.sort();
    nfile = len(flist)
    npath = len(env.workspace)

    for j in range(4,nfile): # range(0,nfile):
        a = flist[j]
        b = a[npath+3:]
        c = ""+path_korea+"\\03mask\\"+str(i)+"\\m_"+b+""

        tempEnvironment0 = arcpy.env.snapRaster
        arcpy.env.snapRaster = mask
        tempEnvironment1 = arcpy.env.extent
        arcpy.env.extent = Extent
        # Process: Extract by Mask
        arcpy.gp.ExtractByMask_sa(a, mask, c)
        arcpy.env.snapRaster = tempEnvironment0
        arcpy.env.extent = tempEnvironment1

        print(b)
