# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# LC_to_bin_by_class.py
# Author: Minso Shin
# Description: Make binary classification data by class from reclassified data
# ---------------------------------------------------------------------------

import arcpy
from arcpy import env
import glob
import re
arcpy.CheckOutExtension("spatial")

path_modis="\\\\10.72.26.46\\irisnas6\\Data\\MODIS_tile\\02region\\EastAsia\\MCD12Q1\\03masked_N50W110S20E150\\"
path_data="\\\\10.72.26.56\\irisnas5\\Data\\"
path_work=path_data+"pre\\MODIS\\MCD12Q1\\"
class_name = ["forest","shrub","savannas","grass","wetland","crop","urban","snow","barren","water"]



for yr in range(2001,2018):
    #env.workspace=""+path_work+""
    a = ""+path_modis+"m_MODIS_LC_500m_"+str(yr)+".tif"
    b = ""+path_work+"01_reclassified\\reclass_MODIS_LC_500m_EA_"+str(yr)+".tif"

    # Process: Reclassify
    arcpy.gp.Reclassify_sa(a, "Value", "1 1;2 1;3 1;4 1;5 1;6 2;7 2;8 3;9 3;10 4;11 5;12 6;13 7;14 6;15 8;16 9;17 10;NODATA 10", b, "DATA")


    for ii in range(0,10):
        c = ""+path_work+"02_LC_binary\\"+str(yr)+"\\MODIS_LC_500m_EA_"+class_name[ii]+"_"+str(yr)+".tif"
        arcpy.gp.RasterCalculator_sa("Con(\""+b+"\"=="+str(ii+1)+",1,0)", c)

        

