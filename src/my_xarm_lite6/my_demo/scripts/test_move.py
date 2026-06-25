#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import rospy
import moveit_commander
from geometry_msgs.msg import Pose

def main():
    # Initializeer MoveIt en de ROS node
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_to_exact_pose_node', anonymous=True)

    # Koppel de robotarm
    move_group = moveit_commander.MoveGroupCommander("arm")

    # Snelheid voor de veiligheid op 20% zetten
    move_group.set_max_velocity_scaling_factor(0.2)
    move_group.set_max_acceleration_scaling_factor(0.2)

    # Maak het doel-pose object aan
    target_pose = Pose()
    
    # 1. Vul de exacte XYZ coördinaten in die je hebt uitgelezen
    target_pose.position.x = -0.1508
    target_pose.position.y = -0.2554
    target_pose.position.z = 0.169
    
    # 2. Vul de exacte Quaternion oriëntatie in (qx, qy, qz, qw)
    target_pose.orientation.x = 1.0
    target_pose.orientation.y = 0.0
    target_pose.orientation.z = 0.0
    target_pose.orientation.w = 0.0

    print("\n==================================================")
    print(" -> Plannen naar de opgeslagen doelpositie...")
    print(" X: {}, Y: {}, Z: {}".format(target_pose.position.x, target_pose.position.y, target_pose.position.z))
    print("==================================================")

    # Stuur het doel naar MoveIt
    move_group.set_pose_target(target_pose)

    # Bereken en voer de beweging uit
    success = move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

    if success:
        print("\n=== Doel succesvol bereikt! ===")
    else:
        print("\n!!! Planning mislukt. Controleer de robotstatus. !!!")

    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
