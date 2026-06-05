cmake_minimum_required(VERSION 3.0.2)
project(conveyor_package)

find_package(catkin REQUIRED)

catkin_package()

catkin_install_python(PROGRAMS
  scripts/conveyor_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
