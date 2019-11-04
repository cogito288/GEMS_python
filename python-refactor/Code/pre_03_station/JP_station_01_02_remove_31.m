clear all; close all; clc

tic

try
    path_data = '//10.72.26.56/irisnas5/Data/';
    cd(path_data)
catch
    path_data = '/share/irisnas5/Data/';
    cd(path_data)
    addpath(genpath('/share/irisnas5/Data/matlab_func/'))
end

% tg = {'SO2','NO','NO2','NOX','CO','OX','NMHC','CH4','THC','SPM','PM25','CO2'};
tg = {'HUM','NETR','PRS','RAIN','SUN','TEMP','UV','WD','WS'};

%% 
%2012³â CO2 ¾øÀ½.
for yr=2009:2016
    for i = 1:9
        eval(['load([path_data,''Station/Station_JP/byPollutant/fail/JP_stn',tg{i},'_'',num2str(yr)])']);
        eval(['stn = table2array(stn',tg{i},'_tbl);']);
        stn(stn(:,8)>=9997,8) = NaN;
        
        if mod(yr,4)==0
            stn(stn(:,3)==2&stn(:,4)>29,:)=[];
        else
            stn(stn(:,3)==2&stn(:,4)>28,:)=[];
        end
        
        stn(stn(:,3)==4&stn(:,4)==31,:)=[];
        stn(stn(:,3)==6&stn(:,4)==31,:)=[];
        stn(stn(:,3)==9&stn(:,4)==31,:)=[];
        stn(stn(:,3)==11&stn(:,4)==31,:)=[];
        
        eval(['stn',tg{i},'_tbl = array2table(stn,''VariableNames'',stn',tg{i},'_tbl.Properties.VariableNames);']);
        eval(['save([path_data,''Station/Station_JP/byPollutant/JP_stn',tg{i},'_'',num2str(yr)],''stn',tg{i},'_tbl'')']);
        clearvars stn*
        disp([num2str(yr),'_',tg{i}])
    end % i
end % yr
toc