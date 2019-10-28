#! /bin/bash

# Install eccodes
source matlab2python/venv/bin/activate

# eccodes need fortran
sudo apt install gfortran

sudo apt-get install libgeos-3.6.2 libgeos-dev -y

mkdir -p ~/custom_builds/eccodes
cd ~/custom_builds/eccodes
wget https://confluence.ecmwf.int/download/attachments/45757960/eccodes-2.14.1-Source.tar.gz?api=v2
tar -xzf eccodes-2.14.1-Source.tar.gz?api=v2
mkdir build ; cd build
mkdir -p ~/source/eccodes
cmake -DCMAKE_INSTALL_PREFIX=~/source/eccodes ../eccodes-2.14.1-Source/
# NetCDF is not installed
# ????? Binary file is writtend into -- Build files have been written to: /home/sehyun/custom_builds/eccodes/build
# nano ~/.bashrc
# export ECCODES_DEFINITION_PATH=/home/sehyun/custom_builds/eccodes/build/share/eccodes/definitions
pip3 install eccodes-python


