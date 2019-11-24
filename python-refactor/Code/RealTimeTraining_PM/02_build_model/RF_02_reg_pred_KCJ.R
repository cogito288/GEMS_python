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
import pickle
#from thundergbm import TGBMClassifier
from sklearn.ensemble import RandomForestRegressor

# load libraries
#library(ranger)
#library(tictoc)
#rm(list=ls(all=TRUE))

target = ["PM10", "PM25"] ## Enter the name of dataset (Please use file names with the unified prefix)
test = ["AOD_GOCI_V1","AOD_AERONET_V1","AOD_AERONET_V2","GOCI_AOD"]
# pathname<-"//10.72.26.56/irisnas5/GEMS/Cloud/"  # Nas5/GEMS
pathname = "/share/irisnas5/GEMS/Cloud/"  # Nas5/GEMS
#setwd(pathname)


for i in [2]:  
  for t in [3]:  ## Target type
    t1=time.time()
    fname = f"rf_{target[i]}_dataset_wtJP_noUTC_{test[t]}_model_ranger.RData"
    rf_model = pickle.load(os.path.join(pathname, "RF/PM/",target[i],"/new", fname)) ## when load models
    fname = f"{target[i]}_dataset_pred_wtJP.csv"
    pred_tmp = pd.read_csv(os.path.join(pathname, "dataset/PM/",target[i],"/new/",fname))
    pred_tmp[pred_tmp=="NaN"] = -9999
    pred = pred_tmp.loc[:,[t,4:25]]
    
    del pred_tmp
    
    pred_cases = rf_model.predict(pred)
    pred_cases = np.exp(pred_cases)
    
    del pred
    
    name = f"{target[i]}_dataset_wtJP_noUTC_{test[t]}_"
 
    fname = f"rf_{name}_pred_ranger.csv"
    pred_cases.to_csv(os.path.join(pathname, "RF/PM/",target[i],"/new", fname),sep=",")
    
    del pred_cases
    
    t2=time.time()
    print(t2-t1)
    
  # i_target
#t_test

