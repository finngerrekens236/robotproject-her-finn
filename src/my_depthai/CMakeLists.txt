cmake_minimum_required(VERSION 3.0.2)
project(my_depthai)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  geometry_msgs
  sensor_msgs
  cv_bridge
  message_generation
)

# Custom service definitie
add_service_files(
  FILES
  DetectObject.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
)

catkin_package(
  CATKIN_DEPENDS
    rospy
    std_msgs
    geometry_msgs
    sensor_msgs
    cv_bridge
    message_runtime
)

# Installeer Python scripts
catkin_install_python(
  PROGRAMS scripts/vision_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

# Installeer launch en config bestanden
install(DIRECTORY launch config models
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
