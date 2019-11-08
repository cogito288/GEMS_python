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
header = ['NDVI','AOD','AE','FMF','SSA','RSDN','Precip','DEM','LC_ratio', # satellite data(9)
    'Temp','Dew','RH','P_srf','MaxWS','PBLH','Visibility', # numerical data(RDAPS)(16)
    'stack1_np.maxWS','stack3_np.maxWS','stack5_np.maxWS','stack7_np.maxWS', # stacked np.maxWS(20)
    'DOY','PopDens','RoadDens'] #, etc data(24)
nvar = 23
if i==1:
    header2 = header+['PM10','stn_num','doy_num','time','yr','ovr','k_ind']
else:
    header2 = header+['PM25','stn_num','doy_num','time','yr','ovr','k_ind']

data_stn=[]
high=[]
low=[]

YEARS = [2015, 2016]
for yr in YEARS:
    if yr%4==0: days = 366
    else: days = 365
    
    fname = f'Station_1km_rm_outlier_{yr}_weight.mat'
    matlab.loadmat(os.path.join(path_nas6,'Station_Korea', fname))
    stn = stn_1km_yr
    
    for doy in range(1,days):
        if doy <=30 && yr == 2015:
            for utc in range(7):
                fname = f'cases_RTT_{yr}_{doy:03d}_{utc:02d}.mat'
                mat = matlab.loadmat(os.path.join(path_nas4, 'cases/RTT_mat', fname)) # data
                data = mat['data']
                data = data[:,[:21,22:24]]
                data[[data[:,-1]==65535),-1] = -9999
                
                # Load station data
                stn_1km = stn[stn[:,0] == doy & stn[:,1] ==yr & stn[:,4]== utc+9 ,:]                
                
                stn_idx = matlab.ismember(stn_1km_location[:,1], stn_1km[:,12])
                stn_conc = stn_1km[:,[10,12,0,4,1]) # PM2.5, stn_num, doy_num,time,yr
                stn_conc[:,5] = 0# PM2.5, stn_num, doy_num,time,yr, ovr
                stn_conc[:,6] = stn_1km_location[stn_idx,4]# PM2.5, stn_num, doy_num,time,yr, ovr, stn_location
                
                data_1 = stn_conc[stn_conc[:,0]<=50,:]            # (x1)
                data_2 = stn_conc[stn_conc[:,0]>50 & stn_conc[:,0]<=80,:]  # (x3)
                data_3 = stn_conc[stn_conc[:,0]>80,:]  # (x5)

                ndata_2 = oversampling_sh(data_2[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],2)
                ndata_3 = oversampling_sh(data_3[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],4)
                
                ndata = np.concatenate((ndata_1,ndata_2,ndata_3), axis=0)
                del data_1, data_2, data_3,  ndata_2, ndata_3 
                
                # remove station pixel among oversampled pixels
                # ndata = [stn_conc, stn_num, doy_num, stn_ind, stn_x, stn_y, over]
                dup_idx = matlab.ismember(ndata[:,6],stn_1km_location[:,4])
                dup_idx = np.multiplye(dup_idx, ndata[:,5]) #oversampling col
                ndata = ndata[dup_idx==0,:]
                
                # Extract input variables at station points & oversampling points
                data_tmp = data[ndata[:,6],:]
                #  data_tmp = cases(ndata[:,6],[1:2,4:-1])
                
                data_tmp[:,nvar:nvar+5] = ndata[:,:6] # data. stn_PM, stn_num, doy_num, time, yr, ovr
                k=((doy-1)*8)+(utc+1)
                data_tmp[:,nvar+6] = k #k_idx
                data_tmp[data_tmp==-9999] = np.nan
                data_tmp = rmmissing[data_tmp, 0]
                data_stn = np.concatenate((data_stn, data_tmp), axis=0)
                print (utc)
            print (doy)
            if doy >= 30 & utc == 7:
                fname = f'{target[i]}_RTT_{yr}_{doy:03d}_{utc:02d}.csv'
                temp_df = pd.DataFrame(data_stn, columns=header2)
                temp_df.to_csv(os.path.join(path_nas4,'dataset', target[i], 'new', fname), float_format='%7.7f')
                print (doy)
        else:
            for utc in range(7):
                k=240               
                # 고농도 남기기
                extra_samples = data_stn[data_stn[:,-1]==1,:]
                if i==1:
                    high_tmp = extra_samples[extra_samples[:,23]>=150,:]
                    low_tmp = extra_samples[extra_samples[:,23]<=60,:]
                else:
                    high_tmp = extra_samples[extra_samples[:,23]>=80,:]
                    low_tmp = extra_samples[extra_samples[:,23]<=30,:]
                if not np.all(high_tmp==0): # notempty
                    high = high
                else:
                    high = np.concatenate((high, high_tmp), axis=0)
                    high[:,-1] = high[:,-1]+1
                    high_uniq = np.unique(high[:,:29], axis=1)
                    high_uniq[:,end+1]=2
                    high = high_uniq

                if not np.all(low_tmp==0): # not empty
                    low = low
                else:
                    low = np.concatenate((low, low_tmp), axis=0)
                    low[:,-1] = low[:,-1]+1                    
                    low_uniq = np.unique(low[:,:29], axis=1)
                    low_uniq[:,end+1]=2
                    low = low_uniq
