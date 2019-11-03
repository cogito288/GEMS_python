import arcpy
from arcpy import env
import glob
import re
arcpy.CheckOutExtension("spatial")

path="\\\\10.72.26.46\\irisnas6\\Data\\MODIS_tile\\02region\\EastAsia\\MYD13A2\\"
mask = "\\\\10.72.26.56\\irisnas5\\Data\\mask\\v_rec_N50W110S20E150.shp"

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
        c = ""+path+"\\03mask\\"+str(i)+"\\m_"+b+""
        tempEnvironment0 = arcpy.env.snapRaster
        arcpy.env.snapRaster = a
        # Process: Extract by Mask
        arcpy.gp.ExtractByMask_sa(a, mask, c)
        arcpy.env.snapRaster = tempEnvironment0
        print(b)
