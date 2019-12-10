#!/bin/bash

#echo "Creating virtualenv"
cd $GEMS_HOME
#/usr/bin/python3 -m virtualenv venv
source venv/bin/activate

INSTALL_DIR=$GEMS_HOME/install
cd $INSTALL_DIR

source $GEMS_HOME/venv/bin/activate
cd $INSTALL_DIR/custom_builds
pip install cython
git clone git clone https://github.com/Unidata/netcdf4-python.git
# check HDF5 and netcdf-4 are installed by 'nc-config --version'. If not installed, you should manually installed.
cd netcdf4-python
python setup.py build
python setup.py install
cd test && python run_all.py
