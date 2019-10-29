/*
 * (C) Copyright 2011- ECMWF.
 *
 * This software is licensed under the terms of the Apache Licence Version 2.0
 * which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
 * In applying this licence, ECMWF does not waive the privileges and immunities
 * granted to it by virtue of its status as an intergovernmental organisation nor
 * does it submit to any jurisdiction.
 */

#ifndef eccodes_ecbuild_config_h
#define eccodes_ecbuild_config_h

/* ecbuild info */

#ifndef ECBUILD_VERSION_STR
#define ECBUILD_VERSION_STR "3.1.0"
#endif
#ifndef ECBUILD_VERSION
#define ECBUILD_VERSION "3.1.0"
#endif
#ifndef ECBUILD_MACROS_DIR
#define ECBUILD_MACROS_DIR  "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/cmake"
#endif

/* config info */

#define ECCODES_OS_NAME          "Linux-5.0.0-23-generic"
#define ECCODES_OS_BITS          64
#define ECCODES_OS_BITS_STR      "64"
#define ECCODES_OS_STR           "linux.64"
#define ECCODES_OS_VERSION       "5.0.0-23-generic"
#define ECCODES_SYS_PROCESSOR    "x86_64"

#define ECCODES_BUILD_TIMESTAMP  "20191029190618"
#define ECCODES_BUILD_TYPE       "RelWithDebInfo"

#define ECCODES_C_COMPILER_ID      "GNU"
#define ECCODES_C_COMPILER_VERSION "7.4.0"

#define ECCODES_CXX_COMPILER_ID      ""
#define ECCODES_CXX_COMPILER_VERSION ""

#define ECCODES_C_COMPILER       "/usr/bin/cc"
#define ECCODES_C_FLAGS          " -pipe -O2 -g -DNDEBUG"

#define ECCODES_CXX_COMPILER     ""
#define ECCODES_CXX_FLAGS        ""

/* Needed for finding per package config files */

#define ECCODES_INSTALL_DIR       "/home/sehyun/GEMS_python/install/source/eccodes"
#define ECCODES_INSTALL_BIN_DIR   "/home/sehyun/GEMS_python/install/source/eccodes/bin"
#define ECCODES_INSTALL_LIB_DIR   "/home/sehyun/GEMS_python/install/source/eccodes/lib"
#define ECCODES_INSTALL_DATA_DIR  "/home/sehyun/GEMS_python/install/source/eccodes/share/eccodes"

#define ECCODES_DEVELOPER_SRC_DIR "/home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source"
#define ECCODES_DEVELOPER_BIN_DIR "/home/sehyun/GEMS_python/install/custom_builds/eccodes/build"

#define EC_HAVE_FORTRAN

#ifdef EC_HAVE_FORTRAN

#define ECCODES_Fortran_COMPILER_ID      "GNU"
#define ECCODES_Fortran_COMPILER_VERSION "7.4.0"

#define ECCODES_Fortran_COMPILER "/usr/bin/gfortran"
#define ECCODES_Fortran_FLAGS    " -O2 -g -DNDEBUG"

#endif

#endif /* eccodes_ecbuild_config_h */
