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
include tests/CMakeFiles/gauss_sub.dir/depend.make

# Include the progress variables for this target.
include tests/CMakeFiles/gauss_sub.dir/progress.make

# Include the compile flags for this target's objects.
include tests/CMakeFiles/gauss_sub.dir/flags.make

tests/CMakeFiles/gauss_sub.dir/gauss_sub.c.o: tests/CMakeFiles/gauss_sub.dir/flags.make
tests/CMakeFiles/gauss_sub.dir/gauss_sub.c.o: /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tests/gauss_sub.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object tests/CMakeFiles/gauss_sub.dir/gauss_sub.c.o"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/gauss_sub.dir/gauss_sub.c.o   -c /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tests/gauss_sub.c

tests/CMakeFiles/gauss_sub.dir/gauss_sub.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/gauss_sub.dir/gauss_sub.c.i"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tests/gauss_sub.c > CMakeFiles/gauss_sub.dir/gauss_sub.c.i

tests/CMakeFiles/gauss_sub.dir/gauss_sub.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/gauss_sub.dir/gauss_sub.c.s"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tests/gauss_sub.c -o CMakeFiles/gauss_sub.dir/gauss_sub.c.s

tests/CMakeFiles/gauss_sub.dir/gauss_sub.c.o.requires:

.PHONY : tests/CMakeFiles/gauss_sub.dir/gauss_sub.c.o.requires

tests/CMakeFiles/gauss_sub.dir/gauss_sub.c.o.provides: tests/CMakeFiles/gauss_sub.dir/gauss_sub.c.o.requires
	$(MAKE) -f tests/CMakeFiles/gauss_sub.dir/build.make tests/CMakeFiles/gauss_sub.dir/gauss_sub.c.o.provides.build
.PHONY : tests/CMakeFiles/gauss_sub.dir/gauss_sub.c.o.provides

tests/CMakeFiles/gauss_sub.dir/gauss_sub.c.o.provides.build: tests/CMakeFiles/gauss_sub.dir/gauss_sub.c.o


# Object files for target gauss_sub
gauss_sub_OBJECTS = \
"CMakeFiles/gauss_sub.dir/gauss_sub.c.o"

# External object files for target gauss_sub
gauss_sub_EXTERNAL_OBJECTS =

tests/gauss_sub: tests/CMakeFiles/gauss_sub.dir/gauss_sub.c.o
tests/gauss_sub: tests/CMakeFiles/gauss_sub.dir/build.make
tests/gauss_sub: lib/libeccodes.so
tests/gauss_sub: /usr/lib/x86_64-linux-gnu/libm.so
tests/gauss_sub: /usr/lib/x86_64-linux-gnu/libopenjp2.so
tests/gauss_sub: tests/CMakeFiles/gauss_sub.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable gauss_sub"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && /usr/bin/cmake -E remove /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests/gauss_sub
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/gauss_sub.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
tests/CMakeFiles/gauss_sub.dir/build: tests/gauss_sub

.PHONY : tests/CMakeFiles/gauss_sub.dir/build

tests/CMakeFiles/gauss_sub.dir/requires: tests/CMakeFiles/gauss_sub.dir/gauss_sub.c.o.requires

.PHONY : tests/CMakeFiles/gauss_sub.dir/requires

tests/CMakeFiles/gauss_sub.dir/clean:
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && $(CMAKE_COMMAND) -P CMakeFiles/gauss_sub.dir/cmake_clean.cmake
.PHONY : tests/CMakeFiles/gauss_sub.dir/clean

tests/CMakeFiles/gauss_sub.dir/depend:
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tests /home/sehyun/GEMS_python/install/custom_builds/eccodes/build /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests/CMakeFiles/gauss_sub.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tests/CMakeFiles/gauss_sub.dir/depend
