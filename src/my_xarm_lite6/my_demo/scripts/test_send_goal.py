#!/usr/bin/env python
# -- coding: utf-8 --

import sys
import rospy
import actionlib
from geometry_msgs.msg import Pose

# Importeer de Action berichten uit jouw eigen package
from my_demo.msg import PickPlaceAction, PickPlaceGoal

def main():
    # Initialiseer de ROS node voor deze test client
    rospy.init_node('test_action_client_node')

    rospy.loginfo("Verbinding maken met de /robot/pick_place Action Server...")
    
    # Maak de Action Client aan
    client = actionlib.SimpleActionClient('/robot/pick_place', PickPlaceAction)
    
    # Wacht maximaal 5 seconden tot de server online is
    if not client.wait_for_server(rospy.Duration(5.0)):
        rospy.logerr("Kan geen verbinding maken met de Action Server. Staat Robot_Action_Server.py wel aan?")
        return

    rospy.loginfo("Verbonden met de server! Goal aanmaken...")

    # Maak het Goal object aan
    goal = PickPlaceGoal()
    
    # Vul de test-coördinaten in (het doel waar de robot heen moet)
    goal.target_pose.position.x = -0.1638
    goal.target_pose.position.y = -0.280
    goal.target_pose.position.z = 0.4  # (De server overschrijft deze momenteel naar 0.165, maar we vullen hem netjes in)
    
    # Vul de quaternion oriëntatie in die uit de camera kwam
    goal.target_pose.orientation.x = 0.0
    goal.target_pose.orientation.y = 0.0
    goal.target_pose.orientation.z = -0.033596
    goal.target_pose.orientation.w = 0.999436

    rospy.loginfo("Goal versturen naar de robot...")
    
    # Stuur het goal op
    client.send_goal(goal)
    
    rospy.loginfo("Wachten tot de robot klaar is met de Pick & Lift beweging...")
    
    # Wacht rustig af tot de robot de hele callback heeft doorlopen
    client.wait_for_result()
    
    # Haal het resultaat op (success = True/False)
    result = client.get_result()
    
    if result and result.success:
        rospy.loginfo("=== TEST SUCCESVOL: De robot heeft de actie afgerond! ===")
    else:
        rospy.logerr("=== TEST MISLUKT: De server meldde een fout. ===")

if __name__ == '__main__':
    main()
