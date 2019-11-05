clear all; clc, close all
%
% 
% path = '//10.72.26.56/irisnas5/GEMS/PM/00_EA6km/';
% genpath(addpath('//10.72.26.46/irisnas5/Data/matlab_func/'))


path = '/share/irisnas5/GEMS/PM/00_EA6km/';
addpath(genpath('/share/irisnas5/Data/matlab_func/'))

%% Read data
target = {'PM10','PM25'};
type = {'conc','time','time_conc'};

for t=1:3
    for i=1:2
        
        if i==1
            header = {'station_PM10','RF_PM10','stn','doy','time','year'};
        else
            header = {'station_PM25','RF_PM25','stn','doy','time','year'};
        end
        
        for yr = 2015:2016
            val_rf = [];
            val_stn = [];
            data_val=[];
            if mod(yr,4)==0
                days = 366;
            else
                days = 365;
            end
            
            for doy=1:days
                for utc = 0:7
                    try
                        val_rf_tmp = csvread([path, 'RTT/',type{t},'/RF/',target{i},'/rf_',target{i},'_RTT_EA6km_',num2str(yr),...
                            '_',num2str(doy, '%03i'),'_',num2str(utc, '%02i'),'_val.csv'],1,1);
                        val_rf =[val_rf;val_rf_tmp];
                        
                        data = csvread([path, 'RTT/',type{t},'/dataset/',target{i},'/',target{i},'_RTT_EA6km_',num2str(yr),...
                            '_',num2str(doy, '%03i'),'_',num2str(utc, '%02i'),'.csv'],1);
                        val_stn_tmp = data(data(:,end)==240 & data(:,end-1)==0,:);
                        val_stn =[val_stn;val_stn_tmp(:,[end-6,end-5:end-2])];
                        val_stn = val_stn(val_stn(:,1)>0,:);
                        
                        disp(utc)
                    catch
                        fprintf('There is no rf file \n')
                        disp(utc)
                    end
                end
                disp(doy)
            end
            
            disp(yr)
        end
        data_val(:,[1,3:6]) = val_stn(:,[1,2:5]);
        data_val(:,2) = val_rf;
        data_val(data_val==-9999)=NaN;
        data_val = rmmissing(data_val,1);
        
        csvwrite_with_headers2([path,'RTT/',type{t},'/stn_location/',type{t},'_',target{i},...
            '_compare_RTT_val_stn_ovr_EA6km_',num2str(yr),'_new.csv'],data_val,header,0,0,'%7.7f');
    end
end