#                 matlab.savemat(os.path.join(path_nas4, 'dataset/',target{i},'/variable_test/extra_samples/',target{i},'_high_',
#                     str(yr),'_',str(doy, '#03i'),'_',str(utc, '#02i'),'.mat'],'high')
#                 matlab.savemat(os.path.join(path_nas4, 'dataset/',target{i},'/variable_test/extra_samples/',target{i},'_low_',
#                     str(yr),'_',str(doy, '#03i'),'_',str(utc, '#02i'),'.mat'],'low')                 
                
                data_stn = data_stn[data_stn[:,]>=2,:]
                high_tmp[:,-1] = high_tmp[:,-1]+1
                low_tmp[:,-1] = low_tmp[:,-1]+1
                data_stn = np.concatenate((low_tmp, high_tmp, data_stn), axis=0)
                data_stn[:,-1] = data_stn[:,-1]-1
                
                fname = f'cases_RTT_{yr}_{doy:03d}_{utc:02d}.mat'
                mat = matlab.loadmat(os.path.join(path_nas4, 'cases/RTT_mat', fname)) # data
                data = mat['data']
                del mat
                data = data[:,[:21,22:24])
                data[[data[:,-1]==65535],-1] = -9999              
                
                # Load station data
                stn_1km = stn[stn[:,0] == doy & stn[:,1] ==yr & stn[:,4]== utc+9 ,:]                
                
                stn_idx = matlab.ismember(stn_1km_location[:,1], stn_1km[:,12])
                stn_conc = stn_1km[:,[10,12,0,4,1]) # PM2.5, stn_num, doy_num,time,yr
                stn_conc[:,5]=0# PM2.5, stn_num, doy_num,time,yr, ovr
                stn_conc[:,6] =stn_1km_location[stn_idx,4]# PM2.5, stn_num, doy_num,time,yr, ovr, stn_location
                
                data_1 = stn_conc[stn_conc[:,0]<=50,:]            # (x1)
                data_2 = stn_conc[stn_conc[:,0]>50 & stn_conc[:,0]<=80,:]  # (x3)
                data_3 = stn_conc[stn_conc[:,0]>80,:]  # (x5)

                ndata_2 = oversampling_sh(data_2[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],1]
                ndata_3 = oversampling_sh(data_3[:,:6],stn_1km_location,lon_kor.shape[0],lon_kor.shape[1],3]
                nndata = np.concatenate((data_1,data_2,data_3,ndata_2, ndata_3), axis=0)
                del data_1, data_2, data_3, ndata_2, ndata_3 
                
                # remove station pixel among oversampled pixels
                # ndata = [stn_conc, stn_num, doy_num, stn_ind, stn_x, stn_y, over]
                dup_idx = matlab.ismember(ndata[:,6],stn_1km_location[:,4])
                dup_idx = np.multiplye(dup_idx, ndata[:,5]) #oversampling col
                ndata = ndata[dup_idx==0,:]
                

                # Extract input variables at station points & oversampling points
                data_tmp = data[ndata[:,6],:]
                data_tmp[:,nvar:nvar+5] = ndata[:,:6] # data. stn_PM, stn_num, doy_num, time, yr, ovr
                data_tmp[:,nvar+6] = k #k_idx
                data_tmp[data_tmp==-9999] = np.nan
                data_tmp = rmmissing[data_tmp, 0]
                data_tmp[data_tmp[:,23]>1000,:] =[]
                data_stn = np.concatenate((data_stn, data_tmp), axis=0)

                high_rate_pre = data_stn[data_stn[:,23]>=400,:].shape[0]/data_stn[:,23].shape[0]*100
                low_rate_pre = data_stn[data_stn[:,23]<=100,:].shape[0]/data_stn[:,23].shape[0]*100
                
                if high_rate_pre<30 & low_rate_pre<30 & size(data_stn[:,-1]>1,0]>1000
                    print ('num of samples = {data_stn.shape[0]:4.0f} \n remove the oversampled samples in the new dataset \n')
                    data_stn[data_stn[:,-1]==1 & data_stn[:,-1]==240 & data_stn[:,23]<80:] = []

                high_rate_pre = data_stn[data_stn[:,23]>=400,:].shape[0]/data_stn[:,23].shape[0]*100
                low_rate_pre = data_stn[data_stn[:,23]<=100,:].shape[0]/data_stn[:,23].shape[0]*100
                # 샘플 조정 part1
                if high_rate_pre>30:
                    print ('high_rate_pre = {high_rate_pre:3.2f} & remove the stacked samples \n')
                    data_stn[data_stn[:,-1]==240 & data_stn[:,-1]==1,:]=[]
                if low_rate_pre>30:
                    print ('low_rate = {low_rate:3.2f} & remove stacked samples \n')
                    data_stn[data_stn[:,23]<=30 & data_stn[:,-1] ==2,:] = []

                high_rate_pre = data_stn[data_stn[:,23]>=400,:].shape[0]/data_stn[:,23].shape[0]*100
                low_rate_pre = data_stn[data_stn[:,23]<=100,:].shape[0]/data_stn[:,23].shape[0]*100
                # 샘플 조정
                if high_rate<30 &low_rate>30:
                    print ('high_rate = {high_rate:3.2f} & stack more \n')
                    print ('low_rate = {low_rate:3.2f} & remove stacked samples \n')
                # 저농도 지우기
                   if np.all(low==0):
                       idx_low = np.where(data_stn[:,25] <= low[-1,25] & data_stn[:,23]<=30 & data_stn[:,-1]==1)[0]
                       data_stn[idx_low,:] = []
                   -1
                    
                elif high_rate<30 & low_rate<30:
                    print ('high_rate = {high_rate:3.2f} & stack more \n')
                    print ('low_rate = {low_rate:3.2f} & stack more \n')
                elif high_rate>30 &low_rate<30:
                    print ('high_rate = {high_rate:3.2f} & remove stacked samples \n')
                    print ('low_rate = {low_rate:3.2f} & stack more \n')
                   # 고농도
                   if np.all(high==0):
                        idx_high = np.where(data_stn[:,25] <= high[-1,25] & data_stn[:,23]>=80 & data_stn[:,-1]==1)[0]
                    data_stn[idx_high,:] = []
                   -1
                elif high_rate>30 & low_rate>30:
                    print (('high_rate = #3.2f \n',high_rate)
                    print (('low_rate = #3.2f \n',low_rate)
                    # 고농도 지우기
                    idx_high = np.where(data_stn[:,25] <= high(-1,25] & data_stn[:,23]>=80 & data_stn[:,-1]==1)[0]
                    data_stn[idx_high,:] = []
                    # 저농도 지우기
                    idx_low = np.where(data_stn[:,25]<= low[-1,25] & data_stn[:,23]<=30 & data_stn[:,-1]==1)[0]
                    data_stn[idx_low,:] = []                
                    # sample수 줄이는 코드 추가필요 전체적인 갯수줄이기
                    # data_stn[:,-1]==1 인 날에대해서 줄이기         
                print (utc)
                fname = f'{target[i]}_RTT_{yr}_{doy:03d}_{utc:02d}.csv'
                temp_df = pd.DataFrame(data_stn, columns=header2)
                temp_df.to_csv(os.path.join(path_nas4,'dataset', target[i], 'new', fname), float_format='%7.7f')
            print (doy)
    print (yr)



