if( ECCODES_IS_BUILD_DIR_EXPORT )
  set( ECCODES_DEFINITION_PATH  /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/share/eccodes/definitions )
  set( ECCODES_SAMPLES_PATH     /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/share/eccodes/samples )
  set( ECCODES_IFS_SAMPLES_PATH /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/share/eccodes/ifs_samples )
else()
  if( NOT DEFINED eccodes_BASE_DIR ) # ecbuild 2.x
    get_filename_component( eccodes_BASE_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE )
  endif()
  set( ECCODES_DEFINITION_PATH  ${eccodes_BASE_DIR}/share/eccodes/definitions )
  set( ECCODES_SAMPLES_PATH     ${eccodes_BASE_DIR}/share/eccodes/samples )
  set( ECCODES_IFS_SAMPLES_PATH ${eccodes_BASE_DIR}/share/eccodes/ifs_samples )
endif()
