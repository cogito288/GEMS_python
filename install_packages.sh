#! /bin/bash

# https://gist.github.com/emmanuelnk/406eee50c388f4f73dcdff521f2aa7b2
sudo apt-get update
sudo apt-get -y upgrade

python3 -V
# Should be higher than or equal to 3.6.5
sudo apt-get install -y python3-pip
sudo apt-get install python3-dev
sudo pip3 install virtualenv 
#virtualenv venv 
source matlab2python/venv/bin/activate

# Cmake
sudo apt-get install build-essential
sudo apt-get install cmake

# Eccodes
mkdir custom_builds/eccodes
cd custom_builds/ecodes
wget https://confluence.ecmwf.int/download/attachments/45757960/eccodes-2.14.1-Source.tar.gz?api=v2
tar -xzf eccodes-2.14.1-Source.tar.gz?aip=v2
mkdir build ; cd build




# Install pygrib
sudo apt-get install libgeos-3.6.2 libgeos-dev
pip install numpy matplotlib 
pip install https://github.com/matplotlib/basemap/archive/master.zip

git clone https://github.com/jswhit/pygrib.git
cd pygrib
cp setup.cfg.template setup.cfg
# nano setup.cfg
# 
