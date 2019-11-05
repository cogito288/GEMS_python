 , close all

# path_data = '//10.72.26.56/irisnas5/Data/'
# path_save = '//10.72.26.56/irisnas5/GEMS/PM/00_EA6km/'
# addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'))

path_data = '/share/irisnas5/Data/'
path_save = '/share/irisnas5/GEMS/PM/00_EA6km/'
addpath(genpath('/share/irisnas5/Data/matlab_func/'))

# path_data = '/Volumes/irisnas5/Data/'
# path_save = '/Volumes/irisnas5/GEMS/PM/00_EA6km/'
# addpath(genpath('/Volumes/irisnas5/Data/matlab_func/'))


## Station index
matlab.loadmat(os.path.join(path_data,'Station/Station_CN/cn_stn_GOCI6km_location_weight.mat'])
matlab.loadmat(os.path.join(path_data,'Station/Station_Korea/stn_GOCI6km_location_weight_v2018.mat'])
matlab.loadmat(os.path.join(path_data,'Station/Station_JP/jp_stn_GOCI6km_location_weight.mat'])
stn_6km_location = [stn_GOCI6km_location jp_stn_GOCI6km_location cn_stn_GOCI6km_location]
cn_dup_scode2_GOCI6km(:,+1:size(jp_dup_scode2_GOCI6km,2))=0
dup_scode2_GOCI6km(:,+1:size(jp_dup_scode2_GOCI6km,2))=0
dup_scode2_6km =[dup_scode2_GOCI6km cn_dup_scode2_GOCI6km jp_dup_scode2_GOCI6km]

clear stn_GOCI6km_location cn_stn_GOCI6km_location jp_stn_GOCI6km_location cn_dup_scode2_GOCI6km dup_scode2_GOCI6km jp_dup_scode2_GOCI6km header_cn_stn_GOCI6km_location header_jp_stn_GOCI6km_location

## Read data
target = {'PM10','PM25'}
type = {'conc','time','time_conc'}

##
for t=1
    for i=1 ########
        
        header = {'AOD','AE','FMF','SSA','NDVI','RSDN','Precip','DEM','LCurban', # satellite data(9)
            'Temp','Dew','RH','P_srf','MaxWS','PBLH','Visibility', # numerical data(RDAPS)(16)
            'stack1_np.maxWS','stack3_np.maxWS','stack5_np.maxWS','stack7_np.maxWS', # stacked np.maxWS(20)
            'DOY','PopDens','RoadDens'} #, etc data(24)
        nvar = 23
        
        if i==1
            header2 = [header,{'PM10','stn_num','doy_num','time','yr','ovr','k_ind'}]
        else
            header2 = [header,{'PM25','stn_num','doy_num','time','yr','ovr','k_ind'}]
        
        
        for yr=2017
            if yr%4==0
                days = 366
            else
                days = 365
            
            
            for doy = 1:days
                try
                    [yy mm dd] = datevec(matlab.datenum(yr,1,doy))
                    for utc = 0:7
                        data = pd.read_csv(os.path.join(path_save, 'RTT/',type{t},'/dataset/',target{i},'/',target{i},'_RTT_EA6km_',
                            str(yr),'_',str(doy, '#03i'),'_',str(utc, '#02i'),'.csv'],1)
                        
                        if i==1
                            data = data(data(:,-6)<=1000,:)
                            val_num = 30
                        elif i==2
                            data = data(data(:,-6)<=600,:)
                            val_num = 20
                        
                        
                        val = data((data(:,-4)==doy & data(:,-3)==utc & data(:,-1)==0),:)
                        val_stn = val(:,-5) # stn_num
                        data((data(:,-4)==doy & data(:,-3)==utc & data(:,-1)==0),:) = []
                        
                        cal_10_fold = []
                        val_10_fold = []
                        
                        if size(val_stn,1)>val_num
                            val_lonlat=[]
                            for lo = 1:size(val_stn,1)
                                val_lonlat(lo,:) = stn_6km_location(np.where(stn_6km_location(:,2)==val(lo,25)),:)
                            
                            dist_tmp = pdist(val_lonlat(:,6:7))
                            dist = squareform(dist_tmp)
                            
                            num_dist = np.zeros(size(val_stn,1))
                            for l=1:size(val_stn,1)
                                [row,col]=np.where(dist(:,l)<1) # 3 km
                                zero_values=np.zeros(size(val_stn,1)-size(row,1),1)
                                num_dist(:,l)=[rowzero_values]
                            
                            clearvars dist_tmp val_lonlat dist zero_values
                            num = []
                            for ii= 1:size(num_dist,2)
                                num_tmp = num_dist(:,ii)
                                num_tmp(num_tmp==0)=[]
                                if size(num_tmp,1)>val_num
                                    val_group = val(num_tmp,:)
                                    idx_val = matlab.ismember(data(:,-5),val_group(:,-5))
                                    
                                    val_10_fold = val(ii,:)
                                    cal_10_fold = [data(idx_val,:) val(matlab.ismember(num_tmp,ii)==0,:)]
                                    
                                    fname = [path_save,'LOO/',type{t},'/dataset/',target{i},'/',target{i},'_RTT_EA6km_',
                                        str(yr),'_',str(doy,'#03i'),'_',str(utc,'#02i')]
                                    save(strcat(fname,'_LOO_',str(ii,'#03i'),'_cal_doy_stn_ovr.mat'),'cal_10_fold')
                                    save(strcat(fname,'_LOO_',str(ii,'#03i'),'_val_doy_stn_ovr.mat'),'val_10_fold')
                                    
                                    cal_10_fold = cal_10_fold(:,1:-6)
                                    val_10_fold = val_10_fold(:,1:-6)
                                    csvwrite_with_headers(strcat(fname,'_LOO_',str(ii,'#03i'),'_cal.csv'),cal_10_fold,header2(1:-6))
                                    csvwrite_with_headers(strcat(fname,'_LOO_',str(ii,'#03i'),'_val.csv'),val_10_fold,header2(1:-6))
                                    
                                    print (utc)
                                else # station number < val_num in specific distance
                                    print (('Station number of #3.0f(DOY) & #1.0f(UTC) is under the #2.0f in row #2.0f \n',doy,utc,val_num,ii)
                                 #val_num
                              #num_dist
                         # distance
                     #utc
                print (doy)
                catch
                    print ([str(yr),'_',str(doy,'#03i')])
                 #try
             #doy
            print (yr)
         # year
        print (target{i})
     #target
 #type
