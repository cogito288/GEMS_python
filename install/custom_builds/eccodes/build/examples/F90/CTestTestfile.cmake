# CMake generated Testfile for 
# Source directory: /home/sehyun/Downloads/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/examples/F90
# Build directory: /home/sehyun/Downloads/GEMS_python/install/custom_builds/eccodes/build/examples/F90
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(eccodes_f_grib_set_pv "/home/sehyun/Downloads/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/examples/F90/grib_set_pv.sh")
set_tests_properties(eccodes_f_grib_set_pv PROPERTIES  ENVIRONMENT "OMP_NUM_THREADS=1" LABELS "eccodes;script")
add_test(eccodes_f_grib_set_data "/home/sehyun/Downloads/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/examples/F90/grib_set_data.sh")
set_tests_properties(eccodes_f_grib_set_data PROPERTIES  ENVIRONMENT "OMP_NUM_THREADS=1" LABELS "eccodes;script")
add_test(eccodes_f_grib_ecc-671 "/home/sehyun/Downloads/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/examples/F90/grib_ecc-671.sh")
set_tests_properties(eccodes_f_grib_ecc-671 PROPERTIES  ENVIRONMENT "OMP_NUM_THREADS=1" LABELS "eccodes;script")
