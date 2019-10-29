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
include examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/depend.make

# Include the progress variables for this target.
include examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/progress.make

# Include the compile flags for this target's objects.
include examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/flags.make

examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.o: examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/flags.make
examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.o: /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/examples/C/bufr_read_scatterometer.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.o"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/examples/C && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.o   -c /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/examples/C/bufr_read_scatterometer.c

examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.i"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/examples/C && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/examples/C/bufr_read_scatterometer.c > CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.i

examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.s"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/examples/C && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/examples/C/bufr_read_scatterometer.c -o CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.s

examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.o.requires:

.PHONY : examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.o.requires

examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.o.provides: examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.o.requires
	$(MAKE) -f examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/build.make examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.o.provides.build
.PHONY : examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.o.provides

examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.o.provides.build: examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.o


# Object files for target c_bufr_read_scatterometer
c_bufr_read_scatterometer_OBJECTS = \
"CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.o"

# External object files for target c_bufr_read_scatterometer
c_bufr_read_scatterometer_EXTERNAL_OBJECTS =

examples/C/c_bufr_read_scatterometer: examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.o
examples/C/c_bufr_read_scatterometer: examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/build.make
examples/C/c_bufr_read_scatterometer: lib/libeccodes.so
examples/C/c_bufr_read_scatterometer: /usr/lib/x86_64-linux-gnu/libm.so
examples/C/c_bufr_read_scatterometer: examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable c_bufr_read_scatterometer"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/examples/C && /usr/bin/cmake -E remove /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/examples/C/c_bufr_read_scatterometer
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/examples/C && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/c_bufr_read_scatterometer.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/build: examples/C/c_bufr_read_scatterometer

.PHONY : examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/build

examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/requires: examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/bufr_read_scatterometer.c.o.requires

.PHONY : examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/requires

examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/clean:
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/examples/C && $(CMAKE_COMMAND) -P CMakeFiles/c_bufr_read_scatterometer.dir/cmake_clean.cmake
.PHONY : examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/clean

examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/depend:
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/examples/C /home/sehyun/GEMS_python/install/custom_builds/eccodes/build /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/examples/C /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/C/CMakeFiles/c_bufr_read_scatterometer.dir/depend

