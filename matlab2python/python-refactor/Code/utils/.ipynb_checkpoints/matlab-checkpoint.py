from datetime import date
import numpy as np
from scipy.spatial import Delaunay
import h5py

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

def ind2sub(siz, IND):
    return np.unravel_index(IND, siz)

def sub2ind(siz, dim1, dim2):
    return np.ravel_multi_index(siz, (dim1, dim2))

def length(arr):
    return max(arr.shape)

def h5read(filename, datasetname):
    with h5py.File(filename, 'r') as f:
        data = f.get(datasetname)[:]
    return data

def dir(dirname, pattern):
    # Not same .. 
    #     list_gpm = matlab.dir(str(yr), '.HDF5')  # list_gpm = dir([num2str(yr),'/*/*.HDF5']);
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

def permute(arr, axes):
    if (arr.ndim) == len(axes):
        return np.transpose(arr, axes)
    elif (arr.ndim+1) == len(axes):
        return np.transpose(arr[:, :, None], axes)
    else:
        return None # should be raise error