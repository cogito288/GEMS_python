# examples/python include file for CMake

set -eax

data_dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/data

# use definitions from binary dir to test if installation will be correct
def_dir="/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/share/eccodes/definitions"
ECCODES_DEFINITION_PATH="${def_dir}"
export ECCODES_DEFINITION_PATH

tools_dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/bin
examples_dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/examples/python
examples_src=/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/examples/python

# use samples from binary dir to test if installation will be correct
samp_dir="/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/share/eccodes/samples"
ECCODES_SAMPLES_PATH=${samp_dir}
export ECCODES_SAMPLES_PATH

PYTHONPATH=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/python3:$PYTHONPATH
export PYTHONPATH

echo "Current directory: `pwd`"
