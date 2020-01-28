### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

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
path_loo = os.path.join(data_base_dir, 'Preprocessed_raw', 'LOO')

target = ["PM10", "PM25"] ## Enter the name of dataset (Please use file names with the unified prefix)
type_list = ["conc","time","time_conc","cloud"]
# pathname<-"//10.72.26.56/irisnas5/GEMS/PM/"  # Nas5/GEMS

num_tree = 500
YEARS = [2016]
for t in [0]: # type
    for i in [0]: # Target 
        for yr in YEARS:
            if yr%4==0: days = 365
            else: days = 366
            
            for doy in range(1, days+1): # 321-323 80
                try:
                    fname = f'{target[i]}_RTT_EA6km_{yr}_{doy:03d}*_LOO_*_cal.csv'
                    cal_list = glob.glob(os.path.join(path_roo,type_list[t],"/dataset/",target[i],fname))
                    fname = f'{target[i]}_RTT_EA6km_{yr}_{doy:03d}*_LOO_*_val.csv'
                    val_list = glob.glob(os.path.join(path_roo,type_list[t],"/dataset/",target[i],fname))
                    
                    for c in range(len(cal_list)): # 820 985
                        try:
                            cal = pd.read_csv(cal_list[c])
                            val = pd.read_csv(val_list[c])

                            cal = cal.loc[cal.iloc[:, 23]>0, :]
                            val = val.loc[val.iloc[:, 23]>0, :]
                            cal.iloc[:, 23] = np.log(cal.iloc[:, 23])
                            val.iloc[:, 23] = np.log(val.iloc[:, 23])
                            
                            ## Mask Random Forest model using ranger
                            ti = time.time()
                            params = {
                                    n_estimators:num_tree,
                                    criterion:'mse', # splitrule = 'variance', “mse” for the mean squared error, which is equal to variance reduction, The function to measure the quality of a split.
                                    min_samples_leaf:5, # min.node.size = 5, 
                                    n_jobs:8, # num.threads = 8, 
                                    verbose:2, # verbose = TRUE. for debugging. 
                                    bootstrap:True, # replace = TRUE, excatly same? not sure...
                                    max_depth:None, # max.depth=default 0. unlimited depth
                                    min_samples_split:1, # Fraction of observations to sample. Default is 1 for sampling with replacement
                                    #importance = "permutation", 
                                    #write.forest = TRUE, 
                                    #scale.permutation.importance = TRUE, 
                                    #save.memory = FALSE, 
                            }
                            rf_model = RandomForestRegressor(**params)
                            rf_model.fit(cal)
                            t2 = time.time()
                            print (t2-t1)
                            
                            if t==3:
                                name = os.path.basenanme(cal_list[c])[36:70]
                            elif t==4:
                                name = os.path.basenanme(cal_list[c])[32:66]
                            else:
                                name = os.path.basenanme(cal_list[c])[31:65]
                            
                            # Validation reslut
                            pred_val = rf_model.predict(val.drop([target[i]]), val[target[i]])
                            pred_val = np.exp(pre_val)
                            
                            # save vali pred
                            fname = f'rf_{name}_val_ranger.csv'
                            pred_val = pd.DataFrame(pred_val)
                            matlab.check_make_dir(os.path.join(paht_loo, type_list[t],"/RF/",target[i]))
                            pred_val.to_csv(os.path.join(paht_loo, type_list[t],"/RF/",target[i], fname), sep=",")
                            print('Predicted val result is saved')
                        except:
                            pass
                    # LOO list
                    print (doy)
                except:
                    pass
                # doy
                print (yr)
            # yr
            print (target[i])
        # target
        print (type_list[t])
    # type                          