### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import scipy.io as sio
import numpy as np
import glob
import pandas as pd

### Setting path
data_base_dir = os.path.join('/', 'media', 'sf_GEMS_1', 'Data')
raw_data_path = os.path.join(data_base_dir, 'Raw', 'GOCI_AOD') 
write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_AOD')

path = 'C:\Temp\jp_stn_org'

# header = {'doy','year','month','day','KST','SO2','CO','O3','NO2','PM10','PM25','scode'}
# pcode = {'01','SO2','ppb';'02','NO','ppb';'03','NO2','ppb';'04','NOX','ppb';'05','CO','x01ppm';...
#     '06','OX','ppb';'07','NMHC','x10ppbc';'08','CH4','x10ppbc';'09','THC','x10ppbc';...
#     '10','SPM','ug_m3';'12','PM25','ug_m3';...
#     '21','WD','x16DIRC';'22','WS','x01m_s';'23','TEMP','x01degC';'24','HUM','percent';...
#     '25','SUN','x001MJ';'26','RAIN','mm';'27','UV','x001MJ';'28','PRS','mb';'29','NETR','x001MJ';...
#     '41','CO2','x01ppm';'42','O3','ppb';}

# '43','HCL'; '44','HF'; '45','H2S'; '46','SHC'; '47','UHC'

p=12; varname = 'PM25'; # p=51

header_p = ['doy','year','month','day','scode','ccode','KST', 'stn_{varname}']
# '측정년도/측정국코드/시도코드/측정항목코드/측정단위코드/측정월/측정일'

stnPM25 = stnPM25_tbl_old_09.values
stn_unq_09 = np.unique(stnPM25[:,[0,4,6], axis=1)
yr=2009

# for yr=2015:2015#2016
curr_path = os.path.join(path, str(yr))
flist = glob.glob(os.path.join(curr_path, f'*_{p:02d}.txt'))
flist [os.path.basename(f) for f in flist]

data=[]
for k in range(len(flist)):
    data_temp = pd.read_csv(flist[k])
    data= np.concatenate((data, data_temp), axis=0)

data_org = data
# data_unq = np.unique(data_org[:,[1,5,6]], axis=1)

data_p = data[:,3].values
idx_PM25 = matlab.ismember(data_p,'PM25')
idx_PMBH = matlab.ismember(data_p,'PMBH')
idx_PMFL = matlab.ismember(data_p,'PMFL')

# data_unit = table2cell(data(:,5))
# bb =matlab.ismember(data_unit,data_unit(1))
# sum(bb)==size(data,1)

data[:,3:5]=[]

data = data.values

# test1
data_PMBH = data[idx_PMBH,:]
data_PMFL = data[idx_PMFL,:]
data_PM25 = data[idx_PM25,:]
data_PMBH_unq = np.unique(data_PMBH[:,[1,3,4]], axis=1)
data_PMFL_unq = np.unique(data_PMFL[:,[1,3,4]], axis=1)
data_PM25_unq = np.unique(data_PM25[:,[1,3,4]], axis=1)

# test2
stn_unq_PMFL = np.unique(data_PMFL[:,1])
stn_unq_PMBH = np.unique(data_PMBH[:,1])
stn_unq_PM25 = np.unique(data_PM25[:,1])
a = matlab.ismember(stn_unq_PMFL,stn_unq_PM25); np.sum(a)
stn_unq_PMFL[a]
a_PM25 = data_PM25[data_PM25[:,1]==27115010,:]
a_PMFL = data_PMFL[data_PMFL[:,1]==27115010,:]

b = matlab.ismember(stn_unq_PMBH,stn_unq_PM25); np.sum(b)
c = matlab.ismember(stn_unq_PMFL,stn_unq_PMBH); np.sum(c)

a2 = matlab.ismember(stn_unq_PM25,stn_unq_PMFL); np.sum(a2)
b2 = matlab.ismember(stn_unq_PM25,stn_unq_PMBH); np.sum(b2)
c2 = matlab.ismember(stn_unq_PMBH,stn_unq_PMFL); np.sum(c2)

#% PM25, PMBH 두개다 있는 스테이션값 중에서 PMBH로 측정한거 다 제거
#% idx_rm = idx_PMBH & ismember(data(:,2),27115010); % 2015-2016
idx_rm = idx_PMFL & matlab.ismember(data[:,1],27115010)) # 2011-2014
data[idx_rm,:]=[]

yrmonday = data[:,0]*10000 + data[:,3]*100 + data[:,4]
data_datenum = matlab.datenum(str(yrmonday))
doy_000 = matlab.datenum(f'{yr}00000')
data_doy = data_datenum-doy_000

data_info = np.concatenate((data_doy,data[:,0],data[:,2],data[:,4],data[:,1:3]), axis=1) # 'doy','year','month','day','scode','ccode'

data_new = []
for KST in range(1,24+1):
    data_temp = data_info
    data_temp[:,6]=KST
    data_temp = np.concatenate((data_temp, data[:,4+KST]), axis=1)
    data_new= np.concatenate((data_new, data_temp), axis=0)


if yr%4==0:
    data_new[data_new[:,2]==2 & data_new[:,3]>29,:] = []
else:
    data_new[data_new[:,2]==2 & data_new[:,3]>28,:] = []


data_new[data_new[:,2]==4 & data_new[:,3]==31,:] = []
data_new[data_new[:,2]==6 & data_new[:,3]==31,:] = []
data_new[data_new[:,2]==9 & data_new[:,3]==31,:] = []
data_new[data_new[:,2]==11 & data_new[:,3]==31,:] = []

stnPM25_tbl = pd.DateFrame(data_new, columns=['VariableNames']+header_p) 
fname = f'JP_stnPM25_{yr}.csv'
stnPM25_tbl.to_csv(os.path.join(path, fname))
#matlab.savemat(os.path.join(path,'/JP_stnPM25_',num2str(yr)],'stnPM25_tbl')
