  

time.time()

# path_data = '/Volumes/irisnas5/Data/'
# path= '/Volumes/irisnas5/GEMS/PM/00_EA6km/'
# addpath(genpath('/Volumes/irisnas5/Data/matlab_func/'))

# path_data = '//10.72.26.56/irisnas5/Data/'
# path= '//10.72.26.56/irisnas5/GEMS/PM/00_EA6km/'
# addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'))
# # # #
path_data = '/share/irisnas5/Data/'
path= '/share/irisnas5/GEMS/PM/00_EA6km/'
addpath(genpath('/share/irisnas5/Data/matlab_func/'))

type = {'conc','time','time_conc'}
target = {'PM10','PM25'}

## Load grid
matlab.loadmat(os.path.join(path_data,'grid/grid_goci.mat'])

for t=2
    for i=1
        for yr=2015:2017
            if yr%4==0
                days = 366
                daysInMonths = [31,29,31,30,31,30,31,31,30,31,30,31]
            else
                days = 365
                daysInMonths = [31,28,31,30,31,30,31,31,30,31,30,31]
            
            
            
            daily = []
            monthly=[]
            annual =[]
            for doy = 1:days
                [yy, mm, dd] = datevec(matlab.datenum(yr,1,doy))
                try
                    for utc=0:7
                        
                        # load cases file for nan matrix
                        matlab.loadmat(os.path.join(path_data, 'EA_GOCI6km/cases_mat/',str(yr),'/cases_EA6km_',str(yr),'_',
                            str(doy, '#03i'),'_',str(utc,'#02i'),'.mat'])
                        data = table2array(data_tbl)
                        data = data(:,[5:12,59,13:19,28:31,36:38])
                        
                        data(data==-9999)np.nan
                        data(np.isnp.full(data)==1)=-9999
                        [idy,idx] = np.where(data == -9999)
                        idy = np.unique(idy)
                        data(idy.flatten(),:) = -9999
                        data(data==-9999)np.nan
                        nanidx =np.isnp.full(data(:,1))
                        clear data_tbl data idy idx
                        
                        try
                            # read prediction file
                            pred = pd.read_csv(os.path.join(path,'RTT/',type{t},'/RF_pred/',target{i},'/rf_',target{i},'_RTT_EA6km_',
                                str(yr),'_',str(doy,'#03i'),'_',str(utc,'#02i'),'.csv'],1,1)
                            
                            # nan masking to prediction PM concentration.
                            pred(nanidx==1,:)=nan
                            if yr==2015 & doy==30
                                daily(1:218999,1:7) =nan
                                daily(:,utc+1)=pred
                            else
                                daily(:,utc+1)=pred
                            
                            
