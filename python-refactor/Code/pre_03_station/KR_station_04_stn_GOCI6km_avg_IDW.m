clear all; close all; clc

tic

% Station index
% path_data = '//10.72.26.56/irisnas5/Data/';
path_data = '/share/irisnas5/Data/';
path_stn_kor = [path_data,'Station/Station_Korea/'];
% addpath(genpath('/share/irisnas5/Data/matlab_func/'))

%% South Korea
load([path_stn_kor,'stn_GOCI6km_location_weight_v201904.mat'])

dup_scode2 = dup_scode2_GOCI6km(:,2:end);
unq_scode2 = stn_GOCI6km_location(stn_GOCI6km_location(:,9)==0,2);
dup_dist = stn_GOCI6km_location(ismember(stn_GOCI6km_location(:,2),dup_scode2),[2,8]);

for yr=2019 %2005:2019
    tStart = tic;
    load([path_stn_kor,'stn_scode_data/stn_scode_data_',num2str(yr),'.mat'])
    % ndata_scode: {'DOY','year','month','day','time','SO2','CO','O3','NO2','PM10','PM25','scode1','scode2'};
    
    if mod(yr,4)==0; days=366; else; days=365; end
     
    stn_GOCI6km_yr = [];
    
    for doy=1:days
        stn_temp = ndata_scode(ndata_scode(:,1)==doy,:);
        for KST = 0:23 %%%%
            stn_temp2 = stn_temp(stn_temp(:,5)==KST,:);
            if isempty(stn_temp2)==0
                stn_GOCI6km = stn_temp2(ismember(stn_temp2(:,13),unq_scode2),:);
                
                for j=1:size(dup_scode2,1)
                    stn_GOCI6km_temp = stn_temp2(ismember(stn_temp2(:,13),dup_scode2(j,:)),:);
                    
                    if size(stn_GOCI6km_temp,1)==1
                        stn_GOCI6km_temp2 = stn_GOCI6km_temp;
                        stn_GOCI6km = [stn_GOCI6km;stn_GOCI6km_temp2];
                    elseif size(stn_GOCI6km_temp,1)~=0
                        weight_sum = [];
                        
                        for k = 1:size(stn_GOCI6km_temp,1)
                            stn_GOCI6km_temp(k,14) = dup_dist(dup_dist(:,1)==stn_GOCI6km_temp(k,13),2);
                            nanidx = isnan(stn_GOCI6km_temp(k,6:11))==0;
                            weight = nanidx ./stn_GOCI6km_temp(k,14);
                            stn_GOCI6km_temp(k,6:11) = stn_GOCI6km_temp(k,6:11) .* weight;
                            weight_sum = [weight_sum; weight];
                        end
                    
                        min_dist = min(stn_GOCI6km_temp(:,14));
                    
                        stn_GOCI6km_temp2 = stn_GOCI6km_temp(stn_GOCI6km_temp(:,14)==min_dist,:);
                        if size(stn_GOCI6km_temp2,1)~=1
                            stn_GOCI6km_temp2(2:end,:)=[];
                        end
                        % 픽셀중심에 더 가까운 관측소의 scode2를 사용하기 위함. 관측값은 가중평균한 값으로 다시 할당될거이므로 신경 쓰지말기
                    
                        weight_sum = sum(weight_sum,1);
                        stn_GOCI6km_temp2(6:11)=nansum(stn_GOCI6km_temp(:,6:11),1)./weight_sum;
                        stn_GOCI6km = [stn_GOCI6km;stn_GOCI6km_temp2(:,1:end-1)];
                    end
                end
                stn_GOCI6km = sortrows(stn_GOCI6km,13); % sort by scode2
                stn_GOCI6km_yr = [stn_GOCI6km_yr; stn_GOCI6km];
            end
        end
        disp(doy)
    end
    save([path_stn_kor,'Station_GOCI6km_',num2str(yr),'_weight'],'stn_GOCI6km_yr','-v7.3')
    tElapsed = toc(tStart);
end

toc
