import arcpy
from arcpy import env
import glob
import re
arcpy.CheckOutExtension("spatial")

path="\\\\10.72.26.46\\irisnas6\\Data\\MODIS_tile\\02region\\EastAsia\\MYD13A2\\"
#Extent = "112.99111237331 23.9931929698016 146.998439892367 48.0049852944791"
#mask = "\\\\10.72.26.56\\irisnas5\\Data\\Aerosol\\SRTM\\SRTM_DEM_mask.tif"

for i in range(2019,2020):
    print(i)
    env.workspace=""+path+"\\01mosaic\\"+str(i)+""
    flist = glob.glob(str(env.workspace)+"\\*.tif")
    flist.sort();
    nfile = len(flist)
    npath = len(env.workspace)

    for j in range(4,nfile): # range(0,nfile):
        a = flist[j]
        b = a[npath+1:]
        c = ""+path+"\\02prj_GCS_WGS84\\"+str(i)+"\\p_"+b+""
        d = ""+path+"\\03mask\\"+str(i)+"\\m_"+b+""

        # Process: Project Raster
        #tempEnvironment0 = arcpy.env.snapRaster
        #arcpy.env.snapRaster = mask
        #tempEnvironment1 = arcpy.env.extent
        #arcpy.env.extent = Extent
        arcpy.ProjectRaster_management(a, c, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", "NEAREST", "1.02308446206551E-02 1.02308446206551E-02", "", "", "PROJCS['Unknown_datum_based_upon_the_custom_spheroid_Sinusoidal',GEOGCS['GCS_Unknown_datum_based_upon_the_custom_spheroid',DATUM['D_Not_specified_based_on_custom_spheroid',SPHEROID['Custom_spheroid',6371007.181,0.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Sinusoidal'],PARAMETER['false_easting',0.0],PARAMETER['false_northing',0.0],PARAMETER['central_meridian',0.0],UNIT['Meter',1.0]]")
        #arcpy.env.snapRaster = tempEnvironment0
        #arcpy.env.extent = tempEnvironment1

        # Process: Extract by Mask
        #arcpy.gp.ExtractByMask_sa(c, mask, d)

        print(b)
