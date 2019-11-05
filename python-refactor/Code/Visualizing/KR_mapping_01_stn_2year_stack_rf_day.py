  

time.time()

path_data = '//10.72.26.46/irisnas6/Data/Aerosol/'
path = '//10.72.26.46/irisnas6/Work/Aerosol/'
# path_data = '/share/irisnas6/Data/Aerosol/'
# path = '/share/irisnas6/Work/Aerosol/'
# addpath(genpath('/share/irisnas6/Work/Aerosol/matlab_func/'))

tg = {'PM10','PM25'}

## Load grid
matlab.loadmat(os.path.join(path_data,'grid/grid_korea.mat'])
matlab.loadmat(os.path.join(path_data,'Station_Korea/stn_1km_location_weight.mat']) # stn_1km_location
# scode1,scode2, lat_org, lon_org, pxid, lat_px, lon_px

##
for yr=2015:2016
    # nanidx for cases
    matlab.loadmat(os.path.join(path,'Korea/cases/nanidx_1km_hourly_',str(yr)]) # nanidx
    
    # station
    matlab.loadmat(os.path.join(path_data,'Station_Korea/Station_1km_rm_outlier_',str(yr),'_weight.mat']) # stn_1km_yr
    
    stn_1km_yr(:,5)=stn_1km_yr(:,5)-9 # KST to UTC
    stn = stn_1km_yr
    
    stn_nanidx = []
    
    for doy=1:size(nanidx,2)   
        for utc=0:7
            nanidx_temp = nanidx(:,doy,utc+1)
            stn_temp = stn(stn(:,1)==doy&stn(:,5)==utc,:)
            
            for k=1:size(stn_temp,1)
                pid = stn_1km_location(stn_1km_location(:,2)==stn_temp(k,13),5)
                stn_temp(k,14)=nanidx_temp(pid)
            
            
            stn_nanidx = [stn_nanidxstn_temp]
        
    
    stn_fill = stn_nanidx(stn_nanidx(:,14)==0,1:13)
    matlab.savemat(os.path.join(path,'Korea/cases/KR_1km_stn_rf_day_',str(yr),'.mat'],'stn_fill')
 # yr

