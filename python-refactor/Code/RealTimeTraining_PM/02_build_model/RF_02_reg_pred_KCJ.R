
# load libraries
library(ranger)
library(tictoc)
rm(list=ls(all=TRUE))

tic() 

target<-c("PM10","PM25")	## Enter the name of dataset (Please use file names with the unified prefix)
test<-c("AOD_GOCI_V1","AOD_AERONET_V1","AOD_AERONET_V2","GOCI_AOD")
# pathname<-"//10.72.26.56/irisnas5/GEMS/Cloud/"  # Nas5/GEMS
pathname<-"/share/irisnas5/GEMS/Cloud/"  # Nas5/GEMS
setwd(pathname)


for (i in 2)  
{
  tic()
  for (t in 3)  ## Target type
  {
    t1=Sys.time()
    
    load(paste("RF/PM/",target[i],"/new/rf_",target[i],"_dataset_wtJP_noUTC_",test[t],"_model_ranger.RData",sep="")) ## when load models
    
    
    pred_tmp<-read.csv(file=paste("dataset/PM/",target[i],"/new/",target[i],"_dataset_pred_wtJP.csv",sep=""))
    pred_tmp[pred_tmp=="NaN"] <- -9999
    pred<-pred_tmp[,c(t,5:25)]
    
    rm(pred_tmp)
    
    pred_cases = predict(rf_model,data=pred)
    pred_cases<-exp(pred_cases$predictions)
    
    rm(pred)
    
    name<-paste(target[i],"_dataset_wtJP_noUTC_",test[t],"_",sep="")
    
    write.table(pred_cases,paste("RF/PM/",target[i],"/new/rf_",name,"_pred_ranger.csv",sep=""),sep=",",append=FALSE)
    
    rm(pred_cases)
    
    
    t2=Sys.time()
    print(t2-t1)
    
  } # i_target
  toc()
} #t_test



