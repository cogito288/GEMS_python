# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/share/ecbuild/check_linker

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/ecbuild_tmp/check_linker

# Include any dependencies generated for this target.
include CMakeFiles/dso1.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/dso1.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/dso1.dir/flags.make

CMakeFiles/dso1.dir/dso1.c.o: CMakeFiles/dso1.dir/flags.make
CMakeFiles/dso1.dir/dso1.c.o: /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/share/ecbuild/check_linker/dso1.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --progress-dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/ecbuild_tmp/check_linker/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/dso1.dir/dso1.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/dso1.dir/dso1.c.o   -c /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/share/ecbuild/check_linker/dso1.c

CMakeFiles/dso1.dir/dso1.c.i: cmake_force
	@echo "Preprocessing C source to CMakeFiles/dso1.dir/dso1.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/share/ecbuild/check_linker/dso1.c > CMakeFiles/dso1.dir/dso1.c.i

CMakeFiles/dso1.dir/dso1.c.s: cmake_force
	@echo "Compiling C source to assembly CMakeFiles/dso1.dir/dso1.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/share/ecbuild/check_linker/dso1.c -o CMakeFiles/dso1.dir/dso1.c.s

CMakeFiles/dso1.dir/dso1.c.o.requires:

.PHONY : CMakeFiles/dso1.dir/dso1.c.o.requires

CMakeFiles/dso1.dir/dso1.c.o.provides: CMakeFiles/dso1.dir/dso1.c.o.requires
	$(MAKE) -f CMakeFiles/dso1.dir/build.make CMakeFiles/dso1.dir/dso1.c.o.provides.build
.PHONY : CMakeFiles/dso1.dir/dso1.c.o.provides

CMakeFiles/dso1.dir/dso1.c.o.provides.build: CMakeFiles/dso1.dir/dso1.c.o


# Object files for target dso1
dso1_OBJECTS = \
"CMakeFiles/dso1.dir/dso1.c.o"

# External object files for target dso1
dso1_EXTERNAL_OBJECTS =

lib/libdso1.so: CMakeFiles/dso1.dir/dso1.c.o
lib/libdso1.so: CMakeFiles/dso1.dir/build.make
lib/libdso1.so: CMakeFiles/dso1.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --progress-dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/ecbuild_tmp/check_linker/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C shared library lib/libdso1.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/dso1.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/dso1.dir/build: lib/libdso1.so

.PHONY : CMakeFiles/dso1.dir/build

CMakeFiles/dso1.dir/requires: CMakeFiles/dso1.dir/dso1.c.o.requires

.PHONY : CMakeFiles/dso1.dir/requires

CMakeFiles/dso1.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/dso1.dir/cmake_clean.cmake
.PHONY : CMakeFiles/dso1.dir/clean

CMakeFiles/dso1.dir/depend:
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/ecbuild_tmp/check_linker && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/share/ecbuild/check_linker /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/share/ecbuild/check_linker /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/ecbuild_tmp/check_linker /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/ecbuild_tmp/check_linker /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/ecbuild_tmp/check_linker/CMakeFiles/dso1.dir/DependInfo.cmake
.PHONY : CMakeFiles/dso1.dir/depend
