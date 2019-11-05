
library(ranger) 
library(tictoc)
rm(list=ls(all=TRUE))

tic() 

target<-c("PM10","PM25")	## Enter the name of dataset (Please use file names with the unified prefix)
type<-c("conc","time","time_conc")
# pathname<-"//10.72.26.56/irisnas5/GEMS/PM/00_EA6km/RTT/"  # Nas5/GEMS
pathname<-"/share/irisnas5/GEMS/PM/00_EA6km/RTT/"  # Nas5/GEMS
setwd(pathname)

num_tree = 500

for (t in 2)
{
  for (i in 1) # Target type
  {
    
    for (yr in 2017)
    {
      if(yr==2016){
        days=366;
      }else{
        days=365;
      }
      
      for (doy in 1:days) #321-323 80
      {
        for (utc in 0:7)
        {
          tic() 
          try({
            data<-read.csv(file=paste(type[t],"/dataset/",target[i],"/",target[i],"_RTT_EA6km_",yr,"_",sprintf("%03d",doy),"_",sprintf("%02d",utc),".csv",sep="")) #For calibration 
            cal<-data[,c(1:24)]; 
            val<-data[data[,30] ==240,];
            val<-val[val[,29] ==0,c(1:24)];
            
            cal<-cal[cal[,24]>0, ]
            val<-val[val[,24]>0, ]
            
            cal[,24]<-log(cal[,24])
            val[,24]<-log(val[,24])
            
            pred<-read.csv(file=paste("/share/irisnas5/Data/EA_GOCI6km/cases_csv/",yr,"/cases_EA6km_",yr,"_",sprintf("%03d",doy),"_",sprintf("%02d",utc),".csv",sep=""))
            pred<-pred[,c(5:12,59,13:19,28:31,36:38)] #5:12,59,13:19,28:31,36:38
            pred[pred=="NaN"] <- -9999
            
            ## Make Random Forest model using ranger
            t1=Sys.time()
            if (i==1){
              rf_model = ranger(formula=PM10 ~., data=cal, num.trees = num_tree, importance = "permutation", write.forest = TRUE, scale.permutation.importance = TRUE, 
                                min.node.size = 5, replace = TRUE, splitrule = 'variance', num.threads = 8, save.memory = FALSE, verbose = TRUE)
            } else {
              rf_model = ranger(formula=PM25 ~., data=cal, num.trees = num_tree, importance = "permutation", write.forest = TRUE, scale.permutation.importance = TRUE, 
                                min.node.size = 5, replace = TRUE, splitrule = 'variance', num.threads = 8, save.memory = FALSE, verbose = TRUE)
            }
            
            
            
            t2=Sys.time()
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
            
            
            name<-paste(target[i],"_RTT_EA6km_",yr,"_",sprintf("%03d",doy),"_",sprintf("%02d",utc),sep="")
            
            # Prediction result
            pred_cases = predict(rf_model, data = pred)
            pred_cases<-exp(pred_cases$predictions)
            
            # save pred prediction
            write.table(pred_cases,paste(type[t],"/RF_pred/",target[i],"/rf_",name,".csv",sep=""),sep=",",append=FALSE)
            # print('Predicted prediction result is saved')
            
            # Validation result
            pred_val = predict(rf_model,data=val)
            pred_val<-exp(pred_val$predictions)
            
            # save vali prediction
            write.table(pred_val, paste(type[t],"/RF/",target[i],"/rf_",name,"_val.csv",sep=""),sep=",",append=FALSE)
            print('Predicted val result is saved')
            
            toc()
          }) # try
        }#utc
      } #doy
    } #year
  } #target
} #type

toc()


