set -ea
# For CMake

set -x

proj_dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source
build_dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build
data_dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/data

# use definitions from binary dir to test if installation will be correct
def_dir="/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/share/eccodes/definitions"
ECCODES_DEFINITION_PATH="${def_dir}"
export ECCODES_DEFINITION_PATH

# binaries are in the TOP CMAKE_BINARY_DIR
tools_dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/bin
tigge_dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/bin

# If this environment variable is set, then run the
# executables with valgrind. See ECC-746
EXEC=""
if test "x$ECCODES_TEST_WITH_VALGRIND" != "x"; then
   tools_dir="valgrind --error-exitcode=1 -q /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/bin"
   EXEC="valgrind --error-exitcode=1 -q "
fi

# ecCodes tests are in the PROJECT_BINARY_DIR
test_dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests

# use samples from binary dir to test if installation will be correct
samp_dir="/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/share/eccodes/samples"
ECCODES_SAMPLES_PATH=${samp_dir}
export ECCODES_SAMPLES_PATH

# Options
HAVE_JPEG=1
HAVE_LIBJASPER=0
HAVE_LIBOPENJPEG=1
HAVE_PNG=0
HAVE_AEC=0
HAVE_EXTRA_TESTS=0
HAVE_MEMFS=0

echo "Current directory: `pwd`"
