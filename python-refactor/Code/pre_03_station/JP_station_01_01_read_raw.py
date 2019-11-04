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

path = 'C:\Temp\jp_stn_copy'

# header = {'doy','year','month','day','KST','SO2','CO','O3','NO2','PM10','PM25','scode'}
pcode = [['01','SO2','ppb'],
         ['02','NO','ppb'], 
         ['03','NO2','ppb'],
         ['04','NOX','ppb'],
         ['05','CO','x01ppm'],
         ['06','OX','ppb'],
         ['07','NMHC','x10ppbc'],
         ['08','CH4','x10ppbc'],
         ['09','THC','x10ppbc'],
         ['10','SPM','ug_m3'],
         ['12','PM25','ug_m3'],
         ['21','WD','x16DIRC'],
         ['22','WS','x01m_s'],
         ['23','TEMP','x01degC'],
         ['24','HUM','percent'],
         ['25','SUN','x001MJ'],
         ['26','RAIN','mm'],
         ['27','UV','x001MJ'],
         ['28','PRS','mb'],
         ['29','NETR','x001MJ'],
         ['41','CO2','x01ppm'],
         ['42','O3','ppb']]

# '43','HCL'; '44','HF'; '45','H2S'; '46','SHC'; '47','UHC'

# p=1; varname = 'SO2'
# p=2; varname = 'NO'
# p=3; varname = 'NO2'
# p=4; varname = 'NOX'
# p=5; varname = 'CO'
# p=6; varname = 'OX'
# p=7; varname = 'NMHC'
# p=8; varname = 'CH4'
# p=9; varname = 'THC'
# p=10; varname = 'SPM'
# p=12; varname = 'PM25'; p=51
# p=21; varname = 'WD'
# p=22; varname = 'WS'
# p=23; varname = 'TEMP'
# p=24; varname = 'HUM'
# p=25; varname = 'SUN'
# p=26; varname = 'RAIN'
# p=27; varname = 'UV'
# p=28; varname = 'PRS'
# p=29; varname = 'NETR'
# p=41; varname = 'CO2'
# p=42; varname = 'O3'
varname = 'PM25'; p=51

header_p = ['doy','year','month','day','scode','ccode','KST', 'stn_{varname}']
# '측정년도/측정국코드/시도코드/측정항목코드/측정단위코드/측정월/측정일'

YEARS = [2016] # range(2009, 2009+1)
for y in YEARS:
    curr_path = os.path.join(path, str(yr))
    list_char = glob.glob(os.path.join(curr_path, f'*_{p:02d}.txt'))
    list_char [os.path.basename(f) for f in list_char]

    data=[]
    for k in range(len(list_char)): 
        data_temp = pd.read_csv(list_char[k])
        data=np.concatenate((data, data_temp), axis=0)


    # data_p = table2cell(data(:,4))
    # aa = ismember(data_p,data_p(1))
    # sum(aa)==size(data,1)
    # 
    # data_unit = table2cell(data(:,5))
    # bb = ismember(data_unit,data_unit(1))
    # sum(bb)==size(data,1)

    if p = 12:
        vv = data[:, 3].values # Have to check ...
        idx_PM25 = matlab.ismember(vv,'PM25')
        idx_PMBH = matlab.ismember(vv,'PMBH')
        idx_PMFL = matlab.ismember(vv,'PMFL')
        data_PMBH = data[idx_PMBH,:]
        data_PMFL = data[idx_PMFL,:]
        data = data[idx_PM25,:]

    data[:,3:5]=[]

    data = data.values
    yrmonday = data[:,0]*10000 + data[:,3]*100 + data[:,4]
    data_datenum = matlab.datenum(str(yrmonday))
    doy_000 = matlab.datenum(f'{yr}00000')
    data_doy = data_datenum-doy_000

    data_info = np.concatenate((data_doy,data[:,0],data[:,3],data[:,4],data[:,1:3]), axis=1) # 'doy','year','month','day','scode','ccode'
    data_new = []
    for KST in range(1,24+1):
        data_temp = data_info
        data_temp[:,6]=KST
        data_temp = np.concatenate((data_temp, data[:,4+KST)), axis=1)
        data_new= np.concatenate((data_new, data_temp), axis=0)

    vars()[f'stn{varname}_tbl'] = pd.DateFrame(data_new, columns=['VariableNames']+header_p) 
    # eval(sprintf(['stn',varname,'_tbl = array2table(data_new,''VariableNames'',header_p);']))
    fname = f'JP_stn{varname}_{yr}.mat'
    vars()[f'stn{varname}_tbl'].to_csv(os.path.join(path, fname))

    #matlab.savemat(path, fname, {f'stn{varname}_tbl':vars()[f'stn{varname}_tbl'])
    # stnPM25_tbl = array2table(data_new,'VariableNames',header_p)
    # matlab.savemat(os.path.join(path,'/JP_stnPM25_',num2str(yr)],'stnPM25_tbl')
