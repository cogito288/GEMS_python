### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import scipy.io as sio
import numpy as np
import glob
import time
import pandas as pd

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_ea_goci = os.path.join(data_base_dir, 'Preprocessed_raw', 'EA_GOCI6km')

path_rtt = os.path.join(data_base_dir, 'Preprocessed_raw', 'RTT') # path_save 

path_nox_korea = os.path.join(data_base_dir, 'Preprocessed_raw', 'NOX03', 'Korea')
matlab.check_make_dir(path_nox_korea)
path_korea_cases = os.path.join(data_base_dir, 'Preprocessed_raw', 'Korea', 'cases')

path_station = os.path.join(data_base_dir, 'Preprocessed_raw', 'Station') 
path_stn_jp = os.path.join(path_station, 'Station_JP')
path_stn_cn = os.path.join(path_station, 'Station_CN')
path_stn_kr = os.path.join(path_station, 'Station_KR')

path_data = '/share/irisnas5/Data/'
path= '/share/irisnas5/GEMS/PM/00_EA6km/'

target = ['PM10','PM25']
type_list = ['conc','time','time_conc']
YEARS = [2016]

## Load grid
mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_korea.mat'))
lat_kor, lon_kor = mat['lat_kor'], mat['lon_kor']
del mat

for t in [1]:
    for i in [0]:
        for yr in YEARS:
            if yr%4==0:
                days = 366
                daysInMonths = [31,29,31,30,31,30,31,31,30,31,30,31]
            else:
                days = 365
                daysInMonths = [31,28,31,30,31,30,31,31,30,31,30,31]
            daily = []
            monthly=[]
            annual =[]
            for doy in range(1,days+1):
                yy, mm, dd = matlab.get_ymd(yr, doy) # should check 
                #[yy, mm, dd] = datevec(matlab.datenum(yr,1,doy))
                try:
                    for utc in range(7+1): #0:7
                        fname = f"cases_EA6km_{yr}_{doy:03d}_{utc:02d}.mat"
                        # load cases file for nan matrix
                        mat = matlab.loadmat(os.path.join(path_ea_goci, 'cases_mat/',str(yr),fname))['data_tbl']
                        df = pd.DataFrame(columns = mat['header'])
                        for col in mat['header']:
                            df[col] = mat[col]
                        data = df.values
                        del df, mat
                        data = data[:,[4,5,6,7,8,9,10,11,58,12,13,14,15,16,17,18,27,28,29,30,35,36,37]]
                        
                        data[data==-9999] = np.nan
                        data[np.isnan(data)] = -9999
                        idy, idx = np.where(data == -9999)
                        idy = np.unique(idy)
                        data[idy.flatten(order='F'),:] = -9999
                        data[data==-9999] = np.nan
                        nanidx = np.isnan(data[:,0])
                        del data_tbl, data, idy, idx
                        
                        try:
                            # read prediction file
                            fname = f"rf_{target[i]}_RTT_EA6km_{yr}_{doy:03d}_{utc:02d}.csv"
                            pred = pd.read_csv(os.path.join(path_rtt,type_list[t],'RF_pred/',target[i],fname))
                            
                            # nan masking to prediction PM concentration.
                            pred[nanidx==1,:] = np.nan
                            if yr==2015 & doy==30:
                                daily[0:218999,0:7] = np.nan
                                daily[:,utc] = pred
                            else:
                                daily[:,utc] = pred
                            print (utc)
                            #close all
                        except:
                            print (f"{doy:03d}_{utc:02d}")
                                            
                    # save hourly prediction matrix
                    fname = f"{target[i]}_RTT_EA6km_{yr}_{doy:03d}"
                    matlab.savemat(os.path.join(path_ea_goci, 'RF_map/',type_list[t],target[i],'daily/',fname), {'daily':daily})
                    #clear pred
                    
                    daily_avg = np.nanmean(daily,axis=1)
                    if yr==2015:
                        if len(annual)==0:
                            annual = np.zeros((218999, 29))*np.nan
                            annual[:,doy] = daily_avg
                    else:
                        annual[:,doy] = daily_avg
                    
                    
                    # reshaping and mapping
                    daily_avg = daily_avg.reshape(lon_goci.shape)
                    fig, axs = matlab.m_kc(lon_goci,lat_goci,daily_avg)
                    """
                    if i==1:
                        caxis([0 200])
                    else
                        caxis([0 100])
                    """
                    axs.colorbar(fontsize=12)
                    axs.set_title(f'{yr}/{mm:02d}/{dd:02d}', fontsize=14)
                    
                    # save map image
                    name = os.path.join(path_ea_goci, 'RF_map/',type_list[t], target[i],'daily/',f"{target[i]}_RTT_daily_map_{yr:04d}_{doy:03d}")
                    print('-djpeg','-r300',name)
                    print (doy)
                    #close all
                except:
                    print (f"{yr}_{doy:03d}") #[str(yr),'_',str(doy,'#03i')])
                
            
            # save daily prediction matrix
            matlab.savemat(os.path.join(path_ea_goci, 'RF_map/',type_list[t],target[i],'annual/',f'{target[i]}_RTT_EA6km_{yr}.mat'),{'annual':annual})
            
            ## monthly PM mapping
            monthEnds = [0]+np.cumsum(daysInMonths)
            for m in range(1,12+1):
                firstDay = monthEnds[m-1]+1
                lastDay = monthEnds[m]
                
                tmp_axis = list(range(int(firstDay-1), int(lastDay)))
                print (tmp_axis)
                monthly_tmp = annual[:,tmp_axis]
                monthly[:,m-1] = np.nanmean(monthly_tmp,axis=1)               
                monthly_avg = np.reshape(np.nanmean(monthly_tmp,axis=1),lon_goci.shape)
                
                nan_ratio_mon = np.sum(np.isnan(monthly_tmp),axis=1)/monthly_tmp.shape[1]
                nan_ratio_mon = nan_ratio_mon.reshape(lon_goci.shape)
                
                monthly_avg_m = monthly_avg
                monthly_avg_m[nan_ratio_mon>0.95] = np.nan
                
                #reshaping and mapping
                fig, axs = matlab.m_kc(lon_goci,lat_goci,monthly_avg_m)
                axs.colorbar(fontsize=12)
                axs.set_title(f'{yr}/{mm:02d}', fontsize=14)
                #             colormap(jet)
                """
                if i==1:
                    caxis([0 150])
                else
                    caxis([0 60])
                hold on 
                """
                #save map image
                name = os.path.join(path_ea_goci,'RF_map/',type_list[t],target[i],'monthly/',f"{target[i]}_RTT_daily_map_{yr}_{m:02d}")
                print('-djpeg','-r300',name)
                
                print (m)
                #close all
                
            
            matlab.savemat(os.path.join(path_ea_goci, 'RF_map/',type_list[t],target[i],'monthly/',f"{target[i]}_RTT_EA6km_{yr}"), {'monthly':monthly})
            
            ## annual PM mapping
            annual = np.nanmean(monthly,axis=1)
            annual_avg = annual.reshape(lon_goci.shape) 
                      
            nan_ratio_yr = np.sum(np.isnan(monthly),axis=1)/monthly.shape[1]
            nan_ratio_yr = nan_ratio_yr.reshape(lon_goci.shape)
            
            annual_avg_m = annual_avg
            annual_avg_m[nan_ratio_yr>0.95] = np.nan
            
            # reshaping and mapping
            fig, axs = matlab.m_kc(lon_goci,lat_goci,annual_avg_m)
            """
            if i==1
                caxis([0 150])
            else
                caxis([0 60])
            
            colorbar('FontSize',12)
            
            hold on 
            title(str(yr),'fontweight','bold','FontSize',14)
            """
            # save map image
            name = os.path.join(path_ea_goci, 'RF_map/',type_list[t], target[i],'annual/',f"target[i]_RTT_daily_map_{yr}")
            print('-djpeg','-r300',name)
            
            print (yr)
            #close all