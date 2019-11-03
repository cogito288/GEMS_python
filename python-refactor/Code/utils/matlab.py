from datetime import date
import numpy as np
from scipy.spatial import Delaunay
import scipy.io as sio
import h5py
import hdf5storage
import gdal
import os
from pyhdf.SD import SD, SDC ### HDF4 

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
    day = int(datestr[6:])
    if (month==0) and (day==0):
        year -= 1
        month = 12
        day = 31
    d = date(year, month, day) # 00:00:00
    return 366 + d.toordinal()

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
    
def dir(dirname, pattern):
    # Not same .. 
    #     list_gpm = matlab.dir(str(yr), '.HDF5')  # list_gpm = dir([num2str(yr),'/*/*.HDF5']);

    
    """
    # https://wikidocs.net/39
    full_fname_list = []
    try:
        for (path, dirs, files) in os.walk(dirname):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if ext == pattern:
                    full_name_list.extend(list(map(lambda x: os.path.join(path, x), files)))
                    #print("%s/%s" % (path, filename))
    except PermissionError:
        pass
    return full_fname_list
    """

def permute(arr, axes):
    if (arr.ndim) == len(axes):
        return np.transpose(arr, axes)
    elif (arr.ndim+1) == len(axes):
        return np.transpose(arr[:, :, None], axes)
    else:
        return None # should be raise error
    