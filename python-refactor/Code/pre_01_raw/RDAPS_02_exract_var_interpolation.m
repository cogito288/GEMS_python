clear all; clc;
% path_data = '//10.72.26.52/irisnas2/Data/Aerosol/';
% path = '//10.72.26.52/irisnas2/Data/Aerosol_Work/Korea/';

path_data = '/share/irisnas2/Data/Aerosol/';
path = '/share/irisnas2/Data/Aerosol_Work/Korea/';

tic

for yr = 2017 %2015:2016
    cd([path_data, 'RDAPS/',num2str(yr)])
    
    if mod(yr,4)==0
        days = 366;
    else
        days = 365;
    end
    
    for i=1:days
        clearvars data*
        data00 = load(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_00.mat']); %rdaps
        data00 = data00.rdaps;
        
        try
            data06 = load(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_06.mat']); %rdaps
            data06 = data06.rdaps;
        catch
            % 분석장06시 자료가 없을 때, 예측장00-006시 자료 가져오기
            % (2015 232 (Aug20))
            data00_006 = load(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_06_frcst.mat']); %rdaps forecast 06
            data00_006 = data00_006.rdaps;
        end
        
        data12 = load(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_12.mat']); %rdaps
        data12 = data12.rdaps;
        
        try
            data18 = load(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_18.mat']); %rdaps
            data18 = data18.rdaps;
        catch
            % 분석장18시 자료가 없을 때, 12-006시 자료 가져오기
            % From 2016 028 to 045 (Jan28 to Feb14) 18 UTC analysis data missing
            data12_006 = load(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_18_frcst.mat']); %rdaps forecast 06
            data12_006 = data12_006.rdaps;
        end
        
        if i==days
            data24 = load([path_data,'RDAPS/',num2str(yr+1),'/RDAPS_',num2str(yr+1),'_001_00.mat']); %rdaps
        else
            data24 = load(['RDAPS_',num2str(yr),'_',num2str(i+1,'%03i'),'_00.mat']); %rdaps
        end
        data24 = data24.rdaps;
        
        if exist('data06','var') && exist('data18','var')
            for j=1:5
                rdaps = (data06 - data00).*(j/6) + data00; % 01 to 05 UTC
                save(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_',num2str(j,'%02i')],'rdaps');
                rdaps = (data12 - data06).*(j/6) + data06; % 07 to 11 UTC
                save(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_',num2str(j+6,'%02i')],'rdaps');
                rdaps = (data18 - data12).*(j/6) + data12; % 13 to 17 UTC
                save(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_',num2str(j+12,'%02i')],'rdaps');
                rdaps = (data24 - data18).*(j/6) + data18; % 19 to 23 UTC
                save(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_',num2str(j+18,'%02i')],'rdaps');
            end
            
        elseif exist('data06','var')==0 && exist('data18','var')
            for j=1:5
                rdaps = (data00_006 - data00).*(j/6) + data00; % 01 to 05 UTC
                save(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_',num2str(j,'%02i'),'_frcst'],'rdaps');
                rdaps = (data12 - data00_006).*(j/6) + data00_006; % 07 to 11 UTC
                save(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_',num2str(j+6,'%02i'),'_frcst'],'rdaps');
                rdaps = (data18 - data12).*(j/6) + data12; % 13 to 17 UTC
                save(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_',num2str(j+12,'%02i')],'rdaps');
                rdaps = (data24 - data18).*(j/6) + data18; % 19 to 23 UTC
                save(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_',num2str(j+18,'%02i')],'rdaps');
            end
            
        elseif exist('data06','var') && exist('data18','var')==0
            for j=1:5
                rdaps = (data06 - data00).*(j/6) + data00; % 01 to 05 UTC
                save(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_',num2str(j,'%02i')],'rdaps');
                rdaps = (data12 - data06).*(j/6) + data06; % 07 to 11 UTC
                save(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_',num2str(j+6,'%02i')],'rdaps');
                rdaps = (data12_006 - data12).*(j/6) + data12; % 13 to 17 UTC
                save(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_',num2str(j+12,'%02i'),'_frcst'],'rdaps');
                rdaps = (data24 - data12_006).*(j/6) + data12_006; % 19 to 23 UTC
                save(['RDAPS_',num2str(yr),'_',num2str(i,'%03i'),'_',num2str(j+18,'%02i'),'_frcst'],'rdaps');
            end
        end
        
        disp(i)
    end
end

toc
