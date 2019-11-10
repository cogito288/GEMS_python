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
import time

### Setting path
data_base_dir = os.path.join('/', 'media', 'sf_GEMS_1', 'Data')
raw_data_path = os.path.join(data_base_dir, 'Raw', 'GOCI_AOD') 
write_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_AOD')
# path = '/Volumes/irisnas5/GEMS/PM/'
# addpath(genpath('/Volumes/irisnas5/Data/matlab_func/'))

path = '//10.72.26.56/irisnas5/GEMS/PM/'
#addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'))
target=['PM10','PM25']
type_list=['conc','time','time_conc','cloud']
YEARS = [2015, 2016, 2017]
## Read validation result
for t in range(1,3+1):
    for i in [1,2]: # target
        for yr in YEARS:
            val_scatter = []
            fname = f'{type_list[t]}_[target[i]]_compare_RF_LOO_EA6km_val_stn_ovr_new2.csv'
            results = pd.read_csv(os.path.join(path, '00_EA6km/LOO/',type_list[t],'/stn_location/',fname))
            results_yr = results[results[:,-1]==yr,:]
            
            val_scatter[:,0]= results[:,0] #stn
            val_scatter[:,1]= results[:,1] #RF
            if i==1:
                val_scatter = val_scatter[val_scatter[:,0] < 1000,:]
            else:
                val_scatter = val_scatter[val_scatter[:,0] < 600,:]
            val_scatter = val_scatter[val_scatter[:,0] > 0,:]
            val_scatter = val_scatter[val_scatter[:,1] > 0,:]
            
            bias = val_scatter[:,1]-val_scatter[:,0]
            mid = np.divide(val_scatter[:,1]+val_scatter[:,0]), 2)
            
            MBE = np.mean(bias)
            MAE = np.mean(np.abs(bias))
            MFE = np.mean(np.divide(np.abs(bias), mid))*100
            print (f'MBE : {MBE}     MAB : {MAE}     MFE : {MFE}')
            accuracy = [MBE, MAE, MFE]
            #     matlab.savemat(os.path.join(path, 'dataset/scatterplot/LOO/',target{i},'_accuracy_RF.mat'],'accuracy')
            #             matlab.savemat(os.path.join(path_2, 'dataset/scatterplot/',target{i},'_accuracy_test_',str(test, '#02i'),'_set_',str(j,'#02i'),'.mat'],'accuracy')
            
            
            ## density scatter plot
            if i==1:
                # need to implement heatscatter_paper in matlab.py
                PM_val = matlab.heatscatter_paper(val_scatter[:,0], val_scatter[:,1],
                            os.path.join(path,'/dataset/scatterplot'), 'PM10_RF_val.jpg',
                            '','','',
                            1,'',
                           'Observed PM_1_0 Concentration (\mug/m^3)','Estimated PM_1_0 Concentration (\mug/m^3)','PM_1_0 Validation')
                print(f'-djpeg -r300 {path}04_scatterplot/{type_list[t]}_scatter_PM10_LOO_{yr}_new.jpg')
            else:
                PM_val = heatscatter_paper(val_scatter[:,0], val_scatter[:,1], 
                            os.path.join(path,'/dataset/scatterplot'), 'PM25_RF_val.jpg',
                            '','','',
                            1,'',
                            'Observed PM_2_._5 Concentration (\mug/m^3)','Estimated PM_2_._5 Concentration (\mug/m^3)','PM_2_._5 Validation')
                print(f'-djpeg -r300 {path}04_scatterplot/{type_list[t]}_scatter_PM25_LOO_{yr}_new.jpg')

