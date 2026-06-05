cmake_minimum_required(VERSION 3.0.2)
project(hoofdprogramma)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  geometry_msgs
  message_generation
  actionlib
  actionlib_msgs
)

## Voeg bericht toe
add_message_files(
  FILES
  objectDetection.msg
)

## Voeg service toe
add_service_files(
  FILES
  StartCyclus.srv
)

add_action_files(
  FILES
  PickAndPlace.action
)

## Genereer alles
generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
  actionlib_msgs
)

## Declareer afhankelijkheden
catkin_package(
  CATKIN_DEPENDS 
  message_runtime 
  std_msgs 
  geometry_msgs
  actionlib_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

## Python nodes installeren
catkin_install_python(PROGRAMS
  scripts/hoofdprogramma_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
