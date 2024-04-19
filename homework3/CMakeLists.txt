cmake_minimum_required(VERSION 3.0.2)
project(hello_pkg)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
)

catkin_package()

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_executable(talker src/talk.cpp)
target_link_libraries(talker ${catkin_LIBRARIES})

