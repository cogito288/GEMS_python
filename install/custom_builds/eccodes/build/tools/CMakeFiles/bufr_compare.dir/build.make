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
CMAKE_SOURCE_DIR = /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/sehyun/GEMS_python/install/custom_builds/eccodes/build

# Include any dependencies generated for this target.
include tools/CMakeFiles/bufr_compare.dir/depend.make

# Include the progress variables for this target.
include tools/CMakeFiles/bufr_compare.dir/progress.make

# Include the compile flags for this target's objects.
include tools/CMakeFiles/bufr_compare.dir/flags.make

tools/CMakeFiles/bufr_compare.dir/bufr_compare.c.o: tools/CMakeFiles/bufr_compare.dir/flags.make
tools/CMakeFiles/bufr_compare.dir/bufr_compare.c.o: /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tools/bufr_compare.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object tools/CMakeFiles/bufr_compare.dir/bufr_compare.c.o"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tools && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/bufr_compare.dir/bufr_compare.c.o   -c /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tools/bufr_compare.c

tools/CMakeFiles/bufr_compare.dir/bufr_compare.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/bufr_compare.dir/bufr_compare.c.i"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tools && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tools/bufr_compare.c > CMakeFiles/bufr_compare.dir/bufr_compare.c.i

tools/CMakeFiles/bufr_compare.dir/bufr_compare.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/bufr_compare.dir/bufr_compare.c.s"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tools && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tools/bufr_compare.c -o CMakeFiles/bufr_compare.dir/bufr_compare.c.s

tools/CMakeFiles/bufr_compare.dir/bufr_compare.c.o.requires:

.PHONY : tools/CMakeFiles/bufr_compare.dir/bufr_compare.c.o.requires

tools/CMakeFiles/bufr_compare.dir/bufr_compare.c.o.provides: tools/CMakeFiles/bufr_compare.dir/bufr_compare.c.o.requires
	$(MAKE) -f tools/CMakeFiles/bufr_compare.dir/build.make tools/CMakeFiles/bufr_compare.dir/bufr_compare.c.o.provides.build
.PHONY : tools/CMakeFiles/bufr_compare.dir/bufr_compare.c.o.provides

tools/CMakeFiles/bufr_compare.dir/bufr_compare.c.o.provides.build: tools/CMakeFiles/bufr_compare.dir/bufr_compare.c.o


# Object files for target bufr_compare
bufr_compare_OBJECTS = \
"CMakeFiles/bufr_compare.dir/bufr_compare.c.o"

# External object files for target bufr_compare
bufr_compare_EXTERNAL_OBJECTS =

bin/bufr_compare: tools/CMakeFiles/bufr_compare.dir/bufr_compare.c.o
bin/bufr_compare: tools/CMakeFiles/bufr_compare.dir/build.make
bin/bufr_compare: tools/libgrib_tools.a
bin/bufr_compare: lib/libeccodes.so
bin/bufr_compare: /usr/lib/x86_64-linux-gnu/libm.so
bin/bufr_compare: tools/CMakeFiles/bufr_compare.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable ../bin/bufr_compare"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tools && /usr/bin/cmake -E remove /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/bin/bufr_compare
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tools && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/bufr_compare.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
tools/CMakeFiles/bufr_compare.dir/build: bin/bufr_compare

.PHONY : tools/CMakeFiles/bufr_compare.dir/build

tools/CMakeFiles/bufr_compare.dir/requires: tools/CMakeFiles/bufr_compare.dir/bufr_compare.c.o.requires

.PHONY : tools/CMakeFiles/bufr_compare.dir/requires

tools/CMakeFiles/bufr_compare.dir/clean:
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tools && $(CMAKE_COMMAND) -P CMakeFiles/bufr_compare.dir/cmake_clean.cmake
.PHONY : tools/CMakeFiles/bufr_compare.dir/clean

tools/CMakeFiles/bufr_compare.dir/depend:
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tools /home/sehyun/GEMS_python/install/custom_builds/eccodes/build /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tools /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tools/CMakeFiles/bufr_compare.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tools/CMakeFiles/bufr_compare.dir/depend

