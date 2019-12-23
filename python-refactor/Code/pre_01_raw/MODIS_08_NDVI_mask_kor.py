import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

from rasterio.mask import mask
import glob
from fiona.crs import from_epsg
from shapely.geometry import box
import rasterio as rio
import geopandas as gpd

### Setting path
data_base_dir = os.path.join(project_path, 'Data')
path_modis = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS', 'MYD13A2')
"""
maskfile = os.path.join(data_base_dir, 'Raw', 'mask', 'r_mask_korea.tif')
with rio.open(maskfile) as masksrc:
    band = masksrc.read(1)
    maskarr = (band!=255)
    shapes = []
    for geometry, raster_value in features.shapes(band, mask=maskarr, transform=masksrc.transform):
        shapes.append(json.loads(json.dumps(geometry)))
"""
dst_crs = 'EPSG:4326'
# WGS84 coordinates
minx, miny = 123.995024793363, 32.9983435120948
maxx, maxy = 131.513769680712, 39.0077492770766
bbox = box(minx, miny, maxx, maxy)
geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=from_epsg(4326))

def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]


YEARS = [2016]
for yr in YEARS:
    print(yr)
    flist = glob.glob(os.path.join(path_modis, '02prj_GCS_WGS84', str(yr), "*.tif"))
    flist.sort()
    for src_dataset in flist:
        dst_dataset = os.path.join(path_modis, '03mask_SouthKorea_MYD13A2', str(yr), f'm_{os.path.basename(src_dataset)[2:]}')
        matlab.check_make_dir(os.path.dirname(dst_dataset))
        with rio.open(src_dataset) as dst02:
            geo = geo.to_crs(crs=dst02.crs.data)
            coords = getFeatures(geo)
            out_img, out_transform = mask(dataset=dst02, shapes=coords, crop=True)
            out_meta = dst02.meta.copy()
            out_meta.update({"height": out_img.shape[1],
                             "width": out_img.shape[2],
                             "transform": out_transform,
                             "crs": dst_crs,
                             "compress":"LZW"}
                           )
            print (out_meta)
            with rio.open(dst_dataset, 'w', **out_meta) as dst03:
                dst03.write(out_img)
        """
        with rio.open(src_dataset) as dst02:
            out_img, out_transform = mask(dataset=dst02, shapes=shapes, crop=True)
            out_meta = dst02.meta.copy()
            out_meta.update({"height": out_img.shape[1],
                             "width": out_img.shape[2],
                             "transform": out_transform,
                             "crs": dst_crs,
                             "compress":"LZW"}
                           )
            print (out_meta)
            with rio.open(dst_dataset, 'w', **out_meta) as dst03:
                dst03.write(out_img)
        with rio.open(dst_dataset, 'w+') as dst03:
            geo = geo.to_crs(crs=dst03.crs.data)
            coords = getFeatures(geo)
            
            out_img, out_transform = mask(dataset=dst03, shapes=coords, crop=True)
            out_meta = dst03.meta.copy()
            out_meta.update({"height": out_img.shape[1],
                             "width": out_img.shape[2],
                             "transform": out_transform,
                             "crs": dst_crs,
                             "compress":"LZW"}
                           )
            print (out_meta)
            dst03.write(out_img)
        """
        print (os.path.basename(dst_dataset))