#                             pred = reshape(pred, size(lon_goci))
#                             m_kc_RTT(lon_goci,lat_goci,pred)
#                             if i==1
#                                 caxis([0 200])
#                             else
#                                 caxis([0 100])
#                             
#                             colorbar('FontSize',12)
#                             
#                             hold on 
#                             title([str(yr),'/',str(mm, '#02i'),'/',str(dd, '#02i'),' ',
#                                 str(utc+9, '#02i'),':00 KST'],'fontweight','bold','FontSize',14)
#                             
#                             # save map image
#                             name = fullfile(path, ['RF_map/',type{t},'/',target{i},'/hourly/',target{i},'_RTT_daily_map_',
#                                 sprintf('#04d', yr),'_',sprintf('#03d', doy),'_',sprintf('#02d', utc)])
#                             print('-djpeg','-r300',name)
                            
                            print (utc)
                            close all
                        catch
                            print ([str(doy,'#03i'),'_',str(utc,'#02i')])
                        
                    
                    
                    # save hourly prediction matrix
                    matlab.savemat(os.path.join(path, 'RF_map/',type{t},'/',target{i},'/daily/',target{i},'_RTT_EA6km_',
                        str(yr),'_',str(doy,'#03i')],'daily')
                    clear pred
                    
                    daily_avg = np.nanmean(daily,2)
                    if yr==2015
                        annual(1:218999,1:29) = nan
                        annual(:,doy) = daily_avg
                    else
                        annual(:,doy) = daily_avg
                    
                    
                    # reshaping and mapping
                    daily_avg = reshape(daily_avg, size(lon_goci))
                    m_kc_RTT(lon_goci,lat_goci,daily_avg)
                    if i==1
                        caxis([0 200])
                    else
                        caxis([0 100])
                    
                    colorbar('FontSize',12)
                    
                    hold on 
                    title([str(yr),'/',str(mm, '#02i'),'/',str(dd, '#02i')],'fontweight','bold','FontSize',14)
                    
                    # save map image
                    name = fullfile(path, ['RF_map/',type{t},'/',target{i},'/daily/',target{i},'_RTT_daily_map_',
                        sprintf('#04d', yr),'_',sprintf('#03d', doy)])
                    print('-djpeg','-r300',name)
                    
                    print (doy)
                    close all
                catch
                    print ([str(yr),'_',str(doy,'#03i')])
                
            
            # save daily prediction matrix
            matlab.savemat(os.path.join(path, 'RF_map/',type{t},'/',target{i},'/annual/',target{i},'_RTT_EA6km_',
                str(yr)],'annual')
            
            ## monthly PM mapping
            monthEnds = [0, cumnp.sum(daysInMonths)]
            for m = 1:12
                firstDay = monthEnds(m)+1
                lastDay = monthEnds(m+1)
                
                monthly_tmp = annual(:,firstDay:lastDay)
                monthly(:,m) = np.nanmean(monthly_tmp,2)
                
                monthly_avg = reshape(np.nanmean(monthly_tmp,2),size(lon_goci))
                
                nan_ratio_mon = np.sum(np.isnp.full(monthly_tmp),2)/size(monthly_tmp,2)
                nan_ratio_mon = reshape(nan_ratio_mon,size(lon_goci))
                
                monthly_avg_m = monthly_avg
                monthly_avg_m(nan_ratio_mon>0.95) np.nan
                
                #reshaping and mapping
                m_kc_RTT(lon_goci,lat_goci,monthly_avg_m)
                #             colormap(jet)
                if i==1
                    caxis([0 150])
                else
                    caxis([0 60])
                
                colorbar('FontSize',12)
                
                hold on 
                title([str(yr),' / ',str(m, '#02i')],'fontweight','bold','FontSize',14)
                
                #save map image
                name = fullfile(path, ['RF_map/',type{t},'/',target{i},'/monthly/',target{i},'_RTT_daily_map_',
                    str(yr),'_',str(m, '#02i')])
                print('-djpeg','-r300',name)
                
                print (m)
                close all
                
            
            matlab.savemat(os.path.join(path, 'RF_map/',type{t},'/',target{i},'/monthly/',target{i},'_RTT_EA6km_',
                str(yr)],'monthly')
            
            ## annual PM mapping
            annual = np.nanmean(monthly,2)
            annual_avg = reshape(annual,size(lon_goci))
            
            nan_ratio_yr = np.sum(np.isnp.full(monthly),2)/size(monthly,2)
            nan_ratio_yr = reshape(nan_ratio_yr,size(lon_goci))
            
            annual_avg_m = annual_avg
            annual_avg_m(nan_ratio_yr>0.95) np.nan
            
            # reshaping and mapping
            m_kc_RTT(lon_goci,lat_goci,annual_avg_m)
            if i==1
                caxis([0 150])
            else
                caxis([0 60])
            
            colorbar('FontSize',12)
            
            hold on 
            title(str(yr),'fontweight','bold','FontSize',14)
            
            # save map image
            name = fullfile(path, ['RF_map/',type{t},'/',target{i},'/annual/',target{i},'_RTT_daily_map_',
                str(yr)])
            print('-djpeg','-r300',name)
            
            print (yr)
            close all
        
    

