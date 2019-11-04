clear all;clc; close all;

tic 

% path = '//10.72.26.56/irisnas5/Data/Station/Station_JP/';
% addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'))

path = '/share/irisnas5/Data/Station/Station_JP/';
addpath(genpath('/share/irisnas5/Data/matlab_func/'))

%% header

% station_header
header = {'doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25','scode'};

%%
for yr = 2017:2019
    if mod(yr,4)==0; days= 366; else; days=365; end
    if yr==2019; days=151; end
        
    load([path, 'stn_code_data/stn_code_data_',num2str(yr),'.mat']);
    ndata = stn_yr;
    scode = unique(ndata(:,end));
    
    ndata_org = ndata;
    % SO2
    ndata(:,6)=ndata(:,6)*1000; % ppm to ppb
    ndata(ndata(:,6)>400,6)=NaN; 
    % CO
    ndata(:,7)=ndata(:,7)*10; % ppm to 0.1ppm
    ndata(ndata(:,7)>200,7)=NaN;
    % OX
    ndata(:,8)=ndata(:,8)*1000; % ppm to ppb
    ndata(ndata(:,8)>400,8)=NaN;
    % NO2
    ndata(:,9)=ndata(:,9)*1000; % ppm to ppb
    ndata(ndata(:,9)>400,9)=NaN;
    % PM10
    ndata(:,10)=ndata(:,10)*1000; % (mg/m3) to (ug/m3)
    ndata(ndata(:,10)>1000,10)=NaN; 
    % PM25
    % (ug/m3)
    ndata(ndata(:,11)>600,11)=NaN; 
    
    ndata(ndata(:,5)<9 | ndata(:,5)>16,:)=[]; %%%%%%%%
    ndata = sortrows(ndata,[1,5,12]);
    
    stn_JP = [];
    for doy=1:days
        tStart_doy = tic;
        ndata_temp = ndata(ndata(:,1)==doy,:);
        scode_temp = unique(ndata_temp(:,end));
        nstn_temp = size(scode_temp,1);
        if (mod(size(ndata_temp,1),nstn_temp)==0) && (size(ndata_temp,1)>=(nstn_temp*4))
            SO2 = reshape(ndata_temp(:,6),nstn_temp,[]);
            CO = reshape(ndata_temp(:,7),nstn_temp,[]);
            OX = reshape(ndata_temp(:,8),nstn_temp,[]);
            NO2 = reshape(ndata_temp(:,9),nstn_temp,[]);
            PM10 = reshape(ndata_temp(:,10),nstn_temp,[]);
            PM25 = reshape(ndata_temp(:,11),nstn_temp,[]);
            
            nanidx = NaN(nstn_temp,6);
            nanidx(:,1) = sum(isnan(SO2),2)>4; 
            nanidx(:,2) = sum(isnan(CO),2)>4; 
            nanidx(:,3) = sum(isnan(OX),2)>4; 
            nanidx(:,4) = sum(isnan(NO2),2)>4; 
            nanidx(:,5) = sum(isnan(PM10),2)>4; 
            nanidx(:,6) = sum(isnan(PM25),2)>4;
            
            SEM = NaN(nstn_temp,6);
            th = NaN(nstn_temp,6);
            
            SEM(:,1) = 3.291*(nanstd(SO2')')/sqrt(size(SO2,2)); %to remove all those outside of the 99.9% confidence limits
            SEM(:,2) = 3.291*(nanstd(CO')')/sqrt(size(CO,2)); %to remove all those outside of the 99.9% confidence limits
            SEM(:,3) = 3.291*(nanstd(OX')')/sqrt(size(OX,2)); %to remove all those outside of the 99.9% confidence limits
            SEM(:,4) = 3.291*(nanstd(NO2')')/sqrt(size(NO2,2)); %to remove all those outside of the 99.9% confidence limits
            SEM(:,5) = 3.291*(nanstd(PM10')')/sqrt(size(PM10,2)); %to remove all those outside of the 99.9% confidence limits
            SEM(:,6) = 3.291*(nanstd(PM25')')/sqrt(size(PM25,2)); %to remove all those outside of the 99.9% confidence limits
            conc_mean = [nanmean(SO2,2), nanmean(CO,2), nanmean(OX,2), nanmean(NO2,2), nanmean(PM10,2), nanmean(PM25,2)];
            th(:,1) =SEM(:,1)+conc_mean(:,1);
            th(:,2) =SEM(:,2)+conc_mean(:,2);
            th(:,3) =SEM(:,3)+conc_mean(:,3);
            th(:,4) =SEM(:,4)+conc_mean(:,4);
            th(:,5) =SEM(:,5)+conc_mean(:,5);
            th(:,6) =SEM(:,6)+conc_mean(:,6);
            
            nTime = size(SO2,2);
            
            diff1 = SO2 - repmat(th(:,1),[1,nTime]);
            diff2 = CO - repmat(th(:,2),[1,nTime]);
            diff3 = OX - repmat(th(:,3),[1,nTime]);
            diff4 = NO2 - repmat(th(:,4),[1,nTime]);
            diff5 = PM10 - repmat(th(:,5),[1,nTime]);
            diff6 = PM25 - repmat(th(:,6),[1,nTime]);
            
            SO2(diff1>0)=NaN;
            CO(diff2>0)=NaN;
            OX(diff3>0)=NaN;
            NO2(diff4>0)=NaN;
            PM10(diff5>0)=NaN;
            PM25(diff6>0)=NaN;
            
            SO2(nanidx(:,1)==1,:)=NaN;
            CO(nanidx(:,2)==1,:)=NaN;
            OX(nanidx(:,3)==1,:)=NaN;
            NO2(nanidx(:,4)==1,:)=NaN;
            PM10(nanidx(:,5)==1,:)=NaN;
            PM25(nanidx(:,6)==1,:)=NaN;
            
            allvar = [SO2(:),CO(:),OX(:),NO2(:),PM10(:),PM25(:)]; %%
            nanidx_allvar = sum(isnan(allvar),2)==6; %%
            
            ndata_temp(:,6:11)=allvar;
            ndata_temp(nanidx_allvar==1,:)=[]; %%
            stn_JP = [stn_JP; ndata_temp];
            
            tElapsed_doy = toc(tStart_doy);
            disp([num2str(yr),'_',num2str(doy),'--',num2str(tElapsed_doy,'%3.4f'),' sec'])
        else
            fprintf('Less than 4 hourly data in %03i (DOY) \n',doy);
        end
        
    end
    save([path,'stn_code_data/stn_code_data_rm_outlier_',num2str(yr),'_rm.mat'],'stn_JP');
    disp(yr)
end

toc


