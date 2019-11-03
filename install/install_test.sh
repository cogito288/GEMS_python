#!/bin/bash

#echo "Creating virtualenv"
cd $GEMS_HOME
#/usr/bin/python3 -m virtualenv venv
source venv/bin/activate

INSTALL_DIR=$GEMS_HOME/install
cd $INSTALL_DIR

#ECCODES_DEFINITION_PATH=$INSTALL_DIR/custom_builds/eccodes/build/share/eccodes/definitions
#echo "export ECCODES_DEFINITION_PATH=$ECCODES_DEFINITION_PATH" >> ~/.bashrc
#source ~/.bashrc


########################## Install pygrib
# https://gist.github.com/emmanuelnk/406eee50c388f4f73dcdff521f2aa7b2
#sudo apt-get install libgeos-3.6.2 libgeos-dev

source $GEMS_HOME/venv/bin/activate
#pip3 install numpy matplotlib tokenizer
#pip3 install https://github.com/matplotlib/basemap/archive/master.zip


cd $INSTALL_DIR/custom_builds
git clone https://github.com/jswhit/pygrib
cd pygrib
cp $INSTALL_DIR/pygrib_setup.cfg.template setup.cfg
sudo rm -rf .git
zip -r ../pygrib.zip *
cd ..
pip3 install pygrib.zip

cd $INSTALL_DIR
