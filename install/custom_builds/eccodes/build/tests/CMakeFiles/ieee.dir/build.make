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
include tests/CMakeFiles/ieee.dir/depend.make

# Include the progress variables for this target.
include tests/CMakeFiles/ieee.dir/progress.make

# Include the compile flags for this target's objects.
include tests/CMakeFiles/ieee.dir/flags.make

tests/CMakeFiles/ieee.dir/ieee.c.o: tests/CMakeFiles/ieee.dir/flags.make
tests/CMakeFiles/ieee.dir/ieee.c.o: /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tests/ieee.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object tests/CMakeFiles/ieee.dir/ieee.c.o"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/ieee.dir/ieee.c.o   -c /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tests/ieee.c

tests/CMakeFiles/ieee.dir/ieee.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/ieee.dir/ieee.c.i"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tests/ieee.c > CMakeFiles/ieee.dir/ieee.c.i

tests/CMakeFiles/ieee.dir/ieee.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/ieee.dir/ieee.c.s"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tests/ieee.c -o CMakeFiles/ieee.dir/ieee.c.s

tests/CMakeFiles/ieee.dir/ieee.c.o.requires:

.PHONY : tests/CMakeFiles/ieee.dir/ieee.c.o.requires

tests/CMakeFiles/ieee.dir/ieee.c.o.provides: tests/CMakeFiles/ieee.dir/ieee.c.o.requires
	$(MAKE) -f tests/CMakeFiles/ieee.dir/build.make tests/CMakeFiles/ieee.dir/ieee.c.o.provides.build
.PHONY : tests/CMakeFiles/ieee.dir/ieee.c.o.provides

tests/CMakeFiles/ieee.dir/ieee.c.o.provides.build: tests/CMakeFiles/ieee.dir/ieee.c.o


# Object files for target ieee
ieee_OBJECTS = \
"CMakeFiles/ieee.dir/ieee.c.o"

# External object files for target ieee
ieee_EXTERNAL_OBJECTS =

tests/ieee: tests/CMakeFiles/ieee.dir/ieee.c.o
tests/ieee: tests/CMakeFiles/ieee.dir/build.make
tests/ieee: lib/libeccodes.so
tests/ieee: /usr/lib/x86_64-linux-gnu/libm.so
tests/ieee: /usr/lib/x86_64-linux-gnu/libopenjp2.so
tests/ieee: tests/CMakeFiles/ieee.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable ieee"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && /usr/bin/cmake -E remove /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests/ieee
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/ieee.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
tests/CMakeFiles/ieee.dir/build: tests/ieee

.PHONY : tests/CMakeFiles/ieee.dir/build

tests/CMakeFiles/ieee.dir/requires: tests/CMakeFiles/ieee.dir/ieee.c.o.requires

.PHONY : tests/CMakeFiles/ieee.dir/requires

tests/CMakeFiles/ieee.dir/clean:
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && $(CMAKE_COMMAND) -P CMakeFiles/ieee.dir/cmake_clean.cmake
.PHONY : tests/CMakeFiles/ieee.dir/clean

tests/CMakeFiles/ieee.dir/depend:
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tests /home/sehyun/GEMS_python/install/custom_builds/eccodes/build /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests/CMakeFiles/ieee.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tests/CMakeFiles/ieee.dir/depend
