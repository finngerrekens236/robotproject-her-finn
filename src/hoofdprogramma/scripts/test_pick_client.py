#!/usr/bin/env python

import rospy
import actionlib
from hoofdprogramma.msg import PickAndPlaceAction, PickAndPlaceGoal
from geometry_msgs.msg import PoseStamped

rospy.init_node("test_pick_and_place_client")

client = actionlib.SimpleActionClient("/pick_and_place", PickAndPlaceAction)
rospy.loginfo("Wachten op action server...")
client.wait_for_server()
rospy.loginfo("Verbonden met server!")

goal = PickAndPlaceGoal()
goal.kwast_type = "norm"

goal.target_pose.header.frame_id = "base_link"  # of "world", afhankelijk van je setup
goal.target_pose.pose.position.x = 0.1
goal.target_pose.pose.position.y = 0.0
goal.target_pose.pose.position.z = 0.4
goal.target_pose.pose.orientation.x = 0.0
goal.target_pose.pose.orientation.y = 0.0
goal.target_pose.pose.orientation.z = 0.0
goal.target_pose.pose.orientation.w = 1.0

client.send_goal(goal)
client.wait_for_result()

result = client.get_result()
rospy.loginfo("Resultaat: %s", result)
