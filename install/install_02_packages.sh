#! /bin/bash

INSTALL_DIR=$GEMS_HOME/install

# Install eccodes
# eccodes need fortran
sudo apt install gfortran -y
sudo apt-get install libgeos-3.6.2 libgeos-dev -y

# Install eccodes
cd $INSTALL_DIR
mkdir -p custom_builds/eccodes; cd custom_builds/eccodes
wget https://confluence.ecmwf.int/download/attachments/45757960/eccodes-2.14.1-Source.tar.gz?api=v2
tar -xzf eccodes-2.14.1-Source.tar.gz?api=v2
mkdir build ; cd build
mkdir -p $INSTALL_DIR/source/eccodes
cmake -DCMAKE_INSTALL_PREFIX=$INSTALL_DIR/source/eccodes $INSTALL_DIR/custom_builds/eccodes/eccodes-2.14.1-Source/
# NetCDF is not installed
# ????? Binary file is writtend into -- Build files have been written to: /home/sehyun/custom_builds/eccodes/build
# nano ~/.bashrc
# export ECCODES_DEFINITION_PATH=/home/sehyun/custom_builds/eccodes/build/share/eccodes/definitions

echo "Creating virtualenv"
cd $GEMS_HOME
#/usr/bin/python3 -m virtualenv venv
source venv/bin/activate

#deactivate

echo "Installing pip eccodes-python"
pip install eccodes-python
