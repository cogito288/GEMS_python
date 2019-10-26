import os
from pyhdf.SD import SD, SDC

def get_file_lists(path, pattern):
    flist = []
    for file in os.listdir(path):
        if file.endswith(pattern):
            flist.append(file)
    return flist

def get_dataset_from_hdf4(path, dataset):
    result = None
    hdf_file =  SD(path, SDC.READ)
    sds_obj = hdf_file.select(dataset)
    result = sds_obj.get()
    return result