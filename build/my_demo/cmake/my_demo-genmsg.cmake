# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "my_demo: 7 messages, 0 services")

set(MSG_I_FLAGS "-Imy_demo:/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/melodic/share/geometry_msgs/cmake/../msg;-Iactionlib_msgs:/opt/ros/melodic/share/actionlib_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(my_demo_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg" NAME_WE)
add_custom_target(_my_demo_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "my_demo" "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg" "actionlib_msgs/GoalID:actionlib_msgs/GoalStatus:my_demo/PickPlaceResult:std_msgs/Header"
)

get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg" NAME_WE)
add_custom_target(_my_demo_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "my_demo" "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg" "geometry_msgs/Pose:geometry_msgs/Quaternion:geometry_msgs/Point"
)

get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg" NAME_WE)
add_custom_target(_my_demo_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "my_demo" "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg" ""
)

get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceAction.msg" NAME_WE)
add_custom_target(_my_demo_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "my_demo" "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceAction.msg" "actionlib_msgs/GoalID:my_demo/PickPlaceResult:my_demo/PickPlaceActionGoal:my_demo/PickPlaceFeedback:my_demo/PickPlaceActionResult:actionlib_msgs/GoalStatus:geometry_msgs/Pose:my_demo/PickPlaceGoal:std_msgs/Header:geometry_msgs/Quaternion:my_demo/PickPlaceActionFeedback:geometry_msgs/Point"
)

get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg" NAME_WE)
add_custom_target(_my_demo_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "my_demo" "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg" "actionlib_msgs/GoalID:my_demo/PickPlaceFeedback:actionlib_msgs/GoalStatus:std_msgs/Header"
)

get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg" NAME_WE)
add_custom_target(_my_demo_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "my_demo" "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg" ""
)

get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg" NAME_WE)
add_custom_target(_my_demo_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "my_demo" "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg" "actionlib_msgs/GoalID:geometry_msgs/Pose:my_demo/PickPlaceGoal:std_msgs/Header:geometry_msgs/Quaternion:geometry_msgs/Point"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/my_demo
)
_generate_msg_cpp(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/my_demo
)
_generate_msg_cpp(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/my_demo
)
_generate_msg_cpp(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/my_demo
)
_generate_msg_cpp(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/my_demo
)
_generate_msg_cpp(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/my_demo
)
_generate_msg_cpp(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/my_demo
)

### Generating Services

### Generating Module File
_generate_module_cpp(my_demo
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/my_demo
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(my_demo_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(my_demo_generate_messages my_demo_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_cpp _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_cpp _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_cpp _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceAction.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_cpp _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_cpp _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_cpp _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_cpp _my_demo_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(my_demo_gencpp)
add_dependencies(my_demo_gencpp my_demo_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS my_demo_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/my_demo
)
_generate_msg_eus(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/my_demo
)
_generate_msg_eus(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/my_demo
)
_generate_msg_eus(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/my_demo
)
_generate_msg_eus(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/my_demo
)
_generate_msg_eus(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/my_demo
)
_generate_msg_eus(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/my_demo
)

### Generating Services

### Generating Module File
_generate_module_eus(my_demo
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/my_demo
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(my_demo_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(my_demo_generate_messages my_demo_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_eus _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_eus _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_eus _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceAction.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_eus _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_eus _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_eus _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_eus _my_demo_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(my_demo_geneus)
add_dependencies(my_demo_geneus my_demo_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS my_demo_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/my_demo
)
_generate_msg_lisp(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/my_demo
)
_generate_msg_lisp(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/my_demo
)
_generate_msg_lisp(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/my_demo
)
_generate_msg_lisp(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/my_demo
)
_generate_msg_lisp(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/my_demo
)
_generate_msg_lisp(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/my_demo
)

### Generating Services

### Generating Module File
_generate_module_lisp(my_demo
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/my_demo
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(my_demo_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(my_demo_generate_messages my_demo_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_lisp _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_lisp _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_lisp _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceAction.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_lisp _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_lisp _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_lisp _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_lisp _my_demo_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(my_demo_genlisp)
add_dependencies(my_demo_genlisp my_demo_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS my_demo_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/my_demo
)
_generate_msg_nodejs(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/my_demo
)
_generate_msg_nodejs(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/my_demo
)
_generate_msg_nodejs(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/my_demo
)
_generate_msg_nodejs(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/my_demo
)
_generate_msg_nodejs(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/my_demo
)
_generate_msg_nodejs(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/my_demo
)

### Generating Services

### Generating Module File
_generate_module_nodejs(my_demo
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/my_demo
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(my_demo_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(my_demo_generate_messages my_demo_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_nodejs _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_nodejs _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_nodejs _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceAction.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_nodejs _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_nodejs _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_nodejs _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_nodejs _my_demo_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(my_demo_gennodejs)
add_dependencies(my_demo_gennodejs my_demo_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS my_demo_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/my_demo
)
_generate_msg_py(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/my_demo
)
_generate_msg_py(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/my_demo
)
_generate_msg_py(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/my_demo
)
_generate_msg_py(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/my_demo
)
_generate_msg_py(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/my_demo
)
_generate_msg_py(my_demo
  "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Pose.msg;/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Point.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/my_demo
)

### Generating Services

### Generating Module File
_generate_module_py(my_demo
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/my_demo
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(my_demo_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(my_demo_generate_messages my_demo_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionResult.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_py _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceGoal.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_py _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceResult.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_py _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceAction.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_py _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionFeedback.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_py _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceFeedback.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_py _my_demo_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/student/Git-projects/robotproject-her-finn/devel/.private/my_demo/share/my_demo/msg/PickPlaceActionGoal.msg" NAME_WE)
add_dependencies(my_demo_generate_messages_py _my_demo_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(my_demo_genpy)
add_dependencies(my_demo_genpy my_demo_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS my_demo_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/my_demo)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/my_demo
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(my_demo_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(my_demo_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET actionlib_msgs_generate_messages_cpp)
  add_dependencies(my_demo_generate_messages_cpp actionlib_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/my_demo)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/my_demo
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(my_demo_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(my_demo_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET actionlib_msgs_generate_messages_eus)
  add_dependencies(my_demo_generate_messages_eus actionlib_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/my_demo)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/my_demo
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(my_demo_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(my_demo_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET actionlib_msgs_generate_messages_lisp)
  add_dependencies(my_demo_generate_messages_lisp actionlib_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/my_demo)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/my_demo
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(my_demo_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(my_demo_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET actionlib_msgs_generate_messages_nodejs)
  add_dependencies(my_demo_generate_messages_nodejs actionlib_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/my_demo)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/my_demo\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/my_demo
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(my_demo_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(my_demo_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET actionlib_msgs_generate_messages_py)
  add_dependencies(my_demo_generate_messages_py actionlib_msgs_generate_messages_py)
endif()
