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
from calendar import monthrange

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

def oversampling_sh(data, stn_location, dim1, dim2, nover, patch_path):
    """
    Input
    data = [stn_conc,scode2,doy_num,time,yr,ovr]
    
    Output
    ndata : stn_conc, scode2, doy_num, time, yr, ovr, pid
    """
    if data.shape[1]!=6:
        raise ValueError("The number of columns should be six.")
    if nover>36:
        raise ValueError("The maximum value of nover is 36")
    
    data = np.hstack([data, np.zeros((data.shape[0], 1))])
    for k in range(data.shape[0]):
        data[k,6] = stn_location[stn_location[:,1]==data[k,1], 4]
    x,y = ind2sub([dim1, dim2], data[:, 6])
    data = np.hstack([data, x.reshape((-1,1), order='F'), y.reshape((-1,1), order='F')])
    conc = data[:, 0]
    nr, nc = data.shape
    
    patch = loadmat(patch_path)['patch']
    op = patch[:, :, :nover]
    
    ndata = np.tile(data, (1,1,nover))
    ndata[:,7:9,:] = ndata[:,7:9,:] + op
    ndata = np.transpose(ndata, (2,0,1)).reshape(-1, nc)
    ndata[:,5] = 1
    
    idx = (ndata[:, 7]<=0)
    ndata = ndata[~idx, :]
    
    idx = (ndata[:, 8]<=0)
    ndata = ndata[~idx, :]
    
    idx = ndata[:, 7]>dim1
    ndata = ndata[~idx, :]
    
    idx = ndata[:, 8]>dim2
    ndata = ndata[~idx, :]
    
    ndata[:, 6] = sub2ind([dim1, dim2], ndata[:, 7], ndata[:, 8])
    #% ndata: [stn_conc,scode2,doy,utc,yr,ovr,pxid,stn_x,stn_y];
    ndata[ndata[:, 5]==1, 0] = np.multiply(ndata[ndata[:, 5]==1, 0], 
                                           (0.1*np.random.random(size=(np.sum(ndata[:, 5]).astype(int)))+0.95))
    
    #% remove station pixel among oversampled pixels
    dup_idx = np.isin(ndata[:, 6], stn_location[:, 4])
    dup_idx = np.multiply(dup_idx, ndata[:, 5])
    ndata = ndata[dup_idx==0, :]
    
    ndata = ndata[:, :7]
    return ndata
                                                         
def histogram_bin_center(x, bin_centers):
    # https://stackoverflow.com/questions/18065951/why-does-numpy-histogram-python-leave-off-one-element-as-compared-to-hist-in-m
    bin_edges = np.r_[-np.Inf, 0.5 * (bin_centers[:-1] + bin_centers[1:]), 
        np.Inf]
    counts, edges =  np.histogram(x, bin_edges)
    return counts

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

def h5read(filename, datasetname):
    with h5py.File(filename, 'r') as f:
        data = f.get(datasetname)[:]
    if data.flags['C_CONTIGUOUS'] and (not data.flags['F_CONTIGUOUS']):
        data = data.T
    return data

def loadmat(path):
    # First, try to load using h5py only working for 7.3 mat 
    # Second, try to load using scipy io working for 5.0 mat
    result = None
    try:
        with h5py.File(path, 'r') as f:
            if f.keys(): # if key not empty
                result = dict()
                for key in f.keys():
                    result[key] = np.array(f.get(key)) # num type
                    # Convert to F order
                    if result[key].flags['C_CONTIGUOUS'] and (not result[key].flags['F_CONTIGUOUS']):
                        result[key] = result[key].T
    except OSError:
        result = sio.loadmat(path)
        pass
    return result

    

####### Debugging #########
def check_make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
###########################

def savemat(fname, data):
    ### Description
    # Matlab: default < 2 GB. More than 2 GB: 7.3v 
    # scipy.io.savemat can save maximally 4 GB.
    ### Input:
    # dirname: directory name for hdf5storage
    # fname: filename
    # data: dictionary
    check_make_dir(os.path.dirname(fname)) # debugging
    #sio.savemat(os.path.join(dirname, fname), mdict=data)
    hdf5storage.writes(mdict=data,
                      filename=fname,
                      matlab_compatible=True,
                      compress=True,
                      compression_algorithm='gzip')
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
    num_days = monthrange(year, month)[1]
    if day>num_days:
        month += 1
        day = day-num_days
    d = date(year, month, day) # 00:00:00
    result = 366 + d.toordinal() 
    if len(datestr)>8: # suspect yyyymmddHH
        hour = int(datestr[8:10])
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
    
    """
    tri = DT.simplices
    keep = np.ones(len(tri), dtype = bool)
    for i, t in enumerate(tri):
        if abs(np.linalg.det(np.hstack((points[t], np.ones([1,N+1]).T)))) < 1E-15:
            keep[i] = False # Point is coplanar, we don't want to keep it
    tri = tri[keep]
    DT.simplices = tri
    """
    return DT
