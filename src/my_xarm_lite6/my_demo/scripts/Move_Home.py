#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import rospy
import moveit_commander
from geometry_msgs.msg import Pose
import subprocess

def main():
    # Initializeer MoveIt en de ROS node
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('home_robot_node', anonymous=True)

    # Koppel de robotarm
    move_group = moveit_commander.MoveGroupCommander("arm")

    # Snelheid voor de veiligheid op 20% zetten
    move_group.set_max_velocity_scaling_factor(0.2)
    move_group.set_max_acceleration_scaling_factor(0.2)

    # Maak het doel-pose object aan
    target_pose = Pose()
    
    # 1. Vul de exacte XYZ coördinaten in voor de HOME-positie
    target_pose.position.x = -0.0573
    target_pose.position.y = -0.0000
    target_pose.position.z = 0.4730
    
    # 2. Vul de exacte Quaternion oriëntatie in (qx, qy, qz, qw)
    target_pose.orientation.x = 1.000
    target_pose.orientation.y = 0.000
    target_pose.orientation.z = -0.000
    target_pose.orientation.w = 0.000

    print("\n==================================================")
    # Toegevoegde veiligheidsregel: dwing MoveIt om te starten vanaf de actuele live-positie
    move_group.set_start_state_to_current_state()
    print(" -> Robot keert terug naar de HOME-positie...")
    print(" X: {}, Y: {}, Z: {}".format(target_pose.position.x, target_pose.position.y, target_pose.position.z))
    print("==================================================")

    # Stuur het HOME-doel naar MoveIt
    move_group.set_pose_target(target_pose)

    # Bereken en voer de beweging uit
    success = move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

    subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '0'])

    if success:
        print("\n=== Robot staat succesvol HOME! ===")
    else:
        print("\n!!! Homing mislukt. Controleer de robotstatus of starttolerantie. !!!")

    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
