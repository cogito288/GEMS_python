addpath(genpath('/share/irisnas5/Data/matlab_func/'))

%% China
clear all; close all; clc
tic
% path_data = '//10.72.26.56/irisnas5/Data/';

path_data = '/share/irisnas5/Data/';

load([path_data,'Station/Station_CN/cn_stn_GOCI6km_location_weight.mat']) % period_GOCI.csv 사용해서 만든거

dup_scode2 = cn_dup_scode2_GOCI6km(:,2:end);
unq_scode2 = cn_stn_GOCI6km_location(cn_stn_GOCI6km_location(:,9)==0,2);
dup_dist = cn_stn_GOCI6km_location(ismember(cn_stn_GOCI6km_location(:,2),dup_scode2),[2,8]);

for yr=2015:2019
    load([path_data,'Station/Station_CN/stn_scode_data/cn_stn_scode_data_rm_outlier_',num2str(yr),'.mat'])

    if mod(yr,4)==0; days=366; else; days=365; end
    
    stn_GOCI6km_yr = [];
    
    for doy=1:days
        stn_temp = ndata_scode(ndata_scode(:,1)==doy,:);
        for CST = 8:15  % 0:23  %%%%%% 1:24
            stn_temp2 = stn_temp(stn_temp(:,5)==CST,:);
            if isempty(stn_temp2)==0
                stn_GOCI6km = stn_temp2(ismember(stn_temp2(:,22),unq_scode2),:);

                for j=1:size(dup_scode2,1)
                    stn_GOCI6km_temp = stn_temp2(ismember(stn_temp2(:,22),dup_scode2(j,:)),:);

                    if size(stn_GOCI6km_temp,1)==1
                        stn_GOCI6km_temp2 = stn_GOCI6km_temp;
                        stn_GOCI6km = [stn_GOCI6km;stn_GOCI6km_temp2];
                    elseif size(stn_GOCI6km_temp,1)~=0
                        weight_sum = [];
                        for k = 1:size(stn_GOCI6km_temp,1)
                            stn_GOCI6km_temp(k,23) = dup_dist(dup_dist(:,1)==stn_GOCI6km_temp(k,22),2);
                            nanidx = isnan(stn_GOCI6km_temp(k,6:20))==0;
                            weight = nanidx ./stn_GOCI6km_temp(k,23);
                            stn_GOCI6km_temp(k,6:20) = stn_GOCI6km_temp(k,6:20) .* weight;
                            weight_sum = [weight_sum; weight];
                        end

                        min_dist = min(stn_GOCI6km_temp(:,23));

                        stn_GOCI6km_temp2 = stn_GOCI6km_temp(stn_GOCI6km_temp(:,23)==min_dist,:);
                        if size(stn_GOCI6km_temp2,1)~=1
                            stn_GOCI6km_temp2(2:end,:)=[];
                        end
                        % 픽셀중심에 더 가까운 관측소의 scode2를 사용하기 위함. 관측값은 가중평균한 값으로 다시 할당될거이므로 신경 쓰지말기

                        weight_sum = sum(weight_sum,1);
                        stn_GOCI6km_temp2(1,6:20)=nansum(stn_GOCI6km_temp(:,6:20),1)./weight_sum;
                        stn_GOCI6km = [stn_GOCI6km;stn_GOCI6km_temp2(:,1:end-1)];
                    end
                end
                stn_GOCI6km = sortrows(stn_GOCI6km,22); % sort by scode2
                stn_GOCI6km_yr = [stn_GOCI6km_yr; stn_GOCI6km];
            end
        end
        disp(doy)
    end
    cn_stn_GOCI6km_yr=stn_GOCI6km_yr;   
    save([path_data,'Station/Station_CN/cn_Station_GOCI6km_rm_outlier_',num2str(yr),'_weight'],'cn_stn_GOCI6km_yr','-v7.3')
end

toc
