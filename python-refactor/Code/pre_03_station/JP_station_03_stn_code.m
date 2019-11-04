clear all; close all; clc

tic

% path_data = '//10.72.26.56/irisnas5/Data/';
% path = '//10.72.26.56/irisnas5/GEMS/EA_GOCI6km/';

path_data = '/share/irisnas5/Data/';
% path = '/share/irisnas5/GEMS/EA_GOCI6km/';
%
% addpath(genpath('/share/irisnas5/Data/matlab_func/'))

stn_info = csvread([path_data,'Station/Station_JP/jp_stn_code_lonlat_period_filtered_yyyymmdd.csv'],1);
% scode1, scode2, lon, lat, op_start, op_end

scode_unq = unique(stn_info(:,1));
clearvars stn_info

header_ndata = {'doy','yr','mon','day','KST','SO2','CO','OX','NO2','PM10','PM25',...
    'NO','NOX','NMHC','CH4','THC','CO2','scode'};

for yr=2015 %:2016 %2009:2016
    load([path_data,'Station/Station_JP/byPollutant/JP_stnSO2_',num2str(yr)])
    load([path_data,'Station/Station_JP/byPollutant/JP_stnNO_',num2str(yr)])
    load([path_data,'Station/Station_JP/byPollutant/JP_stnNO2_',num2str(yr)])
    load([path_data,'Station/Station_JP/byPollutant/JP_stnNOX_',num2str(yr)])
    load([path_data,'Station/Station_JP/byPollutant/JP_stnCO_',num2str(yr)])
    load([path_data,'Station/Station_JP/byPollutant/JP_stnOX_',num2str(yr)])
    load([path_data,'Station/Station_JP/byPollutant/JP_stnNMHC_',num2str(yr)])
    load([path_data,'Station/Station_JP/byPollutant/JP_stnCH4_',num2str(yr)])
    load([path_data,'Station/Station_JP/byPollutant/JP_stnTHC_',num2str(yr)])
    load([path_data,'Station/Station_JP/byPollutant/JP_stnSPM_',num2str(yr)])
    load([path_data,'Station/Station_JP/byPollutant/JP_stnPM25_',num2str(yr)])
    load([path_data,'Station/Station_JP/byPollutant/JP_stnCO2_',num2str(yr)])
    
    stnSO2 = table2array(stnSO2_tbl);
    stnNO = table2array(stnNO_tbl);
    stnNO2 = table2array(stnNO2_tbl);
    stnNOX = table2array(stnNOX_tbl);
    stnCO = table2array(stnCO_tbl);
    stnOX = table2array(stnOX_tbl);
    stnNMHC = table2array(stnNMHC_tbl);
    stnCH4 = table2array(stnCH4_tbl);
    stnTHC = table2array(stnTHC_tbl);
    stnSPM = table2array(stnSPM_tbl);
    stnPM25 = table2array(stnPM25_tbl);
    stnCO2 = table2array(stnCO2_tbl);
    
    clearvars *_tbl
    
    if mod(yr,4)==0
        days = 366;
    else
        days = 365;
    end
    
    [a_doy,a_KST,a_scode] = meshgrid(1:days,1:24,scode_unq);
    aa = [a_doy(:),a_KST(:),a_scode(:)];
    
    doy000 = datenum([yr,0,0,0,0,0]);
    mm = str2num(datestr(doy000+aa(:,1),'mm'));
    dd = str2num(datestr(doy000+aa(:,1),'dd'));
    
%     clearvars a_doy a_KST a_scode
    
    bb = NaN(size(aa,1),12);
    nanidx = [];
    for k = 1:length(aa)
        tStart = tic;
        aSO2 = stnSO2(stnSO2(:,1)==aa(k,1)&stnSO2(:,7)==aa(k,2)&stnSO2(:,5)==aa(k,3),8);
        aNO = stnNO(stnNO(:,1)==aa(k,1)&stnNO(:,7)==aa(k,2)&stnNO(:,5)==aa(k,3),8);
        aNO2 = stnNO2(stnNO2(:,1)==aa(k,1)&stnNO2(:,7)==aa(k,2)&stnNO2(:,5)==aa(k,3),8);
        aNOX = stnNOX(stnNOX(:,1)==aa(k,1)&stnNOX(:,7)==aa(k,2)&stnNOX(:,5)==aa(k,3),8);
        aCO = stnCO(stnCO(:,1)==aa(k,1)&stnCO(:,7)==aa(k,2)&stnCO(:,5)==aa(k,3),8);
        aOX = stnOX(stnOX(:,1)==aa(k,1)&stnOX(:,7)==aa(k,2)&stnOX(:,5)==aa(k,3),8);
        aNMHC = stnNMHC(stnNMHC(:,1)==aa(k,1)&stnNMHC(:,7)==aa(k,2)&stnNMHC(:,5)==aa(k,3),8);
        aCH4 = stnCH4(stnCH4(:,1)==aa(k,1)&stnCH4(:,7)==aa(k,2)&stnCH4(:,5)==aa(k,3),8);
        aTHC = stnTHC(stnTHC(:,1)==aa(k,1)&stnTHC(:,7)==aa(k,2)&stnTHC(:,5)==aa(k,3),8);
        aSPM = stnSPM(stnSPM(:,1)==aa(k,1)&stnSPM(:,7)==aa(k,2)&stnSPM(:,5)==aa(k,3),8);
        aPM25 = stnPM25(stnPM25(:,1)==aa(k,1)&stnPM25(:,7)==aa(k,2)&stnPM25(:,5)==aa(k,3),8);
        aCO2 = stnCO2(stnCO2(:,1)==aa(k,1)&stnCO2(:,7)==aa(k,2)&stnCO2(:,5)==aa(k,3),8);
        if isempty(aSO2)==0; bb(k,1)=aSO2; end
        if isempty(aCO)==0; bb(k,2)=aCO; end
        if isempty(aOX)==0; bb(k,3)=aOX; end
        if isempty(aNO2)==0; bb(k,4)=aNO2; end
        if isempty(aSPM)==0; bb(k,5)=aSPM; end
        if isempty(aPM25)==0; bb(k,6)=aPM25; end
        if isempty(aNO)==0; bb(k,7)=aNO; end
        if isempty(aNOX)==0; bb(k,8)=aNOX; end
        if isempty(aNMHC)==0; bb(k,9)=aNMHC; end
        if isempty(aCH4)==0; bb(k,10)=aCH4; end
        if isempty(aTHC)==0; bb(k,11)=aTHC; end
        if isempty(aCO2)==0; bb(k,12)=aCO2; end
        
        bb_temp = bb(k,:);
        bb_temp(bb_temp>=9997)=NaN;
        bb(k,:)=bb_temp;
        
        nanidx_temp = sum(isnan(bb_temp));
        if nanidx_temp == 12
            nanidx = [nanidx; k];
        end
        tElapsed = toc(tStart);
        disp([num2str(yr),'_',num2str(aa(k,1),'%03i'),'_',num2str(aa(k,2),'%02i'),' --- ',num2str(tElapsed),' sec'])
    end
    ndata = [aa(:,1),yr.*ones(size(aa,1),1),mm,dd,aa(:,2),bb,aa(:,3)];
    ndata(nanidx,:)=[];
    save([path_data,'Station/Station_JP/stn_code_data/stn_code_data_all_',num2str(yr)],'ndata','header_ndata')
end % yr

toc
