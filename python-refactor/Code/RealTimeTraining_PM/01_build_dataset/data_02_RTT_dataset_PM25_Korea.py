 , close all


# path_nas4 = '//10.72.26.54/irisnas4/Data/Aerosol_Work/'
# path_nas6 = '/10.72.26.46/irisnas6/Data/Aerosol/'
# addpath('/10.72.26.46/irisnas2/Work/Aerosol/matlab_func/')

path_nas4 = '/share/irisnas4/Data/Aerosol_Work/'
path_nas6 = '/share/irisnas6/Data/Aerosol/'
addpath('/share/irisnas6/Work/Aerosol/matlab_func/')

## Station index
matlab.loadmat(os.path.join(path_nas6,'grid/grid_korea.mat'])
matlab.loadmat(os.path.join(path_nas6,'Station_Korea/stn_1km_location_weight.mat'])

## Read data
target = {'PM10','PM25'}
# cd([path_nas4,'cases/RTT/'])

i=2 #1:2 # target  ########################################
header = {'NDVI','AOD','AE','FMF','SSA','RSDN','Precip','DEM','LC_ratio', # satellite data(9)
    'Temp','Dew','RH','P_srf','MaxWS','PBLH','Visibility', # numerical data(RDAPS)(16)
    'stack1_np.maxWS','stack3_np.maxWS','stack5_np.maxWS','stack7_np.maxWS', # stacked np.maxWS(20)
    'DOY','PopDens','RoadDens'} #, etc data(24)
nvar = 23
if i==1
    header2 = [header,{'PM10','stn_num','doy_num','time','yr','ovr','k_ind'}]
else
    header2 = [header,{'PM25','stn_num','doy_num','time','yr','ovr','k_ind'}]


data_stn=[]
high=[] low=[]
for yr = 2015:2016
    if yr%4==0
        days = 366
    else
        days = 365
    
    matlab.loadmat(os.path.join(path_nas6,'Station_Korea/Station_1km_rm_outlier_',str(yr),'_weight.mat'])
    stn = stn_1km_yr
    
    for doy = 1:days
        if doy <=30 && yr == 2015            
            for utc = 0:7
                matlab.loadmat(os.path.join(path_nas4, 'cases/RTT_mat/cases_RTT_',
                    str(yr),'_',str(doy, '#03i'),'_',str(utc,'#02i'),'.mat']) # data
                data = data(:,[1:21,23:24])
                data((data(:,)==65535),) = -9999
                
                # Load station data
                stn_1km = stn(stn(:,1) == doy & stn(:,2) ==yr & stn(:,5)== utc+9 ,:)                
                
                stn_idx = matlab.ismember(stn_1km_location(:,2), stn_1km(:,13))
                stn_conc = stn_1km(:,[11,13,1,5,2]) # PM2.5, stn_num, doy_num,time,yr
                stn_conc(:,6)=0# PM2.5, stn_num, doy_num,time,yr, ovr
                stn_conc(:,7) =stn_1km_location(stn_idx,5)# PM2.5, stn_num, doy_num,time,yr, ovr, stn_location
                
                data_1 = stn_conc(stn_conc(:,1)<=50,:)            # (x1)
                data_2 = stn_conc(stn_conc(:,1)>50 & stn_conc(:,1)<=80,:)  # (x3)
                data_3 = stn_conc(stn_conc(:,1)>80,:)  # (x5)

                ndata_2 = oversampling_sh(data_2(:,1:6),stn_1km_location,size(lon_kor,1),size(lon_kor,2),2)
                ndata_3 = oversampling_sh(data_3(:,1:6),stn_1km_location,size(lon_kor,1),size(lon_kor,2),4)
                
                ndata = [data_1ndata_2ndata_3]
                clearvars data_1 data_2 data_3  ndata_2 ndata_3 
                
                # remove station pixel among oversampled pixels
                # ndata = [stn_conc, stn_num, doy_num, stn_ind, stn_x, stn_y, over]
                dup_idx = matlab.ismember(ndata(:,7),stn_1km_location(:,5))
                dup_idx = dup_idx .* ndata(:,6) #oversampling col
                ndata = ndata(dup_idx==0,:)
                
                # Extract input variables at station points & oversampling points
                data_tmp = data(ndata(:,7),:)
                #  data_tmp = cases(ndata(:,7),[1:2,4:])
                
                data_tmp(:,nvar+1:nvar+6) = ndata(:,(1:6)) # data. stn_PM, stn_num, doy_num, time, yr, ovr
                k=((doy-1)*8)+(utc+1)
                data_tmp(:,nvar+7) = k #k_idx
                
                data_tmp(data_tmp==-9999)np.nan
                data_tmp = rmmissing(data_tmp,1)
                
                data_stn = [data_stn data_tmp]
                print (utc)
                                
            
            print (doy)
            if doy >= 30 & utc == 7
                
                csvwrite_with_headers2([path_nas4,'dataset/',target{i},'/new/',target{i},'_RTT_',
                    str(yr),'_',str(doy,'#03i'),'_',str(utc,'#02i'),'.csv'],data_stn,header2,0,0,'#7.7f')

                print (doy)
            
        else       
            for utc=0:7
                k=240               
                
                # 고농도 남기기
                extra_samples = data_stn(data_stn(:,)==1,:)
                if i==1
                    high_tmp = extra_samples(extra_samples(:,24)>=150,:)
                    low_tmp = extra_samples(extra_samples(:,24)<=60,:)
                else
                    high_tmp = extra_samples(extra_samples(:,24)>=80,:)
                    low_tmp = extra_samples(extra_samples(:,24)<=30,:)
                      
                
                if np.all(high_tmp)==1
                    high = high
                else                    
                    high = [high high_tmp]  high(:,) = high(:,)+1
                    high_uniq = np.unique(high(:,1:29),'rows','stable') high_uniq(:,+1)=2
                    high = high_uniq
                
                
                if np.all(low_tmp)==1
                    low = low
                else
                    low = [low low_tmp]  low(:,) = low(:,)+1                    
                    low_uniq = np.unique(low(:,1:29),'rows','stable') low_uniq(:,+1)=2
                    low = low_uniq
                
                
