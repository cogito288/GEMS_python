 , close all

# path_data = '//10.72.26.56/irisnas5/Data/'
# path_save = '//10.72.26.56/irisnas5/GEMS/PM/00_EA6km/RTT/'
# addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'))

path_data = '/share/irisnas5/Data/'
path_save = '/share/irisnas5/GEMS/PM/00_EA6km/RTT/'
addpath(genpath('/share/irisnas5/Data/matlab_func/'))

# path_data = '/Volumes/irisnas5/Data/'
# path_save = '/Volumes/irisnas5/GEMS/PM/00_EA6km/RTT/'
# addpath(genpath('/Volumes/irisnas5/Data/matlab_func/'))

## Station index
matlab.loadmat(os.path.join(path_data,'grid/grid_goci.mat'])
matlab.loadmat(os.path.join(path_data,'Station/Station_CN/cn_stn_GOCI6km_location_weight.mat'])
matlab.loadmat(os.path.join(path_data,'Station/Station_Korea/stn_GOCI6km_location_weight_v2018.mat'])
matlab.loadmat(os.path.join(path_data,'Station/Station_JP/jp_stn_GOCI6km_location_weight.mat'])
stn_6km_location = [stn_GOCI6km_location jp_stn_GOCI6km_location cn_stn_GOCI6km_location]
cn_dup_scode2_GOCI6km(:,+1:size(jp_dup_scode2_GOCI6km,2))=0
dup_scode2_GOCI6km(:,+1:size(jp_dup_scode2_GOCI6km,2))=0
dup_scode2_6km =[dup_scode2_GOCI6km cn_dup_scode2_GOCI6km jp_dup_scode2_GOCI6km]

clear stn_GOCI6km_location cn_stn_GOCI6km_location jp_stn_GOCI6km_location cn_dup_scode2_GOCI6km dup_scode2_GOCI6km jp_dup_scode2_GOCI6km header_cn_stn_GOCI6km_location header_jp_stn_GOCI6km_location

## header

header = {'AOD','AE','FMF','SSA','NDVI','RSDN','Precip','DEM','LCurban', # satellite data(9)
    'Temp','Dew','RH','P_srf','MaxWS','PBLH','Visibility', # numerical data(RDAPS)(16)
    'stack1_np.maxWS','stack3_np.maxWS','stack5_np.maxWS','stack7_np.maxWS', # stacked np.maxWS(20)
    'DOY','PopDens','RoadDens'} #, etc data(23)    
header2 = [header, {'PM10','stn_num','doy_num','time','yr','ovr','k_ind'}]

nvar = 23

