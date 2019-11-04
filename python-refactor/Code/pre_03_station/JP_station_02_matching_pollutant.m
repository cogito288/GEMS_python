clear all; close all; clc

path = '//10.72.26.56/irisnas5/Data/Station/Station_JP/';
cd(path)

data_tbl = readtable('stn_code_ing/jp_stn_code_lonlat_period_year.csv');
data = table2array(data_tbl);
info_tbl=readtable('stn_code_ing/measured_pollutant_by_stn.csv');
info_tbl = info_tbl(:,{'Year','scode','SO2','CO','OX','NO2','SPM','PM25','NO','NOX','NMHC','CH4'});
info = table2array(info_tbl);
info(isnan(info))=0;

for k=1:size(data,1)
    data(k,8:13)=info(info(:,1)==data(k,7) & info(:,2)==data(k,1),3:8);
end

a = sum(data(:,8:13),2);
aidx=a==0;
data2 = [data(:,1:7),aidx];