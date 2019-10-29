# CMake generated Testfile for 
# Source directory: /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/examples/C
# Build directory: /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/examples/C
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(eccodes_c_grib_multi "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/examples/C/grib_multi.sh")
set_tests_properties(eccodes_c_grib_multi PROPERTIES  ENVIRONMENT "OMP_NUM_THREADS=1" LABELS "eccodes;script")
add_test(eccodes_c_grib_set_data "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/examples/C/grib_set_data.sh")
set_tests_properties(eccodes_c_grib_set_data PROPERTIES  ENVIRONMENT "OMP_NUM_THREADS=1" LABELS "eccodes;script")
add_test(eccodes_c_large_grib1 "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/examples/C/large_grib1.sh")
set_tests_properties(eccodes_c_large_grib1 PROPERTIES  ENVIRONMENT "OMP_NUM_THREADS=1" LABELS "eccodes;script")
add_test(eccodes_c_grib_sections_copy "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/examples/C/grib_sections_copy.sh")
set_tests_properties(eccodes_c_grib_sections_copy PROPERTIES  ENVIRONMENT "OMP_NUM_THREADS=1" LABELS "eccodes;script")
add_test(eccodes_c_get_product_kind_samples "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/examples/C/get_product_kind_samples.sh")
set_tests_properties(eccodes_c_get_product_kind_samples PROPERTIES  ENVIRONMENT "OMP_NUM_THREADS=1" LABELS "eccodes;script")
add_test(eccodes_c_new_sample "/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/examples/C/eccodes_c_new_sample" "out.grib")
set_tests_properties(eccodes_c_new_sample PROPERTIES  ENVIRONMENT "ECCODES_SAMPLES_PATH=/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples;ECCODES_DEFINITION_PATH=/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions;OMP_NUM_THREADS=1" LABELS "eccodes;executable")
