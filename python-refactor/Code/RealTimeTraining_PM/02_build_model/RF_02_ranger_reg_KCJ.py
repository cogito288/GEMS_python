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
import pickle

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km')
path_rtt = os.path.join(path_ea_goci, 'RTT')
path_roo = os.path.join(path_ea_goci, 'LOO')

target = ["PM10", "PM25"] ## Enter the name of dataset (Please use file names with the unified prefix)

# num_tree = 500
for i in [0]:
    # Read the data file
    cal = pd.read_csv(os.path.join(path_rtt, "dataset/",target[i],f"{target[i]}_dataset_cal.csv")) #For calibration
    val = pd.read_csv(os.path.join(path_rtt, "dataset/",target[i], f"{target[i]}_dataset_val.csv")) #For validation
    pred = pd.read_csv(os.path.join(path_rtt, "dataset/",target[i],f"{target[i]}_dataset_pred.csv")) #For prediction

    m = cal.shape[0]
    cal = cal.loc[cal.iloc[:, -1]>0, :]
    cal.iloc[:, -1] = np.log(cal.iloc[:, -1])
    plots = pd.DataFrame(cal) #<-as.data.frame(cal) #attach as data frame
    response_cal = plots.iloc[:, -1]

    m_val = val.shape[0] #nrow(val)
    val = val.loc[val.iloc[:,-1]>0]
    val.iloc[:,-1] = np.log(val.iloc[:, -1])
    plots_val = pd.DataFrame(val) #as.data.frame(val) #attach as data frame
    response_val = plots_val.iloc[:,-1]

    cols = pred.columns
    pred = pred.loc[pred.iloc[:,-1]>0,cols[:24]]
    pred.iloc[:,-1] = np.log(pred.iloc[-1])
    plots_pred = pd.DataFrame(pred) #as.data.frame(pred) #attach as data frame
    response_pred = plots_pred.iloc[:,-1]


    accuracy = np.zeros((1, 4)) #pd.DataFrame(columns=["mse_cal","rmse_cal","mse_val","rmse_val"]) # #matrix(0,nrow=1,ncol=4)
    max_accuracy = 10000

    print("Running model")
    t1=time.time() #Sys.time()
    ss = 0
    for s in range(1, 2+1): #seq(1, 2, by=1)){ # num.random.splits
        ## Make Random Forest model using ranger
        t3=time.time() #Sys.time()
        params = {
            'n_estimators': 500,
            'criterion':'mse',
            'n_jobs':10,
            'min_samples_leaf':4,
            'verbose':2,        
          }
        features = list(plots.columns)
        features.remove(target[i])
        
        rf_model = RandomForestRegressor(**params)
        rf_model.fit(plots[features], plots[target[i]]) 
        
        pred_cal = rf_model.predict(plots[features])
        pred_cal= np.exp(pred_cal)
        #diffvector = list(range(1,m+1)) #c(1:m) #empty space for output
        diffvector = pred_cal-response_cal #RMSD
        diffvector = diffvector**2
        accuracy[0,0]= np.sum(diffvector)/m #compute MSE
        accuracy[0,1] = np.sqrt(np.sum(diffvector)/m) #compute RMSE
        print (accuracy[0,0])
        print (accuracy[0,1])


        pred_val = rf_model.predict(plots_val[features])
        pred_val = np.exp(pred_val)
        #diffvector<-c(1:m_val) #empty space for output
        diffvector = (pred_val-response_val)#RMSD
        diffvector = diffvector**2
        accuracy[0,2]= np.sum(diffvector)/m_val #compute MSE
        accuracy[0,3] = np.sqrt(np.sum(diffvector)/m_val) #compute RMSE
        print (accuracy[0,0])
        print (accuracy[0,1])

        pred_pred = rf_model.predict(plots_pred[features])
        pred_pred = np.exp(pred_pred)

        if (accuracy[0,3]<max_accuracy):
            max_accuracy = accuracy[0,3]
            ss = s
            print (rf_model.feature_importances_)
            name = f"{target[i]}_dataset"

            # save variable importance
            feature_imp = pd.Series(rf_model.feature_importances_).sort_values(ascending=False)
            fname = f"rf_{name}_imp_ranger.csv"
            matlab.check_make_dir(os.path.join(path_rtt, "RF/",target[i]))
            feature_imp.to_csv(os.path.join(path_rtt, "RF/",target[i],fname),sep=",")

            fname = f"rf_{name}_model_ranger.pickle"
            with open(os.path.join(path_rtt, "RF", target[i], fname), 'wb') as f:
                pickle.dump(rf_model, f)
            print(f'RF model is saved with {ss} of num.random.splits')
            parameter = rf_model.get_params() #f'RF model is saved with {ss} of num.random.splits'

            pd.DataFrame(parameter).to_csv(os.path.join(path_rtt, "RF/",target[i],f"rf_{name}_parameter_ranger.csv"), sep=",")

            # save cali prediction
            pd.DataFrmae(pred_cal).to_csv(os.path.join(path_rtt, "RF/",target[i],f"rf_{name}_cal_ranger.csv"),sep=",")
            # print('Predicted cal result is saved')

            # save vali prediction
            pd.DataFrame(pred_val).to_csv(os.path.join(path_rtt, "RF/",target[i],f"rf_{name}_val_ranger.csv"),sep=",")
            # print('Predicted val result is saved')

            # save prediction
            pd.DataFrame(pred_pred).to_csv(os.path.join(path_rtt, "RF/",target[i],f"rf_{name}_pred_ranger.csv"),sep=",")

            pd.DataFrame(accuracy).to_csv(os.path.join(path_rtt, "RF/",target[i],f"rf_{name}_acc_ranger.csv"),sep=",")
            del pred_cal, pred_val, parameter, rf_model

            t4=time.time()
            print(t4-t3)
        
        del m, m_val
        t2=time.time()
        print(t2-t1)

        del val, cal, pred, response_cal,response_val, response_pred, accuracy, n
        #target