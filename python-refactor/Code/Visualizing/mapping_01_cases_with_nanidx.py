  
# path_data = '//10.72.26.46/irisnas6/Data/Aerosol/'
# path = '//10.72.26.46/irisnas6/Work/NOXO3/Korea/'

path_data = '/share/irisnas6/Data/Aerosol/'
path = '/share/irisnas6/Work/NOXO3/Korea/'
addpath(genpath('/share/irisnas6/Work/Aerosol/matlab_func/'))

matlab.loadmat(os.path.join(path_data,'grid/grid_korea.mat'])
m_bnd = m_shaperead([path,'boundary/BND_SIDO_GCS'])

# sel_NO2 = [1,3:4,7:17,21:24,28:49,53]
# sel_O3 = [1:23,25,28:49,53]

yr=2015
# yr=2016

if yr%4==0
    days = 366
else
    days = 365


matlab.loadmat(os.path.join(path,'cases/nanidx_no2_',str(yr)]) # nanidx_no2
matlab.loadmat(os.path.join(path,'cases/nanidx_o3_',str(yr)]) # nanidx_o3

fname0 = 'FBselected'

for doy = 1:days
    fname = [str(yr),'_',str(doy,'#03i')]
    
    data_no2 = pd.read_csv(os.path.join(path,'RF_pred/NO2_',fname0,'/rf_NO2_',fname0,'_log_cases_',fname,'_04.csv'],1)
    if np.sum(nanidx_no2(:,doy)) < 231340
        data_no2(nanidx_no2(:,doy)==1)np.nan
        data_no2 = reshape(data_no2,size(lat_kor))

        m_kor(lon_kor,lat_kor,data_no2)
        caxis([0 30])
        hold on
        for k=1:length(m_bnd.ncst)
            m_line(m_bnd.ncst{k}(:,1),m_bnd.ncst{k}(:,2),'color','k','linewidth',1)
        
        colorbar('FontSize',18)
        print('-djpeg','-r300',[path,'map/RF_',fname0,'_NO2/NO2_',fname,'_04'])
    
    
    data_o3 = pd.read_csv(os.path.join(path,'RF_pred/O3_',fname0,'/rf_O3_',fname0,'_log_cases_',fname,'_04.csv'],1)
    if np.sum(nanidx_o3(:,doy)) < 231340
        data_o3(nanidx_o3(:,doy)==1)np.nan
        data_o3 = reshape(data_o3,size(lat_kor))
        
        m_kor(lon_kor,lat_kor,data_o3)
        caxis([0 80])
        hold on
        for k=1:length(m_bnd.ncst)
            m_line(m_bnd.ncst{k}(:,1),m_bnd.ncst{k}(:,2),'color','k','linewidth',1)
        
        colorbar('FontSize',18)
        print('-djpeg','-r300',[path,'map/RF_',fname0,'_O3/O3_',fname,'_04'])
    
    close all
    print (fname)

