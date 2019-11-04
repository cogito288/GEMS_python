clear all; close all; clc

path = 'C:\Temp\jp_stn_copy';

% header = {'doy','year','month','day','KST','SO2','CO','O3','NO2','PM10','PM25','scode'};
pcode = {'01','SO2','ppb';'02','NO','ppb';'03','NO2','ppb';'04','NOX','ppb';'05','CO','x01ppm';...
    '06','OX','ppb';'07','NMHC','x10ppbc';'08','CH4','x10ppbc';'09','THC','x10ppbc';...
    '10','SPM','ug_m3';'12','PM25','ug_m3';...
    '21','WD','x16DIRC';'22','WS','x01m_s';'23','TEMP','x01degC';'24','HUM','percent';...
    '25','SUN','x001MJ';'26','RAIN','mm';'27','UV','x001MJ';'28','PRS','mb';'29','NETR','x001MJ';...
    '41','CO2','x01ppm';'42','O3','ppb';};

% '43','HCL'; '44','HF'; '45','H2S'; '46','SHC'; '47','UHC'

% p=1; varname = 'SO2';
% p=2; varname = 'NO';
% p=3; varname = 'NO2';
% p=4; varname = 'NOX';
% p=5; varname = 'CO';
% p=6; varname = 'OX';
% p=7; varname = 'NMHC';
% p=8; varname = 'CH4';
% p=9; varname = 'THC';
% p=10; varname = 'SPM';
% p=12; varname = 'PM25'; p=51;
% p=21; varname = 'WD';
% p=22; varname = 'WS';
% p=23; varname = 'TEMP';
% p=24; varname = 'HUM';
% p=25; varname = 'SUN';
% p=26; varname = 'RAIN';
% p=27; varname = 'UV';
% p=28; varname = 'PRS';
% p=29; varname = 'NETR';
% p=41; varname = 'CO2';
% p=42; varname = 'O3';
varname = 'PM25'; p=51;

header_p = {'doy','year','month','day','scode','ccode','KST',['stn',varname]};
% '측정년도/측정국코드/시도코드/측정항목코드/측정단위코드/측정월/측정일'

for yr=2009:2009%2016
cd([path,'/',num2str(yr)])

list = dir(['*_',num2str(p,'%02i'),'.txt']);
list = {list.name}';

data=[];
for k=1:length(list)
    data_temp = readtable(list{k});
    data=[data;data_temp];
end

% data_p = table2cell(data(:,4));
% aa = ismember(data_p,data_p(1));
% sum(aa)==size(data,1)
% 
% data_unit = table2cell(data(:,5));
% bb = ismember(data_unit,data_unit(1));
% sum(bb)==size(data,1)

if p = 12
    vv = table2cell(data(:,4));
    idx_PM25 = ismember(vv,{'PM25'});
    idx_PMBH = ismember(vv,{'PMBH'});
    idx_PMFL = ismember(vv,{'PMFL'});
    data_PMBH = data(idx_PMBH,:);
    data_PMFL = data(idx_PMFL,:);
    data = data(idx_PM25,:);
end

data(:,4:5)=[];

data = table2array(data);
yrmonday = data(:,1)*10000 + data(:,4)*100 + data(:,5);
data_datenum = datenum(num2str(yrmonday),'yyyymmdd');
doy_000 = datenum([yr,0,0,0,0,0]);
data_doy = data_datenum-doy_000;

data_info = [data_doy,data(:,1),data(:,4),data(:,5),data(:,2:3)]; % 'doy','year','month','day','scode','ccode'
data_new = [];
for KST = 1:24
    data_temp = data_info;
    data_temp(:,7)=KST;
    data_temp = [data_temp, data(:,5+KST)];
    data_new=[data_new;data_temp];
end

eval(sprintf(['stn',varname,'_tbl = array2table(data_new,''VariableNames'',header_p);']));
eval(sprintf(['save([path,''/JP_stn',varname,'_'',','num2str(yr)],''stn',varname,'_tbl'')']))
% stnPM25_tbl = array2table(data_new,'VariableNames',header_p);
% save([path,'/JP_stnPM25_',num2str(yr)],'stnPM25_tbl')

end