"""
def ind2sub(siz, IND):
    return np.unravel_index(IND, siz)
def sub2ind(siz, dim1, dim2):
    return np.ravel_multi_index(siz, (dim1, dim2))
"""
def ind2sub(array_shape, ind):
    if len(array_shape) == 2:
        rows = (ind.astype('int') % array_shape[0]).astype(int)
        cols = (ind.astype('int') / array_shape[0]).astype(int) # or numpy.mod(ind.astype('int'), array_shape[1])
        return (rows, cols)
    else:
        raise NotImplementedError
        
def sub2ind(array_shape, rows, cols):
    if len(array_shape) == 2:
        return (rows + cols*array_shape[0]).astype(int)
    else:
        raise NotImplementedError
    
def length(arr):
    if isinstance(arr, np.ndarray):
        return max(arr.shape)
    elif isinstance(arr, list):
        return len(arr)
    else:
        raise NotImplementedError

def ismember(A, B):
    return np.nonzero(np.in1d(A,B))[0]

"""
def repmat(arr, change_size):
    if len(change_size)==2:
        m, n = change_size
        return np.tile(arr, (n, m)).T
    elif len(change_size)==3:
        m, n, r = change_size
        return np.tile(arr, (n, r, m))
    else:
        raise NotImplementedError
"""

def permute(arr, change_size):
    if (len(change_size)!=3) or (len(arr.shape)!=3):
        raise NotImplementedError
    return np.transpose(arr, change_size)


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
    ax.contourf(lon, lat, data)
    ax.set_title(f"{yr}/{mm:02d}", fontsize=25)
    #plt.show()   
    return fig

