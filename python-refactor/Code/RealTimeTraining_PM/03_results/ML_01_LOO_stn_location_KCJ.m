clear all; clc, close all

% path_data = '//10.72.26.56/irisnas5/Data/';
% path = '//10.72.26.56/irisnas5/GEMS/PM/00_EA6km/';
% addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'))

path_data = '/share/irisnas5/Data/';
path = '/share/irisnas5/GEMS/PM/00_EA6km/';
addpath(genpath('/share/irisnas5/Data/matlab_func/'))

% path_data = '/Volumes/irisnas5/Data/';
% path = '/Volumes/irisnas5/GEMS/PM/00_EA6km/';
% addpath(genpath('/Volumes/irisnas5/Data/matlab_func/'))

%% Stations location information
load([path_data,'Station/Station_CN/cn_stn_GOCI6km_location_weight.mat'])
load([path_data,'Station/Station_Korea/stn_GOCI6km_location_weight_v2018.mat'])
load([path_data,'Station/Station_JP/jp_stn_GOCI6km_location_weight.mat'])
stn_6km_location = [stn_GOCI6km_location; jp_stn_GOCI6km_location; cn_stn_GOCI6km_location];
cn_dup_scode2_GOCI6km(:,end+1:size(jp_dup_scode2_GOCI6km,2))=0;
dup_scode2_GOCI6km(:,end+1:size(jp_dup_scode2_GOCI6km,2))=0;
dup_scode2_6km =[dup_scode2_GOCI6km; cn_dup_scode2_GOCI6km; jp_dup_scode2_GOCI6km];

clear stn_GOCI6km_location cn_stn_GOCI6km_location jp_stn_GOCI6km_location cn_dup_scode2_GOCI6km dup_scode2_GOCI6km jp_dup_scode2_GOCI6km header_cn_stn_GOCI6km_location header_jp_stn_GOCI6km_location

%% Read data
target = {'PM10','PM25'};
type = {'conc','time','time_conc'};

for t=1:3
    for i=1:2
        data_LOO = [];
        if i==1
            header = {'station_PM10','estimated_PM10','stn_num','doy','time','year','file_num'};
            header2 = {'RF_PM10_ovr','STN_PM10','stn_num'};
        else
            header = {'station_PM25','estimated_PM25','stn_num','doy','time','year','file_num'};
            header2 = {'RF_PM25_ovr','STN_PM25','stn_num'};
        end
        for yr = 2015:2016
            if mod(yr,4)==0
                days = 366;
            else
                days = 365;
            end
            
            for doy=1:days
                [yy, mm, dd] = datevec(datenum(yr,1,doy));
                try
                    list_val_rf = dir([path, 'LOO/',type{t},'/RF/',target{i},'/rf_',target{i},'_RTT_EA6km_',num2str(yr),...
                        '_',num2str(doy, '%03i'),'*_LOO_*_val_ranger.csv']);
                    list_val_mat = dir([path, 'LOO/',type{t},'/dataset/',target{i},'/',target{i},'_RTT_EA6km_',num2str(yr),...
                        '_',num2str(doy, '%03i'),'*_LOO_*_val*.mat']);
                    
                    RF_LOO_val = []; stn_val = [];
                    data_val=[];
                    for f = 1:length(list_val_rf)
                        load([path,'/LOO/',type{t},'/dataset/',target{i},'/',list_val_mat(f).name]);
                        val_selected = val_10_fold(find(val_10_fold(:,end-1)==0),(end-6:end-2));
                        val_selected(:,end+1) = f;
                        stn_val = [stn_val; val_selected];
                        
                        RF_LOO_val_tmp = csvread([path, 'LOO/',type{t},'/RF/',target{i},'/',list_val_rf(f).name],1,1);
                        RF_LOO_val = [RF_LOO_val; RF_LOO_val_tmp];
                        disp(f)
                    end
                    clearvars stn_val_tmp  rf_val_tmp
                    
                    data_val(:,[1,3:7]) = stn_val(:,[1,2:6]);
                    data_val(:,2) = RF_LOO_val; %stn_PM, rf_PM stn_num, doy, time, year
                    
                    data_val(data_val==-9999)=NaN;
                    nanidx_val = isnan(data_val);
                    nanidx_val = sum(nanidx_val,2);
                    data_val = data_val(nanidx_val==0,:);
                    
                    data_LOO=[data_LOO; data_val];
                    disp(doy)
                    
                catch
                end
            end
        end
        csvwrite_with_headers2([path,'LOO/',type{t},'/stn_location/',type{t},'_',target{i},...
            '_compare_RF_LOO_EA6km_val_stn_ovr_new3.csv'],data_LOO,header,0,0,'%7.7f');

    end
end
