### Package import
import os
import h5py

### Common
import sys
import numpy as np
project_path = 'C:\\Users\\user\\Downloads\\matlab2python\\matlab2python\\python-refactor'
#project_path = '/home/cogito/Uncertainty/matlab2python/python-refactor'
sys.path.insert(0, project_path)
from Code.utils import matlab
from Code.utils import helpers


# Accumulated Precipitation : From the time in the day before To the time in the day
"""
% path_data = '//10.72.26.45/irisnas7/RAW_DATA/GPM/00raw/3IMERGHH/';
% path = '//10.72.26.45/irisnas7/RAW_DATA/GPM/01mat/AP_24h_hourly/';
path_data = '/share/irisnas7/RAW_DATA/GPM/00raw/3IMERGHH/';
path = '/share/irisnas7/RAW_DATA/GPM/01mat/AP_24h_hourly/';
"""
raw_data_path = os.path.join(project_path, 'Data', 'Raw', 'GPM', '3IMERGHH') 
write_path = os.path.join(project_path, 'Data', 'Prepreossed_raw', 'GPM', 'AP_24h_hourly')

"""
name = '2014/3B-HHR.MS.MRG.3IMERG.20141231-S000000-E002959.0000.V04A.HDF5'
lat_gpm = matlab.h5read(os.path.join(raw_data_path, name), '/Grid/lat')
lon_gpm = matlab.h5read(os.path.join(raw_data_path, name), '/Grid/lon')
lat_gpm = np.float64(lat_gpm); lon_gpm = np.float64(lon_gpm)
lat_gpm, lon_gpm = np.meshgrid(lat_gpm, lon_gpm)
sio.savemat('grid_gpm.mat', mdict={'lon_gpm':lon_gpm, 'lat_gpm':lat_gpm})
"""

YEARS = [2016]
for yr in YEARS:
    os.chdir(raw_data_path)
    list_gpm = matlab.dir(str(yr), '.HDF5')  # list_gpm = dir([num2str(yr),'/*/*.HDF5']);
    doy_0 = matlab.datenum(str(yr-1)+'1231')
    
    # First day UTC 00
    list_temp = list_gpm[:48]
    doy = matlab.datenum(list_temp[0][21:29])-doy_0+1
    gpm = np.zeros([1800, 3600, 48]) # lat 1800, lon 3600
    for j in range(48):
        gpm_temp = matlab.h5read(list_gpm[j], '/Grid/precipitationCal')
        gpm_temp = np.float64(gpm_temp)
        gpm_temp[gpm_temp<-9999] = np.nan
        gpm[:,:,j] = gpm_temp
    precip = np.nansum(gpm, axis=2)
    precip = precip*0.5 #### 30분 자료인데, 단위는 hour 단위라서 0.5곱해줌
    sio.savemat(os.path.join(write_path, str(yr), f'gpm_AP_{yr}_{doy:3d}_UTC00.mat'), mdict={'precip':precip})
    
    % For doy 001 UTC01 to doy 365(366) UTC23
    % os.chdir(os.path.join(raw_data_path, str(yr)))
    for aa in range(3, mathlab.length(list_gpm)-48+1, 2):
        gpm = gpm[:,:,2:]
        list_temp = list_gpm[aa+45:aa+47]
        doy = matlab.datenum(list_gpm[aa][21:29])-doy0+1
        UTC = list_gpm[aa][31:33]
        for j in range(2):
            gpm_temp = matlab.h5read(list_temp[j], '/Grid/precipitationCal')
            gpm_temp = np.float64(gpm_temp)
            gpm_temp[gpm_temp<-9999] = np.nan
            gpm[:,:,j+46] = gpm_temp
        precip = np.nansum(gpm, axis=2)
        precip = precip*0.5 # 30분 자료인데, 단위는 hour 단위라서 0.5곱해줌
        sio.savemat(os.path.join(write_path, str(yr), f'gpm_AP_{yr}_{doy:03d}_UTC{UTC}.mat'), mdict={'precip':precip})
    print (year)
"""
% %%
% for yr = 2018
%     cd(path_data)
%     list_gpm_a = dir([num2str(yr-1),'/12/*1231-*.HDF5']);
%     list_gpm = dir([num2str(yr),'/*/*.HDF5']);
%     list_gpm_f = [{list_gpm_a.folder}';{list_gpm.folder}'];
%     list_gpm = [{list_gpm_a.name}';{list_gpm.name}'];
%     
%     doy0 = datenum([num2str(yr-1),'1231'],'yyyymmdd');
%     
%     % First day UTC 00
%     list_temp = list_gpm(1:48);
%     doy = datenum(list_temp{1}(22:29),'yyyymmdd')-doy0+1;
%     gpm = zeros(1800,3600,48); %lat 1800, lon 3600
%     
%     for j=1:48
%         gpm_temp = h5read([list_gpm_f{j},'/',list_temp{j}], '/Grid/precipitationCal');
%         gpm_temp = double(gpm_temp);
%         gpm_temp(gpm_temp<-9999)=nan;
%         gpm(:,:,j) = gpm_temp;
%     end
%     
%     precip = nansum(gpm,3);
%     precip = precip * 0.5;%%%% 30분 자료인데, 단위는 hour 단위라서 0.5곱해줌
%     save([path,num2str(yr),'/gpm_AP_',num2str(yr),'_',num2str(doy,'%03i'),...
%         '_UTC00.mat'], 'precip');
%     
%     % For doy 001 UTC01 to doy 365(366) UTC23
% %     cd([path_data,num2str(yr)])
%     for aa = 3:2:length(list_gpm)-48
%         gpm = gpm(:,:,3:end);
%         list_temp = list_gpm(aa+46:aa+47);
%         list_f_temp = list_gpm_f(aa+46:aa+47);
%         doy = datenum(list_gpm{aa}(22:29),'yyyymmdd')-doy0+1;
%         UTC = list_gpm{aa}(32:33);
%         for j=1:2
%             gpm_temp = h5read([list_f_temp{j},'/',list_temp{j}], '/Grid/precipitationCal');
%             gpm_temp = double(gpm_temp);
%             gpm_temp(gpm_temp<-9999)=nan;
%             gpm(:,:,j+46) = gpm_temp;
%         end
%         
%         precip = nansum(gpm,3);
%         precip = precip * 0.5;%%%% 30분 자료인데, 단위는 hour 단위라서 0.5곱해줌
%         save([path,num2str(yr),'/gpm_AP_',num2str(yr),'_',num2str(doy,'%03i'),...
%             '_UTC',UTC,'.mat'], 'precip');
%         disp(['gpm_AP_',num2str(yr),'_',num2str(doy,'%03i'),'_UTC',UTC])
%     end
%     disp(yr)
% end
"""