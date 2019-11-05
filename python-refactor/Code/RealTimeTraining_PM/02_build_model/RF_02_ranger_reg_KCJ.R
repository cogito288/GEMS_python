
library(ranger) 
library(tictoc)
rm(list=ls(all=TRUE))

tic() 

target<-c("PM10","PM25")	## Enter the name of dataset (Please use file names with the unified prefix)
# pathname<-"//10.72.26.56/irisnas5/GEMS/PM/00_EA6km/offline/"  # Nas5/GEMS
pathname<-"/share/irisnas5/GEMS/PM/00_EA6km/offline/"  # Nas5/GEMS
setwd(pathname)

# num_tree = 500
for (i in 2)
{
  tic()
  # Read the data file
  cal<-read.csv(file=paste("dataset/",target[i],"/",target[i],"_dataset_cal.csv",sep="")) #For calibration
  val<-read.csv(file=paste("dataset/",target[i],"/",target[i],"_dataset_val.csv",sep="")) #For validation
  pred<-read.csv(file=paste("dataset/",target[i],"/",target[i],"_dataset_pred.csv",sep="")) #For prediction
  
  m<-nrow(cal)
  n<-ncol(cal)
  cal<-cal[cal[,n]>0, ]
  cal[n]<-log(cal[,n])
  plots<-as.data.frame(cal) #attach as data frame
  response_cal<-plots[,n]
  
  m_val<-nrow(val)
  val<-val[val[,n]>0, ]
  val[,n]<-log(val[n])
  plots_val<-as.data.frame(val) #attach as data frame
  response_val<-plots_val[,n]
  
  pred<-pred[pred[,n]>0,c(1:24)]
  pred[,n]<-log(pred[n])
  plots_pred<-as.data.frame(pred) #attach as data frame
  response_pred<-plots_pred[,n]
  
  
  accuracy <-matrix(0,nrow=1,ncol=4)
  max_accuracy <- 10000
  colnames(accuracy)<-c("mse_cal","rmse_cal","mse_val","rmse_val")
  
  print("Running model")
  t1=Sys.time()
  ss <- 0
  for (s in seq(1, 2, by=1)){ # num.random.splits
    
    ## Make Random Forest model using ranger
    t3=Sys.time()
    if (i==1){
      rf_model = ranger(formula=PM10 ~., data=plots, num.trees = 500, mtry=5, num.random.splits = s,
                        importance = "permutation", write.forest = TRUE, scale.permutation.importance = TRUE, 
                        min.node.size = 4, replace = TRUE, splitrule = 'variance', num.threads = 10, save.memory = FALSE, verbose = TRUE)
      
    } else {
      rf_model = ranger(formula=PM25 ~., data=plots, num.trees = 500, mtry=5, num.random.splits = s,
                        importance = "permutation", write.forest = TRUE, scale.permutation.importance = TRUE, 
                        min.node.size = 4, replace = TRUE, splitrule = 'variance', num.threads = 10, save.memory = FALSE, verbose = TRUE)
    }
    
    pred_cal = predict(rf_model,data=plots)
    pred_cal<-exp(pred_cal$predictions)
    diffvector<-c(1:m) #empty space for output
    diffvector<-(pred_cal-response_cal)#RMSD
    diffvector<-diffvector^2
    accuracy[1,1]<-sum(diffvector)/m #compute MSE
    accuracy[1,2]<-sqrt(sum(diffvector)/m) #compute RMSE
    accuracy[1,1]
    accuracy[1,2]
    
    
    pred_val = predict(rf_model,data=plots_val)
    pred_val<-exp(pred_val$predictions)
    diffvector<-c(1:m_val) #empty space for output
    diffvector<-(pred_val-response_val)#RMSD
    diffvector<-diffvector^2
    accuracy[1,3]<-sum(diffvector)/m_val #compute MSE
    accuracy[1,4]<-sqrt(sum(diffvector)/m_val) #compute RMSE
    accuracy[1,3] 
    accuracy[1,4]
    
    pred_pred = predict(rf_model,data=plots_pred)
    pred_pred<-exp(pred_pred$predictions)
   
    if (accuracy[1,4]<max_accuracy){
      max_accuracy <- accuracy[1,4]
      ss <- s
      
      importance(rf_model)
      
      
      name<-paste(target[i],"_dataset",sep="")
      
      # save variable importance
      write.table(importance(rf_model),paste("RF/",target[i],"/rf_",name,"_imp_ranger.csv",sep=""),sep=",",append=FALSE)
      
      save(rf_model, file=paste("RF/",target[i],"/rf_",name,"_model_ranger.RData",sep=""))
      print(paste0('RF model is saved with ',ss,' of num.random.splits'))
      parameter<-paste0('RF model is saved with ',ss,' of num.random.splits')
      
      write.table(parameter, paste("RF/",target[i],"/rf_",name,"_parameter_ranger.csv",sep=""),sep=",",append=FALSE)
      
      # save cali prediction
      write.table(pred_cal, paste("RF/",target[i],"/rf_",name,"_cal_ranger.csv",sep=""),sep=",",append=FALSE)
      # print('Predicted cal result is saved')
      
      # save vali prediction
      write.table(pred_val, paste("RF/",target[i],"/rf_",name,"_val_ranger.csv",sep=""),sep=",",append=FALSE)
      # print('Predicted val result is saved')
      
      # save prediction
      write.table(pred_pred, paste("RF/",target[i],"/rf_",name,"_pred_ranger.csv",sep=""),sep=",",append=FALSE)
      
      write.table(accuracy,paste("RF/",target[i],"/rf_",name,"_acc_ranger.csv",sep=""),sep=",",append=FALSE)
      
      
      rm(pred_cal, pred_val, parameter, rf_model)
      
      t4=Sys.time()
      print(t4-t3)
    }# if
  } # num.random.splits (s)
  
  
  rm(m, m_val)
  t2=Sys.time()
  print(t2-t1)

  rm(val, cal, pred, response_cal,response_val, response_pred, accuracy, n)
}#target

toc()


