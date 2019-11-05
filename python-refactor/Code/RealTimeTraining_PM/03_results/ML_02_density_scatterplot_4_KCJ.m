clear all; clc;

tic
% path = '/Volumes/irisnas5/GEMS/PM/';
% addpath(genpath('/Volumes/irisnas5/Data/matlab_func/'))

path = '//10.72.26.56/irisnas5/GEMS/PM/';
addpath(genpath('//10.72.26.56/irisnas5/Data/matlab_func/'))


target={'PM10','PM25'};
type={'conc','time','time_conc','cloud'};
%% Read validation result
for t=2:3
    for i=1 % target
        
        val_scatter = [];
        results = csvread([path, '00_EA6km/RTT/',type{t},'/stn_location/',type{t},'_',target{i},'_compare_RTT_val_stn_ovr_EA6km.csv'],1);
%         results_yr = results(results(:,end)==2015,:);
        
        val_scatter(:,1)= results(:,1);%stn
        val_scatter(:,2)= results(:,2);%RF
        
        if i==1
            val_scatter = val_scatter(val_scatter(:,1) < 1000,: );
        else
            val_scatter = val_scatter(val_scatter(:,1) < 600,: );
        end
        
        val_scatter = val_scatter(val_scatter(:,1) > 0,: );
        val_scatter = val_scatter(val_scatter(:,2) > 0,: );
        
        bias = val_scatter(:,2)-val_scatter(:,1);
        mid = (val_scatter(:,2)+val_scatter(:,1))./2;
        
        MBE = mean(bias);
        MAE = mean(abs(bias));
        MFE = mean(abs(bias)./mid)*100;
        disp(['MBE : ',num2str(MBE),'     MAB : ',num2str(MAE),'     MFE : ',num2str(MFE)])
        accuracy = [MBE, MAE, MFE];
        %     save([path, 'dataset/scatterplot/LOO/',target{i},'_accuracy_RF.mat'],'accuracy');
        %             save([path_2, 'dataset/scatterplot/',target{i},'_accuracy_test_',num2str(test, '%02i'),'_set_',num2str(j,'%02i'),'.mat'],'accuracy');
        
        
        %% density scatter plot
        
        if i==1
            PM_val = heatscatter_paper(val_scatter(:,1), val_scatter(:,2), [path,'/dataset/scatterplot'], 'PM10_RF_val.jpg',...
                '','','',1,'','Observed PM_1_0 Concentration (\mug/m^3)','Estimated PM_1_0 Concentration (\mug/m^3)','PM_1_0 Validation');
            print('-djpeg','-r300',[path,'04_scatterplot/RTT/',type{t},'_scatter_PM10_RTT.jpg']);
        else
            PM_val = heatscatter_paper(val_scatter(:,1), val_scatter(:,2), [path,'/dataset/scatterplot'], 'PM25_RF_val.jpg',...
                '','','',1,'','Observed PM_2_._5 Concentration (\mug/m^3)','Estimated PM_2_._5 Concentration (\mug/m^3)','PM_2_._5 Validation');
            print('-djpeg','-r300',[path,'04_scatterplot/RTT/',type{t},'_scatter_PM25_RTT.jpg']);
        end
        
    end
end

