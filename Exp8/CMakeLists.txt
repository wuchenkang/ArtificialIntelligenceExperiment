cmake_minimum_required(VERSION 3.10)

set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 14)

add_executable(Reversi Reversi.h Reversi.cpp MinMax.h MainProcess.cpp)
