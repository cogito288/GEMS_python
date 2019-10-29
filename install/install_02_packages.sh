#! /bin/bash

source ~/.bashrc
INSTALL_DIR=$GEMS_HOME/install

################################# Install eccodes
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
pip3 install eccodes-python


################################ # pyhdf for HDF4     
# https://github.com/fhs/pyhdf/blob/master/doc/install.rst
#echo "Installing pyhdf"
#sudo apt-get install build-essential python3-dev python3-numpy libhdf4-dev -y 
#cd $INSTALL_DIR
#git clone https://github.com/fhs/pyhdf.git

############################### Install gdal
# https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html
sudo apt-get install python3.6-dev -y
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update 
sudo apt-get update 
sudo apt-get install gdal-bin -y
# To verify the installation, you can run 
ogrinfo --version

sudo apt-get install libgdal-dev -y
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
pip3 install --global-option=build_ext --global-option="-I/usr/include/gdal/" GDAL==2.0.1

############################### Install pyhdf
pip3 install pyhdf




