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
include tests/CMakeFiles/bufr_get_element.dir/depend.make

# Include the progress variables for this target.
include tests/CMakeFiles/bufr_get_element.dir/progress.make

# Include the compile flags for this target's objects.
include tests/CMakeFiles/bufr_get_element.dir/flags.make

tests/CMakeFiles/bufr_get_element.dir/bufr_get_element.c.o: tests/CMakeFiles/bufr_get_element.dir/flags.make
tests/CMakeFiles/bufr_get_element.dir/bufr_get_element.c.o: /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tests/bufr_get_element.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object tests/CMakeFiles/bufr_get_element.dir/bufr_get_element.c.o"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/bufr_get_element.dir/bufr_get_element.c.o   -c /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tests/bufr_get_element.c

tests/CMakeFiles/bufr_get_element.dir/bufr_get_element.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/bufr_get_element.dir/bufr_get_element.c.i"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tests/bufr_get_element.c > CMakeFiles/bufr_get_element.dir/bufr_get_element.c.i

tests/CMakeFiles/bufr_get_element.dir/bufr_get_element.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/bufr_get_element.dir/bufr_get_element.c.s"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tests/bufr_get_element.c -o CMakeFiles/bufr_get_element.dir/bufr_get_element.c.s

tests/CMakeFiles/bufr_get_element.dir/bufr_get_element.c.o.requires:

.PHONY : tests/CMakeFiles/bufr_get_element.dir/bufr_get_element.c.o.requires

tests/CMakeFiles/bufr_get_element.dir/bufr_get_element.c.o.provides: tests/CMakeFiles/bufr_get_element.dir/bufr_get_element.c.o.requires
	$(MAKE) -f tests/CMakeFiles/bufr_get_element.dir/build.make tests/CMakeFiles/bufr_get_element.dir/bufr_get_element.c.o.provides.build
.PHONY : tests/CMakeFiles/bufr_get_element.dir/bufr_get_element.c.o.provides

tests/CMakeFiles/bufr_get_element.dir/bufr_get_element.c.o.provides.build: tests/CMakeFiles/bufr_get_element.dir/bufr_get_element.c.o


# Object files for target bufr_get_element
bufr_get_element_OBJECTS = \
"CMakeFiles/bufr_get_element.dir/bufr_get_element.c.o"

# External object files for target bufr_get_element
bufr_get_element_EXTERNAL_OBJECTS =

tests/bufr_get_element: tests/CMakeFiles/bufr_get_element.dir/bufr_get_element.c.o
tests/bufr_get_element: tests/CMakeFiles/bufr_get_element.dir/build.make
tests/bufr_get_element: lib/libeccodes.so
tests/bufr_get_element: /usr/lib/x86_64-linux-gnu/libm.so
tests/bufr_get_element: tests/CMakeFiles/bufr_get_element.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/sehyun/GEMS_python/install/custom_builds/eccodes/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable bufr_get_element"
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && /usr/bin/cmake -E remove /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests/bufr_get_element
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/bufr_get_element.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
tests/CMakeFiles/bufr_get_element.dir/build: tests/bufr_get_element

.PHONY : tests/CMakeFiles/bufr_get_element.dir/build

tests/CMakeFiles/bufr_get_element.dir/requires: tests/CMakeFiles/bufr_get_element.dir/bufr_get_element.c.o.requires

.PHONY : tests/CMakeFiles/bufr_get_element.dir/requires

tests/CMakeFiles/bufr_get_element.dir/clean:
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests && $(CMAKE_COMMAND) -P CMakeFiles/bufr_get_element.dir/cmake_clean.cmake
.PHONY : tests/CMakeFiles/bufr_get_element.dir/clean

tests/CMakeFiles/bufr_get_element.dir/depend:
	cd /home/sehyun/GEMS_python/install/custom_builds/eccodes/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source /home/sehyun/GEMS_python/install/custom_builds/eccodes/eccodes-2.14.1-Source/tests /home/sehyun/GEMS_python/install/custom_builds/eccodes/build /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests /home/sehyun/GEMS_python/install/custom_builds/eccodes/build/tests/CMakeFiles/bufr_get_element.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tests/CMakeFiles/bufr_get_element.dir/depend
