
file(READ /home/sehyun/Downloads/GEMS_python/install/custom_builds/eccodes/build/eccodes.pc.tmp _content)

string(REPLACE "/home/sehyun/Downloads/GEMS_python/install/custom_builds/eccodes/build/lib" "\${libdir}" _content "${_content}")
if(NOT "lib" STREQUAL "lib")
  string(REPLACE "/home/sehyun/Downloads/GEMS_python/install/custom_builds/eccodes/build/lib" "\${libdir}" _content "${_content}")
endif()
string(REPLACE "/home/sehyun/source/eccodes/lib" "\${libdir}" _content "${_content}")

file(WRITE /home/sehyun/Downloads/GEMS_python/install/custom_builds/eccodes/build/lib/pkgconfig/eccodes.pc "${_content}")
