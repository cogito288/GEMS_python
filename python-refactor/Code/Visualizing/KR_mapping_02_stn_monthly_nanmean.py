  

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
stn_location = stn_1km_location
# scode1,scode2, lat_org, lon_org, pxid, lat_px, lon_px

##
for yr=2015:2016
    matlab.loadmat(os.path.join(path,'Korea/cases/KR_1km_stn_rf_day_',str(yr),'.mat']) # 'stn_fill'
 
    for mm=1:12
        data_temp = stn_fill(stn_fill(:,3)==mm,:)
#         data_temp = stn_fill # yearly
        scode2_unq = np.unique(data_temp(:,13))
        data_avg = []
        for ss = 1:length(scode2_unq)
            data_temp2 = data_temp(data_temp(:,13)==scode2_unq(ss),:)
            data_temp2 = np.nanmean(data_temp2,1)
            data_avg = [data_avg data_temp2]
        
        
        data_avg = data_avg(:,[13,10,11]) # scode2, stn_pm10, stn_pm
        
        for k=1:size(data_avg,1)
            data_avg(k,4:5)=stn_location(stn_location(:,2)==data_avg(k,1),3:4) 
            # scode2, stn_pm10, stn_pm25, lat_org, lon_org
        
        
        stnpm10 = data_avg(:,[1:2,4:5])
        stnpm10 = rmmissing(stnpm10,1)
        figure set(gcf,'Position',[1000,100,900,800])
        m_proj('lambert','long',[124 131.5],'lat',[33 39])
        m_gshhs_i('color','k','linewidth',2)
        m_grid('box','fancy','time.time()kdir','in','fontsize',20)
        hold on
        s = m_scatter(stnpm10(:,4),stnpm10(:,3),70, stnpm10(:,2),'filled') # stn_pm10
        s.MarkerEdgeColor='k'
        caxis([0 80])
        title([str(yr),' / ',str(mm,'#02i')],'fontsize',25,'fontweight','bold')
#         title(str(yr),'fontsize',25,'fontweight','bold')  # yearly
        colorbar('FontSize',18)
        print('-djpeg','-r300',[path,'Korea/RF_pred/PM10_stn_monthly_',str(yr),'_',str(mm,'#02i')])
#         print('-djpeg','-r300',[path,'Korea/RF_pred/PM10_stn_yearly_',str(yr)])  # yearly
        
        stnpm25 = data_avg(:,[1,3:5])
        stnpm25 = rmmissing(stnpm25,1)
        figure set(gcf,'Position',[1000,100,900,800])
        m_proj('lambert','long',[124 131.5],'lat',[33 39])
        m_gshhs_i('color','k','linewidth',2)
        m_grid('box','fancy','time.time()kdir','in','fontsize',20)
        hold on
        s = m_scatter(stnpm25(:,4),stnpm25(:,3),70, stnpm25(:,2),'filled') # stn_pm25
        s.MarkerEdgeColor='k'
        caxis([0 40])
        title([str(yr),' / ',str(mm,'#02i')],'fontsize',25,'fontweight','bold')
#         title(str(yr),'fontsize',25,'fontweight','bold')  # yearly
        colorbar('FontSize',18)
        print('-djpeg','-r300',[path,'Korea/RF_pred/PM25_stn_monthly_',str(yr),'_',str(mm,'#02i')])
#         print('-djpeg','-r300',[path,'Korea/RF_pred/PM25_stn_yearly_',str(yr)]) # yearly
#         
     # mm: month
 # yr
