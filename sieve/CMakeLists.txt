cmake_minimum_required(VERSION 3.10)

project(Scratch VERSION 1.0)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories(${PROJECT_SOURCE_DIR})

add_subdirectory(third_party/googletest)
add_subdirectory(third_party/abseil-cpp)
add_subdirectory(base)
add_subdirectory(sieve)
