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

yr = 2009
matlab.loadmat(os.path.join(data_base_dir,'Station/Station_JP', f'jp_stn_scode_data_{yr}.mat'))

# header_ndata = {'doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode','scode2'}

## byPollutant 파일 불러와서, 바꿔야하는 날짜들에 해당하는 행만 뽑아놓고 나머진 지우기
if yr%4==0:
    doy_chg = [60,61,121,182,274,335]
else:
    doy_chg = [59,60,61,120,181,273,334]


tg = ['SO2','CO','OX','NO2','SPM','PM25']
for i in range(6):
    fname = f'JP_stn{tg[i]}_{yr}.mat'
    stn = matlab.loadmat(os.path.join(data_base_dir, 'Station', 'Station_JP', 'byPollutant', fname))[f'stn{tg[i]}_tbl']
    stn_sub = stn[np.isin(stn[:, 0], doy_chg),:]
    vars()[f'stn{tg[i]}'] = stn_sub
    del stn
stnPM10 = copy.deepcopy(stnSPM)
del stn_sub, stnSPM
    
## scode2 할때 하나 기간 잘못입력해서 삭제해줘야하는 샘플 지우기
if yr==2016:
    ndata_scode = np.delete(ndata_scode, ndata_scode[:,0]==90 & ndata_scode[:,12]==281090100, axis=0)
    ndata_scode = np.delete(ndata_scode, ndata_scode[:,0]==91 & ndata_scode[:,12]==281090100, axis=0)
chg_idx = np.where(np.isin(ndata_scode[:,0],doy_chg))[0]

# matlab.loadmat(os.path.join(path_data,'Station/Station_JP/jp_stn_scode_data_change_',str(yr)])
# 9997 이상 제거하는거 다음번에 돌릴땐 넣어야할듯

for kk in range(len(chg_idx)):
    k = chg_idx[kk]
    aSO2 = stnSO2[stnSO2[:,0]==ndata_scode[k,0] & stnSO2[:,6]==ndata_scode[k,4] & stnSO2[:,4]==ndata_scode[k,11],7]
    aCO = stnCO[stnCO[:,0]==ndata_scode[k,0] & stnCO[:,6]==ndata_scode[k,4] & stnCO[:,4]==ndata_scode[k,11],7]
    aOX = stnOX[stnOX[:,0]==ndata_scode[k,0] & stnOX[:,6]==ndata_scode[k,4] & stnOX[:,4]==ndata_scode[k,11],7]
    aNO2 = stnNO2[stnNO2[:,0]==ndata_scode[k,0] & stnNO2[:,6]==ndata_scode[k,4] & stnNO2[:,4]==ndata_scode[k,11],7]
    aPM00 = stnPM00[stnPM00[:,0]==ndata_scode[k,0] & stnPM00[:,6]==ndata_scode[k,4] & stnPM00[:,4]==ndata_scode[k,11],7]
    aPM25 = stnPM25[stnPM25[:,0]==ndata_scode[k,0] & stnPM25[:,6]==ndata_scode[k,4] & stnPM25[:,4]==ndata_scode[k,11],7]
    
    if len(aSO2)!=0: ndata_scode[k,5] = aSO2; else: ndata_scode[k,5]=np.nan 
    if len(aCO)!=0: ndata_scode[k,6] = aCO; else: ndata_scode[k,6]=np.nan
    if len(aOX)!=0: ndata_scode[k,7] = aOX; else: ndata_scode[k,7]=np.nan
    if len(aNO2)!=0: ndata_scode[k,8] = aNO2; else: ndata_scode[k,8]=np.nan
    if len(aPM10)!=0: ndata_scode[k,9] = aPM10; else: ndata_scode[k,9]=np.nan
    if len(aPM25)!=0: ndata_scode[k,10] = aPM25; else: ndata_scode[k,10]=np.nan
    
    if ((kk+1)%10)==0:
        print (f'{kk} / {len(chg_idx}')     
fname = f'jp_stn_scode_data_change_{yr}.mat'
matlab.savemat(os.path.join(data_base_dir,'Station/Station_JP/', fname),
               {'ndata_scode':ndata_scode,'header_ndata':header_ndata})