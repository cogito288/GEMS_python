# Install script for directory: /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/ifs_samples/grib1_mlgrib2

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/sehyun/GEMS_python/install/source/eccodes")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "RelWithDebInfo")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/eccodes/ifs_samples/grib1_mlgrib2" TYPE FILE PERMISSIONS OWNER_WRITE OWNER_READ GROUP_READ WORLD_READ FILES
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/ifs_samples/grib1_mlgrib2/gg_ml.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/ifs_samples/grib1_mlgrib2/gg_sfc.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/ifs_samples/grib1_mlgrib2/sh_ml.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/ifs_samples/grib1_mlgrib2/sh_sfc.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/BUFR3.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/BUFR3_local.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/BUFR3_local_satellite.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/BUFR4.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/BUFR4_local.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/BUFR4_local_satellite.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/GRIB1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/GRIB2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/budg.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/clusters_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/gg_sfc_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/gg_sfc_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/lambert_bf_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/polar_stereographic_pl_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/polar_stereographic_pl_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/polar_stereographic_sfc_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/polar_stereographic_sfc_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_ml_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_ml_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_1024_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_1024_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_1280_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_1280_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_128_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_128_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_160_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_160_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_2000_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_2000_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_200_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_200_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_256_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_256_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_320_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_320_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_32_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_32_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_400_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_400_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_48_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_48_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_512_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_512_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_640_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_640_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_64_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_64_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_80_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_80_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_96_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_96_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_pl_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_sfc_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_sfc_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_gg_sfc_jpeg_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_ll_sfc_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_ll_sfc_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_ml_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_ml_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_1024_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_1024_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_1280_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_1280_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_128_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_128_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_160_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_160_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_2000_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_2000_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_200_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_200_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_256_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_256_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_320_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_320_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_32_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_32_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_400_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_400_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_48_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_48_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_512_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_512_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_640_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_640_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_80_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_80_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_96_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_96_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_pl_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_sfc_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_sfc_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/reduced_rotated_gg_sfc_jpeg_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/regular_gg_ml_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/regular_gg_ml_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/regular_gg_pl_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/regular_gg_pl_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/regular_gg_sfc_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/regular_gg_sfc_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/regular_ll_pl_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/regular_ll_pl_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/regular_ll_sfc_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/regular_ll_sfc_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/rotated_gg_ml_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/rotated_gg_ml_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/rotated_gg_pl_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/rotated_gg_pl_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/rotated_gg_sfc_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/rotated_gg_sfc_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/rotated_ll_pl_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/rotated_ll_pl_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/rotated_ll_sfc_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/rotated_ll_sfc_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/sh_ml_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/sh_ml_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/sh_pl_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/sh_pl_grib2.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/sh_sfc_grib1.tmpl"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/samples/sh_sfc_grib2.tmpl"
    )
endif()