def heatscatter_paper(X, Y, outpath, outname, numbins=120, markersize=20, marker='o', plot_colorbar=1, plot_lsf=True, xlab=None, ylab=None, titl=None):
    """
    %% heatscatter(X, Y, outpath, outname, numbins, markersize, marker, plot_colorbar, plot_lsf, xlab, ylab, title)
    % mandatory:
    %            X                  [x,1] array containing variable X
    %            Y                  [y,1] array containing variable Y
    %            outpath            path where the output-file should be saved.
    %                                leave blank for current working directory
    %            outname            name of the output-file. if outname contains
    %                                filetype (e.g. png), this type will be used.
    %                                Otherwise, a pdf-file will be generated
    % optional:
    %            numbins            [double], default 50
    %                                number if bins used for the
    %                                heat3-calculation, thus the coloring
    %            markersize         [double], default 10
    %                                size of the marker used in the scatter-plot
    %            marker             [char], default 'o'
    %                                type of the marker used in the scatter-plot
    %            plot_colorbar      [double], boolean 0/1, default 1
    %                                set whether the colorbar should be plotted
    %                                or not
    %            plot_lsf           [boolean], boolean False/True, default True
    %                                set whether the least-square-fit line
    %                                should be plotted or not (together with
    %                                the correlation/p-value of the data
    %            xlab               [char], default ''
    %                                lable for the x-axis
    %            ylab               [char], default ''
    %                                lable for the y-axis
    %            title              [char], default ''
    %                                title of the figure
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    hist, xedges, yedges = np.histogram2d(X, Y, bins=(numbins,numbins))
    xpos, ypos = np.meshgrid(xedges[:-1]+xedges[1:], yedges[:-1]+yedges[1:])

    xpos = xpos.flatten()/2.
    ypos = ypos.flatten()/2.
    zpos = np.zeros_like(xpos)

    dx = xedges [1] - xedges [0]
    dy = yedges [1] - yedges [0]
    dz = hist.flatten()

    cmap = cm.get_cmap('jet') # Get desired colormap - you can change this!
    max_height = np.max(dz)   # get range of colorbars so we can normalize
    min_height = np.min(dz)
    # scale each z to [0,1], and get their rgb values
    rgba = [cmap((k-min_height)/max_height) for k in dz] 
    
    fig, ax = plt.subplots(1,1)
    ax.scatter(X, Y, s=markersize, c=rgba, marker=marker)
    
    from sklearn.metrics import mean_squared_error
    if (plot_lsf):
        OLS = np.polyfit(X,Y,1)
        correlation_coeff = np.corr(X,Y)
        R_squre = np.power(correlation_coeff,2)
        RMSE = np.sqrt(mean_squared_error(X, Y));
        rRMSE = 100*RMSE/mean(X);
        RMSE_unit = '(\mug/m^3)'; #%'(ppm)';
        unit = '(%)';
        
        annotation = f'Y: {OLS[0]:.2f} x + {OLS[1]:.2f} \n R^2 : {R_squre:.2f} \n RMSE : {RMSE:.2f} {RMSE_unit} \n rRMSE: {rRMSE:.1f} {unit}'
        l = lsline;
        set(l, 'Color', 'k');

        ax.annotate(annotation, xy=(0.25, 0.80), xytext=(0.1, 0.1), 
                     bbox=dict(boxstyle='square', color=None), 
                     )
        plt.rc('font', size=12) 
        Max = np.max(X)
        Max = Max/100;
        MM = np.ceil(Max)
        MM = MM*100;
        ax.set_xlim(0, MM)
        ax.set_ylim(0, MM)
        
        #line([0 MM],[0 MM],'Color','k','LineStyle',':');
        
        if xlab is not None:
            ax.set_xlabel(xlab, fontsize=13)
        if ylab is not None:
            ax.set_ylabel(ylab, fontsize=13)
        if titl is not None:
            ax.set_title(titl, fontsize=16)

    fname, ext = os.path.splitext(outname)
    if exe=='':
        outname += '.pdf'
    outfile = os.path.join(outpath, outname)
    
    #%     print('-djpeg','-r1000',outfile);
    #%     saveas(f, outfile);
    print (' Done!\n');
    plt.show()
    
def m_kor(lon,lat,data,*args):
    numarg = 3+len(args)

    if numarg == 3:
        numplot = 1
    elif numarg == 6:
        numplot = 2
    elif numarg == 9:
        numplot = 3
    elif numarg == 12:
        numplot = 4
    else:
        raise ValueError('Please enter the command correctly.')

    east = 131.5
    west = 124
    north = 39
    south = 33
    if numarg == 3:
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplots(1,1,1, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(lon, lat, data) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
        plt.show()   
        
    elif numarg == 6:
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplots(1,2,1, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(lon, lat, data) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
        
        ax = fig.add_subplots(1,2,2, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(args[0], args[1], args[2]) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
       

    elif numarg == 9:
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplots(1,numplot,1, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(lon, lat, data) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
        
        ax = fig.add_subplots(1,numplot,2, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(args[0], args[1], args[2]) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
        
        ax = fig.add_subplots(1,numplot,3, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(args[3], args[4], args[5]) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);

    elif numarg == 12:
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplots(1,numplot,1, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(lon, lat, data) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
        
        ax = fig.add_subplots(1,numplot,2, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(args[0], args[1], args[2]) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
        
        ax = fig.add_subplots(1,numplot,3, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(args[3], args[4], args[5]) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
        
        ax = fig.add_subplots(1,numplot,4, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(args[6], args[7], args[8]) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
    return fig, fig.axes

def m_kc(lon,lat,data,*args):
    numarg = 3+len(args)

    if numarg == 3:
        numplot = 1
    elif numarg == 6:
        numplot = 2
    elif numarg == 9:
        numplot = 3
    elif numarg == 12:
        numplot = 4
    else:
        raise ValueError('Please enter the command correctly.')
                          
    east = 131.5
    west = 113
    north = 48
    south = 24
    if numarg == 3:
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplots(1,1,1, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(lon, lat, data) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
        plt.show()   
        
    elif numarg == 6:
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplots(1,2,1, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(lon, lat, data) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
        
        ax = fig.add_subplots(1,2,2, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(args[0], args[1], args[2]) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
       

    elif numarg == 9:
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplots(1,numplot,1, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(lon, lat, data) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
        
        ax = fig.add_subplots(1,numplot,2, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(args[0], args[1], args[2]) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
        
        ax = fig.add_subplots(1,numplot,3, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(args[3], args[4], args[5]) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);

    elif numarg == 12:
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplots(1,numplot,1, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(lon, lat, data) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
        
        ax = fig.add_subplots(1,numplot,2, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(args[0], args[1], args[2]) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
        
        ax = fig.add_subplots(1,numplot,3, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(args[3], args[4], args[5]) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
        
        ax = fig.add_subplots(1,numplot,4, projection=ccrs.LambertConformal(central_longitude=(east+west)/2))
        ax.set_extent([west, east, south, north])
        ax.gridlines()  # m_grid('box','fancy','tickdir','in','fontsize',20);
        ax.contourf(args[6], args[7], args[8]) # m_pcolor(lon,lat,data); shading flat
        ax.coastlines() #  m_gshhs_i('color','k','linewidth',2);
    return fig, fig.axes