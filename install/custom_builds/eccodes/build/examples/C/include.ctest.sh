# examples/C include file for CMake

set -eax

proj_dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source
data_dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/data

# use definitions from binary dir to test if installation will be correct
def_dir="/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/share/eccodes/definitions"
ECCODES_DEFINITION_PATH="${def_dir}"
export ECCODES_DEFINITION_PATH

tools_dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/bin
examples_dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/examples/C

# If this environment variable is set, then run the
# executables with valgrind
if test "x$ECCODES_TEST_WITH_VALGRIND" != "x"; then
   tools_dir="valgrind --error-exitcode=1 -q $tools_dir"
   examples_dir="valgrind --error-exitcode=1 -q $examples_dir"
fi

# use samples from binary dir to test if installation will be correct
samp_dir="/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/share/eccodes/samples"
ECCODES_SAMPLES_PATH=${samp_dir}
export ECCODES_SAMPLES_PATH
