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
#from thundergbm import TGBMClassifier
from sklearn.ensemble import RandomForestRegressor

#library(ranger) 
#library(tictoc)
#rm(list=ls(all=TRUE))

#tic() 

target = ["PM10", "PM25"] ## Enter the name of dataset (Please use file names with the unified prefix)
type_list = ["conc","time","time_conc"]

# pathname<-"//10.72.26.56/irisnas5/GEMS/PM/00_EA6km/RTT/"  # Nas5/GEMS
pathname = "/share/irisnas5/GEMS/PM/00_EA6km/RTT/"  # Nas5/GEMS
#setwd(pathname)

num_tree = 500
YEARS = [2017]
for t in [2]:
  for i in [1]: # Target type 
    for yr in YEARS:
      if(yr==2016):        days=366;
      else:                days=365;
      for doy in range(1, days+1):  #321-323 80
        for utc in range(7+1) : #0:7)
          try:
            fname = f"{target[i]}_RTT_EA6km_{yr}_{doy:03d}_{utc:02d}.csv"
            data = pd.read_csv(os.path.join(pathname, type[t], dataset, target[i], fname)) #For calibration 
            cols = data.columns
            cal = data[cols[:24]]
            val = data[data[29]==240]
            val = val[val[28]==0, cols[:24]]
            cal = cal[cal[23]>0]
            val = val[val[23]>0]
            cal.loc[:, 23] = np.log(cal[:, 23])
            val.loc[:, 23] = np.log(val[:, 23])
            
            #cal<-data[,c(1:24)]; 
            #val<-data[data[,30] ==240,];
            #val<-val[val[,29] ==0,c(1:24)];
            #cal<-cal[cal[,24]>0, ]
            #val<-val[val[,24]>0, ]
            #cal[,24]<-log(cal[,24])
            #val[,24]<-log(val[,24])
            
            fname = f"cases_EA6km_{yr}_{doy:03d}_{utc:02d}.csv"
            pred = pd.read_csv(os.path.join("share", "irisnas5", "Data", "EA_GOCI6km", "cases_csv", str(yr), fname))
            cols = pred.columns
            pred = pred[:,cols[4:12,58,12:19,27:31,35:38]] #5:12,59,13:19,28:31,36:38
            pred[pred=="NaN"] = -9999
            
            ## Make Random Forest model using ranger
            t1=time.time()
            if (i==1):
              params = {
                n_estimators=num_tree, 
                criterion:'mse',
                min_samples_leaf:5,
                n_jobs:8,
                verbose:2
              }
              rf_model = RandomForestRegressor(params)
              rm_model.fit(cal)
            else:
              rf_model = RandomForestRegressor(params)
              rf_model.fit(cal)
            t2=time.time()
            print(t2-t1)
            # importance(rf_model)
            # print('RF training is finished')
            
            # # save variable importance
            # write.table(importance(rf_model),paste("RF/PM/",target[i],"/rf_",name,"_imp_ranger_2.csv",sep=""),sep=",",append=FALSE)
            # 
            # save(rf_model, file=paste("RF/PM/",target[i],"/rf_",name,"_model_ranger.RData",sep=""))
            # print('RF model is saved')
            
            # # Make calibration result
            # pred_cal = predict(rf_model,data=cal)
            # pred_cal<-exp(pred_cal$predictions)
            
            # # save cali prediction
            # write.table(pred_cal, paste("RF/PM/",target[i],"/rf_",name,"_cal_ranger_2.csv",sep=""),sep=",",append=FALSE)
            # print('Predicted cal result is saved')
            
            
            name = f"{target[i]}_RTT_EA6km_{yr}_{doy:03d}_{utc:02d}"            
            # Prediction result
            pred_cases = rf_model.predict(pred) # predict(rf_model, data = pred)
            pred_cases = np.exp(pred_cases)
            
            # save pred prediction
            fname = f"rf_{name}.csv"
            pred_cases = pd.DataFrame(pred_cases)
            pred_cases.to_csv(os.path.join(pathname, type[t], "RF_pred",target[i], fname), sep=",")
            # print('Predicted prediction result is saved')
            
            # Validation result
            pred_val = rf_model.predict(val) #predict(rf_model,data=val)
            pred_val = np.exp(pred_val)
            
            # save vali prediction
            pred_val = pd.DataFrame(pred_val)
            fname = f"rf_{name}_val.csv"
            pred_val.to_csv(os.path.join(pathname, type[t],"/RF/",target[i],fname), sep=",")
            print('Predicted val result is saved')
     
          # try
        #utc
      #doy
    #year
  #target
#type
