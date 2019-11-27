from datetime import date
import numpy as np
from scipy.spatial import Delaunay
import scipy.io as sio
import h5py
import hdf5storage
import gdal
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from pyhdf.SD import SD, SDC ### HDF4 

"""
Notes
[A, B]  -> np.concatenate((A,B),axis=1)
[A; B]  -> np.concatenate((A,B),axis=0)

[b,I] = sortrows(a,i)  ->       I = argsort(a[:,i]), b=a[I,:]
"""


"""
def csvwrite_with_headers(path, data, header):
	#% This function functions like the build in MATLAB function csvwrite but
	#% allows a row of headers to be easily inserted
	#%
	#% known limitations
	#% 	The same limitation that apply to the data structure that exist with
	#%   csvwrite apply in this function, notably:
	#%       m must not be a cell array
	#%
	#% Inputs
	#%
	#%   filename    - Output filename
	#%   m           - array of data
	#%   headers     - a cell array of strings containing the column headers.
	#%                 The length must be the same as the number of columns in m.
	#%   r           - row offset of the data (optional parameter)
	#%   c           - column offset of the data (optional parameter)
	#%
	#%
	#% Outputs
	#%   None
	#%% initial checks on the inputs
	#if ~ischar(filename)
    #	error('FILENAME must be a string');
	#end

	#% the r and c inputs are optional and need to be filled in if they are
	#% missing
	#if nargin < 4
    #	r = 0;
	#end
	# if nargin < 5
    #	c = 0;
	#end

	#if ~iscellstr(headers)
    #	error('Header must be cell array of strings')
	#end

	if len(header) != data.shape[1]:	#if length(headers) ~= size(m,2)
		raise ValueError('number of header entries must match the number of columns in the data')
	#%% write the header string to the file
	#%turn the headers into a single comma seperated string if it is a cell
	#%array,
	header_string = headers[0]
	for col in headers[1:]:
		header_string += ',{}'.format(col)
	#%if the data has an offset shifting it right then blank commas must
	#%be inserted to match
	if r>0:
    	for i in range(r):
        header_string = [',',header_string];
    end
end

%write the string to a file
fid = fopen(filename,'w');
fprintf(fid,'%s\r\n',header_string);
fclose(fid);

%% write the append the data to the file

%
% Call dlmwrite with a comma as the delimiter
%
dlmwrite(filename, m,'-append','delimiter',',','roffset', r,'coffset',c);
"""


    
    
# https://stackoverflow.com/questions/620305/convert-year-month-day-to-day-of-year-in-python
def is_leap_year(year):
    """ if year is a leap year return True
        else return False """
    if year % 100 == 0:
        return year % 400 == 0
    return year % 4 == 0

def get_doy(Y,M,D):
    """ given year, month, day return day of year
        Astronomical Algorithms, Jean Meeus, 2d ed, 1998, chap 7 """
    if is_leap_year(Y):
        K = 1
    else:
        K = 2
    N = int((275 * M) / 9.0) - K * int((M + 9) / 12.0) + D - 30
    return N

def get_ymd(Y,N):
    """ given year = Y and day of year = N, return year, month, day
        Astronomical Algorithms, Jean Meeus, 2d ed, 1998, chap 7 """    
    if is_leap_year(Y):
        K = 1
    else:
        K = 2
    M = int((9 * (K + N)) / 275.0 + 0.98)
    if N < 32:
        M = 1
    D = N - int((275 * M) / 9.0) + K * int((M + 9) / 12.0) + 30
    return Y, M, D
    

def sortrows(arr, columns):
    # B = sortrows(A,column)
    # np.lexsort ? 
    # Should test performance 
    # columns : list
    tmp_df = pd.DataFram(arr, columns=list(range(arr.ndim)))
    tmp_df.sort_values(by=columns, inplace=True)
    data = tmp_df.values
    del tmp_df
    return data         

def hdfread(path, dataset): # HDF4
    result = None
    hdf_file =  SD(path, SDC.READ)
    sds_obj = hdf_file.select(dataset)
    result = sds_obj.get()
    return result

def loadmat(path, keys=[]):
    # corresponds to load
    data = sio.loadmat(path)
    new_data = []
    if keys:
        for key in keys:
            new_data.append(data[key])
        return new_data
    else:
        return data
    """
    # Since we save hdf as scipy mat, we should using scipy.io.loadmat
    # Otherwise, we should change loadmat and savemat both to use h5py or hdf5storage
    arr = None
    with h5py.File(path, 'r') as f:
        if keys: # not empty
            arr = dict()
            for key in keys:
                data = f.get(key)
                data = np.array(data)
                arr[key] = data
        else: # if key(datasetname) is empty
            arr = f
    return arr
    """

####### Debugging #########
def check_make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
###########################

def savemat(dirname, fname, data):
    ### Description
    # Matlab: default < 2 GB. More than 2 GB: 7.3v 
    # scipy.io.savemat can save maximally 4 GB.
    ### Input:
    # dirname: directory name for hdf5storage
    # fname: filename
    # data: dictionary
    check_make_dir(dirname) # debugging
    sio.savemat(os.path.join(dirname, fname), mdict=data)
    """
    For matlab 7.3 mat saving
    if not isinstance(data, dict):
        hdf5storage.write(data, dirname, fname, matlab_compatible=True)
    else:
        filename = os.path.join(dirname, fname)
        hdf5storage.writes(data, filename=filename, matlab_compatible=True)
    """

