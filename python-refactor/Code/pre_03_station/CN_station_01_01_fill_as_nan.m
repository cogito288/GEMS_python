clear all; close all; clc

tic
% 
path_data = '//10.72.26.46/irisnas6/Data/Aerosol/';
path = '//10.72.26.46/irisnas6/Work/Aerosol/';

% path_data = '/share/irisnas6/Data/Aerosol/';
% path = '/share/irisnas6/Work/Aerosol/';
% 
% addpath(genpath('/share/irisnas6/Work/Aerosol/matlab_func/'))

stn_info_cn = csvread([path_data,'Station_CN/cn_stn_code_lonlat_period.csv'],1);
% scode1, scode2, lon, lat, op_start, op_end

%% read files 서희가 만든 china stn 파일 불러와서 빈 날짜 시간 nan으로 채우기
% header_ndata = {'doy','yr','mon','day','CST','AQI','PM25','PM25_24h',...
%     'PM10','PM10_24h','SO2','SO2_24h','NO2','NO2_24h','O3','O3_24h',...
%     'O3_8h','O3_8h_24h','CO','CO_24h','scode'};

yr=2015;
load([path_data,'Station_CN/stn_code_data/stn_code_data_rm_outlier_',num2str(yr)])
unq_doy = unique(ndata(:,1)); % 1, 262, 비었음
unq_scode = unique(ndata(:,21));
aa = nan(length(unq_scode),21);
aa(:,2)=yr; aa(:,21)=unq_scode;

% doy1
aa1=aa;
aa1(:,[1,3:4])=1;
ndata_doy1=[];
for CST=8:15
    aa1_temp = aa1;
    aa1_temp(:,5)=CST;
    ndata_doy1=[ndata_doy1;aa1_temp];
end

% doy 262
aa2=aa;
aa2(:,1)=262; aa2(:,3)=9; aa2(:,4)=19;
ndata_doy262=[];
temp_tbl = readtable('Z:\In_situ\AirQuality_China\china_sites\2015/china_sites_20150919.csv');
scode_char = temp_tbl.Properties.VariableNames(4:end)';
scode_char = char(scode_char);
scode_num = str2num(scode_char(:,2:5));
aa2(:,21) = scode_num;

temp=table2array(temp_tbl(:,[2,4:end]));
for CST=8:15
    aa2_temp = aa2;
    aa2_temp(:,5)=CST;
    
    temp2 = temp(temp(:,1)==CST,2:end);
    temp2 = temp2';
    
    if isempty(temp2)==0
        aa2_temp(:,6:20)=temp2;
    end
    
    ndata_doy262 = [ndata_doy262; aa2_temp];
end
  
ndata_1 = ndata(ndata(:,1)<262,:);
ndata_2 = ndata(ndata(:,1)>262,:);
ndata = [ndata_doy1; ndata_1; ndata_doy262; ndata_2];

% temp = csvread([path_data,'Station_CN/temp262.csv'],1);

list16=dir('stn_code_data_rm_*2016*');
list16={list16.name}';
ndata = importdata(list16{1});
for k=2:length(list16)
    load(list16{k})
    ndata=[ndata;stn_CN];
end
save([path_data,'Station_CN/stn_code_data/stn_code_data_rm_outlier_',num2str(yr)],'ndata','header_ndata','-v7.3')
