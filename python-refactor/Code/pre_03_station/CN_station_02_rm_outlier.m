clear all;clc; close all;

tic 

% % for local 
% path = '//10.72.26.56/irisnas5/Data/Station/Station_CN/';
% addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'))


% for server
path = '/share/irisnas5/Data/Station/Station_CN/';
addpath(genpath('/share/irisnas5/Data/matlab_func/'))

% % for mac
% path_nas6 = '/Volumes/irisnas6/Data/Aerosol/Station_CN/';
% addpath(genpath('/Volumes/irisnas6/Work/Aerosol/matlab_func/'));
%% STN_header

% Korea station_header
% {'DOY','year','month','day','time','SO2','CO','O3','NO2','PM10','PM25','Lat','Lon','station'};

% China station header
% {'doy','yr','mm','dd','time','AQI','PM2.5','PM2.5_24h','PM10',...
%   'PM10_24h','SO2','SO2_24h','NO2','NO2_24h','O3','O3_24h','O3_8h','O3_8h_24h','CO','CO_24h','stn_num'}
% cd(path_nas6)
%%
for yr = 2015:2019
    if mod(yr,4)==0; days= 366; else; days=365; end
    if yr==2019; days=151; end
        
    load([path, 'stn_code_data/stn_code_data_',num2str(yr),'.mat']);
    ndata = stn_doy;
    scode = unique(ndata(:,end));
    
    ndata_org = ndata;
    % CO
    ndata(:,19)=ndata(:,19)/1.15; % (mg/m3) to ppm (1 ppm = 1.15 mg m-3)
    ndata(ndata(:,19)>20,19)=NaN;
    % SO2 
    ndata(:,11)=ndata(:,11)/2.62; % (?g/m3) to ppb (1 ppb = 2.62 ?g m-3)
    ndata(ndata(:,11)>400,11)=NaN;
    % NO2
    ndata(:,13)=ndata(:,13)/1.88; % (?g/m3) to ppb (1 ppb = 1.88 ?g m-3)
    ndata(ndata(:,13)>400,13)=NaN;
    % O3
    ndata(:,15)=ndata(:,15)/1.96; % (?g/m3) to ppb (1 ppb = 1.96 ?g m-3)
    ndata(ndata(:,15)>400,15)=NaN;
    % PM25 (ug/m3)
    ndata(ndata(:,7)>600,7)=NaN;
    % PM10 (ug/m3)
    ndata(ndata(:,9)>1000,9)=NaN;
    
    ndata(ndata(:,5)<8 | ndata(:,5)>15,:)=[];
    ndata = sortrows(ndata,[1,5,21]);
    
    stn_CN = [];
    for doy=1:days
        tStart_doy = tic;
        ndata_temp = ndata(ndata(:,1)==doy,:);
        scode_temp = unique(ndata_temp(:,end));
        nstn_temp = size(scode_temp,1);
        if (mod(size(ndata_temp,1),nstn_temp)==0) && (size(ndata_temp,1)>=(nstn_temp*4))
            CO = reshape(ndata_temp(:,19),nstn_temp,[]);
            SO2 = reshape(ndata_temp(:,11),nstn_temp,[]);
            O3 = reshape(ndata_temp(:,15),nstn_temp,[]);
            NO2 = reshape(ndata_temp(:,13),nstn_temp,[]);
            PM10 = reshape(ndata_temp(:,9),nstn_temp,[]);
            PM25 = reshape(ndata_temp(:,7),nstn_temp,[]);
            
            nanidx = NaN(nstn_temp,6);
            nanidx(:,1) = sum(isnan(CO),2)>4; 
            nanidx(:,2) = sum(isnan(SO2),2)>4; 
            nanidx(:,3) = sum(isnan(O3),2)>4; 
            nanidx(:,4) = sum(isnan(NO2),2)>4; 
            nanidx(:,5) = sum(isnan(PM10),2)>4; 
            nanidx(:,6) = sum(isnan(PM25),2)>4;
            
            SEM = NaN(nstn_temp,6);
            th = NaN(nstn_temp,6);
            
            SEM(:,1) = 3.291*(nanstd(CO')')/sqrt(size(CO,2)); %to remove all those outside of the 99.9% confidence limits
            SEM(:,2) = 3.291*(nanstd(SO2')')/sqrt(size(SO2,2)); %to remove all those outside of the 99.9% confidence limits
            SEM(:,3) = 3.291*(nanstd(O3')')/sqrt(size(O3,2)); %to remove all those outside of the 99.9% confidence limits
            SEM(:,4) = 3.291*(nanstd(NO2')')/sqrt(size(NO2,2)); %to remove all those outside of the 99.9% confidence limits
            SEM(:,5) = 3.291*(nanstd(PM10')')/sqrt(size(PM10,2)); %to remove all those outside of the 99.9% confidence limits
            SEM(:,6) = 3.291*(nanstd(PM25')')/sqrt(size(PM25,2)); %to remove all those outside of the 99.9% confidence limits
            conc_mean = [nanmean(CO,2), nanmean(SO2,2), nanmean(O3,2), nanmean(NO2,2), nanmean(PM10,2), nanmean(PM25,2)];
            th(:,1) =SEM(:,1)+conc_mean(:,1);
            th(:,2) =SEM(:,2)+conc_mean(:,2);
            th(:,3) =SEM(:,3)+conc_mean(:,3);
            th(:,4) =SEM(:,4)+conc_mean(:,4);
            th(:,5) =SEM(:,5)+conc_mean(:,5);
            th(:,6) =SEM(:,6)+conc_mean(:,6);
            
            nTime = size(CO,2);
            
            diff1 = CO - repmat(th(:,1),[1,nTime]);
            diff2 = SO2 - repmat(th(:,2),[1,nTime]);
            diff3 = O3 - repmat(th(:,3),[1,nTime]);
            diff4 = NO2 - repmat(th(:,4),[1,nTime]);
            diff5 = PM10 - repmat(th(:,5),[1,nTime]);
            diff6 = PM25 - repmat(th(:,6),[1,nTime]);
            
            CO(diff1>0)=NaN;
            SO2(diff2>0)=NaN;
            O3(diff3>0)=NaN;
            NO2(diff4>0)=NaN;
            PM10(diff5>0)=NaN;
            PM25(diff6>0)=NaN;
            
            CO(nanidx(:,1)==1,:)=NaN;
            SO2(nanidx(:,2)==1,:)=NaN;
            O3(nanidx(:,3)==1,:)=NaN;
            NO2(nanidx(:,4)==1,:)=NaN;
            PM10(nanidx(:,5)==1,:)=NaN;
            PM25(nanidx(:,6)==1,:)=NaN;
            
%             allvar = [PM25(:),PM10(:),SO2(:),NO2(:),O3(:),CO(:)]; %%
%             nanidx_allvar = sum(isnan(allvar),2)==6; %%
            
            ndata_temp(:,[7,9,11,13,15,19])=[PM25(:),PM10(:),SO2(:),NO2(:),O3(:),CO(:)];
%             ndata_temp(nanidx_allvar==1,:)=[]; %%
            stn_CN = [stn_CN; ndata_temp];
            
            tElapsed_doy = toc(tStart_doy);
            disp([num2str(yr),'_',num2str(doy),'--',num2str(tElapsed_doy,'%3.4f'),' sec'])
        else
            fprintf('Less than 4 hourly data in %03i (DOY) \n',doy);
        end
        
    end
    save([path,'stn_code_data/stn_code_data_rm_outlier_',num2str(yr),'.mat'],'stn_CN');
    disp(yr)
end

toc