#                 matlab.savemat(os.path.join(path_nas4, 'dataset/',target{i},'/variable_test/extra_samples/',target{i},'_high_',
#                     str(yr),'_',str(doy, '#03i'),'_',str(utc, '#02i'),'.mat'],'high')
#                 matlab.savemat(os.path.join(path_nas4, 'dataset/',target{i},'/variable_test/extra_samples/',target{i},'_low_',
#                     str(yr),'_',str(doy, '#03i'),'_',str(utc, '#02i'),'.mat'],'low')                 
                
                data_stn = data_stn(data_stn(:,)>=2,:)
                high_tmp(:,) = high_tmp(:,)+1
                low_tmp(:,) = low_tmp(:,)+1
                data_stn = [low_tmp high_tmp data_stn]
                data_stn(:,) = data_stn(:,)-1
                
                matlab.loadmat(os.path.join(path_nas4, 'cases/RTT_mat/cases_RTT_',
                    str(yr),'_',str(doy, '#03i'),'_',str(utc,'#02i'),'.mat']) # data
                data = data(:,[1:21,23:24])
                data((data(:,)==65535),) = -9999              
                
                # Load station data
                stn_1km = stn(stn(:,1) == doy & stn(:,2) ==yr & stn(:,5)== utc+9 ,:)                
                
                stn_idx = matlab.ismember(stn_1km_location(:,2), stn_1km(:,13))
                stn_conc = stn_1km(:,[11,13,1,5,2]) # PM2.5, stn_num, doy_num,time,yr
                stn_conc(:,6)=0# PM2.5, stn_num, doy_num,time,yr, ovr
                stn_conc(:,7) =stn_1km_location(stn_idx,5)# PM2.5, stn_num, doy_num,time,yr, ovr, stn_location
                
                data_1 = stn_conc(stn_conc(:,1)<=50,:)            # (x1)
                data_2 = stn_conc(stn_conc(:,1)>50 & stn_conc(:,1)<=80,:)  # (x3)
                data_3 = stn_conc(stn_conc(:,1)>80,:)  # (x5)

                ndata_2 = oversampling_sh(data_2(:,1:6),stn_1km_location,size(lon_kor,1),size(lon_kor,2),2)
                ndata_3 = oversampling_sh(data_3(:,1:6),stn_1km_location,size(lon_kor,1),size(lon_kor,2),4)
                
                ndata = [data_1data_2data_3ndata_2ndata_3]
                clearvars data_1 data_2 data_3  ndata_2 ndata_3 
                
                # remove station pixel among oversampled pixels
                # ndata = [stn_conc, stn_num, doy_num, stn_ind, stn_x, stn_y, over]
                dup_idx = matlab.ismember(ndata(:,7),stn_1km_location(:,5))
                dup_idx = dup_idx .* ndata(:,6) #oversampling col
                ndata = ndata(dup_idx==0,:)
                
                # Extract input variables at station points & oversampling points
                data_tmp = data(ndata(:,7),:)
                #  data_tmp = cases(ndata(:,7),[1:2,4:])
                
                data_tmp(:,nvar+1:nvar+6) = ndata(:,(1:6)) # data. stn_PM, stn_num, doy_num, time, yr, ovr
                data_tmp(:,nvar+7) = k #k_idx
                
                data_tmp(data_tmp==-9999)np.nan
                data_tmp = rmmissing(data_tmp,1)                
                data_tmp(data_tmp(:,24)>200,:) =[]
                
                data_stn = [data_stn data_tmp]

                
                high_rate_pre = size(data_stn(data_stn(:,24)>=80,:),1)/size(data_stn(:,24),1) *100
                low_rate_pre = size(data_stn(data_stn(:,24)<=30,:),1)/size(data_stn(:,24),1) *100
                
                if high_rate_pre<30 & low_rate_pre<30 & size(data_stn(:,)>1,1)>1000
                    print (('num of samples = #4.0f \n remove the oversampled samples in the new dataset \n',size(data_stn,1))
                    data_stn(data_stn(:,-1)==1 & data_stn(:,)==240 & data_stn(:,24)<80,:) = []
                
                
                high_rate_pre = size(data_stn(data_stn(:,24)>=80,:),1)/size(data_stn(:,24),1) *100
                low_rate_pre = size(data_stn(data_stn(:,24)<=30,:),1)/size(data_stn(:,24),1) *100
                
            # 샘플 조정 part1
                if high_rate_pre>30
                    print (('high_rate_pre = #3.2f & remove the stacked samples \n',high_rate_pre)
                    data_stn(data_stn(:,)==240 & data_stn(:,-1)==1,:)=[]
                
                
                if low_rate_pre>30                    
                    print (('low_rate_pre = #3.2f & remove stacked samples \n',low_rate_pre)
                    data_stn(data_stn(:,24)<=30 & data_stn(:,) ==2,:) = []
                
            
                
                high_rate = size(data_stn(data_stn(:,24)>=80,:),1)/size(data_stn(:,24),1) *100
                low_rate = size(data_stn(data_stn(:,24)<=30,:),1)/size(data_stn(:,24),1) *100
            
            # 샘플 조정
                if high_rate<30 &low_rate>30
                    print (('high_rate = #3.2f & stack more \n',high_rate)
                    print (('low_rate = #3.2f & remove stacked samples \n',low_rate)
                # 저농도 지우기
                   if np.all(low)==0
                       idx_low = np.where(data_stn(:,26) <= low(,26) & data_stn(:,24)<=30 & data_stn(:,)==1)
                       data_stn(idx_low,:) = []
                   
                    
                elif high_rate<30 & low_rate<30
                    print (('high_rate = #3.2f & stack more \n',high_rate)
                    print (('low_rate = #3.2f & stack more \n',low_rate)
                    
                elif high_rate>30 &low_rate<30
                    print (('high_rate = #3.2f & remove the stacked samples \n',high_rate)
                    print (('low_rate = #3.2f & stack more \n',low_rate)
               # 고농도
                   if np.all(high)==0
                    idx_high = np.where(data_stn(:,26) <= high(,26) & data_stn(:,24)>=80 & data_stn(:,)==1)
                       data_stn(idx_high,:) = []
                   
                elif high_rate>30 & low_rate>30
                    print (('high_rate = #3.2f \n',high_rate)
                    print (('low_rate = #3.2f \n',low_rate)
                # 고농도 지우기
                    idx_high = np.where(data_stn(:,26) <= high(,26) & data_stn(:,24)>=80 & data_stn(:,)==1)
                    data_stn(idx_high,:) = []
                # 저농도 지우기
                    idx_low = np.where(data_stn(:,26)<= low(,26) & data_stn(:,24)<=30 & data_stn(:,)==1)
                    data_stn(idx_low,:) = []
                    
                    
                # sample수 줄이는 코드 추가필요 전체적인 갯수줄이기
                # data_stn(:,)==1 인 날에대해서 줄이기         
                                 
                
                print (utc)
                csvwrite_with_headers2([path_nas4,'dataset/',target{i},'/new/',target{i},'_RTT_',
                    str(yr),'_',str(doy,'#03i'),'_',str(utc,'#02i'),'.csv'],data_stn,header2,0,0,'#7.7f')
            
            print (doy)
        
    
    print (yr)




