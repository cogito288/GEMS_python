clear all;clc; close all;

% % for local 
% % path_nas6 = '//10.72.26.56/irisnas5/Data/Station/Station_JP/';
% % addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'));


% for server
path_nas6 = '/share/irisnas5/Data/Station/Station_JP/';
addpath(genpath('/share/irisnas5/Data/matlab_func/'));


%% STN_header

% Korea station_header
% {'DOY','year','month','day','time','SO2','CO','O3','NO2','PM10','PM25','Lat','Lon','station'};

% Japan station_header
% {'DOY','year','month','day','time','SO2','CO','OX','NO2','PM10','PM25','Lat','Lon','station'};

% China station header
% {'doy','yr','mm','dd','time','AQI','PM2.5','PM2.5_24h','PM10',...
%   'PM10_24h','SO2','SO2_24h','NO2','NO2_24h','O3','O3_24h','O3_8h','O3_8h_24h','CO','CO_24h','stn_num'}

cd(path_nas4)
%%
stn_JP = [];
for yr = 2019
    if mod(yr,4)==0
        days= 366;
    else
        days=365;
    end
    load([path_nas6, '/jp_stn_code_data_',num2str(yr),'.mat']);
    stn_yr = stn;
    stn_yr(stn_yr==-9999)=nan;
    stn_num = unique(stn_yr(:,end));
    
    stn_doy = [];
    PM10 = []; PM25 = [];  O3 = []; NO2 = []; CO = []; SO2 = [];
    for doy=1:days
        for i=1:length(stn_num)
            for tt = 9:16 % tt: china local time(GEMS time resoluion(9-16KST))
                
                try
                    stn = stn_yr(stn_yr(:,1)==doy & stn_yr(:,5)==tt,:);
                    stn(stn(:,6)>20,6) = nan;
                    stn(stn(:,7)>400,7) = nan;
                    stn(stn(:,8)>400,8) = nan;
                    stn(stn(:,9)>300,9) = nan;
                    stn(stn(:,10)>600,10) = nan;
                    stn(stn(:,11)>1000,11) = nan;
                    CO(i,tt-7) = stn(i,6);
                    SO2(i,tt-7) = stn(i,7);
                    O3(i,tt-7) = stn(i,8);
                    NO2(i,tt-7) = stn(i,9);
                    PM10(i,tt-7) =stn(i,10);
                    PM25(i,tt-7) =stn(i,11);
                    disp(tt)
                catch
                    CO(i,tt-7) = nan;
                    SO2(i,tt-7) = nan;
                    O3(i,tt-7) =nan;
                    NO2(i,tt-7) = nan;
                    PM10(i,tt-7) = nan;
                    PM25(i,tt-7) = nan;                          
                    fprintf('NO file in%3.0f(DOY) \n',doy);
                end
            end
            disp(i)
        end
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
        for ii=1:1497
            CO(ii,CO(ii,:)>th(ii,1))=nan;
            SO2(ii,SO2(ii,:)>th(ii,2))=nan;
            O3(ii,O3(ii,:)>th(ii,3))=nan;
            NO2(ii,NO2(ii,:)>th(ii,4))=nan;
            PM10(ii,PM10(ii,:)>th(ii,5))=nan;
            PM25(ii,PM25(ii,:)>th(ii,6))=nan;
        end
        try
          stn_tt = [];
            for tt2 = 9:16                
                stn = ndata(ndata(:,1)==doy & ndata(:,5)==tt,:);
                stn(:,6:11) = [PM25(:,tt2-7), PM10(:,tt2-7), SO2(:,tt-7), NO2(:,tt-7), O3(:,tt-7), CO(:,tt-7)];

                stn_tt = [stn_tt; stn];
            end
        catch
            fprintf('NO file in%3.0f(DOY) \n',doy);
        end
        
        disp(doy)
        stn_doy = [stn_doy; stn_tt];
    end
    stn_JP = [stn_JP; stn_doy];
    save([path_nas6,'stn_code_data/stn_code_data_rm_outlier_',num2str(yr),'.mat'],'stn_JP');
    disp(yr)
end


