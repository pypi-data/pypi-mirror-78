cmake_minimum_required(VERSION 2.8.3)

project(dynamic-fba)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "-Wno-deprecated-register" )

################### Find pybind11

set(PYBIND11_PYTHON_VERSION 3)
find_package(pybind11 REQUIRED)

################### Set path for custom FindModules

set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

################### Find glpk packages

find_package(GLPK REQUIRED)
message(STATUS "GLPK_LIBRARY = ${GLPK_LIBRARY}")
message(STATUS "GLPK_INCLUDE_DIR = ${GLPK_INCLUDE_DIR}")

################### Find sundials packages

find_package(SUNDIALS REQUIRED)
message(STATUS "SUNDIALS_LIBRARIES = ${SUNDIALS_LIBRARIES}")
message(STATUS "SUNDIALS_INCLUDE_DIR = ${SUNDIALS_INCLUDE_DIR}")

################### Include directories and libraries

add_compile_options("-I${GLPK_INCLUDE_DIR}")
add_compile_options("-I${SUNDIALS_INCLUDE_DIR}")
link_libraries(
  ${GLPK_LIBRARY}
  ${SUNDIALS_LIBRARIES}
  )

################### Source files

set(SRC ./src/extension/)
aux_source_directory(${SRC}/emblp/ EMBLP_FILES)
aux_source_directory(${SRC}/methods/ METHOD_FILES)
set(MODULE_FILES ${SRC}dfba_utils.cpp ${EMBLP_FILES} ${METHOD_FILES})

################### Build module

pybind11_add_module(dfba_utils ${MODULE_FILES})
