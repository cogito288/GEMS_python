clear all; close all; clc

tic

% path_data = '//10.72.26.56/irisnas5/Data/';

path_data = '/share/irisnas5/Data/';
path = '/share/irisnas5/Data/Station/Station_JP/';
% addpath(genpath('/share/irisnas6/Work/Aerosol/matlab_func/'))

stn_info = csvread([path,'jp_stn_code_lonlat_period_filtered_yyyymmdd.csv'],1);
% scode1, scode2, lon, lat, op_start, op_end

%% read stn_code_data file
header_ndata = {'doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode','scode2'};

yr=2019;
ndata = importdata([path,'stn_code_data/stn_code_data_rm_outlier_',num2str(yr),'_rm.mat']);
% ndata(:,12:13)=[]; % O3, NOX
ndata(ndata==-9999)=NaN;

%% stn_scode_data for Japan

ndata(:,13)=0; % add column for scode2

ndata_scode = [];
% Assign scode2
for j=1:size(stn_info,1)
    ndata_temp = ndata(ndata(:,12)==stn_info(j,1),:);
    for k = 1:5 %%%%%%%%%%%%
        for dd = 1:31
            ndata_temp2 = ndata_temp(ndata_temp(:,3)==k & ndata_temp(:,4)==dd,:);
            if isempty(ndata_temp2)==0
                yyyymmdd = yr*10000+k*100+dd;
                idx = (stn_info(j,5)<yyyymmdd)&(stn_info(j,6)>=yyyymmdd);
                if idx==1
                    ndata_temp2(:,end)=stn_info(j,2);
                    ndata_scode=[ndata_scode;ndata_temp2];
                end
            end
        end
    end
    if mod(j,100)==0
        save([path,'stn_scode_data_',num2str(yr),'_',num2str(j-99,'%04i'),'.mat'],'ndata_scode','-v7.3')
        ndata_scode = [];
    elseif j==size(stn_info,1)
        save([path,'stn_scode_data_',num2str(yr),'_2401.mat'],'ndata_scode','-v7.3')
    end
    
    disp([num2str(j),'/',num2str(size(stn_info,1))])
end

ndata_scode = [];
for k = 1:100:2401
    fname = [path,'stn_scode_data_',num2str(yr),'_',num2str(k,'%04i'),'.mat'];
    ndata_scode_temp = importdata(fname);
    ndata_scode = [ndata_scode; ndata_scode_temp];
end
save([path,'jp_stn_scode_data_rm_outlier_',num2str(yr)],'ndata_scode','header_ndata','-v7.3')

for k = 1:100:2401
    fname = [path,'stn_scode_data_',num2str(yr),'_',num2str(k,'%04i'),'.mat'];
    delete(fname)
end

toc

%% stack
% yr=2009;
% for k=1401:1416
%     ndata_scode(ndata_scode(:,13)==stn_info(k,2),:)=[];
% end
% ndata_scode_all=ndata_scode;
% save([path_data,'Station_JP/stn_scode_data_',num2str(yr),'_1_1400'],'ndata_scode_all','header_ndata','-v7.3')
% load([path_data,'Station_JP/stn_scode_data_',num2str(yr),'_1_1400']);
% load([path_data,'Station_JP/stn_scode_data_',num2str(yr),'_1401_1700']);
% ndata_scode_all = [ndata_scode_all;ndata_scode];
% load([path_data,'Station_JP/stn_scode_data_',num2str(yr),'_1701_2000']);
% ndata_scode_all = [ndata_scode_all;ndata_scode];
% load([path_data,'Station_JP/stn_scode_data_',num2str(yr),'_2001_end']);
% ndata_scode_all = [ndata_scode_all;ndata_scode];
% ndata_scode=ndata_scode_all;
% save([path_data,'Station_JP/stn_scode_data_',num2str(yr)],'ndata_scode','header_ndata','-v7.3')
% 
