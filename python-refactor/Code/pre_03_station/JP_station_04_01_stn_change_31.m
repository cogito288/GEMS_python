clear all; close all; clc

tic

% path_data = '//10.72.26.56/irisnas5/Data/';
% path = '//10.72.26.56/irisnas5/GEMS/EA_GOCI6km/';

path_data = '/share/irisnas5/Data/';
% path = '/share/irisnas5/GEMS/EA_GOCI6km/';
%
% addpath(genpath('/share/irisnas5/Data/matlab_func/'))

% stn_info = csvread([path_data,'Station/Station_JP/jp_stn_code_lonlat_period_filtered_yyyymmdd.csv'],1);
% scode1, scode2, lon, lat, op_start, op_end

yr=2009;
load([path_data,'Station/Station_JP/jp_stn_scode_data_',num2str(yr)])

% header_ndata = {'doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode','scode2'};

%% byPollutant 파일 불러와서, 바꿔야하는 날짜들에 해당하는 행만 뽑아놓고 나머진 지우기
if mod(yr,4)==0
    doy_chg = [61,62,122,183,275,336];
else
    doy_chg = [60,61,62,121,182,274,335];
end

tg = {'SO2','CO','OX','NO2','SPM','PM25'};
for i=1:6
    eval(['load([path_data,''Station/Station_JP/byPollutant/JP_stn',tg{i},'_'',num2str(yr)])']);
    eval(['stn = table2array(stn',tg{i},'_tbl);']);
    stn_sub = stn(ismember(stn(:,1),doy_chg),:);
    eval(['stn',tg{i},'= stn_sub;']);
    clearvars *_tbl
end
stnPM10 = stnSPM;
clearvars stn stn_sub stnSPM
    
%% scode2 할때 하나 기간 잘못입력해서 삭제해줘야하는 샘플 지우기
if yr==2016
ndata_scode(ndata_scode(:,1)==90&ndata_scode(:,13)==281090100,:)=[];
ndata_scode(ndata_scode(:,1)==91&ndata_scode(:,13)==281090100,:)=[];
end

%%
chg_idx = find(ismember(ndata_scode(:,1),doy_chg));

% load([path_data,'Station/Station_JP/jp_stn_scode_data_change_',num2str(yr)])
% 9997 이상 제거하는거 다음번에 돌릴땐 넣어야할듯

for kk = 1:length(chg_idx)
    k = chg_idx(kk);
    aSO2 = stnSO2(stnSO2(:,1)==ndata_scode(k,1)&stnSO2(:,7)==ndata_scode(k,5)&stnSO2(:,5)==ndata_scode(k,12),8);
    aCO = stnCO(stnCO(:,1)==ndata_scode(k,1)&stnCO(:,7)==ndata_scode(k,5)&stnCO(:,5)==ndata_scode(k,12),8);
    aOX = stnOX(stnOX(:,1)==ndata_scode(k,1)&stnOX(:,7)==ndata_scode(k,5)&stnOX(:,5)==ndata_scode(k,12),8);
    aNO2 = stnNO2(stnNO2(:,1)==ndata_scode(k,1)&stnNO2(:,7)==ndata_scode(k,5)&stnNO2(:,5)==ndata_scode(k,12),8);
    aPM10 = stnPM10(stnPM10(:,1)==ndata_scode(k,1)&stnPM10(:,7)==ndata_scode(k,5)&stnPM10(:,5)==ndata_scode(k,12),8);
    aPM25 = stnPM25(stnPM25(:,1)==ndata_scode(k,1)&stnPM25(:,7)==ndata_scode(k,5)&stnPM25(:,5)==ndata_scode(k,12),8);
    
    if isempty(aSO2)==0; ndata_scode(k,6) = aSO2; else; ndata_scode(k,6)=NaN; end
    if isempty(aCO)==0; ndata_scode(k,7) = aCO; else; ndata_scode(k,7)=NaN;end
    if isempty(aOX)==0; ndata_scode(k,8) = aOX; else; ndata_scode(k,8)=NaN;end
    if isempty(aNO2)==0; ndata_scode(k,9) = aNO2; else; ndata_scode(k,9)=NaN;end
    if isempty(aPM10)==0; ndata_scode(k,10) = aPM10; else; ndata_scode(k,10)=NaN;end
    if isempty(aPM25)==0; ndata_scode(k,11) = aPM25; else; ndata_scode(k,11)=NaN;end
    
    if mod(kk,10)==0
    disp([num2str(kk),' / ',num2str(length(chg_idx))])
    end
end

save([path_data,'Station/Station_JP/jp_stn_scode_data_change_',num2str(yr)],'ndata_scode','header_ndata')

toc
