clear all; close all; clc

tic

path_data = '//10.72.26.56/irisnas5/Data/';

% path_data = '/share/irisnas5/Data/';
% path = '/share/irisnas6/Work/Aerosol/';

% addpath(genpath('/share/irisnas2/Data/Aerosol_Work/matlab_func/'))

load([path_data,'grid/grid_goci.mat'])
latlon_data = [lat_goci(:),lon_goci(:)];

%% China
stn_info_cn = csvread([path_data,'Station/Station_CN/cn_stn_code_lonlat_period_GOCI.csv'],1);
% scode1, scode2, lon, lat, op_start, op_end
% idx_coverage = stn_info_cn(:,3)>=113 & stn_info_cn(:,3)<=147 & stn_info_cn(:,4)>=24 & stn_info_cn(:,4)<=48;
% stn_info_cn = stn_info_cn(idx_coverage,:);

new_station = zeros(size(stn_info_cn,1),4);
for i=1:size(stn_info_cn,1)
    dist = latlon_data;
    dist(:,1) = dist(:,1)-stn_info_cn(i,4);
    dist(:,2) = dist(:,2)-stn_info_cn(i,3);
    dist(:,3) = sqrt(sum(dist(:,1:2).^2,2));
    dist_min = min(dist(:,3));
    new_station(i,1) = find(dist(:,3)==dist_min);
    new_station(i,4) = dist_min;
end
new_station(:,2:3)=latlon_data(new_station(:,1),:);

stn = [stn_info_cn(:,[1,2,4,3]), new_station]; % scode1,scode2, lat_org, lon_org, pxid, lat_px, lon_px, dist_btw_org_px
% new_station = stn;
% save([path_data,'Station_CN/cn_GOCI6km_new_station.mat'],'new_station')

stn_unq = unique(stn(:,5));
unq_cnt = hist(stn(:,5),stn_unq);
unqidx = unq_cnt~=1;
stn_GOCI6km = stn(ismember(stn(:,5),stn_unq(unqidx==0)),:);
stn_GOCI6km(:,end+1)=0;

idx = stn_unq(unqidx);
dup_scode2_GOCI6km = zeros(length(idx),max(unq_cnt)+1);
dup_scode2_GOCI6km(:,1)=idx;

for i = 1:length(idx)
    aa = stn(stn(:,5)==dup_scode2_GOCI6km(i,1),2);
    dup_scode2_GOCI6km(i,2:length(aa)+1)=aa;

    stn_GOCI6km_temp = stn(stn(:,5)==idx(i),:);
    stn_GOCI6km_temp(:,end+1)=1;
    stn_GOCI6km = [stn_GOCI6km; stn_GOCI6km_temp];
end

stn_GOCI6km = sortrows(stn_GOCI6km,2);
cn_stn_GOCI6km_location = stn_GOCI6km;
cn_dup_scode2_GOCI6km = dup_scode2_GOCI6km;
header_cn_stn_GOCI6km_location = {'scode1','scode2','lat_org','lon_org','pxid','lat_px','lon_px','avgid','dist'};
% stn_1km_location_tbl = array2table(stn_1km_location, 'VariableNames',header);
% csvwrite_with_headers([path_data,'stn_1km.csv'],stn_1km,header)
save([path_data,'Station/Station_CN/cn_stn_GOCI6km_location_weight.mat'],...
    'cn_stn_GOCI6km_location','cn_dup_scode2_GOCI6km','header_cn_stn_GOCI6km_location')


