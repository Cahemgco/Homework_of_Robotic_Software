cmake_minimum_required(VERSION 3.1)
project(show_pic)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
add_executable(show_pic show_pic.cpp)
TARGET_LINK_LIBRARIES(show_pic ${OpenCV_LIBS})

