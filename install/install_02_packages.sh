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
wget -O eccodes-2.14.1-Source.tar.gz https://confluence.ecmwf.int/download/attachments/45757960/eccodes-2.14.1-Source.tar.gz?api=v2
tar -xzf eccodes-2.14.1-Source.tar.gz
mkdir build ; cd build
cmake \
-DCMAKE_INSTALL_PREFIX=~/source/eccodes \
-ENABLE_NETCDF=ON \
-ENABLE_JPG=OFF \
-ENABLE_PNG=OFF \
-ENABLE_PYTHON=ON \
-ENABLE_FORTRAN=OFF \
 ../eccodes-2.14.1-Source/
make
ctest
make install

# NetCDF is not installed
# ????? Binary file is writtend into -- Build files have been written to: /home/sehyun/custom_builds/eccodes/build
# nano ~/.bashrc

ECCODES_DIR=~/source/eccodes
ECCODES_DEFINITION_PATH=~/source/eccodes/share/eccodes/definitions
echo "export ECCODES_DEFINITION_PATH=$ECCODES_DEFINITION_PATH" >> ~/.bashrc # https://gist.github.com/emmanuelnk/406eee50c388f4f73dcdff521f2aa7b2
echo "export ECCODES_DIR=$ECCODES_DIR" >> ~/.bashrc # https://confluence.ecmwf.int//display/ECC/ecCodes+installation


echo "Creating virtualenv"
cd $GEMS_HOME
/usr/bin/python3 -m virtualenv venv
echo '' > venv/.gitignore
source venv/bin/activate

#deactivate
#echo "Installing pip eccodes-python"
# https://confluence.ecmwf.int//display/ECC/ecCodes+installation
#pip3 install --install-option="--prefix=$ECCODES_DIR" eccodes-python 

############################### pygrib
source $GEMS_HOME/venv/bin/activate
sudo apt-get install libgeos-3.6.2 libgeos-dev
pip install numpy matplotlib 
pip install https://github.com/matplotlib/basemap/archive/master.zip
cd $INSTALL_DIR/custom_builds
git clone https://github.com/jswhit/pygrib
cd pygrib
cp $INSTALL_DIR/pygrib_setup.cfg.template setup.cfg
sudo rm -rf .git
zip -r ../pygrib.zip *
cd ..
pip3 install pygrib.zip


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
pip3 install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL==`gdal-config --version`


sudo apt install python-gdal -y
############################### Install pyhdf
pip3 install pyhdf
