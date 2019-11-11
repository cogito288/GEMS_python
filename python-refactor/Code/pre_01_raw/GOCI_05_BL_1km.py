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

### Setting path
data_base_dir = os.path.join('/', 'media', 'sf_GEMS', 'Data')
goci_path = os.path.join(data_base_dir, 'Preprocessed_raw', 'GOCI_filtered') 
korea_path = os.path.join(data_base_dir, 'Station', 'AirQuality_Korea')

### Setting period
YEARS = [2016] #, 2018, 2019

lat_kor, lon_kor = matlab.loadmat(os.path.join(data_base_dir, 'grid', 'grid_korea.mat'), keys=['lat_kor', 'lon_kor'])
lat_goci, lon_goci = matlab.loadmat(os.path.join(data_base_dir, 'grid', 'grid_goci.mat'), keys=['lat_goci', 'lon_goci'])

grid_goci = np.vstack((lon_goci.T.flatten(), lat_goci.T.flatten())).T
grid_kor = np.vstack((lon_kor.T.flatten(), lat_kor.T.flatten())).T
"""
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

lon_surr = lon_goci.flatten()[list(surrPx.flatten().astype(int))].reshape(surrPx.shape) # lon_goci[surrPx]
lat_surr = lat_goci.flatten()[list(surrPx.flatten().astype(int))].reshape(surrPx.shape)
diff_lon = lon_surr - matlab.repmat(grid_kor[:, 0], (1, 4))
diff_lat = lat_surr - matlab.repmat(grid_kor[:, 1], (1, 4))

d_surr = np.sqrt(np.power(diff_lon, 2) + np.power(diff_lat, 2))
invDsq = 1./np.power(d_surr, 2)

k = np.zeros((matlab.length(I), 1))

for i in range(matlab.length(I)):
    k[i] = surrPx[i, d_surr[i, :]==min(d_surr[i, :])]

matlab.savemat(os.path.join(data_base_dir, 'grid'), 'grid_goci_surrPx.mat', {'surrPx':surrPx, 'd_surr':d_surr, 'invDsq':invDsq, 'k':k})
"""
d_surr, invDsq, k, surrPx = matlab.loadmat(os.path.join(data_base_dir, 'grid', 'grid_goci_surrPx.mat'), keys=['d_surr', 'invDsq', 'k', 'surrPx'])

def do_masking(GOCI):
    # global var: surrPX, k, invDsq, lon_kor
    GOCI = GOCI_aod
    mask = GOCI.flatten()[k.astype(int)]
    mask = np.isnan(mask)
    value = GOCI.flatten()[list(surrPx.flatten().astype(int))].reshape(surrPx.shape)
    valueD = np.multiply(value, invDsq) # ".*": element-wise multiplication
    invDsq_nan = invDsq
    invDsq_nan[np.isnan(value)] = np.nan
    GOCI = np.divide(np.nansum(valueD, axis=1), np.nansum(invDsq_nan, axis=1))
    GOCI = GOCI.reshape(lon_kor.shape)
    #GOCI[mask] = np.nan
    tmp = GOCI.flatten()
    tmp[mask.flatten()] = np.nan
    GOCI = tmp.reshape(GOCI.shape)
    return GOCI

avgtime = []
YEARS = [2016] # YEARS = range(2016, 2019+1)
for yr in YEARS:
    list_AOD = glob.glob(os.path.join(goci_path, 'AOD', str(yr), "*.mat"))
    list_AE = glob.glob(os.path.join(goci_path, 'AE', str(yr), "*.mat")) 
    list_FMF = glob.glob(os.path.join(goci_path, 'FMF', str(yr), "*.mat"))
    list_SSA = glob.glob(os.path.join(goci_path, 'SSA', str(yr), "*.mat"))
    list_AOD = [os.path.basename(f) for f in list_AOD]
    list_AE = [os.path.basename(f) for f in list_AE]
    list_FMF = [os.path.basename(f) for f in list_FMF]
    list_SSA = [os.path.basename(f) for f in list_SSA]
    
    for j in range(len(list_AOD)):
        tStart = time.time()
        mat = matlab.loadmat(os.path.join(goci_path, 'AOD', str(yr), list_AOD[j]))
        GOCI_aod = mat['GOCI_aod']
        mat = matlab.loadmat(os.path.join(goci_path, 'AE', str(yr), list_AE[j]))
        GOCI_ae = mat['GOCI_ae']
        mat = matlab.loadmat(os.path.join(goci_path, 'FMF', str(yr), list_FMF[j]))
        GOCI_fmf = mat['GOCI_fmf']
        mat = matlab.loadmat(os.path.join(goci_path, 'SSA', str(yr), list_SSA[j]))
        GOCI_ssa = mat['GOCI_ssa']
        
        GOCI_aod = do_masking(GOCI_aod)
        GOCI_ae = do_masking(GOCI_ae)
        GOCI_ssa = do_masking(GOCI_ssa)

        matlab.savemat(os.path.join(goci_path, 'GOCI', 'AOD', str(yr)), f'kor_{list_AOD[j]}.mat', {'GOCI_aod':GOCI_aod})
        matlab.savemat(os.path.join(goci_path, 'GOCI', 'AE', str(yr)), f'kor_{list_AE[j]}.mat', {'GOCI_AE':GOCI_ae})
        matlab.savemat(os.path.join(goci_path, 'GOCI', 'FMF', str(yr)), f'kor_{list_FMF[j]}.mat', {'GOCI_FMF':GOCI_fmf})
        matlab.savemat(os.path.join(goci_path, 'GOCI', 'SSA', str(yr)), f'kor_{list_SSA[j]}.mat', {'GOCI_SSA':GOCI_ssa})
        print (list_AOD[j])
        tEnd = time.time()
        avgtime.append(tEnd-tStart)
    print (yr)
avgtime = np.nanmean(avgtime)
print (avgtime)
