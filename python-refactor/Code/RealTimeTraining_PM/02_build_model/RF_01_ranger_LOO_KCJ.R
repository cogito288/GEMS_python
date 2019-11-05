
library(ranger) 
library(tictoc)
rm(list=ls(all=TRUE))

tic() 

target<-c("PM10","PM25")	## Enter the name of dataset (Please use file names with the unified prefix)
type<-c("conc","time","time_conc","cloud")
# pathname<-"//10.72.26.56/irisnas5/GEMS/PM/"  # Nas5/GEMS
pathname<-"/share/irisnas5/GEMS/PM/"  # Nas5/GEMS
setwd(pathname)

num_tree = 500
for (t in 1)
{
  for (i in 1) # Target type
  {
    
    for (yr in 2015:2017)
    {
      if(yr==2015){
        days=365;
      }else{
        days=366;
      }
      
      for (doy in 1:days) #321-323 80
      {
        try({
          cal_list<- Sys.glob((paste("00_EA6km/LOO/",type[t],"/dataset/",target[i],"/",target[i],"_RTT_EA6km_",yr,"_",sprintf("%03d",doy),"*_LOO_*_cal.csv",sep="")))
          val_list<- Sys.glob((paste("00_EA6km/LOO/",type[t],"/dataset/",target[i],"/",target[i],"_RTT_EA6km_",yr,"_",sprintf("%03d",doy),"*_LOO_*_val.csv",sep="")))
          
          for (c in 1:length(cal_list))  #820 985
          {
            tic() 
            
            try({
              cal<-read.csv(file=(cal_list[c])) #For calibration 
              val<-read.csv(file=(val_list[c])) #For validation
              cal<-cal[cal[,24]>0, ]
              val<-val[val[,24]>0, ]
              cal[,24]<-log(cal[,24])
              val[,24]<-log(val[,24])
              
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
              
              if(t==3){
                name<-paste(substr(cal_list[c],37,70),sep="")
              }else if (t==4){
                name<-paste(substr(cal_list[c],33,66),sep="")
              }else{
                name<-paste(substr(cal_list[c],32,65),sep="")
              }
              
              # Validation result
              pred_val = predict(rf_model,data=val)
              pred_val<-exp(pred_val$predictions)
              
              # save vali prediction
              write.table(pred_val, paste("00_EA6km/LOO/",type[t],"/RF/",target[i],"/rf_",name,"_val_ranger.csv",sep=""),sep=",",append=FALSE)
              # print('Predicted val result is saved')
              
              
              toc()      
            },silent = TRUE)
          } # LOO_list
        },silent = TRUE)
      } # doy
    } #yr
  } # tatget
} #type
toc()


