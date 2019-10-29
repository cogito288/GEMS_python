#!/bin/bash

#echo "Creating virtualenv"
cd $GEMS_HOME
#/usr/bin/python3 -m virtualenv venv
source venv/bin/activate

#INSTALL_DIR=$GEMS_HOME/install
#cd $INSTALL_DIR

#cd $GEMS_HOME/install
#deactivate
#echo "Installing pip eccodes-python"
#pip install eccodes-python

# pyhdf for HDF4
#sudo apt-get install build-essential python3-dev python3-numpy libhdf4-dev -y
#cd $INSTALL_DIR/custom_builds
#git clone https://github.com/fhs/pyhdf.git

sudo apt-get install python3.6-dev
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
sudo apt-get update
sudo apt-get install gdal-bin
# To verify the installation, you can run
ogrinfo --version

sudo apt-get install libgdal-dev
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
pip3 install GDAL

