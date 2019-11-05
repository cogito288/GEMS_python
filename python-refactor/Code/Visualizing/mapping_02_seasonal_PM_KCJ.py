  

time.time()

# path_data = '/Volumes/irisnas5/Data/'
# path= '/Volumes/irisnas5/GEMS/PM/00_EA6km/'
# addpath(genpath('/Volumes/irisnas5/Data/matlab_func/'))

# path_data = '//10.72.26.56/irisnas5/Data/'
# path= '//10.72.26.56/irisnas5/GEMS/PM/00_EA6km/'
# addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'))

path_data = '/share/irisnas5/Data/'
path= '/share/irisnas5/GEMS/PM/00_EA6km/'
addpath(genpath('/share/irisnas5/Data/matlab_func/'))

season_name = {'Spring','Summer','Fall','Winter'}
season_name2 = {'MAM','JJA','SON','DJF'}
type = {'conc','time','time_conc'}
target = {'PM10','PM25'}

## Load grid
matlab.loadmat(os.path.join(path_data,'grid/grid_goci.mat'])

season_num = [61,153,245,336]

for t=1:2:3
    for i=1:2
        for yr=2015:2017
            if yr%4==0
                days = 366
                daysInMonths = [31,29,31,30,31,30,31,31,30,31,30,31]
            else
                days = 365
                daysInMonths = [31,28,31,30,31,30,31,31,30,31,30,31]
            
            matlab.loadmat(os.path.join(path, 'RF_map/',type{t},'/',target{i},'/annual/',target{i},'_RTT_EA6km_',str(yr),'.mat'])
            

            for s= 1:4
                if s==4
                    ssss = [1:60, 336:days]
                else
                    ss = season_num(:,s:s+1)
                    sss= season_num(:,s+1)-1
                    ssss=ss:sss
                
                season = annual(:,ssss)
                
                clearvars ss sss ssss
                
                season_avg = reshape(np.nanmean(season,2),size(lon_goci))
                
                nan_ratio_ss = np.sum(np.isnp.full(season),2)/size(season,2)
                nan_ratio_ss = reshape(nan_ratio_ss,size(lon_goci))
                
                season_avg_m = season_avg
                season_avg_m(nan_ratio_ss>0.95) np.nan
                
                #reshaping and mapping
                m_kc_cloud(lon_goci,lat_goci,season_avg_m)
                #             colormap(jet)
                if i==1
                    caxis([0 150])
                else
                    caxis([0 60])
                
                colorbar('FontSize',12)
                
#                 mode_name = strrep(version{v},string('_'),string(' '))
                name_titile = [str(yr),' ', season_name{s},' (',season_name2{s},') ']
                
                hold on 
                title(name_titile,'fontweight','bold','FontSize',16)
                
                #save map image
                name = fullfile(path, ['RF_map/',type{t},'/',target{i},'/seasonal/',target{i},'_RTT_season_map_',
                    str(yr),'_',season_name{s},''])
                print('-djpeg','-r300',name)
                
                close all
            
        
    
    print (target{i})

print (type{t})



