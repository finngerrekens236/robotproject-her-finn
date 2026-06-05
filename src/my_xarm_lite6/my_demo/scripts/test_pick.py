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
    rospy.init_node('pick_and_lift_node', anonymous=True)

    # Koppel de robotarm EN de gripper
    move_group = moveit_commander.MoveGroupCommander("arm")
    

    # Snelheid voor de veiligheid op 20% zetten
    move_group.set_max_velocity_scaling_factor(0.2)
    move_group.set_max_acceleration_scaling_factor(0.2)
   

    # ==========================================
    # STAP 1: GRIPPER OPENEN VÓÓR VERPPLAATSING
    # ==========================================
    print("\n -> Gripper openen...")
    # 'open' is vaak een voorgedefinieerde state in je MoveIt Setup Assistant.
    # Als je met joint-waarden werkt, gebruik dan gripper_group.set_joint_value_target(...)
    subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '1'])

    # ==========================================
    # STAP 2: NAAR HET PRODUCT BEWEGEN
    # ==========================================
    target_pose = Pose()
    
    # De exacte XYZ coördinaten
    target_pose.position.x = -0.1050998
    target_pose.position.y = -0.272537
    target_pose.position.z = 0.165
    
    # De exacte Quaternion oriëntatie
    target_pose.orientation.x = 1.0
    target_pose.orientation.y = 0.0
    target_pose.orientation.z = 0.0
    target_pose.orientation.w = 0.0

    print("\n==================================================")
    print(" -> Plannen naar de doelpositie...")
    print(" X: {}, Y: {}, Z: {}".format(target_pose.position.x, target_pose.position.y, target_pose.position.z))
    print("==================================================")

    move_group.set_pose_target(target_pose)
    success = move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

    if not success:
        print("\n!!! Planning naar product mislukt. Script afgebroken. !!!")
        moveit_commander.roscpp_shutdown()
        return

    # ==========================================
    # STAP 3: PRODUCT GRIJPEN (GRIPPER DICHT)
    # ==========================================
    print("\n -> Product grijpen (gripper sluiten)...")
    subprocess.call(['rosservice', 'call', '/ufactory/vacuum_gripper_set', '0'])
    
    rospy.sleep(0.5) # Even een halve seconde wachten om te zorgen dat hij de grip stevig heeft

    # ==========================================
    # STAP 4: 5 CENTIMETER OMHOOG (Z + 0.05m)
    # ==========================================
    print("\n -> 5 centimeter omhoog bewegen voor de veiligheid...")
    
    # We nemen de huidige positie als startpunt voor de lift
    lift_pose = move_group.get_current_pose().pose
    
    # We tellen 5 centimeter (0.05 meter) op bij de huidige Z-hoogte
    lift_pose.position.z += 0.05

    move_group.set_pose_target(lift_pose)
    success_lift = move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

    

    if success_lift:
        print("\n=== Product succesvol gegrepen en opgetild! ===")
    else:
        print("\n!!! Optillen mislukt. Controleer robotlimieten. !!!")

    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass