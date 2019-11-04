clear all; close all; clc

tic

% path_data = '//10.72.26.56/irisnas5/Data/';
path_data = '/share/irisnas5/Data/';
path_stn_kor = [path_data,'Station/Station_Korea/'];
addpath(genpath('/share/irisnas5/Data/matlab_func/'))

stn_info = csvread([path_data,'Station/Station_Korea/stn_code_lonlat_period_2005_201904.csv'],1);
% scode1, scode2, lon, lat, op_start, op_end

%% read raw files
header_ndata = {'doy','yr','mon','day','KST','SO2','CO','O3','NO2','PM10','PM25','scode','scode2'};

%% stn_scode_data for South Korea
for yr=2008:2009 %2005:2019
    if yr==2019
        ndata=importdata([path_stn_kor,'stn_code_data/stn_code_data_2019_010100_042300.mat']);
    else
        ndata=importdata([path_stn_kor,'stn_code_data/stn_code_data_',num2str(yr),'.mat']);
    end
        
    ndata(:,13)=0; % add column for scode2
    ndata_scode = [];
    ndata(ndata<0)=NaN;
    
% Assign scode2
for j=1:size(stn_info,1)
    ndata_temp = ndata(ndata(:,12)==stn_info(j,1),:);
    for k = 1:12
        ndata_temp2 = ndata_temp(ndata_temp(:,3)==k,:);
        if isempty(ndata_temp2)==0
            yrmon = yr*100+k;
            idx = (stn_info(j,5)<=yrmon)&(stn_info(j,6)>yrmon);
            if idx==1
                ndata_temp2(:,13)=stn_info(j,2);
                ndata_scode=[ndata_scode;ndata_temp2];
            end
        end
    end
    disp([num2str(j),'/',num2str(size(stn_info,1))])
end
save([path_stn_kor,'stn_scode_data_',num2str(yr)],'ndata_scode','header_ndata','-v7.3')
end

toc

