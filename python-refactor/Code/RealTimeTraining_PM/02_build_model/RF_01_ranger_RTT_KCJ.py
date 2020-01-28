### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import time
import numpy as np
import glob
import pandas as pd
#from thundergbm import TGBMClassifier
from sklearn.ensemble import RandomForestRegressor

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km')
path_rtt = os.path.join(data_base_dir, 'Preprocessed_raw', 'RTT')

target = ["PM10", "PM25"] ## Enter the name of dataset (Please use file names with the unified prefix)
type_list = ["conc","time","time_conc"]

num_tree = 500
YEARS = [2016]
for t in [2]: # type
    for i in [0]: # target
        for yr in YEARS:
            if yr%4==0: days = 365
            else: days = 366
            
            for doy in range(1, days+1): # 321-323 80
                for utc in range(7+1) : #0:7)
                    try:
                        fname = f"{target[i]}_RTT_EA6km_{yr}_{doy:03d}_{utc:02d}.csv"
                        data = pd.read_csv(os.path.join(path_rtt, type_list[t], 'dataset', target[i], fname)) #For calibration 
                        cols = data.columns

                        cal = data.loc[:, cols[:24]]
                        cal = cal.loc[cal.iloc[:, 23]>0, :]
                        cal.iloc[:, 23] = np.log(cal.iloc[:, 23])

                        val = data.loc[data.iloc[:, 29]==240, :]
                        val = val.loc[val.iloc[:, 28]==0, cols[:24]]
                        val = val.loc[val.iloc[:, 23]>0, :]
                        val.iloc[:, 23] = np.log(val.iloc[:, 23])

                        ## Make Random Forest model using ranger
                        t1=time.time()
                        params = {
                                'n_estimators':num_tree, 
                                'criterion':'mse',
                                'min_samples_leaf':5,
                                'n_jobs':8,
                                'verbose':2
                                }

                        features = ['AOD', 'AE', 'FMF', 'SSA', 'NDVI', 'RSDN', 'Precip', 'DEM', 'LCurban',
           'Temp', 'Dew', 'RH', 'P_srf', 'MaxWS', 'PBLH', 'Visibility',
           'stack1_maxWS', 'stack3_maxWS', 'stack5_maxWS', 'stack7_maxWS', 'DOY',
           'PopDens', 'RoadDens']
                        rf_model = RandomForestRegressor(**params)
                        rf_model.fit(cal.loc[:, features].values, cal.loc[:, target[i]].values)

                        t2=time.time()
                        print(t2-t1)

                        fname = f"cases_EA6km_{yr}_{doy:03d}_{utc:02d}.csv"
                        pred = pd.read_csv(os.path.join(path_ea_goci, "cases_csv", str(yr), fname))

                        features = ['AOD', 'AE', 'FMF', 'SSA', 'NDVI', 'RSDN', 'Precip', 'DEM', 'LC_urban', # LCurban
           'Temp', 'Dew', 'RH', 'P_srf', 'MaxWS', 'PBLH', 'Visibility',
           'stack1_maxWS', 'stack3_maxWS', 'stack5_maxWS', 'stack7_maxWS', 'DOY',
           'PopDens', 'RoadDens']
                        pred = pred.loc[:,features+[target[i]]] 
                        pred.fillna(-9999, inplace=True)

                        name = f"{target[i]}_RTT_EA6km_{yr}_{doy:03d}_{utc:02d}"       

                        # Prediction result
                        pred_cases = rf_model.predict(pred[features].values) # predict(rf_model, data = pred)
                        pred_cases = np.exp(pred_cases)

                        # save pred prediction
                        fname = f"rf_{name}.csv"
                        pred_cases = pd.DataFrame(pred_cases)
                        matlab.check_make_dir(os.path.join(path_rtt, type_list[t],"RF_pred",target[i]))
                        pred_cases.to_csv(os.path.join(path_rtt, type_list[t], "RF_pred",target[i], fname), sep=",")
                        # print('Predicted prediction result is saved')

                        features = ['AOD', 'AE', 'FMF', 'SSA', 'NDVI', 'RSDN', 'Precip', 'DEM', 'LCurban',
           'Temp', 'Dew', 'RH', 'P_srf', 'MaxWS', 'PBLH', 'Visibility',
           'stack1_maxWS', 'stack3_maxWS', 'stack5_maxWS', 'stack7_maxWS', 'DOY',
           'PopDens', 'RoadDens']
                        # Validation result
                        pred_val = rf_model.predict(val[features]) #predict(rf_model,data=val)
                        pred_val = np.exp(pred_val)

                        # save vali prediction
                        pred_val = pd.DataFrame(pred_val)
                        fname = f"rf_{name}_val.csv"
                        matlab.check_make_dir(os.path.join(path_rtt, type_list[t],"RF",target[i]))
                        pred_val.to_csv(os.path.join(path_rtt, type_list[t],"RF",target[i], fname), sep=",")
                        print('Predicted val result is saved')
                    except:
                        pass