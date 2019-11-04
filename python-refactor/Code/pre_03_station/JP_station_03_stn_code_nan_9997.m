path_data = '/share/irisnas5/Data/';

for yr=2009:2016
    load([path_data,'Station/Station_JP/stn_scode_data_add_NOX_O3/jp_stn_scode_data_add_NOX_O3_',num2str(yr),'.mat'])
    ndata_scode = sortrows(ndata_scode,[13,1,5]);
    ndata_scode_nan = ndata_scode(:,[6:11,14:15]);
    ndata_scode_nan(ndata_scode_nan>=9997)=NaN;
    ndata_scode_nan(ndata_scode_nan<0)=NaN;
    ndata_scode(:,[6:11,14:15])=ndata_scode_nan;
    save([path_data,'Station/Station_JP/stn_scode_data_add_NOX_O3/jp_stn_scode_data_add_NOX_O3_',...
        num2str(yr),'.mat'],'ndata_scode','header_ndata','-v7.3')
end