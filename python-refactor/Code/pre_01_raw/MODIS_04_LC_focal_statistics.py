# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# focal_statistics.py
# Author: Minso Shin
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
from arcpy import env
import glob
import re
#arcpy.CheckOutExtension("spatial")

path_data="\\\\10.72.26.56\\irisnas5\\Data\\"
path_work=path_data+"pre\\MODIS\\MCD12Q1\\"
class_name = ["forest","shrub","savannas","grass","wetland","crop","urban","snow","barren","water"]

YEARS = range(2001, 2018)
for yr in YEARS:
    workspace = os.path.join(path_work, "02_LC_binary", str(yr))
    #env.workspace=""+path_work+"02_LC_binary\\"+str(yr)
    
    for ii in range(0,10):
        src_dataset = os.path.join(workspace, f"MODIS_LC_500m_EA_{class_name[ii]}_{yr}.tif"
        dst_dataset = os.path.join(path_work, "03_LC_ratio", str(yr), f"EA_{class_name[ii]}_ratio_r6_500m_{yr}.tif"
        #a = "MODIS_LC_500m_EA_"+class_name[ii]+"_"+str(yr)+".tif"
        #b = ""+path_work+"03_LC_ratio\\"+str(yr)+"\\EA_"+class_name[ii]+"_ratio_r6_500m_"+str(yr)+".tif"
        #arcpy.gp.FocalStatistics_sa(a, b, "Circle 6 CELL", "MEAN", "DATA")
        
