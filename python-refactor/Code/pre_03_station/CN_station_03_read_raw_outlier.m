clear all; close all; clc

tic
% 
% path_data = '//10.72.26.56/irisnas5/Data/';

path_data = '/share/irisnas5/Data/';
path = '/share/irisnas5/Data/Station/Station_CN/';
% addpath(genpath('/share/irisnas5/Data/matlab_func/'))

stn_info_cn = csvread([path_data,'Station/Station_CN/cn_stn_code_lonlat_period.csv'],1);
% scode1, scode2, lon, lat, op_start, op_end

%% read files 서희가 만든 china stn 파일 불러와서 년도별로 파일 묶기
% header_ndata = {'doy','yr','mon','day','CST','AQI','PM25','PM25_24h',...
%     'PM10','PM10_24h','SO2','SO2_24h','NO2','NO2_24h','O3','O3_24h',...
%     'O3_8h','O3_8h_24h','CO','CO_24h','scode'};
% 
% for yr=2015:2016
%     cd([path_data,'Station_CN/rm_outlier/',num2str(yr)])
%     list = dir('*.mat');
%     list = {list.name}';
%     
%     ndata = [];
%     for k = 1:length(list)
%         load(list{k}) %stn_CN
%         ndata = [ndata; stn_CN];
%         disp(list{k})
%     end
%     save([path_data,'Station_CN/stn_code_data/stn_code_data_rm_outlier_',num2str(yr)],'ndata','header_ndata','-v7.3')
% end

% list15=dir('stn_code_data_rm_*2015*');
% list15={list15.name}';
% ndata = importdata(list15{1});
% for k=2:length(list15)
%     load(list15{k})
%     ndata=[ndata;stn_CN];
% end
% save([path_data,'Station_CN/stn_code_data/stn_code_data_rm_outlier_',num2str(yr)],'ndata','header_ndata','-v7.3')
% 
% list16=dir('stn_code_data_rm_*2016*');
% list16={list16.name}';
% ndata = importdata(list16{1});
% for k=2:length(list16)
%     load(list16{k})
%     ndata=[ndata;stn_CN];
% end
% save([path_data,'Station_CN/stn_code_data/stn_code_data_rm_outlier_',num2str(yr)],'ndata','header_ndata','-v7.3')

%% stn_scode_data for China
header_ndata = {'doy','yr','mon','day','CST','AQI','PM25','PM25_24h',...
    'PM10','PM10_24h','SO2','SO2_24h','NO2','NO2_24h','O3','O3_24h',...
    'O3_8h','O3_8h_24h','CO','CO_24h','scode','scode2'};

for yr=2019 %2015:2019
ndata=importdata([path_data,'Station/Station_CN/stn_code_data/stn_code_data_rm_outlier_',num2str(yr),'.mat']);
ndata(:,end+1)=0;

ndata_scode = [];
% Assign scode2
for j=1:size(stn_info_cn,1)
    ndata_temp = ndata(ndata(:,end-1)==stn_info_cn(j,1),:);
    for k = 1:5 %%%%%%%%%%%%%%%%%%
        ndata_temp2 = ndata_temp(ndata_temp(:,3)==k,:);
        if isempty(ndata_temp2)==0
            yrmon = yr*100+k;
            idx = (stn_info_cn(j,5)<=yrmon)&(stn_info_cn(j,6)>=yrmon);
            if idx==1
                ndata_temp2(:,end)=stn_info_cn(j,2);
                ndata_scode=[ndata_scode;ndata_temp2];
            end
        end
    end
    if mod(j,100)==0
        save([path,'stn_scode_data_',num2str(yr),'_',num2str(j-99,'%04i'),'.mat'],'ndata_scode','-v7.3')
        ndata_scode = [];
    elseif j==size(stn_info_cn,1)
        save([path,'stn_scode_data_',num2str(yr),'_1501.mat'],'ndata_scode','-v7.3')
    end

    disp([num2str(j),'/',num2str(size(stn_info_cn,1))])
end

ndata_scode = [];
for k = 1:100:1501
    ndata_scode_temp = importdata([path,'stn_scode_data_',num2str(yr),'_',num2str(k,'%04i'),'.mat']);
    ndata_scode = [ndata_scode; ndata_scode_temp];
end
save([path,'stn_scode_data/cn_stn_scode_data_rm_outlier_',num2str(yr)],'ndata_scode','header_ndata','-v7.3')

disp(yr)
end

toc

