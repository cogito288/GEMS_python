#! /bin/bash

# https://gist.github.com/emmanuelnk/406eee50c388f4f73dcdff521f2aa7b2
sudo apt-get update
sudo apt-get -y upgrade

python3 -V
# Should be higher than or equal to 3.6.5
sudo apt-get install -y python3-pip
sudo apt-get install python3-dev
sudo pip3 install virtualenv 
#source matlab2python/venv/bin/activate

# see plot in terminal 
sudo apt-get install python3-tk -y


# Cmake
sudo apt-get install build-essential
sudo apt-get install cmake

GEMS_HOME="/home/sehyun/GEMS_python"
# bash_profile에 PATH를 추가해줍니다.
echo "export GEMS_HOME=$GEMS_HOME" >> ~/.bashrc
echo "export PATH=$PATH:$GEMS_HOME" >> ~/.bashrc

echo "Root directory is $GEMS_HOME"
source ~/.bashrc
# 끝!
echo "Done!"
