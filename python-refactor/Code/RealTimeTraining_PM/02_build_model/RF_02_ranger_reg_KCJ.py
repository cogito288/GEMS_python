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
import pickle


#3library(ranger) 
#library(tictoc)
#rm(list=ls(all=TRUE))

target = ["PM10", "PM25"] ## Enter the name of dataset (Please use file names with the unified prefix)
# pathname<-"//10.72.26.56/irisnas5/GEMS/PM/00_EA6km/offline/"  # Nas5/GEMS
pathname<-"/share/irisnas5/GEMS/PM/00_EA6km/offline/"  # Nas5/GEMS
#setwd(pathname)

# num_tree = 500
for i in [2]:
  # Read the data file
  cal = pd.read_csv(os.path.join(pathname, "dataset/",target[i],f"{target[i]}_dataset_cal.csv")) #For calibration
  val = pd.read_csv(os.path.join(pathname, "dataset/",target[i], f"{target[i]}_dataset_val.csv")) #For validation
  pred = pd.read_csv(os.path.join(pathname, "dataset/",target[i],f"{target[i]}_dataset_pred.csv")) #For prediction
  
  m = cal.shape[0]
  n = cal.shape[1]
  cal = cal[cal[n]>0]
  cal.loc[:, n] = np.log(cal[:,n])
  plots = pd.DataFrame(cal) #<-as.data.frame(cal) #attach as data frame
  response_cal = plots.loc[:,n]
  
  m_val = val.shape[0] #nrow(val)
  val = val[val.loc[:,n]>0]
  val.loc[:,n] = np.log(val[n])
  plots_val = pd.DataFrame(val) #as.data.frame(val) #attach as data frame
  response_val = plots_val[:,n]
  
  cols = pred.columns
  pred = pred[pred.loc[:,n]>0,cols[:24]]
  pred.loc[:,n] = np.log(pred[n])
  plots_pred = pd.DataFrame(pred) #as.data.frame(pred) #attach as data frame
  response_pred = plots_pred.loc[:,n]
  
  
  accuracy = np.zeros((1, 4)) #pd.DataFrame(columns=["mse_cal","rmse_cal","mse_val","rmse_val"]) # #matrix(0,nrow=1,ncol=4)
  max_accuracy = 10000
  
  print("Running model")
  t1=time.time() #Sys.time()
  ss = 0
  for s in range(1, 2+1): #seq(1, 2, by=1)){ # num.random.splits
    
    ## Make Random Forest model using ranger
    t3=time.time() #Sys.time()
    params = {
        n_estimators = 500,
        criterion:'mse',
        n_jobs=10,
        min_samples_leaf:4,
        verbose:2,        
      }
    if (i==1):
      rf_model = RandomForestRegressor(params)
      rm_model.fit(plots) 
    else:
      rf_model = RandomForestRegressor(params)
      rm_model.fit(plots) 
    
    pred_cal = rf_model.predict(plots)
    pred_cal= np.exp(pred_cal)
    diffvector = list(range(1,m+1)) #c(1:m) #empty space for output
    diffvector = pred_cal-response_cal#RMSD
    diffvector = diffvector**2
    accuracy[0,0]= np.sum(diffvector)/m #compute MSE
    accuracy[0,1] = np.sqrt(np.sum(diffvector)/m) #compute RMSE
    print (accuracy[0,0])
    print (accuracy[0,1])
    
    
    pred_val = predict(rf_model,data=plots_val)
    pred_val<-exp(pred_val$predictions)
    diffvector<-c(1:m_val) #empty space for output
    diffvector<-(pred_val-response_val)#RMSD
    diffvector<-diffvector^2
    accuracy[1,3]<-sum(diffvector)/m_val #compute MSE
    accuracy[1,4]<-sqrt(sum(diffvector)/m_val) #compute RMSE
    accuracy[1,3] 
    accuracy[1,4]
    
    pred_pred = rf_model.predict(plots_pred)
    pred_pred = np.exp(pred_pred)
   
    if (accuracy[0,3]<max_accuracy):
      max_accuracy = accuracy[0,3]
      ss = s
      print (rf_model.feature_importances_)
      #importance(rf_model)
      name = f"{target[i]}_dataset"
      
      # save variable importance
      feature_imp = pd.Series(rf_model.feature_importances_).sort_values(ascending=False)
      fname = f"{rf_{name}_imp_ranger.csv"
      feature_imp.to_csv(os.path.join(pathname, "RF/",target[i],fname),sep=",")
      
      fname = f"rf_{name}_model_ranger.RData"
      with open(os.path.join(pathname, "RF", target[i], fname), 'wb') as f:
        pickle.dump(rf_model, f)
      print(f'RF model is saved with {ss} of num.random.splits')
      parameter = f'RF model is saved with {ss} of num.random.splits'
      
      pd.DataFrame(parameter).to_csv(os.path.join(pathname, "RF/",target[i],f"/rf_{name}_parameter_ranger.csv"), sep=",")
      
      # save cali prediction
      pd.DataFrmae(pred_cal).to_csv(os.path.join(pathname, "RF/",target[i],f"/rf_{name}_cal_ranger.csv"),sep=",")
      # print('Predicted cal result is saved')
      
      # save vali prediction
      pd.DataFrame(pred_val).to_csv(os.path.join(pathname, "RF/",target[i],f"/rf_{name}_val_ranger.csv"),sep=",")
      # print('Predicted val result is saved')
      
      # save prediction
      pd.DataFrame(pred_pred).to_csv(os.path.join(pathname, "RF/",target[i],f"/rf_{name}_pred_ranger.csv"),sep=",")
      
      pd.DataFrame(accuracy).to_csv(os.path.join(pathname, "RF/",target[i],f"/rf_{name}_acc_ranger.csv"),sep=",")
      del pred_cal, pred_val, parameter, rf_model
      #rm(pred_cal, pred_val, parameter, rf_model)
      
      t4=time.time()
      print(t4-t3)
    # if
  # num.random.splits (s)
  del m, m_val
  #rm(m, m_val)
  t2=time.time()
  print(t2-t1)

  del val, cal, pred, response_cal,response_val, response_pred, accuracy, n
#target

