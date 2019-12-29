### Package Import
import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import numpy as np
import glob
import time
import copy

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_goci_filter = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_filtered')
path_goci_final = os.path.join(data_base_dir, 'Preprocessed_raw', 'final', 'GOCI') 

path_grid_raw = os.path.join(data_base_dir, 'Raw', 'grid')
path_processed_grid = os.path.join(data_base_dir, 'Preprocessed_raw', 'grid')

### Setting period
YEARS = [2016] #, 2018, 2019

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_korea.mat'))
lat_kor, lon_kor = mat['lat_kor'], mat['lon_kor']
del mat

mat = matlab.loadmat(os.path.join(path_grid_raw, 'grid_goci.mat'))
lat_goci, lon_goci = mat['lat_goci'], mat['lon_goci']
del mat

grid_kor = np.array([lon_kor.ravel(order='F'), lat_kor.ravel(order='F')]).T
grid_goci = np.array([lon_goci.ravel(order='F'), lat_goci.ravel(order='F')]).T

def create_grid_goci_surrPx(grid_goci):
    DT = matlab.delaunayTriangulation(grid_goci)
    ti = DT.find_simplex(grid_kor)
    triPx = DT.simplices[ti, :]

    triPx_UL = np.min(triPx, axis=1)
    I, J = matlab.ind2sub(lon_goci.shape, triPx_UL)
    surrPx = np.zeros((len(I), 4))
    surrPx[:, 0] = matlab.sub2ind(lon_goci.shape, I, J) # Upper Left
    surrPx[:, 1] = matlab.sub2ind(lon_goci.shape, I, J+1) # Upper Right
    surrPx[:, 2] = matlab.sub2ind(lon_goci.shape, I+1, J) # Lower Left
    surrPx[:, 3] = matlab.sub2ind(lon_goci.shape, I+1, J+1) # Lower Right

    lon_surr = lon_goci.T.flatten()[list(surrPx.flatten().astype(int))].reshape(surrPx.shape) # lon_goci[surrPx]
    lat_surr = lat_goci.T.flatten()[list(surrPx.flatten().astype(int))].reshape(surrPx.shape)
    diff_lon = lon_surr - np.tile(grid_kor[:, 0][:, None], (1,4))
    diff_lat = lat_surr - np.tile(grid_kor[:, 1][:, None], (1,4))

    d_surr = np.sqrt(np.power(diff_lon, 2) + np.power(diff_lat, 2))
    invDsq = 1./np.power(d_surr, 2)

    k = np.zeros((len(I), 1))

    for i in range(len(I)):
        k[i] = surrPx[i, d_surr[i, :]==min(d_surr[i, :])]

    fname = os.path.join(path_processed_grid, 'grid_goci_surrPx.mat')
    matlab.savemat(fname, {'surrPx':surrPx, 'd_surr':d_surr, 'invDsq':invDsq, 'k':k})
tStart = time.time()
create_grid_goci_surrPx(grid_goci)    
tElapsed = time.time() - tStart
print (f'time taken for creating grid_goci_surrPx.mat: {tElapsed}')
fname = os.path.join(path_processed_grid, 'grid_goci_surrPx.mat')
mat = matlab.loadmat(fname)
d_surr, invDsq, k, surrPx = mat['d_surr'], mat['invDsq'], mat['k'], mat['surrPx']
del mat


def do_masking(arr):
    # global var: surrPX, k, invDsq, lon_kor
    flatten_arr = arr.T.flatten()
    
    mask = flatten_arr[k.astype(int)]
    mask = np.isnan(mask)
    
    value = flatten_arr[surrPx.flatten().astype(int)].reshape(surrPx.shape)
    valueD = np.multiply(value, invDsq)
    
    invDsq_nan = copy.deepcopy(invDsq)
    invDsq_nan[np.isnan(value)] = np.nan
    
    result_arr = np.divide(np.nansum(valueD, axis=1), np.nansum(invDsq_nan, axis=1))
    result_arr[mask.flatten()] = np.nan
    result_arr = result_arr.reshape(lon_kor.shape)
    
    return result_arr

avgtime = []
for yr in YEARS:
    list_AOD = glob.glob(os.path.join(path_goci_filter, 'AOD', str(yr), "*.mat"))
    list_AOD = [os.path.basename(f) for f in list_AOD]
    list_AOD.sort()
    for fname in list_AOD:
        tStart = time.time()
        doy = int(fname[14:17])
        utc = int(fname[18:20])

        fname = os.path.join(path_goci_filter, 'AOD', str(yr), f'GOCI_AOD_{yr}_{doy:03d}_{utc:02d}.mat')
        GOCI_aod = matlab.loadmat(fname)['GOCI_aod']
        GOCI_aod = do_masking(GOCI_aod)
        fname = os.path.join(path_goci_final, 'AOD', str(yr), f'kor_GOCI_AOD_{yr}_{doy:03d}_{utc:02d}.mat')
        matlab.savemat(fname, {'GOCI_aod':GOCI_aod})

        fname = os.path.join(path_goci_filter, 'AE', str(yr), f'GOCI_AE_{yr}_{doy:03d}_{utc:02d}.mat')
        GOCI_ae = matlab.loadmat(fname)['GOCI_ae']
        GOCI_ae = do_masking(GOCI_ae)
        fname = os.path.join(path_goci_final, 'AE', str(yr), f'kor_GOCI_AE_{yr}_{doy:03d}_{utc:02d}.mat')
        matlab.savemat(fname, {'GOCI_ae':GOCI_ae})

        fname = os.path.join(path_goci_filter, 'FMF', str(yr), f'GOCI_FMF_{yr}_{doy:03d}_{utc:02d}.mat')
        GOCI_fmf = matlab.loadmat(fname)['GOCI_fmf']
        GOCI_fmf = do_masking(GOCI_fmf)
        fname = os.path.join(path_goci_final, 'FMF', str(yr), f'kor_GOCI_FMF_{yr}_{doy:03d}_{utc:02d}.mat')
        matlab.savemat(fname, {'GOCI_fmf':GOCI_fmf})

        fname = os.path.join(path_goci_filter, 'SSA', str(yr), f'GOCI_SSA_{yr}_{doy:03d}_{utc:02d}.mat')
        GOCI_ssa = matlab.loadmat(fname)['GOCI_ssa']
        GOCI_ssa = do_masking(GOCI_ssa)
        fname = os.path.join(path_goci_final, 'SSA', str(yr), f'kor_GOCI_SSA_{yr}_{doy:03d}_{utc:02d}.mat')
        matlab.savemat(fname, {'GOCI_ssa':GOCI_ssa})

        print (f'{yr}_{doy:03d}_{utc:02d}')
        tElapsed = time.time() - tStart
        print (f'time taken : {tElapsed}')
        avgtime.append(tElapsed)
    print (yr)
avgtime = np.nanmean(avgtime)
print (avgtime)
