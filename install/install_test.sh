#!/bin/bash

#echo "Creating virtualenv"
cd $GEMS_HOME
#/usr/bin/python3 -m virtualenv venv
source venv/bin/activate

INSTALL_DIR=$GEMS_HOME/install
cd $INSTALL_DIR

cd $GEMS_HOME/install
deactivate
#echo "Installing pip eccodes-python"
#pip install eccodes-python