## Read data
data_stn=[]
high=[] low=[]
for yr = 2015:2017
    if yr%4==0
        days = 366
    else
        days = 365
    
    matlab.loadmat(os.path.join(path_data,'Station/Station_Korea/Station_GOCI6km_',str(yr),'_weight.mat'])
    matlab.loadmat(os.path.join(path_data,'Station/Station_CN/cn_Station_GOCI6km_rm_outlier_',str(yr),'_weight.mat'])
    if yr < 2017
        matlab.loadmat(os.path.join(path_data,'Station/Station_JP/jp_Station_GOCI6km_',str(yr),'_weight.mat'])
    else        
        matlab.loadmat(os.path.join(path_data,'Station/Station_JP/jp_Station_GOCI6km_rm_outlier_',str(yr),'_weight.mat'])
    
    jp_stn_GOCI6km_yr = jp_stn_GOCI6km_yr(jp_stn_GOCI6km_yr(:,5)>=9 &jp_stn_GOCI6km_yr(:,5)<=16,1:13)
    stn_GOCI6km_yr = stn_GOCI6km_yr(stn_GOCI6km_yr(:,5)>=9 &stn_GOCI6km_yr(:,5)<=16,:)
    stn_GOCI6km_yr(:,5)=stn_GOCI6km_yr(:,5)-9 jp_stn_GOCI6km_yr(:,5)=jp_stn_GOCI6km_yr(:,5)-9 cn_stn_GOCI6km_yr(:,5)=cn_stn_GOCI6km_yr(:,5)-8
    stn= [stn_GOCI6km_yr jp_stn_GOCI6km_yr cn_stn_GOCI6km_yr(:,[1:5,11,19,15,13,9,7,21:22])]
    
    clear stn_GOCI6km_yr jp_stn_GOCI6km_yr cn_stn_GOCI6km_yr

    for doy = 1:days
        if np.all(data_stn)==1
        elif size(data_stn(data_stn(:,29)==1,:),1)>1
            rmovr = datasample(data_stn(data_stn(:,-1)==1,:), round(size(data_stn(data_stn(:,-1)==1,:),1)*0.9),'Replace',false)
            data_stn(data_stn(:,-1)==1,:)=[]
            data_stn=[data_stn rmovr]
        else
            data_stn(data_stn(:,-1)==1,:)=[]
        
        if doy <=30 && yr == 2015
            for utc = 0:7
                if np.all(data_stn)==1
                elif size(data_stn(data_stn(:,29)==1,:),1)>1
                    rmovr = datasample(data_stn(data_stn(:,-1)==1,:), round(size(data_stn(data_stn(:,-1)==1,:),1)*0.99),'Replace',false)
                    data_stn(data_stn(:,-1)==1,:)=[]
                    data_stn=[data_stn rmovr]
                else                    
                    data_stn(data_stn(:,-1)==1,:)=[]
                
                matlab.loadmat(os.path.join(path_data, 'EA_GOCI6km/cases_mat/',str(yr),'/cases_EA6km_',str(yr),'_',
                    str(doy, '#03i'),'_',str(utc,'#02i'),'.mat']) # data_tbl
                data = data_tbl(:,header) 
                data = table2array(data)                
                clear data_tbl
                                
                # Load station data
                stn_6km = stn(stn(:,1) == doy & stn(:,2) ==yr & stn(:,5)== utc,:)
                
                if np.all(stn_6km)==0 # no observation data in some utc
                    stn_idx = matlab.ismember(stn_6km_location(:,2), stn_6km(:,13))
                    stn_conc = stn_6km(:,[10,13,1,5,2]) # PM10, stn_num, doy_num,time,yr
                    stn_conc(:,6)=0# PM10, stn_num, doy_num,time,yr, ovr
                    stn_conc(:,7) =stn_6km_location(stn_idx,5)# PM10, stn_num, doy_num,time,yr, ovr, stn_location
                   
                    data_1 = stn_conc(stn_conc(:,1)<=20,:)            # (x0.03)
                    data_2 = stn_conc(stn_conc(:,1)>20 & stn_conc(:,1)<=40,:) # (x0.07)
                    data_3 = stn_conc(stn_conc(:,1)>40 & stn_conc(:,1)<=60,:) # (x0.1)
                    data_4 = stn_conc(stn_conc(:,1)>60 & stn_conc(:,1)<=80,:)  # (x0.2)
                    data_5 = stn_conc(stn_conc(:,1)>80 & stn_conc(:,1)<=100,:)  # (x0.4)
                    data_6 = stn_conc(stn_conc(:,1)>100 & stn_conc(:,1)<=120,:)  # (x0.6)
                    data_7 = stn_conc(stn_conc(:,1)>120 & stn_conc(:,1)<=180,:)  # (x1)
                    data_8 = stn_conc(stn_conc(:,1)>180 & stn_conc(:,1)<=270,:)  # (x3)
                    data_9 = stn_conc(stn_conc(:,1)>270 & stn_conc(:,1)<=360,:) # (x9)
                    data_10 = stn_conc(stn_conc(:,1)>360 & stn_conc(:,1)<=540,:) # (x16)
                    data_11 = stn_conc(stn_conc(:,1)>540,:)            # (x37)
                    
                    data_1 = rmmissing(data_1,1)
                    data_2 = rmmissing(data_2,1)
                    data_3 = rmmissing(data_3,1)
                    data_4 = rmmissing(data_4,1)
                    data_5 = rmmissing(data_5,1)
                    data_6 = rmmissing(data_6,1)
                    if size(data_1,1)>1
                        data_1 = datasample(data_1, round(size(data_1,1)*0.03),'Replace',false)
                    
                    if size(data_2,1)>1
                        data_2 = datasample(data_2, round(size(data_2,1)*0.07),'Replace',false)
                    
                    if size(data_3,1)>1
                        data_3 = datasample(data_3, round(size(data_3,1)*0.1),'Replace',false)
                    
                    if size(data_4,1)>1
                        data_4 = datasample(data_4, round(size(data_4,1)*0.2),'Replace',false)
                    
                    if size(data_5,1)>1
                        data_5 = datasample(data_5, round(size(data_5,1)*0.4),'Replace',false)
                    
                    if size(data_6,1)>1
                        data_6 = datasample(data_6, round(size(data_6,1)*0.6),'Replace',false)
                    
                    nndata = [data_1data_2data_3data_4data_5data_6data_7data_8data_9data_10data_11]
                    
                    ndata_8 = oversampling_sh(data_8(:,1:6),stn_6km_location,size(lon_goci,1),size(lon_goci,2),2)
                    ndata_9 = oversampling_sh(data_9(:,1:6),stn_6km_location,size(lon_goci,1),size(lon_goci,2),8)
                    ndata_10 = oversampling_sh(data_10(:,1:6),stn_6km_location,size(lon_goci,1),size(lon_goci,2),15)
                    ndata_11 = oversampling_sh(data_11(:,1:6),stn_6km_location,size(lon_goci,1),size(lon_goci,2),36)
                    
                    ndata = [nndatandata_8ndata_9ndata_10ndata_11]
                    clearvars nndata data_1 data_2 data_3 data_4 data_5 data_6 data_7 data_8 data_9 data_10 data_11 ndata_8 ndata_9 ndata_10 ndata_11
                                        
                    # remove station pixel among oversampled pixels
                    # ndata = [stn_conc, stn_num, doy_num, stn_ind, stn_x, stn_y, over]
                    dup_idx = matlab.ismember(ndata(:,7),stn_6km_location(:,5))
                    dup_idx = dup_idx .* ndata(:,6) #oversampling col
                    ndata = ndata(dup_idx==0,:)

                    # Extract input variables at station points & oversampling points
                    data_tmp = data(ndata(:,7),:)
                    
                    data_tmp(:,nvar+1:nvar+6) = ndata(:,(1:6)) # data. stn_PM, stn_num, doy_num, time, yr, ovr
                    k=((doy-1)*8)+(utc+1)
                    data_tmp(:,nvar+7) = k #k_idx
                                            
                    data_tmp(data_tmp==-9999)np.nan
                    data_tmp = rmmissing(data_tmp,1)
                                                            
                    data_stn = [data_stn data_tmp]
                    data_stn = matlab.sortrows(data_stn,30)
                    print (utc)
                
            
            print (doy)
            if doy >= 30 & utc == 7                     
                csvwrite_with_headers2([path_save,'time_conc/dataset/PM10/PM10_RTT_EA6km_',
                    str(yr),'_',str(doy,'#03i'),'_',str(utc,'#02i'),'.csv'],data_stn,header2,0,0,'#7.7f')
                print (doy)
            
        else       
            for utc=0:7
                k=240          
                
                # leave the high concentration samples
                extra_samples = data_stn(data_stn(:,)==1,:)
                
                high_tmp = extra_samples(extra_samples(:,24)>=400,:)
                low_tmp = extra_samples(extra_samples(:,24)<=100,:)
                    
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
                
                
                data_stn = data_stn(data_stn(:,)>=2,:)
                high_tmp(:,) = high_tmp(:,)+1
                low_tmp(:,) = low_tmp(:,)+1
                data_stn = [low_tmp high_tmp data_stn]
                data_stn(:,) = data_stn(:,)-1
                
                
                if np.all(data_stn)==1
                elif size(data_stn(data_stn(:,29)==1,:),1)>1
                    rmovr = datasample(data_stn(data_stn(:,-1)==1,:), round(size(data_stn(data_stn(:,-1)==1,:),1)*0.99),'Replace',false)
                    data_stn(data_stn(:,-1)==1,:)=[]
                    data_stn=[data_stn rmovr]
                else                    
                    data_stn(data_stn(:,-1)==1,:)=[]
                
                
                matlab.loadmat(os.path.join(path_data, 'EA_GOCI6km/cases_mat/',str(yr),'/cases_EA6km_',str(yr),'_',
                    str(doy, '#03i'),'_',str(utc,'#02i'),'.mat']) # data_tbl
                data = data_tbl(:,header) 
                data = table2array(data)                
                clear data_tbl
                
                # Load station data
                stn_6km = stn(stn(:,1) == doy & stn(:,2) ==yr & stn(:,5)== utc ,:)   
                
                if np.all(stn_6km)==0 # no observation data in some utc
                    stn_idx = matlab.ismember(stn_6km_location(:,2), stn_6km(:,13))
                    stn_conc = stn_6km(:,[10,13,1,5,2]) # PM10, stn_num, doy_num,time,yr
                    stn_conc(:,6)=0# PM10, stn_num, doy_num,time,yr, ovr
                    stn_conc(:,7) =stn_6km_location(stn_idx,5)# PM10, stn_num, doy_num,time,yr, ovr, stn_location
                    
                    data_1 = stn_conc(stn_conc(:,1)<=20,:)            # (x0.03)
                    data_2 = stn_conc(stn_conc(:,1)>20 & stn_conc(:,1)<=40,:) # (x0.07)
                    data_3 = stn_conc(stn_conc(:,1)>40 & stn_conc(:,1)<=60,:) # (x0.1)
                    data_4 = stn_conc(stn_conc(:,1)>60 & stn_conc(:,1)<=80,:)  # (x0.2)
                    data_5 = stn_conc(stn_conc(:,1)>80 & stn_conc(:,1)<=100,:)  # (x0.4)
                    data_6 = stn_conc(stn_conc(:,1)>100 & stn_conc(:,1)<=120,:)  # (x0.6)
                    data_7 = stn_conc(stn_conc(:,1)>120 & stn_conc(:,1)<=180,:)  # (x1)
                    data_8 = stn_conc(stn_conc(:,1)>180 & stn_conc(:,1)<=270,:)  # (x3)
                    data_9 = stn_conc(stn_conc(:,1)>270 & stn_conc(:,1)<=360,:) # (x9)
                    data_10 = stn_conc(stn_conc(:,1)>360 & stn_conc(:,1)<=540,:) # (x16)
                    data_11 = stn_conc(stn_conc(:,1)>540,:)            # (x37)
                    
                    data_1 = rmmissing(data_1,1)
                    data_2 = rmmissing(data_2,1)
                    data_3 = rmmissing(data_3,1)
                    data_4 = rmmissing(data_4,1)
                    data_5 = rmmissing(data_5,1)
                    data_6 = rmmissing(data_6,1)
                    if size(data_1,1)>1
                        data_1 = datasample(data_1, round(size(data_1,1)*0.03),'Replace',false)
                    
                    if size(data_2,1)>1
                        data_2 = datasample(data_2, round(size(data_2,1)*0.07),'Replace',false)
                    
                    if size(data_3,1)>1
                        data_3 = datasample(data_3, round(size(data_3,1)*0.1),'Replace',false)
                    
                    if size(data_4,1)>1
                        data_4 = datasample(data_4, round(size(data_4,1)*0.2),'Replace',false)
                    
                    if size(data_5,1)>1
                        data_5 = datasample(data_5, round(size(data_5,1)*0.4),'Replace',false)
                    
                    if size(data_6,1)>1
                        data_6 = datasample(data_6, round(size(data_6,1)*0.6),'Replace',false)
                    
                    nndata = [data_1data_2data_3data_4data_5data_6data_7data_8data_9data_10data_11]
                    
                    ndata_8 = oversampling_sh(data_8(:,1:6),stn_6km_location,size(lon_goci,1),size(lon_goci,2),2)
                    ndata_9 = oversampling_sh(data_9(:,1:6),stn_6km_location,size(lon_goci,1),size(lon_goci,2),8)
                    ndata_10 = oversampling_sh(data_10(:,1:6),stn_6km_location,size(lon_goci,1),size(lon_goci,2),15)
                    ndata_11 = oversampling_sh(data_11(:,1:6),stn_6km_location,size(lon_goci,1),size(lon_goci,2),36)
                    
                    ndata = [nndatandata_8ndata_9ndata_10ndata_11]
                    clearvars nndata data_1 data_2 data_3 data_4 data_5 data_6 data_7 data_8 data_9 data_10 data_11 ndata_8 ndata_9 ndata_10 ndata_11
                    
                    # remove station pixel among oversampled pixels
                    # ndata = [stn_conc, stn_num, doy_num, stn_ind, stn_x, stn_y, over]
                    dup_idx = matlab.ismember(ndata(:,7),stn_6km_location(:,5))
                    dup_idx = dup_idx .* ndata(:,6) #oversampling col
                    ndata = ndata(dup_idx==0,:)
                    
                    # Extract input variables at station points & oversampling points
                    data_tmp = data(ndata(:,7),:)
                    
                    data_tmp(:,nvar+1:nvar+6) = ndata(:,(1:6)) # data. stn_PM, stn_num, doy_num, time, yr, ovr
                    data_tmp(:,nvar+7) = k #k_idx
                    
                    data_tmp(data_tmp==-9999)np.nan
                    data_tmp = rmmissing(data_tmp,1)
                    data_tmp(data_tmp(:,24)>1000,:) =[]
                    
                    data_stn = [data_stn data_tmp]
                    
                    high_rate_pre = size(data_stn(data_stn(:,24)>=400,:),1)/size(data_stn(:,24),1) *100
                    low_rate_pre = size(data_stn(data_stn(:,24)<=100,:),1)/size(data_stn(:,24),1) *100
                    
                    if high_rate_pre<30 & low_rate_pre<30 & size(data_stn(:,)>1,1)>10000
                        print (('num of samples = #4.0f \n remove the oversampled samples in the oldest dataset \n',size(data_stn,1))
                        data_stn(data_stn(:,-1)==1 & data_stn(:,)<=8 & data_stn(:,24)>100 & data_stn(:,24)<400,:) = []
                    
                    
                    high_rate_pre = size(data_stn(data_stn(:,24)>=400,:),1)/size(data_stn(:,24),1) *100
                    low_rate_pre = size(data_stn(data_stn(:,24)<=100,:),1)/size(data_stn(:,24),1) *100
                    
                    # sample adjustment part1 -> remove the oversampled data
                    if high_rate_pre>30
                        print (('high_rate_pre = #3.2f & remove the stacked samples \n',high_rate_pre)
                        data_stn(data_stn(:,)==1 & data_stn(:,-1)==1 & data_stn(:,24)>=400,:)=[]
                    
                    
                    if low_rate_pre>30
                        print (('low_rate_pre = #3.2f & remove stacked samples \n',low_rate_pre)
                        data_stn(data_stn(:,)==1 & data_stn(:,-1)==1 &data_stn(:,24)<=100,:) = []
                    
                    
                    high_rate = size(data_stn(data_stn(:,24)>=400,:),1)/size(data_stn(:,24),1) *100
                    low_rate = size(data_stn(data_stn(:,24)<=100,:),1)/size(data_stn(:,24),1) *100
                    
                    # sample adjustment
                    if high_rate<30 &low_rate>30
                        print (('high_rate = #3.2f & stack more \n',high_rate)
                        print (('low_rate = #3.2f & remove stacked samples \n',low_rate)
                        # remove the low concentration samples
                        if np.all(low)==0
                            idx_low = np.where(data_stn(:,26) <= low(,26) & data_stn(:,24)<=100 & data_stn(:,)==1) # remove the low concentration samples under than doy
                            data_stn(idx_low,:) = []
                        
                        
                    elif high_rate<30 & low_rate<30
                        print (('high_rate = #3.2f & stack more \n',high_rate)
                        print (('low_rate = #3.2f & stack more \n',low_rate)
                        
                    elif high_rate>30 &low_rate<30
                        print (('high_rate = #3.2f & remove the stacked samples \n',high_rate)
                        print (('low_rate = #3.2f & stack more \n',low_rate)
                        # remove the high concentration samples
                        if np.all(high)==0
                            idx_high = np.where(data_stn(:,26) <= high(,26) & data_stn(:,24)>=400 & data_stn(:,)==1)
                            data_stn(idx_high,:) = []
                        
                    elif high_rate>30 & low_rate>30
                        print (('high_rate = #3.2f \n',high_rate)
                        print (('low_rate = #3.2f \n',low_rate)
                        # remove the high concentration samples
                        idx_high = np.where(data_stn(:,26) <= high(,26) & data_stn(:,24)>=400 & data_stn(:,)==1)
                        data_stn(idx_high,:) = []
                        # remove the low concentration samples
                        idx_low = np.where(data_stn(:,26) <= low(,26) & data_stn(:,24)<=100 & data_stn(:,)==1)
                        data_stn(idx_low,:) = []
                    
                    
                    data_stn = matlab.sortrows(data_stn,30)
                    csvwrite_with_headers2([path_save,'time_conc/dataset/PM10/PM10_RTT_EA6km_',
                        str(yr),'_',str(doy,'#03i'),'_',str(utc,'#02i'),'.csv'],data_stn,header2,0,0,'#7.7f')
                    print (utc)
                
            
            print (doy)
        
    
    print (yr)


