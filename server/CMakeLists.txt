cmake_minimum_required (VERSION 3.0.2)
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
project (agc_server)
add_executable(agc_server agc_server.cpp)
TARGET_LINK_LIBRARIES(agc_server pthread)
