import sys
import os
base_dir = os.environ['GEMS_HOME']
project_path = os.path.join(base_dir, 'python-refactor')
sys.path.insert(0, project_path)
from Code.utils import matlab

import json
import glob
from rasterio import features
from rasterio.mask import mask
from rasterio.warp import reproject
import rasterio as rio
import time

### Setting path
data_base_dir = os.path.join('/data2', 'sehyun', 'Data')
path_myd_processed = os.path.join(data_base_dir, 'Preprocessed_raw', 'MODIS', 'MYD13A2')
maskfile = os.path.join(data_base_dir, 'Raw', 'mask', 'r_mask_korea.tif')
with rio.open(maskfile) as masksrc:
    band = masksrc.read(1)
    maskarr = (band!=255)
    shapes = []
    for geometry, raster_value in features.shapes(band, mask=maskarr, transform=masksrc.transform):
        shapes.append(json.loads(json.dumps(geometry)))

YEARS = [2016]
for yr in YEARS:
    print(yr)
    flist = glob.glob(os.path.join(path_myd_processed, '02prj_GCS_WGS84', str(yr), "*.tif"))
    flist.sort()
    for src_dataset in flist:
        tStart = time.time()
        dst_dataset = os.path.join(path_myd_processed, '03mask_SouthKorea_MYD13A2', str(yr), f'm_{os.path.basename(src_dataset)[2:]}')
        matlab.check_make_dir(os.path.dirname(dst_dataset))
        with rio.open(src_dataset) as src:
            kwargs = src.meta.copy()
            kwargs['transform'] = masksrc.transform

            temp_dataset = os.path.join(os.path.dirname(dst_dataset), 'temp.tif')
            resolution = 1.02308446206551E-02
            dst_crs = masksrc.crs
            with rio.open(temp_dataset, 'w+', **kwargs) as temp_dst:
                for i in range(1, src.count+1):
                    reproject(
                        source=rio.band(src, i),
                        destination=rio.band(temp_dst, i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        src_nodata=-9999,
                        dst_transform=masksrc.transform,
                        dst_crs=dst_crs,
                        dst_nodata=-9999,
                        dst_resolution=resolution,
                    )
                out_img, out_transform = mask(dataset=temp_dst, shapes=shapes, crop=True)
                with rio.open(temp_dataset) as temp_dst:
                    out_meta = temp_dst.meta.copy()
                    out_meta.update({"height": out_img.shape[1],
                                     "width": out_img.shape[2],
                                     "transform": out_transform,
                                     "crs": dst_crs,
                                     "compress":"LZW"}
                                   )
                    with rio.open(dst_dataset, 'w', **out_meta) as dst:
                        dst.write(out_img)
            os.remove(temp_dataset)
        tElapsed = time.time() - tStart
        print (f'time taken : {tElapsed}')
        print (os.path.basename(dst_dataset))
