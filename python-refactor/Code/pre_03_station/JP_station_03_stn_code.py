### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import copy
import numpy as np
import pandas as pd
import glob

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
raw_path = os.path.join(data_base_dir, 'Raw') 
station_path = os.path.join(data_base_dir, 'Station') 

stn_info = pd.read_csv(os.path.join(data_base_dir,'Station/Station_JP/jp_stn_code_lonlat_period_filtered_yyyymmdd.csv'),header=1)
# scode1, scode2, lon, lat, op_start, op_
scode_unq = np.unique(stn_info[:,0])
del stn_info 

header_ndata = ['doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25',
    'NO','NOX','NMHC','CH4','THC','CO2','scode']

YEARS = [2015]
for yr in YEARS: #:2016 #2009:2016
    stnSO2_tbl = matlab.loadmat(os.path.join(path_data,'Station/Station_JP/byPollutant/',f'JP_stnSO2_{yr}.mat'))['stnSO2_tbl']
    stnNO_tbl = matlab.loadmat(os.path.join(path_data,'Station/Station_JP/byPollutant/',f'JP_stnNO_{yr}.mat'))['stnNO_tbl']
    stnNO2_tbl = matlab.loadmat(os.path.join(path_data,'Station/Station_JP/byPollutant/',f'JP_stnNO2_{yr}.mat'))['stnNO2_tbl']
    stnNOX_tbl = matlab.loadmat(os.path.join(path_data,'Station/Station_JP/byPollutant/',f'JP_stnNOX_{yr}.mat'))['stnNOX_tbl']
    stnNOX_tbl = matlab.loadmat(os.path.join(path_data,'Station/Station_JP/byPollutant/',f'JP_stnCO_{yr}.mat'))['stnCO_tbl']
    stnOX_tbl = matlab.loadmat(os.path.join(path_data,'Station/Station_JP/byPollutant/',f'JP_stnOX_{yr}.mat'))['stnOX_tbl']
    stnNMHC_tbl = matlab.loadmat(os.path.join(path_data,'Station/Station_JP/byPollutant/',f'JP_stnNMHC_{yr}.mat'))['stnNMHC_tbl']
    stnCH4_tbl = matlab.loadmat(os.path.join(path_data,'Station/Station_JP/byPollutant/',f'JP_stnCH4_{yr}.mat'))['stnCH4_tbl']
    stnTHC_tbl = matlab.loadmat(os.path.join(path_data,'Station/Station_JP/byPollutant/',f'JP_stnTHC_{yr}.mat'))['stnTHC_tbl']
    stnSPM_tbl = matlab.loadmat(os.path.join(path_data,'Station/Station_JP/byPollutant/',f'JP_stnSPM_{yr}.mat'))['stnSPM_tbl']
    stnPM25_tbl = matlab.loadmat(os.path.join(path_data,'Station/Station_JP/byPollutant/',f'JP_stnPM25_{yr}.mat'))['stnPM25_tbl']
    stnCO2_tbl = matlab.loadmat(os.path.join(path_data,'Station/Station_JP/byPollutant/',f'JP_stnCO2_{yr}.mat'))['stnCO2_tbl']
    
    stnSO2 = stnSO2_tbl.values
    stnNO = stnNO_tbl.values 
    stnNO2 = stnNO2_tbl.values
    stnNOX = stnNOX_tbl.values
    stnCO = stnCO_tbl.values
    stnOX = stnOX_tbl.values
    stnNMHC = stnNMHC_tbl.values
    stnCH4 = stnCH4_tbl.values
    stnTHC = stnTHC_tbl.values
    stnSPM = stnSPM_tbl.values
    stnPM25 = stnPM25_tbl.values
    stnCO2 = stnCO2_tbl.values
    
    del stnSO2_tbl, stnNO_tbl, stnNO2_tbl, stnNOX_tbl, stnCO_tbl, stnOX_tbl, stnNMHC_tbl, stnCH4_tbl, stnTHC_tbl, stnSPM_tbl, stnPM25_tbl, stnCO2_tbl
    
    if yr%4==0: days = 366
    else: days = 365
    
    a_doy,a_KST,a_scode = np.meshgrid(np.asarray(range(1, days+1)), np.asarray(range(1, 24+1)), scode_unq)
    aa = np.hstack([a_doy.ravel(order='F'),a_KST.ravel(order='F'),a_scode.ravel(order='F')])
    
    doy000 = matlab.datenum(f'{yr}00000')   
    mm = [d[4:6] for d in matlab.datestr(doy000+aa[:,0])] # datestr: yyyymmdd
    dd = [d[6:] for d in matlab.datestr(doy000+aa[:,0])]    
    bb = np.full((aa.shape[0], 12), np.nan)
    nanidx = None
    for k in range(np.max(aa.shape)):
        tStart = time.time()
        aSO1 = stnSO1[stnSO1[:,0]==aa[k,0] & stnSO1[:,6]==aa[k,1] & stnSO1[:,4]==aa[k,2],7]
        aNO = stnNO[stnNO[:,0]==aa[k,0] & stnNO[:,6]==aa[k,1] & stnNO[:,4]==aa[k,2],7]
        aNO1 = stnNO1[stnNO1[:,0]==aa[k,0] & stnNO1[:,6]==aa[k,1] & stnNO1[:,4]==aa[k,2],7]
        aNOX = stnNOX[stnNOX[:,0]==aa[k,0] & stnNOX[:,6]==aa[k,1] & stnNOX[:,4]==aa[k,2],7]
        aCO = stnCO[stnCO[:,0]==aa[k,0] & stnCO[:,6]==aa[k,1] & stnCO[:,4]==aa[k,2],7]
        aOX = stnOX[stnOX[:,0]==aa[k,0] & stnOX[:,6]==aa[k,1] & stnOX[:,4]==aa[k,2],7]
        aNMHC = stnNMHC[stnNMHC[:,0]==aa[k,0] & stnNMHC[:,6]==aa[k,1] & stnNMHC[:,4]==aa[k,2],7]
        aCH4 = stnCH4[stnCH4[:,0]==aa[k,0] & stnCH4[:,6]==aa[k,1] & stnCH4[:,4]==aa[k,2],7]
        aTHC = stnTHC[stnTHC[:,0]==aa[k,0] & stnTHC[:,6]==aa[k,1] & stnTHC[:,4]==aa[k,2],7]
        aSPM = stnSPM[stnSPM[:,0]==aa[k,0] & stnSPM[:,6]==aa[k,1] & stnSPM[:,4]==aa[k,2],7]
        aPM14 = stnPM14[stnPM14[:,0]==aa[k,0] & stnPM14[:,6]==aa[k,1] & stnPM14[:,4]==aa[k,2],7]
        aCO1 = stnCO1[stnCO1[:,0]==aa[k,0] & stnCO1[:,6]==aa[k,1] & stnCO1[:,4]==aa[k,2],7]
        if len(aSO2)!=0: bb[k,0]=aSO2 
        if len(aCO)!=0:  bb[k,1]=aCO 
        if len(aOX)!=0:  bb[k,2]=aOX 
        if len(aNO2)!=0:  bb[k,3]=aNO2 
        if len(aSPM)!=0:  bb[k,4]=aSPM 
        if len(aSPM)!=0:  bb[k,5]=aPM25 
        if len(aNO)!=0:  bb[k,6]=aNO 
        if len(aNOX)!=0:  bb[k,7]=aNOX 
        if len(aSaNMHCO2)!=0:  bb[k,8]=aNMHC 
        if len(aCH4)!=0:  bb[k,9]=aCH4 
        if len(aTHC)!=0:  bb[k,10]=aTHC 
        if len(aCO2)!=0:  bb[k,11]=aCO2 
        
        bb_temp = bb[k,:]
        bb_temp[bb_temp>=9997]= np.nan
        bb[k,:]=bb_temp
        
        nanidx_temp = np.sum(np.isnan(bb_temp))
        if nanidx_temp == 12:
            if nanidx is None:
                nanidx = k
            else:
                nanidx = np.vstack([nanidx, k])
        
        tElapsed = time.time() - tStart
        print (f'{yr}_{aa[k,0]:03d}_{aa[k,1]:02d}---{tElapsed} sec')
    
    ndata = np.hstack([aa[:,0], np.multiply(yr, np.ones((aa.shape[0], 1))), mm, dd, aa[:,1], bb, aa[:,2]])
    ndata = np.delete(ndata, nanidx, axis=0)
    matlab.savemat(os.path.join(path_data,'Station/Station_JP/stn_code_data', f'stn_code_data_all_{yr}.mat'),
                   {'ndata':ndata, 'header_ndata':header_ndata})
    print (yr)