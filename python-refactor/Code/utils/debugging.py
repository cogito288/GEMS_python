import os
import glob

def check_make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)