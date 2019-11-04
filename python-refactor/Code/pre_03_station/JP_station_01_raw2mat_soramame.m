clear all;clc; close all;

% for local
% path_data = '//10.72.26.46/irisnas6/Data/In_situ/AirQuality_Japan/';
% path = '//10.72.26.56/irisnas5/Data/Station/Station_JP/';
% addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'))

path_data = '/share/irisnas6/Data/In_situ/AirQuality_Japan/';
path = '/share/irisnas5/Data/Station/Station_JP/';
% addpath(genpath('/share/irisnas5/Data/matlab_func/'))

header = {'doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode'};

for yr = 2017
    for mm=1:12
        list_stn = dir([path_data, num2str(yr),'_soramame/',num2str(yr),num2str(mm,'%02i'),'_00/*.csv']);
        list_stn_f = {list_stn.folder}';
        list_stn = {list_stn.name}';
        
        stn_mm=[];
        for k=1:size(list_stn,1)            
            stn_tbl_temp = readtable([list_stn_f{k},'/',list_stn{k}]);
            
            scode = table2array(stn_tbl_temp(:,1));
            dstr = table2array(stn_tbl_temp(:,2));
            dvec = datevec(dstr,'yyyy/mm/dd');
            dnum = datenum(dstr,'yyyy/mm/dd');
            doy_000 = datenum([yr,0,0,0,0,0]);
            doy = dnum-doy_000;
            stn_value = table2array(stn_tbl_temp(:,3:15));
            
            data = [doy,dvec(:,1:3),stn_value(:,[1,2,6,7,4,11,12]),scode];
            % {'doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode'};

            stn_mm = [stn_mm; data];
        end
        save([path,'stn_code_data/stn_code_data_',num2str(yr),'_',num2str(mm,'%02i'),'.mat'],'stn_mm','-v7.3');
        disp(mm)
    end        
    
    disp('Stack monthly data to yearly data')
    stn_yr = [];
    for mm=1:12
        load([path,'stn_code_data/stn_code_data_',num2str(yr),'_',num2str(mm,'%02i'),'.mat']);
        stn_yr=[stn_yr;stn_mm];
    end
    save([path, 'stn_code_data/stn_code_data_',num2str(yr),'_2.mat'],'stn_yr','-v7.3');
    disp(yr)
end

