# Install script for directory: /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/eccodes/definitions" TYPE FILE PERMISSIONS OWNER_WRITE OWNER_READ GROUP_READ WORLD_READ FILES
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/boot.def"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/empty_template.def"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/parameters_version.def"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/mars_param.table"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/param_id.table"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/stepUnits.table"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/CMakeLists.txt"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/eccodes/definitions" TYPE FILE FILES "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/installDefinitions.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/eccodes/definitions" TYPE DIRECTORY FILES
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/budg"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/bufr"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/cdf"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/common"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/grib1"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/grib2"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/grib3"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/gts"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/mars"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/metar"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/tide"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/hdf5"
    "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/definitions/wrap"
    FILES_MATCHING REGEX "/[^/]*\\.def$" REGEX "/[^/]*\\.txt$" REGEX "/[^/]*\\.list$" REGEX "/[^/]*\\.table$" REGEX "/4\\.2\\.192\\.[^/]*\\.table$" EXCLUDE PERMISSIONS OWNER_WRITE OWNER_READ GROUP_READ WORLD_READ)
endif()