def datenum(datestr):
    # matlab datenum
    # Ordinal 1:
    #     Matlab: January 1 of year 0
    #     Python: January 1 of year 1
    year = int(datestr[:4])
    month = int(datestr[4:6])
    day = int(datestr[6:8])
    if (month==0) and (day==0):
        year -= 1
        month = 12
        day = 31
        
    d = date(year, month, day) # 00:00:00
    result = 366 + d.toordinal() 
    if len(datestr)>8: # suspect yyyymmddHH
        hour = datestr[8:10]
        result += (hour/24)
    return result

def datestr(ordinal):
    origin = np.datetime64('0000-01-01', 'D') - np.timedelta64(1, 'D')
    date = ordinal * np.timedelta64(1, 'D') + origin
    return date


def delaunayTriangulation(points):
    # https://stackoverflow.com/questions/36604172/difference-between-matlab-delaunayn-and-scipy-delaunay
    N = points.ndim # The dimensions of points
    options = 'Qt Qbb Qc' if N <= 3 else 'Qt Qbb Qc Qx' # Set the QHull options
    DT = Delaunay(points, qhull_options = options)
    
    tri = DT.simplices
    keep = np.ones(len(tri), dtype = bool)
    for i, t in enumerate(tri):
        if abs(np.linalg.det(np.hstack((points[t], np.ones([1,N+1]).T)))) < 1E-15:
            keep[i] = False # Point is coplanar, we don't want to keep it
    tri = tri[keep]
    DT.simplices = tri
    
    return DT
"""
def ind2sub(siz, IND):
    return np.unravel_index(IND, siz)

def sub2ind(siz, dim1, dim2):
    return np.ravel_multi_index(siz, (dim1, dim2))
"""
def ind2sub(array_shape, ind):
    if len(array_shape) != 2:
        raise NotImplementedError
    rows = (ind.astype('int') / array_shape[1]).astype(int)
    cols = (ind.astype('int') % array_shape[1]).astype(int) # or numpy.mod(ind.astype('int'), array_shape[1])
    return (rows, cols)

def sub2ind(array_shape, rows, cols):
    if len(array_shape) != 2:
        raise NotImplementedError
    return (rows*array_shape[1] + cols).astype(int)

def length(arr):
    if isinstance(arr, np.ndarray):
        return max(arr.shape)
    elif isinstance(arr, list):
        return len(arr)
    else:
        raise NotImplementedError

def ismember(A, B):
    return np.nonzero(np.in1d(A,B))[0]
        
def repmat(arr, change_size):
    if len(change_size)==2:
        m, n = rep_size
        return np.tile(arr, (n, m)).T
    elif len(change_size)==3:
        m, n, r = rep_size
        return np.tile(arr, (n, r, m))
    else:
        raise NotImplementedError
        
def permute(arr, change_size):
    if (len(change_size)!=3) or (len(arr.shape)!=3):
        raise NotImplementedError
    return np.transpose(arr, change_size)

def h5read(filename, datasetname):
    with h5py.File(filename, 'r') as f:
        data = f.get(datasetname)[:]
    return data

def get_files_endswith(dirname, pattern):
    # Simple dir 
    # e.g. dir('*.tif')
    # Here, pattern: ".tif"
    files = []
    for file in os.listdir(dirname):
        if os.endswith(pattern):
            files.append(file)
    return files

def permute(arr, axes):
    if (arr.ndim) == len(axes):
        return np.transpose(arr, axes)
    elif (arr.ndim+1) == len(axes):
        return np.transpose(arr[:, :, None], axes)
    else:
        return None # should be raise error
    
def heatscatter_paper(X, Y, outpath, outname, numbins=120, markersize=20, marker='o',
                      plot_colorbar=1, plot_lsf=1, xlab='', ylab='', title=''):
    # (X, Y, outpath, outname, numbins, markersize, marker, plot_colorbar, plot_lsf, xlab, ylab, title)
    # (val_scatter[:,0], val_scatter[:,1], [path,'/dataset/scatterplot'], 'PM10_RF_val.jpg','','','',1,'','Observed PM_1_0 Concentration (\mug/m^3)','Estimated PM_1_0 Concentration (\mug/m^3)','PM_1_0 Validation')
    values, xedges, yedges = np.histogram2d(X, Y, [numbins, numbins])
    centers_X = (xedges[:-1] + xedges[1:]) / 2
    centers_Y = (yedges[:-1] + yedges[1:]) / 2
    
    binsize_X = np.abs(centers_X[1] - centers_X[0]) / 2
    binsize_Y = np.abs(centers_Y[1] - centers_Y[0]) / 2
    bins_X = np.zeros((numbins, 2))
    bins_Y = np.zeros((numbins, 2))
    
    for i in range(numbins):
        bins_X[i, 0] = centers_X[i] - binsize_X
        bins_X[i, 1] = centers_X[i] + binsize_X
        bins_Y[i, 0] = centers_Y[i] - binsize_Y
        bins_Y[i, 1] = centers_Y[i] + binsize_Y
    scatter_COL = np.zeros((length(X), 1))
    onepercent = np.round(length(X) / 100)    
    print ('Generating colormap...\n')
    # Need to implement more
    
def m_kor(lon, lat, data):
    east = 131.5
    west = 124
    north = 39
    south = 33
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplots(1,1,1, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
    ax.set_extent([west, east, south, north])
    ax.gridlines()
    ax.contourf(lons, lats, data)
    ax.set_title(f"{yr}/{mm:02d}", fontsize=25)
    #plt.show()   
    return fig
