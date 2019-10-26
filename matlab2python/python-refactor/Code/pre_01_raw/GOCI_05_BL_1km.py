### Package Import
import os
import scipy.io as sio
from scipy.spatial import Delaunay
import time

import sys
project_path = '/home/cogito/Uncertainty/matlab2python/python-refactor'
sys.path.insert(0, project_path)

from Code.utils.matlab import *
from Code.utils.helpers import *

### Setting path
# path_data = '/share/irisnas6/Data/GOCI_AOD/01mat/GOCI/';
# path = '/share/irisnas6/Data/GOCI_AOD/01mat/GOCI_filtered/';
data_path = os.path.join(project_path, 'Data', 'Prepreossed_raw', 'GOCI_AOD') 
goci_path = os.path.join(project_path, 'Data', 'Prepreossed_raw', 'GOCI_filtered')
korea_path = os.path.join(project_path, 'Data', 'Station', 'AirQuality_Korea')
#os.chdir(data_path)

grid_goci = sio.loadmat(os.path.join(data_path, 'grid', 'grid_korea.mat'))
grid_kor = sio.loadmat(os.path.join(data_path, 'grid', 'grid_goci.mat'))

grid_goci = list(zip(lon_goci.flatten(), lat_goci.flatten()))
grid_kor = list(zip(lon_kor.flatten(), lat_kor.flatten()))

"""
### Find surrounding pixels using delaunay triangulation
DT = matlab.delaunayTriangulation(grid_goci)
ti = DT.find_simplex(grid_kor)
triPx = DT[ti, :]
triPx_UL = np.min(triPx, axis=1)
I, J = matlab.ind2sub(lon_goci.shape, triPx_UL)
surrPx = np.zeros(mathlab.length(I), 4)
surrPx[:, 1] = matlab.sub2ind(lon_goci.shape, I, J) # Upper Left
surrPx[:, 2] = matlab.sub2ind(lon_goci.shape, I, J+1) # Upper Right
surrPx[:, 3] = matlab.sub2ind(lon_goci.shape, I+1, J) # Lower Left
surrPx[:, 4] = matlab.sub2ind(lon_goci.shape, I+1, J+1) # Lower Right

lon_surr = lon_goci[surrPx]
lat_surr = lat_goci[surrPx]
diff_lon = lon_surr - np.tile(grid_kor[:, 1], (1, 4))
diff_lat = lat_surr - np.tile(grid_kor[:, 2], (1, 4))

d_surr = np.sqrt(np.power(diff_lon, 2) + np.power(diff_lat))
inDsq = 1./np.power(d_surr)

k = np.zeros(matlab.length(I), 1)
for i in range(matlab.length(I)):
    k[i] = surrPx[i, d_surr[i, :]==min(d_surr[i, :])]
sio.savemat(os.path.join(data_path, 'grid_goci_surrPx.mat', mdict={'surrPx':surrPx, 'd_surr':d_surr, 'invDsq':invDsq, 'k':k}))
"""
surrPx = sio.loadmat(os.path.join(data_path, 'grid', 'grid_goci_surrPx.mat'))
def do_masking(GOCI):
    # global var: surrPX, k, invDsq, lon_kor
    mask = GOCI[k]
    mask = np.isnan(mask)
    value = GOCI[surrPx]
    valueD = np.multiply(value, invDsq) # ".*": element-wise multiplication
    invDsq_nan = invDsq
    invDsq_nan[np.isnan(value)] = np.nan
    GOCI = np.divide(np.nansum(valueD, axis=1), np.nansum(invDsq_nan, axis=1))
    GOCI = GOCI.reshape(lon_kor.shape)
    GOCI[mask] = np.nan
    return GOCI

avgtime = []
YEARS = range(2017, 2019+1)
for yr in YEARS:
    list_AOD = get_file_lists(os.path.join(goci_path, 'AOD', str(yr)), ".mat")
    list_AE = get_file_lists(os.path.join(goci_path, 'AE', str(yr)), ".mat")    
    list_FMF = get_file_lists(os.path.join(goci_path, 'FMF', str(yr)), ".mat")
    list_SSA = get_file_lists(os.path.join(goci_path, 'SSA', str(yr)), ".mat")
    
    for j in range(len(list_AOD)):
        tStart = time.time()
        GOCI_aod = sio.loadmat(os.path.join(goci_path, 'AOD', str(yr), list_AOD[j]))
        GOCI_ae = sio.loadmat(os.path.join(goci_path, 'AE', str(yr), list_AE[j]))
        GOCI_fmf = sio.loadmat(os.path.join(goci_path, 'FMF', str(yr), list_FMF[j]))
        GOCI_ssa = sio.loadmat(os.path.join(goci_path, 'SSA', str(yr), list_SSA[j]))
        
        GOCI_aod = do_masking(GOCI_aod)
        GOCI_ae = do_masking(GOCI_ae)
        GOCI_ssa = do_masking(GOCI_ssa)
        
        sio.savemat(os.path.join(goci_path, 'GOCI', 'AOD', str(yr), f'kor_{list_AOD[j]}.mat'), mdict={'GOCI_aod':GOCI_aod})
        sio.savemat(os.path.join(goci_path, 'GOCI', 'AE', str(yr), f'kor_{list_AE[j]}.mat'), mdict={'GOCI_AE':GOCI_ae})
        sio.savemat(os.path.join(goci_path, 'GOCI', 'FMF', str(yr), f'kor_{list_FMF[j]}.mat'), mdict={'GOCI_FMF':GOCI_fmf})
        sio.savemat(os.path.join(goci_path, 'GOCI', 'SSA', str(yr), f'kor_{list_SSA[j]}.mat'), mdict={'GOCI_SSA':GOCI_ssa})
        
        print (list_AOD[j])
        tEnd = time.time()
        avgtime.append(tEnd-tStart)
    print (yr)

avgtime = np.nanmean(avgtime)
print (avgtime)