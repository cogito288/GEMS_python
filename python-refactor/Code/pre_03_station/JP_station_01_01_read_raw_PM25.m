clear all; close all; clc

path = 'C:\Temp\jp_stn_org';

% header = {'doy','year','month','day','KST','SO2','CO','O3','NO2','PM10','PM25','scode'};
% pcode = {'01','SO2','ppb';'02','NO','ppb';'03','NO2','ppb';'04','NOX','ppb';'05','CO','x01ppm';...
%     '06','OX','ppb';'07','NMHC','x10ppbc';'08','CH4','x10ppbc';'09','THC','x10ppbc';...
%     '10','SPM','ug_m3';'12','PM25','ug_m3';...
%     '21','WD','x16DIRC';'22','WS','x01m_s';'23','TEMP','x01degC';'24','HUM','percent';...
%     '25','SUN','x001MJ';'26','RAIN','mm';'27','UV','x001MJ';'28','PRS','mb';'29','NETR','x001MJ';...
%     '41','CO2','x01ppm';'42','O3','ppb';};

% '43','HCL'; '44','HF'; '45','H2S'; '46','SHC'; '47','UHC'

p=12; varname = 'PM25'; % p=51;

header_p = {'doy','year','month','day','scode','ccode','KST',['stn',varname]};
% '측정년도/측정국코드/시도코드/측정항목코드/측정단위코드/측정월/측정일'

stnPM25 = table2array(stnPM25_tbl_old_09);
stn_unq_09 = unique(stnPM25(:,[1,5,7]),'rows'); yr=2009;

% for yr=2015:2015%2016
cd([path,'/',num2str(yr)])

list = dir(['*_',num2str(p,'%02i'),'.txt']);
list = {list.name}';

data=[];
for k=1:length(list)
    data_temp = readtable(list{k});
    data=[data;data_temp];
end

data_org = data;
% data_unq = unique(data_org(:,[2,6,7]),'rows');

data_p = table2cell(data(:,4));
idx_PM25 = ismember(data_p,{'PM25'});
idx_PMBH = ismember(data_p,{'PMBH'});
idx_PMFL = ismember(data_p,{'PMFL'});

% data_unit = table2cell(data(:,5));
% bb = ismember(data_unit,data_unit(1));
% sum(bb)==size(data,1)

data(:,4:5)=[];

data = table2array(data);

% test1
data_PMBH = data(idx_PMBH,:);
data_PMFL = data(idx_PMFL,:);
data_PM25 = data(idx_PM25,:);
data_PMBH_unq = unique(data_PMBH(:,[2,4,5]),'rows');
data_PMFL_unq = unique(data_PMFL(:,[2,4,5]),'rows');
data_PM25_unq = unique(data_PM25(:,[2,4,5]),'rows');
% test2
stn_unq_PMFL = unique(data_PMFL(:,2));
stn_unq_PMBH = unique(data_PMBH(:,2));
stn_unq_PM25 = unique(data_PM25(:,2));
a = ismember(stn_unq_PMFL,stn_unq_PM25); sum(a)
stn_unq_PMFL(a)
a_PM25 = data_PM25(data_PM25(:,2)==27115010,:);
a_PMFL = data_PMFL(data_PMFL(:,2)==27115010,:);

b = ismember(stn_unq_PMBH,stn_unq_PM25); sum(b)
c = ismember(stn_unq_PMFL,stn_unq_PMBH); sum(c)

a2 = ismember(stn_unq_PM25,stn_unq_PMFL); sum(a2)
b2 = ismember(stn_unq_PM25,stn_unq_PMBH); sum(b2)
c2 = ismember(stn_unq_PMBH,stn_unq_PMFL); sum(c2)

% PM25, PMBH 두개다 있는 스테이션값 중에서 PMBH로 측정한거 다 제거
% idx_rm = idx_PMBH & ismember(data(:,2),27115010); % 2015-2016
idx_rm = idx_PMFL & ismember(data(:,2),27115010); % 2011-2014
data(idx_rm,:)=[];

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

if mod(yr,4)==0
    data_new(data_new(:,3)==2&data_new(:,4)>29,:)=[];
else
    data_new(data_new(:,3)==2&data_new(:,4)>28,:)=[];
end

data_new(data_new(:,3)==4&data_new(:,4)==31,:)=[];
data_new(data_new(:,3)==6&data_new(:,4)==31,:)=[];
data_new(data_new(:,3)==9&data_new(:,4)==31,:)=[];
data_new(data_new(:,3)==11&data_new(:,4)==31,:)=[];

stnPM25_tbl = array2table(data_new,'VariableNames',header_p);
save([path,'/JP_stnPM25_',num2str(yr)],'stnPM25_tbl')

% end