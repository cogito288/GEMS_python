clear all; close all; clc

tic

path_insiu = '//10.72.26.46/irisnas6/Data/In_situ/AirQuality_SouthKorea/';
path = '//10.72.26.56/irisnas5/Data/Station/Station_Korea/';

% path_data = '/share/irisnas2/Data/Aerosol/';
% path = '/share/irisnas5/Data/Station/Station_Korea/';

% addpath(genpath('/share/irisnas5/Data/matlab_func/'))

%% 2005-2013 (xlsx, PM2.5없음)
for yr=2005:2013 
data = [];
for i=1:4
    [num,txt,raw] = xlsread([path_insiu,num2str(yr),'/',num2str(yr),'년',num2str(i,'%02i'),'분기.xlsx']);
    data_temp = txt(2:end,3:9);
    data = [data;data_temp];
end

dvec = datevec(data(:,2),'yyyymmddHH');
data_datenum = datenum(data(:,2),'yyyymmddHH');
doy_000 = datenum([yr,0,0,0,0,0]);
data_doy = floor(data_datenum-doy_000);

data = str2double(data);
data(data<0)=NaN;

ndata = [data_doy,dvec(:,1:4),data(:,3:end),NaN(size(data_doy)),data(:,1)];
% doy, yr, mon, day, time, SO2, CO, O3, NO2, PM10, (PM25), scode

save([path,'stn_code_data/stn_code_data_',num2str(yr)],'ndata','-v7.3')
end


%% 2014-2016 (csv, PM2.5 컬럼 있음)
for yr=2014:2016 
data = [];
for i=1:4
    [num,txt,raw] = xlsread([path_insiu,num2str(yr),'/',num2str(yr),'년',num2str(i),'분기.csv']);
    data_temp = raw(2:end,[2,4:10]);
    data = [data;data_temp];
end

data = cell2mat(data);
data(data<0)=NaN;

dstr = num2str(data(:,2));
dvec = datevec(dstr,'yyyymmddHH');
data_datenum = datenum(dstr,'yyyymmddHH');
doy_000 = datenum([yr,0,0,0,0,0]);
data_doy = floor(data_datenum-doy_000);

ndata = [data_doy,dvec(:,1:4),data(:,3:end),data(:,1)];
% doy, yr, mon, day, time, SO2, CO, O3, NO2, PM10, (PM25), scode

save([path,'stn_code_data/stn_code_data_',num2str(yr)],'ndata','-v7.3')
end

%% 2017-2018 2분기 (xlsx, PM2.5 있음)
for yr=2018 %2017:2018
data = [];
for i=1:4
    [num,txt,raw] = xlsread([path_insiu,num2str(yr),'/',num2str(yr),'년 ',num2str(i),'분기.xlsx']);
    data_temp = raw(2:end,[2,4:10]);
    data = [data;data_temp];
end

data_1 =  str2double(data(:,1));
data_2 = cell2mat(data(:,2:end));
data = [data_1, data_2];
data(data<0)=NaN;

dstr = num2str(data(:,2));
dvec = datevec(dstr,'yyyymmddHH');
data_datenum = datenum(dstr,'yyyymmddHH');
doy_000 = datenum([yr,0,0,0,0,0]);
data_doy = floor(data_datenum-doy_000);

ndata = [data_doy,dvec(:,1:4),data(:,3:end),data(:,1)];
% doy, yr, mon, day, time, SO2, CO, O3, NO2, PM10, (PM25), scode

save([path,'stn_code_data/stn_code_data_',num2str(yr)],'ndata','-v7.3')
end

%% 2018 3분기 - 4분기 (xlsx, PM2.5있음.. 근데 중간에 망 정보가 들어가면서 컬럼 위치가 변경됨)
i=4;
[num,txt,raw] = xlsread([path_insiu,num2str(yr),'/',num2str(yr),'년 ',num2str(i),'분기.xlsx']);
data_temp = raw(2:end,[3,5:11]);
data = [data;data_temp];

%% 201810_201904 
data = [];
[num,txt,raw] = xlsread([path_insiu,'201810_201904/201810_201904_pt1.csv']);
data_temp = raw(2:end,[2,6:7,10,9,8,11,12]);
data = [data;data_temp];

[num,txt,raw] = xlsread([path_insiu,'201810_201904/201810_201904_pt2.csv']);
data_temp = raw(2:end,[2,6:7,10,9,8,11,12]);
data = [data;data_temp];

data = cell2mat(data);
data(data<0)=NaN;

dstr = num2str(data(:,2));
dvec = datevec(dstr,'yyyymmddHH');
yr=2019;
yr_idx = dvec(:,1)==yr;
dvec=dvec(yr_idx,:);
dstr=dstr(yr_idx,:);
data=data(yr_idx,:);
data_datenum = datenum(dstr,'yyyymmddHH');

doy_000 = datenum([yr,0,0,0,0,0]);
data_doy = floor(data_datenum-doy_000);

ndata = [data_doy,dvec(:,1:4),data(:,3:end),data(:,1)];
% doy, yr, mon, day, time, SO2, CO, O3, NO2, PM10, (PM25), scode

save([path,'stn_code_data/stn_code_data_',num2str(yr)],'ndata','-v7.3')


%% 12월 31일 24시 -> 1월 1일 00시 
path = '/share/irisnas5/Data/Station/Station_Korea/';

yr=2005;
load([path,'stn_code_data/stn_code_data_',num2str(yr)]);
data_mv = ndata(ndata(:,2)==(yr+1),:);
doy_unq = unique(data_mv(:,1))

% if length(doy_unq)==1
    data_mv(:,1)=1;
% else
%     stop
% end

ndata(ndata(:,2)==(yr+1),:)=[];
save([path,'stn_code_data/stn_code_data_',num2str(yr)],'ndata','-v7.3')

for yr=2016:2017 %2006:2017
load([path,'stn_code_data/stn_code_data_',num2str(yr)]);
ndata = [data_mv; ndata];
data_mv = ndata(ndata(:,2)==(yr+1),:);
doy_unq = unique(data_mv(:,1))

if length(doy_unq)==1
    data_mv(:,1)=1;
    ndata(ndata(:,2)==(yr+1),:)=[];
    save([path,'stn_code_data/stn_code_data_',num2str(yr)],'ndata','-v7.3')
else
    stop
end

end

save([path,'stn_code_data/stn_code_data_',num2str(yr),'_001_00'],'data_mv','-v7.3')



