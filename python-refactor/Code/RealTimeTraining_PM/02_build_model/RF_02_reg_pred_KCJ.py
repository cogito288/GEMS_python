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
import pickle
#from thundergbm import TGBMClassifier
from sklearn.ensemble import RandomForestRegressor

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km')
path_rtt = os.path.join(path_ea_goci, 'RTT')
path_roo = os.path.join(path_ea_goci, 'LOO')

target = ["PM10", "PM25"] ## Enter the name of dataset (Please use file names with the unified prefix)
test = ["AOD_GOCI_V1","AOD_AERONET_V1","AOD_AERONET_V2","GOCI_AOD"]
# pathname<-"//10.72.26.56/irisnas5/GEMS/Cloud/"  # Nas5/GEMS
pathname = "/share/irisnas5/GEMS/Cloud/"  # Nas5/GEMS
#setwd(pathname)


for i in [1]:  
    for t in [2]:  ## Target type
        t1=time.time()
        fname = f"rf_{target[i]}_dataset_wtJP_noUTC_{test[t]}_model_ranger.RData"
        with open(os.path.join(path_rtt, "RF", "PM",target[i],"new", fname), 'rb') as f:
            rf_model = pickle.load(f)
            
        fname = f"{target[i]}_dataset_pred_wtJP.csv"
        pred_tmp = pd.read_csv(os.path.join(path_rtt, "dataset", "PM",target[i],"new/",fname))
        pred_tmp[pd.isnull(pred_tmp)] = -9999
        tmp_cols = [t]+list(range(4,25))
        pred = pred_tmp.iloc[:,tmp_cols]
        del pred_tmp

        pred_cases = rf_model.predict(pred)
        pred_cases = np.exp(pred_cases)
        del pred

        name = f"{target[i]}_dataset_wtJP_noUTC_{test[t]}_"

        fname = f"rf_{name}_pred_ranger.csv"
        pd.DataFrame(pred_cases).to_csv(os.path.join(path_rtt, "RF/PM/",target[i],"new", fname),sep=",")
        del pred_cases

        t2=time.time()
        print(t2-t1)