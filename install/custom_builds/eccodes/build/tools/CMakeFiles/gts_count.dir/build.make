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
include tools/CMakeFiles/gts_count.dir/depend.make

# Include the progress variables for this target.
include tools/CMakeFiles/gts_count.dir/progress.make

# Include the compile flags for this target's objects.
include tools/CMakeFiles/gts_count.dir/flags.make

tools/CMakeFiles/gts_count.dir/codes_count.c.o: tools/CMakeFiles/gts_count.dir/flags.make
tools/CMakeFiles/gts_count.dir/codes_count.c.o: /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tools/codes_count.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object tools/CMakeFiles/gts_count.dir/codes_count.c.o"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tools && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/gts_count.dir/codes_count.c.o   -c /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tools/codes_count.c

tools/CMakeFiles/gts_count.dir/codes_count.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/gts_count.dir/codes_count.c.i"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tools && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tools/codes_count.c > CMakeFiles/gts_count.dir/codes_count.c.i

tools/CMakeFiles/gts_count.dir/codes_count.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/gts_count.dir/codes_count.c.s"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tools && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tools/codes_count.c -o CMakeFiles/gts_count.dir/codes_count.c.s

tools/CMakeFiles/gts_count.dir/codes_count.c.o.requires:

.PHONY : tools/CMakeFiles/gts_count.dir/codes_count.c.o.requires

tools/CMakeFiles/gts_count.dir/codes_count.c.o.provides: tools/CMakeFiles/gts_count.dir/codes_count.c.o.requires
	$(MAKE) -f tools/CMakeFiles/gts_count.dir/build.make tools/CMakeFiles/gts_count.dir/codes_count.c.o.provides.build
.PHONY : tools/CMakeFiles/gts_count.dir/codes_count.c.o.provides

tools/CMakeFiles/gts_count.dir/codes_count.c.o.provides.build: tools/CMakeFiles/gts_count.dir/codes_count.c.o


# Object files for target gts_count
gts_count_OBJECTS = \
"CMakeFiles/gts_count.dir/codes_count.c.o"

# External object files for target gts_count
gts_count_EXTERNAL_OBJECTS =

bin/gts_count: tools/CMakeFiles/gts_count.dir/codes_count.c.o
bin/gts_count: tools/CMakeFiles/gts_count.dir/build.make
bin/gts_count: tools/libgrib_tools.a
bin/gts_count: lib/libeccodes.so
bin/gts_count: /usr/lib/x86_64-linux-gnu/libm.so
bin/gts_count: tools/CMakeFiles/gts_count.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable ../bin/gts_count"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tools && /usr/bin/cmake -E remove /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/bin/gts_count
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tools && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/gts_count.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
tools/CMakeFiles/gts_count.dir/build: bin/gts_count

.PHONY : tools/CMakeFiles/gts_count.dir/build

tools/CMakeFiles/gts_count.dir/requires: tools/CMakeFiles/gts_count.dir/codes_count.c.o.requires

.PHONY : tools/CMakeFiles/gts_count.dir/requires

tools/CMakeFiles/gts_count.dir/clean:
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tools && $(CMAKE_COMMAND) -P CMakeFiles/gts_count.dir/cmake_clean.cmake
.PHONY : tools/CMakeFiles/gts_count.dir/clean

tools/CMakeFiles/gts_count.dir/depend:
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tools /home/sehyun/GEMS_python/install/custom_builds/eccodes/build /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tools /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tools/CMakeFiles/gts_count.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tools/CMakeFiles/gts_count.dir/depend
